from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableSerializable, Runnable
from langchain_core.tools.structured import BaseTool
from langchain_core.messages import ToolMessage
from app.model.runner.queue_callback_handler import QueueCallBackHandler


class AsyncAgentExecutor():
    def __init__(self, max_iter: int):
        self.max_iter = max_iter

    async def ainvoke(
            self,
            agent_and_tools: tuple[RunnableSerializable, list[BaseTool]],
            streamer: QueueCallBackHandler,
            input: str,
            cache_key: str,
            config: dict,
            verbose=False):
        """
Custom asynchronous tool-calling runnable chain executor using the ReAct (Reasoning and Acting) technique.\n

If the agent doesn't have any tools to call then normal LCEL chain astream function will work

In each ReAct loop:\n
- The model calls a tool.\n
- This executor runs the corresponding tool.\n
- Then it appends both the tool call and its execution duckduck to the `agent_scratchpad`, in order.
- If model call final_answer tool then the ReAct iteration would stop

        :param cache_key: unique cache key for access global variables
        :param agent_and_tools: a mydict contains LCEL runnable chain and a AsyncCallbackHandler object as a callback example : {agent : your_agent , tool_list : [your tools]} toollist can be empty if agent doesn't have any tool
        :param streamer: Custom async callback handler
        :param input: user input
        :param config: configurable parameters like k , session_id , streamer etc.
        :param verbose: To get information about ReAct cycle define this True , default value = False
        :return: None
        """

        agent = agent_and_tools[0]
        tool_list = agent_and_tools[1]
        agent_with_callback = agent.with_config(callbacks=[streamer])

        if tool_list == []:
            async def stream(cache_key: str):
                output = None
                async for token in agent_with_callback.astream(
                        input={
                            "query": input,
                            "cache_key": cache_key,
                        },
                        config=config
                ):
                    if output is None:
                        output = token
                    else:
                        output += token
                return output

            return await stream(cache_key=cache_key)


        else:
            print("ELSE ÇALIŞTI")
            counter = 1
            agent_scratchpad = []

            async def stream(agent: Runnable,
                             input: str,
                             cache_key: str,
                             config: dict,
                             ) \
                    -> AIMessage:

                """
                async custom streaming function with verbose
                :param agent: LCEL Runnable chain wrapped with RunnableWithMessageHistory and a AsyncCallbackHandler object as a callback
                :param input: user input
                :param config: configurable parameters like k , session_id , streamer etc.
                :return: AI message Chunk with content and tool_call
                """
                output = None
                async for chunk in agent.astream(
                        input=
                        {
                            "query": input,
                            "cache_key":cache_key,
                            "agent_scratchpad": agent_scratchpad
                        },
                        config=config
                ):
                    if output is None:
                        output = chunk
                    else:
                        output += chunk
                # print(f"OUTPUT = {output.tool_calls[0]['args']['input']}")
                if tool_calls := output.tool_calls:
                    if verbose:
                        if tool_name := tool_calls[0].get("name"):
                            print(f"TOOL NAME : {tool_name}")
                        if tool_args := tool_calls[0].get("args"):
                            print(f"TOOL ARGS : {tool_args}")
                    print(f"TOOL CALLS : {output.tool_calls}")
                    print(f"TYPE TOOL CALLS : {type(output.tool_calls)}")
                    return AIMessage(
                        tool_calls=output.tool_calls,
                        content=output.content
                    )

            name2tool = {tool.name: tool.coroutine for tool in tool_list}
            while counter <= self.max_iter:
                result = await stream(
                    agent=agent_with_callback,
                    input=input,
                    cache_key=cache_key,
                    config=config,
                )
                agent_scratchpad.append(result)
                #print(duckduck)
                for tool_call in result.tool_calls:
                    tool_call_id = tool_call['id']
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']
                    tool_exec = await name2tool[tool_name](**tool_args)
                    tool_msg = ToolMessage(
                        content=f"Tool name : {tool_name} , Content : {tool_exec}",
                        tool_call_id=tool_call_id
                    )
                    agent_scratchpad.append(tool_msg)
                    print(f"AGENT SCRATCHPAD : {agent_scratchpad}")
                    if tool_name == "final_answer":
                        print("final answer çalıştı")
                        print(f"TOOL EXEC RESULT: {tool_exec}")
                        return tool_exec
                counter += 1

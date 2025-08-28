import asyncio
from app.model.async_agent_executor import AsyncAgentExecutor
from app.model.queue_callback_handler import QueueCallBackHandler
from langchain_core.runnables import RunnableSerializable
from langchain.tools import BaseTool

executor = AsyncAgentExecutor(10)


async def token_generator(
        agent_and_tools: tuple[RunnableSerializable, list[BaseTool]],
        streamer: QueueCallBackHandler,
        input: str,
        config: dict,
        verbose: bool = False

):
    """
    A token generator for the frontend that yields <step>, <step_args>, etc., based on the streamer’s token.


        :param agent_and_tools: a dict contains LCEL runnable chain and a AsyncCallbackHandler object as a callback example : {agent : your_agent , tool_list : [your tools]} toollist can be empty if agent doesn't have any tool
        :param streamer: Custom async callback handler
        :param input: user input
        :param config: configurable parameters like k , session_id , streamer etc.
        :param verbose: to see console logs pass True
        """

    task = asyncio.create_task(
        executor.ainvoke(
            agent_and_tools=agent_and_tools,
            streamer=streamer,
            input=input,
            config=config,
            verbose=verbose))

    async for token in streamer:
        print(f"TOKEN GENERATOR TOKEN : {token}")
        if isinstance(token , str):
            if token == "<<STEP_END>>":
                print("STEP END ÇALIŞTI")
                yield "</step_content>\n\n</step>"
        else:
            tool_calls = token.message.additional_kwargs.get("tool_calls")
            if tool_calls and len(tool_calls)>0:
                print("TOOL CALLS ÇALIŞTI")
                if tool_name := tool_calls[0]["function"]["name"]:
                    print("TOOL NAME ÇALIŞTI")
                    print(f"YIELD VALUE : <step><step_name>{tool_name}</step_name>\n\n<step_content>\n\n")
                    yield f"data: <step>\n\n<step_name>{tool_name}</step_name>\n\n<step_content>\n\n"
        yield f"data: {token}\n\n"


    await task

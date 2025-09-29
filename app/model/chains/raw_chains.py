from langchain_core.tools import StructuredTool
from app.model.prompts import base_prompts
from app.model.models import chat_model, summarymodel  , utility_model
from app.model.tools import tool_list
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI
import ast


def chain_maker(
        basemodel: RunnableSerializable,
        prompt : ChatPromptTemplate,
        tool_list = list[StructuredTool])\
    -> RunnableSerializable:
    return (
            {
                "agent_scratchpad": lambda x: x.get("agent_scratchpad", []),
                "memory": lambda x: x.get("memory", []),
                "query": lambda x: x.get("query", []),
                "cache_key":lambda x:x.get("cache_key", [])
            }
            | prompt
            | basemodel.bind_tools(tools=tool_list, tool_choice="any")
    )
math_agent = chain_maker(basemodel=chat_model,prompt= base_prompts.math_agent_prompt , tool_list=tool_list.math_agent_toollist)
utility_agent = chain_maker(basemodel=utility_model,prompt=base_prompts.utility_agent_prompt , tool_list=tool_list.utility_agent_toollist)
database_analysis_agent = chain_maker(basemodel=utility_model,prompt=base_prompts.database_analysis_agent_prompt , tool_list=tool_list.database_analysis_agent_toollist)
database_visualization_agent = chain_maker(basemodel=utility_model,prompt=base_prompts.database_visualization_agent_prompt , tool_list=tool_list.database_visualization_agent_toollist)
database_visualization_agent_dependent = chain_maker(basemodel=utility_model,prompt=base_prompts.database_visualization_agent_dependent_prompt, tool_list=tool_list.database_visualization_agent_dependent_toollist)

chat_agent: RunnableSerializable = (
        {
            "memory": lambda x: x.get("memory", []),
            "query": lambda x: x.get("query", []),
            "cache_key": lambda x: x.get("cache_key", [])
        }
        | base_prompts.chat_agent_prompt
        | chat_model

)

supervisor_agent: RunnableSerializable = (
    {
        "query": lambda x:x,
        "agent_history": lambda x:x.get("agent_history" , [])
    }
    |base_prompts.supervisor_agent_prompt
    |utility_model
)

summary_agent: RunnableSerializable = (
        {
            "summary": lambda x: x["summary"],
            "messages": lambda x: x["messages"]
        }
        | base_prompts.summary_agent_prompt
        | summarymodel
)


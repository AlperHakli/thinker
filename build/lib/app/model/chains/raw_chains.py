from app.model.prompts import base_prompts
from app.model.models import basemodel, summarymodel
from app.model.tools import tool_list

from langchain_core.runnables import RunnableSerializable

math_agent: RunnableSerializable = (
        {
            "agent_scratchpad": lambda x: x.get("agent_scratchpad", []),
            "memory": lambda x: x.get("memory", []),
            "query": lambda x: x.get("query", [])
        }
        | base_prompts.math_agent_prompt
        | basemodel.bind_tools(tools=tool_list.math_agent_toollist, tool_choice="any")

)
chat_agent: RunnableSerializable = (
        {
            "memory": lambda x: x.get("memory", []),
            "query": lambda x: x.get("query", [])
        }
        | base_prompts.chat_agent_prompt
        | basemodel

)

utility_agent: RunnableSerializable = (
        {
            "query": lambda x: x["query"],
            "agent_scratchpad": lambda x: x.get("agent_scratchpad", []),
            "memory": lambda x: x.get("memory", []),

        }
        | base_prompts.utility_agent_prompt
        | basemodel.bind_tools(tools=tool_list.utility_agent_toollist, tool_choice="any")

)

summary_agent: RunnableSerializable = (
        {
            "summary": lambda x: x["summary"],
            "messages": lambda x: x["messages"]
        }
        | base_prompts.summary_agent_prompt
        | summarymodel
)

data_analysis_agent: RunnableSerializable = (
    {
        "query" : lambda x:x["query"],
        "agent_scratchpad" : lambda x:x.get("agent_scratchpad" , []),
        "memory": lambda x: x.get("memory", []),
    }
    | base_prompts.database_analysis_agent_prompt
    | basemodel.bind_tools(tools = tool_list.database_analysis_agent_toollist, tool_choice="any")

)

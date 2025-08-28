from app.model.tools import tool_list
from app.model.chains import raw_chains, memory_chains

#TODO Do not forget that sequence must be same with agent_router's prompt templates

agents_and_tools = [
    (memory_chains.math_agent_with_memory, tool_list.math_agent_toollist),
    (memory_chains.chat_agent_with_memory, tool_list.chat_agent_toollist),
    (memory_chains.utility_agent_with_memory, tool_list.utility_agent_toollist),
    (memory_chains.data_analysis_agent_with_memory , tool_list.database_analysis_agent_toollist)
]

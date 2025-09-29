from app.model.tools import tool_list
from app.model.chains import raw_chains, memory_chains

#TODO Do not forget that sequence must be same with agent_router's prompt templates



agents_and_tools = {
   "chat_agent": (memory_chains.chat_agent_with_memory, tool_list.chat_agent_toollist),
   "math_agent": (memory_chains.math_agent_with_memory, tool_list.math_agent_toollist),
   "utility_agent": (memory_chains.utility_agent_with_memory, tool_list.utility_agent_toollist),
   "data_analysis_agent": (memory_chains.data_analysis_agent_with_memory , tool_list.database_analysis_agent_toollist),
   "data_visualization_agent": (memory_chains.data_visualization_agent_with_memory , tool_list.database_visualization_agent_toollist),
   # if database visualization agent use the calculations from previous agents (probably data analysis agent)
   # then it will use data_visualization_agent_dependent instead of data_visualization_agent
   "data_visualization_agent_dependent": (memory_chains.data_visualization_agent_dependent_with_memory , tool_list.database_visualization_agent_dependent_toollist)
}

agents_and_tools_as_list = list(agents_and_tools.values())

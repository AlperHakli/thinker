from app.model.tools import math_tools, global_tools, utility_tools, database_analysis_tools

#TODO add more tools like data analysis tools , data visualization tools , maybe model builder tools at the future


math_agent_toollist = \
    [
        global_tools.final_answer,
        math_tools.arithmetic_calculations
    ]

chat_agent_toollist = []

utility_agent_toollist = \
    [
        global_tools.final_answer,
        utility_tools.get_current_time,
        utility_tools.get_location,
        utility_tools.search_on_web
    ]

database_analysis_agent_toollist = [
    global_tools.load_db,
    global_tools.final_answer,
    database_analysis_tools.get_correlation,
    database_analysis_tools.get_median_mean_std_var_min_max_mode,
]

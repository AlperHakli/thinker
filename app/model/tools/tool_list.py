from langchain_core.tools import StructuredTool , BaseTool
from app.model.tools import math_tools
from app.model.tools.database_analysis_tools import get_correlation ,get_median_mean_std_var_min_max_mode
from app.model.tools.database_visualization_tools import bar_plot_tool ,box_plot_tool ,heatmap_plot_tool , line_plot_tool , pie_plot_tool , scatter_plot_tool
from app.model.tools.database_visualization_tools.database_visualization_dependent_tools import  bar_plot_dependent_tool , box_plot_dependent_tool , heatmap_plot_dependent_tool , line_plot_dependent_tool , pie_plot_dependent_tool , scatter_plot_dependent_tool
from app.model.tools.utility_tools import  get_current_time , get_location , search_on_web
from app.model.tools.global_tools import final_answer , load_db
from app.model.tools.math_tools import arithmetic_calculations
from app.model.db_cache import DB_CACHE

#TODO add more tools like data analysis tools , data visualization tools , maybe model builder tools at the future



math_agent_toollist = \
    [
        final_answer.final_answer,
        arithmetic_calculations.arithmetic_calculations
    ]
# chat agent doesn't require any tools maybe in the future I create different personas
chat_agent_toollist = []

utility_agent_toollist = \
    [
        final_answer.final_answer,
        get_current_time.get_current_time,
        get_location.get_location,
        search_on_web.search_on_web
    ]

database_analysis_agent_toollist = [

    final_answer.final_answer,
    get_correlation.get_correlation,
    get_median_mean_std_var_min_max_mode.get_median_mean_std_var_min_max_mode,
    load_db.load_db,
]

database_visualization_agent_toollist = [

    final_answer.final_answer,
    bar_plot_tool.bar_plot_tool,
    box_plot_tool.box_plot_tool,
    heatmap_plot_tool.heatmap_plot_tool,
    line_plot_tool.line_plot_tool,
    pie_plot_tool.pie_plot_tool,
    scatter_plot_tool.scatter_plot_tool,
    load_db.load_db,
]

# if database visualization agent use the calculations from previous agents (probably database analysis agent) then it will use these tools
# in that scenerio the agent doesn't need load_db tool because it will not load a data
database_visualization_agent_dependent_toollist = [
    final_answer.final_answer,
    bar_plot_dependent_tool.bar_plot_dependent_tool,
    box_plot_dependent_tool.box_plot_dependent_tool,
    heatmap_plot_dependent_tool.heatmap_plot_dependent_tool,
    line_plot_dependent_tool.line_plot_dependent_tool,
    pie_plot_dependent_tool.pie_plot_dependent_tool,
    scatter_plot_dependent_tool.scatter_plot_dependent_tool,

]





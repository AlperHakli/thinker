import seaborn as sns
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from app.model.db_cache import DB_CACHE
from typing import Union


#TODO you must complete this visualization tools today
@tool
async def bar_plot(
        file_key: str,
        x_column_name: str = None,
        y_column_name: str = None,
        outside_plot_color: str = None,
        inside_plot_color: str = None,
        bar_color: str = None,
        x_ticks_rotation: int = None,
        xticks_color: str = None,
        yticks_color: str = None,
        xlabel_color: str = None,
        ylabel_color: str = None,
        window_title: str = None,

) \
        -> Union[str, None]:
    """
    Bar Plot Drawer you can use this tool to draw a bar plot
    :param file_key : key value of the database
    :param outside_plot_color : The background color of the figure area outside the plot axes
    :param inside_plot_color : The background color of the plotting area where data and grid lines are drawn
    xticks means numbers or strings in the x axes
    yticks means numbers or strings in the y axes
    window_title is title of the plot
    """
    try:
        figure_decoration = {}
        db_uncomputed = DB_CACHE[file_key]
        db = db_uncomputed.compute()
        if x_column_name and y_column_name is None:
            return "Mention about both x column name and y column name cannot be empty user must specify at least one of them"
        if x_column_name is None:
            x_range = range(len(db[y_column_name]))
            ax = sns.barplot(x=x_range, y=db[y_column_name])
        elif y_column_name is None:
            y_range = range(len(db[x_column_name]))
            ax = sns.barplot(x=db[x_column_name], y=y_range)
        else:
            ax = sns.barplot(x = db[x_column_name] , y = db[y_column_name])
        if outside_plot_color is not None:
            figure_decoration["figure.facecolor"] = outside_plot_color
        if inside_plot_color is not None:
            figure_decoration["axes.facecolor"] = inside_plot_color
        if bar_color is not None:
            ...








    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user"

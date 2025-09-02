from app.model.tools.database_visualization_tools.visualization_imports import *
from app.model.tools.database_visualization_tools.helper_functions import multiple_variable_adjuster
import pandas as pd
@tool
async def violin_plot_tool(
        file_key: str = None,
        x_column_name: str = None,
        y_column_name: str = None,
        hue_column_name: str = None,
        window_title: str = None,
        plot_title: str = None,
        x_label_text: str = None,
        y_label_text: str = None,
        outside_plot_color: str = "white",
        inside_plot_color: str = "white",
        x_label_color: str = "black",
        y_label_color: str = "black",
        x_tick_color: str = "black",
        y_tick_color: str = "black",
        x_tick_rotation: float = 0,
        y_tick_rotation: float = 0,
        plot_title_color: str = "black",
        violin_color: str = "white",
        violin_line_color: str = "black",
        violin_line_width: float = 1,
)\
    -> str :
    """
    Use this tool to draw violin plot
    You van draw Violin plot with this tool,

    <x_column_name> : only x-axis column name x-axis column name only
    <y_column_name> :  only y-axis column name y-axis column name only
    <file_key> : key value of the database.
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_label_color> : x-axis color title color x-axis label
    <y_label_color> : y-axis color title color y-axis label
    <x_label_text> : title x-axis label
    <y_label_text> title y-axis label
    <x_tick_color> : x-axis color tick number color categorical value x-axis
    <y_tick_color> : y-axis color tick number color categorical value y-axis
    <x_tick_rotation> : x-axis tick rotation number rotation categorical value x-axis
    <y_tick_rotation> : y-axis tick rotation number rotation categorical value y-axis
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color
    <hue_column_name>: specifies a categorical column to split the boxes into different colors, so each category is shown separately—for example, grouping by gender to show male and female boxes in different colors.
    <violin_color> inside violin color
    <violin_line_color> violin border line color
    <violin_line_width> violin border line width
    """


    db = DB_CACHE[file_key]

    def normalize_none(param):
        return None if param == '' else param

    x_column_name = normalize_none(x_column_name)
    y_column_name = normalize_none(y_column_name)
    hue_column_name = normalize_none(hue_column_name)

    if x_column_name == y_column_name:
        return "call final_answer mention x column name and y column name can not be same user must specify that column belong x-axis or y-axis"

    if x_column_name is None and y_column_name is None:
        return "call final_answer tool and mention in a friendly, slightly funny way that both x-axis and y-axis column names cannot be None user must specify at least one of them"
    is_numeric_1 = False
    is_numeric_2 = False
    if x_column_name is not None:
        is_numeric_1 = pd.api.types.is_numeric_dtype(db[x_column_name])
    if y_column_name is not None:
        is_numeric_2 = pd.api.types.is_numeric_dtype(db[y_column_name])


    native_scale = is_numeric_1 or is_numeric_2

    ax = sns.violinplot(
        x=db[x_column_name] if x_column_name is not None else range(len(db[y_column_name])),
        y=db[y_column_name] if y_column_name is not None else range(len(db[x_column_name])),
        native_scale=native_scale,
        color=violin_color,
        linecolor=violin_line_color,
        linewidth=violin_line_width,
        hue=db[hue_column_name] if hue_column_name is not None else None)

    ax = multiple_variable_adjuster(
        ax=ax,
        outside_plot_color=outside_plot_color,
        inside_plot_color=inside_plot_color,
        x_label_color=x_label_color,
        y_label_color=y_label_color,
        x_label_text=x_label_text,
        y_label_text=y_label_text,
        x_tick_color=x_tick_color,
        y_tick_color=y_tick_color,
        x_tick_rotation=x_tick_rotation,
        y_tick_rotation=y_tick_rotation,
        window_title=window_title,
        plot_title=plot_title,
        plot_title_color=plot_title_color)

    plt.tight_layout()
    plt.show()
    return f"call the final_answer , you can mention about you have successfully drawn the plot and you can praise yourself with his language"
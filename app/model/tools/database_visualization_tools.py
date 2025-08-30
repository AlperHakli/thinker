import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from app.model.db_cache import DB_CACHE
from typing import Union
import pandas as pd

#TODO you must complete this visualization tools today

variable_adjuster_base_prompt: str = """
    <x_column_name and y_column_name> real column names that will use when plotting the linechart
    <file_key> : key value of the database.
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_axis_label_color and y_axis_label_color> Color of title of x-axis and y-axis
    <x_axis_label_value and y_axis_label_value>: Title value of x-axis and y-axis Don't use these values unless user wants to give a title the plot
    <x_ticks_color and y_ticks_color>: Color of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <x_ticks_rotation and y_ticks_rotation: Rotation value of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color
"""


def _multiple_variable_adjuster(
        ax: plt.Axes,
        x_column_name: str = None,
        y_column_name: str = None,
        outside_plot_color: str = None,
        inside_plot_color: str = None,
        x_axis_label_color: str = None,
        y_axis_label_color: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        x_ticks_color: str = None,
        y_ticks_color: str = None,
        x_ticks_rotation: float = None,
        y_ticks_rotation: float = None,
        window_title: str = None,
        plot_title: str = None,
        plot_title_color: str = None,

) \
        -> plt.Axes:
    """
    Multiple variable adjuster for base matplotlib.Axes class \n
    Visualization tools will use this function
    """

    default_x_axis_label_color = "black"
    default_y_axis_label_color = "black"
    default_plot_title_color = "black"
    default_line_color = "darkblue"

    fig = ax.get_figure()

    if outside_plot_color is not None:
        fig.set_facecolor(outside_plot_color)

    if inside_plot_color is not None:
        ax.set_facecolor(inside_plot_color)

    if x_ticks_color is not None:
        ax.tick_params(axis="x", color=x_ticks_color, labelcolor=x_ticks_color)

    if y_ticks_color is not None:
        ax.tick_params(axis="y", color=y_ticks_color, labelcolor=y_ticks_color)

    if x_ticks_rotation is not None:
        ax.tick_params(axis="x", labelrotation=x_ticks_rotation)

    if y_ticks_rotation is not None:
        ax.tick_params(axis="y", labelrotation=y_ticks_rotation)

    if x_axis_label_color is not None:
        default_x_axis_label_color = x_axis_label_color

    if y_axis_label_color is not None:
        default_y_axis_label_color = y_axis_label_color

    if x_axis_label_value is not None:
        ax.set_xlabel(xlabel=x_axis_label_value, color=default_x_axis_label_color)
    elif x_column_name is not None:
        ax.set_xlabel(xlabel=x_column_name, color=default_x_axis_label_color)
        # probably model used id column
    else:
        ax.set_xlabel(xlabel="Index", color=default_x_axis_label_color)

    if y_axis_label_value is not None:
        ax.set_ylabel(ylabel=y_axis_label_value, color=default_y_axis_label_color)
    elif y_column_name is not None:
        ax.set_ylabel(ylabel=y_column_name, color=default_y_axis_label_color)
    else:
        ax.set_ylabel(ylabel="Index", color=default_y_axis_label_color)

    if plot_title_color is not None:
        default_plot_title_color = plot_title_color

    if plot_title is not None:
        ax.set_title(label=plot_title, color=default_plot_title_color, loc="center")

    if window_title is not None:
        fig.canvas.manager.set_window_title(title=window_title)

    return ax


@tool
async def bar_plot_tool(
        file_key: str,
        x_column_name: str = None,
        y_column_name: str = None,
        outside_plot_color: str = None,
        inside_plot_color: str = None,
        x_axis_label_color: str = None,
        y_axis_label_color: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        x_ticks_color: str = None,
        y_ticks_color: str = None,
        x_ticks_rotation: int = None,
        y_ticks_rotation: int = None,
        window_title: str = None,
        plot_title: str = None,
        plot_title_color: str = None,
        bar_color: str = None,
        grid_color: str = None,
        grid_line_style: str = None,

) \
        -> Union[str, None]:
    """
    you HAVE TO use these param names do not give random names except this tool's params
    If user doesn't specify any columns then DO NOT fill x_column_name and y_column_name
    Bar Plot Drawer you can use this tool to draw a bar plot
    
    <x_column_name and y_column_name> real column names that will use when plotting the linechart
    <file_key> : key value of the database.
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_axis_label_color and y_axis_label_color> Color of title of x-axis and y-axis
    <x_axis_label_value and y_axis_label_value>: Title value of x-axis and y-axis Don't use these values unless user wants to give a title the plot
    <x_ticks_color and y_ticks_color>: Color of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <x_ticks_rotation and y_ticks_rotation: Rotation value of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color
    
    """
    try:
        grid_decoration = {}
        db = DB_CACHE[file_key].compute()
        if x_column_name is None and y_column_name is None:
            return "mention in a friendly, slightly funny way that both x-axis and y-axis column names cannot be None user must specify at least one of them"

        if grid_color is not None:
            grid_decoration["grid.color"] = grid_color
        if grid_line_style is not None:
            grid_decoration["grid.linestyle"] = grid_line_style

        sns.set_style("whitegrid", rc=grid_decoration)

        ax = sns.barplot(
            x=db[x_column_name] if x_column_name else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name else range(len(db[x_column_name])),
            color=bar_color
        )
        ax = _multiple_variable_adjuster(
            ax=ax,
            x_column_name=x_column_name,
            y_column_name=y_column_name,
            outside_plot_color=outside_plot_color,
            inside_plot_color=inside_plot_color,
            x_axis_label_color=x_axis_label_color,
            y_axis_label_color=y_axis_label_color,
            x_axis_label_value=x_axis_label_value,
            y_axis_label_value=y_axis_label_value,
            x_ticks_color=x_ticks_color,
            y_ticks_color=y_ticks_color,
            x_ticks_rotation=x_ticks_rotation,
            y_ticks_rotation=y_ticks_rotation,
            window_title=window_title,
            plot_title=plot_title,
            plot_title_color=plot_title_color)

        plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot and you can praise yourself"


    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user"


@tool
async def pie_plot_tool(
        file_key: str,
        column_name: str = None,
        interval_count: int = None,
        how_many_numbers_after_dot: int = None,
        label_color: str = None,
        value_color: str = None,
        background_color: str = None,
        window_title: str = None,
        plot_header: str = None,
        plot_header_color: str = None,

) \
        -> Union[str, None]:
    """
    Use this tool to draw Pie plot
    You can use this function to show value distribution of a column in a pie plot
    values:
    <interval_count> Number of bins: the value that determines into how many parts the data will be divided.
    <how_many_numbers_after_dot> indicates the number of decimal places to display after the dot.
    <label_color> sets the color of the label for each pie slice.
    <value_color> sets the color of the value (percentage or number) displayed inside each pie slice.
    <background_color> Background color of plot
    <window_title> sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_header and plot_header color> plot_header sets the title of the plot, and plot_header_color sets its color.


    """

    db = DB_CACHE[file_key].compute()

    is_numeric = pd.api.types.is_numeric_dtype(db[column_name])
    default_how_many_numbers_after_dot = 2
    default_plot_title = column_name
    default_plot_title_color = "white"
    fig = plt.figure()

    if how_many_numbers_after_dot is not None:
        default_how_many_numbers_after_dot = how_many_numbers_after_dot
    if plot_header is not None:
        default_plot_title = plot_header
    if plot_header_color is not None:
        default_plot_title_color = plot_header_color

    if is_numeric:
        default_interval_count = 5

        if interval_count is not None:
            default_interval_count = interval_count

        temp = {}
        newdb = pd.DataFrame()
        linspace_result = np.linspace(db[column_name].min(), db[column_name].max(), default_interval_count + 1)
        newdb["binned"] = pd.cut(db[column_name], bins=linspace_result, include_lowest=True, right=True)
        labels = newdb["binned"].unique().tolist()
        result_labels = []
        for label in labels:
            result_labels.append(f"{label.left.round(2)} - {label.right.round(2)}")
        patches, texts, autotexts = plt.pie(newdb["binned"].value_counts(), labels=result_labels,
                                            autopct=f"%1.{default_how_many_numbers_after_dot}f%%")

    else:
        labels = db[column_name].unique().tolist()
        patches, texts, autotexts = plt.pie(db[column_name].value_counts(), labels=labels,
                                            autopct=f"%1.{default_how_many_numbers_after_dot}f%%")

    if label_color is not None:
        for text in texts:
            text.set_color(label_color)

    if value_color is not None:
        for autotext in autotexts:
            autotext.set_color(value_color)
    if background_color is not None:
        fig.set_facecolor(background_color)
    if window_title is not None:
        fig.canvas.manager.set_window_title(window_title)
    plt.title(label=default_plot_title, color=default_plot_title_color)

    plt.show()
    return f"call the final_answer , you can mention about you have successfully drawn the plot and you can praise yourself"


@tool
async def line_plot_tool(
        file_key: str,
        x_column_name: str = None,
        y_column_name: str = None,
        outside_plot_color: str = None,
        inside_plot_color: str = None,
        x_axis_label_color: str = None,
        y_axis_label_color: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        x_ticks_color: str = None,
        y_ticks_color: str = None,
        x_ticks_rotation: float = None,
        y_ticks_rotation: float = None,
        window_title: str = None,
        plot_title: str = None,
        plot_title_color: str = None,
        line_color: str = None,

) \
        -> Union[str, None]:
    """
    Use this tool to draw a line plot
    
    <x_column_name and y_column_name> real column names that will use when plotting the linechart
    <file_key> : key value of the database.
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_axis_label_color and y_axis_label_color> Color of title of x-axis and y-axis
    <x_axis_label_value and y_axis_label_value>: Title value of x-axis and y-axis Don't use these values unless user wants to give a title the plot
    <x_ticks_color and y_ticks_color>: Color of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <x_ticks_rotation and y_ticks_rotation: Rotation value of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color
    
    <line_color> color of the line plot's line

    """
    try:

        if x_column_name is None and y_column_name is None:
            return "call the final_answer tool and mention in a friendly, slightly funny way that both x-axis and y-axis column names cannot be None user must specify at least one of them with his language"

        db = DB_CACHE[file_key].compute()

        default_line_color = "darkblue"

        if line_color is not None:
            default_line_color = line_color

        ax = sns.lineplot(
            x=db[x_column_name] if x_column_name else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name else range(len(db[x_column_name])),
            color=default_line_color
        )

        ax = _multiple_variable_adjuster(
            ax=ax,
            x_column_name=x_column_name,
            y_column_name=y_column_name,
            outside_plot_color=outside_plot_color,
            inside_plot_color=inside_plot_color,
            x_axis_label_color=x_axis_label_color,
            y_axis_label_color=y_axis_label_color,
            x_axis_label_value=x_axis_label_value,
            y_axis_label_value=y_axis_label_value,
            x_ticks_color=x_ticks_color,
            y_ticks_color=y_ticks_color,
            x_ticks_rotation=x_ticks_rotation,
            y_ticks_rotation=y_ticks_rotation,
            window_title=window_title,
            plot_title=plot_title,
            plot_title_color=plot_title_color)

        plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot and you can praise yourself with his language"

    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user with his language"


@tool
async def scatter_plot_tool(
        file_key: str = None,
        x_column_name: str = None,
        y_column_name: str = None,
        outside_plot_color: str = None,
        inside_plot_color: str = None,
        x_axis_label_color: str = None,
        y_axis_label_color: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        x_ticks_color: str = None,
        y_ticks_color: str = None,
        x_ticks_rotation: float = None,
        y_ticks_rotation: float = None,
        window_title: str = None,
        plot_title: str = None,
        plot_title_color: str = None,
        scatter_dot_color: str = None,

) \
        -> Union[str, None]:
    """
    Use this tool to draw a scatter plot
    You can draw Scatter chart with using this tool

    <x_column_name and y_column_name> real column names that will use when plotting the linechart
    <file_key> : key value of the database.
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_axis_label_color and y_axis_label_color> Color of title of x-axis and y-axis
    <x_axis_label_value and y_axis_label_value>: Title value of x-axis and y-axis Don't use these values unless user wants to give a title the plot
    <x_ticks_color and y_ticks_color>: Color of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <x_ticks_rotation and y_ticks_rotation: Rotation value of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color

    <scatter_dot_color> color of the scatter dots

    """
    try:
        db = DB_CACHE[file_key].compute()

        default_scatter_color = "darkblue"

        if scatter_dot_color is not None:
            default_scatter_color = scatter_dot_color

        ax = sns.scatterplot(
            x=db[x_column_name] if x_column_name else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name else range(len(db[x_column_name])),
            color=default_scatter_color,
            hue= None,
            palette= None,
        )

        ax = _multiple_variable_adjuster(
            ax=ax,
            x_column_name=x_column_name,
            y_column_name=y_column_name,
            outside_plot_color=outside_plot_color,
            inside_plot_color=inside_plot_color,
            x_axis_label_color=x_axis_label_color,
            y_axis_label_color=y_axis_label_color,
            x_axis_label_value=x_axis_label_value,
            y_axis_label_value=y_axis_label_value,
            x_ticks_color=x_ticks_color,
            y_ticks_color=y_ticks_color,
            x_ticks_rotation=x_ticks_rotation,
            y_ticks_rotation=y_ticks_rotation,
            window_title=window_title,
            plot_title=plot_title,
            plot_title_color=plot_title_color)

        plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot and you can praise yourself with his language"

    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user with his language"








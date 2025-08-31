import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from app.model.db_cache import DB_CACHE
from typing import Union
import pandas as pd


#TODO you must complete this visualization tools today


def _multiple_variable_adjuster(
        ax: plt.Axes,
        window_title: str = None,
        plot_title: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        inside_plot_color: str = None,

        #These parameters below Never going to be None you have to pass all these variables
        outside_plot_color: str = None,

        x_axis_label_color: str = None,
        y_axis_label_color: str = None,
        x_ticks_color: str = None,
        y_ticks_color: str = None,
        x_ticks_rotation: float = None,
        y_ticks_rotation: float = None,
        plot_title_color: str = None,



) \
        -> plt.Axes:
    """
    Multiple variable adjuster for matplotlib.Axes class \n
    Some visualization tools will use this function \n
    You have to pass every color and rotation values otherwise it will give error
    """


    # as I said above in this architecture these values cannot be None maybe we can control if these values are None or not
    # but it costs more than giving default values

    not_none_variables = [outside_plot_color, x_axis_label_color, y_axis_label_color,
                            x_ticks_color, y_ticks_color, x_ticks_rotation,
                          y_ticks_rotation, plot_title_color]

    for variable in not_none_variables:
        try:
            assert variable is not None
        except AssertionError:
            raise AssertionError(f"Variable {variable} cannot be None")

    fig = ax.get_figure()

    fig.set_facecolor(outside_plot_color)

    if inside_plot_color is not None:
        ax.set_facecolor(inside_plot_color)

    ax.tick_params(axis="x", color=x_ticks_color, labelcolor=x_ticks_color, labelrotation=x_ticks_rotation)
    ax.tick_params(axis="y", color=y_ticks_color, labelcolor=y_ticks_color, labelrotation=y_ticks_rotation)

    if x_axis_label_value is not None:
        ax.set_xlabel(xlabel=x_axis_label_value, color=x_axis_label_color)
    else:
        ax.set_xlabel(xlabel="")


    if y_axis_label_value is not None:
        ax.set_ylabel(ylabel=y_axis_label_value, color=y_axis_label_color)
    else:
        ax.set_ylabel(ylabel="")

    if plot_title is not None:
        ax.set_title(label=plot_title, color=plot_title_color, loc="center")


    if window_title is not None:
        fig.canvas.manager.set_window_title(title=window_title)

    return ax


@tool
async def bar_plot_tool(
        file_key: str = None,
        x_column_name: str = None,
        y_column_name: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        window_title: str = None,
        plot_title: str = None,
        outside_plot_color: str = "white",
        inside_plot_color: str = "white",
        x_axis_label_color: str = "black",
        y_axis_label_color: str = "black",
        x_ticks_color: str = "black",
        y_ticks_color: str = "black",
        plot_title_color: str = "black",
        bar_color: str = "purple",
        grid_color: str = "black",
        x_ticks_rotation: float = 0,
        y_ticks_rotation: float = 0,

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
    <distribution> if user wants to distribution of a variable set it True, user maybe want to see
    
    """
    try:
        grid_decoration = {}

        db = DB_CACHE[file_key].compute()
        if x_column_name is None and y_column_name is None:
            return "call final_answer tool and mention in a friendly, slightly funny way that both x-axis and y-axis column names cannot be None user must specify at least one of them"

        sns.set_style("whitegrid", rc={"grid.color": grid_color})

        ax = sns.barplot(
            x=db[x_column_name] if x_column_name is not None else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name is not None else range(len(db[x_column_name])),
            color=bar_color
        )
        ax = _multiple_variable_adjuster(
            ax=ax,
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
        window_title: str = None,
        plot_header: str = None,
        interval_count: int = 5,
        how_many_numbers_after_dot: int = 2,
        label_color: str = "black",
        value_color: str = "purple",
        background_color: str = "white",
        plot_header_color: str = "black",
        every_pie_pieces_color: str = None

) \
        -> Union[str, None]:
    """
    Use this tool to draw Pie plot
    You can use this function to show value distribution of a column in a pie plot whatever column is numeric or not
    values:
    <interval_count> Number of bins: the value that determines into how many parts the data will be divided.
    <how_many_numbers_after_dot> indicates the number of decimal places to display after the dot.
    <label_color> sets the color of the label for each pie slice.
    <value_color> sets the color of the value (percentage or number) displayed inside each pie slice.
    <background_color> Background color of plot
    <window_title> sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_header and plot_header color> plot_header sets the title of the plot, and plot_header_color sets its color.
    <every_pie_pieces_color> color of the every pie piece



    """
    try:
        if column_name is None:
            return "call the final_answer tool and mention about user must write a column name with his language friendly"

        default_color = sns.color_palette("Set2")
        if every_pie_pieces_color is not None:
            default_color = every_pie_pieces_color

        db = DB_CACHE[file_key].compute()

        is_numeric = pd.api.types.is_numeric_dtype(db[column_name])
        fig = plt.figure()

        if is_numeric:

            temp = {}
            newdb = pd.DataFrame()
            linspace_result = np.linspace(db[column_name].min(), db[column_name].max(), interval_count + 1)
            newdb["binned"] = pd.cut(db[column_name], bins=linspace_result, include_lowest=True, right=True)
            labels = newdb["binned"].unique().tolist()
            result_labels = []
            for label in labels:
                result_labels.append(f"{label.left.round(2)} - {label.right.round(2)}")
            patches, texts, autotexts = plt.pie(newdb["binned"].value_counts(), labels=result_labels,
                                                autopct=f"%1.{how_many_numbers_after_dot}f%%", colors=default_color)

        else:
            labels = db[column_name].unique().tolist()
            patches, texts, autotexts = plt.pie(db[column_name].value_counts(), labels=labels,
                                                autopct=f"%1.{how_many_numbers_after_dot}f%%", colors=default_color)

        for text in texts:
            text.set_color(label_color)

        for autotext in autotexts:
            autotext.set_color(value_color)

        fig.set_facecolor(background_color)

        if window_title is not None:
            fig.canvas.manager.set_window_title(window_title)

        if plot_header is not None:
            plt.title(label=plot_header, color=plot_header_color)

        plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot and you can praise yourself"
    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user"



@tool
async def line_plot_tool(
        file_key: str = None,
        x_column_name: str = None,
        y_column_name: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        window_title: str = None,
        plot_title: str = None,
        outside_plot_color: str = "white",
        inside_plot_color: str = "white",
        x_axis_label_color: str = "black",
        y_axis_label_color: str = "black",
        x_ticks_color: str = "black",
        y_ticks_color: str = "black",
        plot_title_color: str = "black",
        line_color: str = "purple",
        x_ticks_rotation: float = 0,
        y_ticks_rotation: float = 0,

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

        ax = sns.lineplot(
            x=db[x_column_name] if x_column_name is not None else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name is not None else range(len(db[x_column_name])),
            color=line_color
        )

        ax = _multiple_variable_adjuster(
            ax=ax,
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
        return f"call the final_answer tool and mention about this error {e} to user"



@tool
async def scatter_plot_tool(
        file_key: str = None,
        x_column_name: str = None,
        y_column_name: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        window_title: str = None,
        plot_title: str = None,
        outside_plot_color: str = "white",
        inside_plot_color: str = "white",
        x_axis_label_color: str = "black",
        y_axis_label_color: str = "black",
        x_ticks_color: str = "black",
        y_ticks_color: str = "black",
        plot_title_color: str = "black",
        scatter_dot_color: str = "purple",
        x_ticks_rotation: float = 0,
        y_ticks_rotation: float = 0,

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
        if x_column_name is None and y_column_name is None:
            return "call final_answer tool and mention in a friendly, slightly funny way that both x-axis and y-axis column names cannot be None user must specify at least one of them"

        db = DB_CACHE[file_key].compute()

        ax = sns.scatterplot(
            x=db[x_column_name] if x_column_name is not None else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name is not None else range(len(db[x_column_name])),
            color=scatter_dot_color,
            hue=None,
            palette=None,
        )

        ax = _multiple_variable_adjuster(
            ax=ax,
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
async def heatmap_plot_tool(
        file_key: str = None,
        column_names: list[str] = None,
        window_title: str = None,
        plot_title: str = None,
        x_axis_label_value: str = None,
        y_axis_label_value: str = None,
        background_color: str = "white",
        x_axis_label_color: str = "black",
        y_axis_label_color: str = "black",
        x_ticks_color: str = "black",
        y_ticks_color: str = "black",
        x_ticks_rotation: float = 0,
        y_ticks_rotation: float = 0,
        plot_title_color: str = "black",
        grid_width: float = None,
        grid_color: str = None,
        annot: bool = False,
) \
        -> Union[str, None]:
    """
    Use this to plot a correlation matrices with heatmap
    <column_names> string column list that will add to correlation calculation
    <background_color> background_color of the plot
    <x_axis_label_color and y_axis_label_color> Color of title of x-axis and y-axis
    <x_axis_label_value and y_axis_label_value>: Title value of x-axis and y-axis Don't use these values unless user wants to give a title the plot
    <x_ticks_color and y_ticks_color>: Color of the axis tick labels. Ticks are the values shown along the x- and y-axes.
    <x_ticks_rotation and y_ticks_rotation: Rotation value of the axis tick labels. Ticks are the numeric or percentage values shown along the x- and y-axes.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot, and it's color
    <annot> if user wants to see numbers or percentages in the heatmap's squares then set this True
    <grid_width and grid_color> grid lines between heatmap's squares
    <annot> If user wants to see value of the square it can be number or percentage set this True
    """
    try:
        if grid_width<0:
            return "Call the final_answer and mention about that the grid_width cannot be smaller than zero"

        if len(column_names)<=1:
            return "Call the final_answer tool and mention about number of column must be bigger than 1 "



        db = DB_CACHE[file_key].compute()

        extra_string = ""
        if not pd.api.types.is_numeric_dtype(db):
            db = db.select_dtypes("number")
            extra_string = "also you have successfully deleted non numeric columns"


        ax = sns.heatmap(
            data=db.corr(),
            linecolor=grid_color if grid_color is not None else "white",
            linewidths=grid_width if grid_width is not None else 1,
            annot=annot
        )

        ax = _multiple_variable_adjuster(
            ax=ax,
            outside_plot_color=background_color,
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

        plt.tight_layout()
        plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot {extra_string} and you can praise yourself with his language"

    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user with his language"

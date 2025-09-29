from app.model.tools.database_visualization_tools.visualization_imports import *
from app.model.tools.database_visualization_tools.helper_functions import _multiple_variable_adjuster
import streamlit as st
from app.config import settings


@tool
async def bar_plot_tool(
        cache_key: str,
        x_column_name: str = None,
        y_column_name: str = None,
        x_label_text: str = None,
        y_label_text: str = None,
        window_title: str = None,
        plot_title: str = None,
        outside_plot_color: str = "white",
        inside_plot_color: str = "white",
        x_label_color: str = "black",
        y_label_color: str = "black",
        x_tick_color: str = "black",
        y_tick_color: str = "black",
        plot_title_color: str = "black",
        bar_color: str = "purple",
        grid_color: str = "black",
        x_tick_rotation: float = 0,
        y_tick_rotation: float = 0,

) \
        -> str:
    """
    Bar Plot Drawer you can use this tool to draw a bar plot
    To draw a Bar Plot use this tool
    If user doesn't specify any columns then DO NOT fill x_column_name and y_column_name
    <x_column_name and y_column_name>: specify the DataFrame columns to be plotted on the x-axis and y-axis,respectively.
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_label_color and y_label_color> : Sets the color of the x-axis and y-axis titles (axis labels). These control only the axis titles, not the tick values.
    <x_label_text and y_label_text> : The text for the x-axis and y-axis titles (axis labels). Only use these if you want to display a custom name for each axis.
    <x_tick_color and y_tick_color> : Sets the color of the tick labels along the x-axis and y-axis. Ticks are the numeric or categorical values shown along the axes. This does not affect the axis title.
    <x_tick_rotation and y_tick_rotation> : Sets the rotation angle (in degrees) of the tick labels on the x-axis and y-axis. Use this to tilt tick labels for better readability or to avoid overlap.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color
    <which_axis> Indicates which axis the data will be drawn on values : "x" or "y"
    <bar_color> bar color bar bar color

    """

    try:

        plt.figure(figsize=settings.VISUALIZATION_SIZE)
        sns.set_style("whitegrid", rc={"grid.color": grid_color})

        if x_column_name is None and y_column_name is None:
            return "call final_answer tool and mention in a friendly, slightly funny way that both x-axis and y-axis column names cannot be None user must specify at least one of them"
        db = DB_CACHE[cache_key]["dask_plan"].compute()

        ax = sns.barplot(
            x=db[x_column_name] if x_column_name is not None else range(len(db[y_column_name])),
            y=db[y_column_name] if y_column_name is not None else range(len(db[x_column_name])),
            color=bar_color
        )

        ax = _multiple_variable_adjuster(
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
        st.session_state.visualization_list.append(plt.gcf())
        # plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot"

    except Exception as e:
        return f"call the final_answer tool and mention this error {e} to user"

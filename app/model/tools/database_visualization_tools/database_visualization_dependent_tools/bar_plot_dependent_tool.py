from app.model.tools.database_visualization_tools.visualization_imports import *
from app.model.tools.database_visualization_tools.helper_functions import _multiple_variable_adjuster
import streamlit as st
from app.config import settings


@tool
async def bar_plot_dependent_tool(
        cache_key: str,
        variable_name: str = None,
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
    <cache_key> read it from system prompt
    <variable_name>: variables that you will visualize only select single variable if the variable associated with this tool
    <important> the variable name must be one of them: [mean,median,standard_deviation,variance,minimum,maximum,mode,unique_counts,correlation]
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_label_color and y_label_color> : Sets the color of the x-axis and y-axis titles (axis labels). These control only the axis titles, not the tick values.
    <x_label_text and y_label_text> : The text for the x-axis and y-axis titles (axis labels). Only use these if you want to display a custom name for each axis.
    <x_tick_color and y_tick_color> : Sets the color of the tick labels along the x-axis and y-axis. Ticks are the numeric or categorical values shown along the axes. This does not affect the axis title.
    <x_tick_rotation and y_tick_rotation> : Sets the rotation angle (in degrees) of the tick labels on the x-axis and y-axis. Use this to tilt tick labels for better readability or to avoid overlap.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot, and it's color
    <which_axis> Indicates which axis the data will be drawn on values : "x" or "y"
    <bar_color> bar color bar bar color

    """

    try:

        plt.figure(figsize=settings.VISUALIZATION_SIZE)

        sns.set_style("whitegrid", rc={"grid.color": grid_color})

        if variable_name is not None:
            if variable_name == "correlation":
                return "YOU MUST Mention this: you cannot draw correlation matrices with bar plot call the heatmap plot tool"
            # print(f"VARİABLE NAMES: {variable_name}")
            variables_that_will_visualize = DB_CACHE[cache_key]["analysis_result"][variable_name]

            ax = sns.barplot(
                x=variables_that_will_visualize.keys(),
                y=variables_that_will_visualize.values(),
                color=bar_color
            )
        else:
            return "Mention you dont understand what variable you will draw"

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

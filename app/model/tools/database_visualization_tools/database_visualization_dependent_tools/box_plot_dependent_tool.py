from app.model.tools.database_visualization_tools.visualization_imports import *
from app.model.tools.database_visualization_tools.helper_functions import _multiple_variable_adjuster
import streamlit as st
from app.config import settings
@tool
async def box_plot_dependent_tool(
        cache_key: str,
        variable_name: str = None,
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
        box_color: str = "white",
) \
        -> str:
    """
    Use this tool to draw a box plot

    <variable_name>: variables that you will visualize only select single variable if the variable associated with this tool
    <important> the variable name must be one of them: [mean,median,standard_deviation,variance,minimum,maximum,mode,unique_counts,correlation]
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
    <box_color> : color box  all colors box color box
    <median_line_color and median_line_width> Control the color and thickness of the internal line in each box, representing the median value of the distribution.
    """
    try:

        plt.figure(figsize=settings.VISUALIZATION_SIZE)

        if variable_name is not None:
            if variable_name == "correlation":
                return "YOU MUST Mention this: you cannot draw correlation matrices with box plot call the heatmap plot tool"
            # print(f"VARİABLE NAMES: {variable_name}")
            variables_that_will_visualize = DB_CACHE[cache_key]["analysis_result"][variable_name]
            print(f"VARİABLES THAT WİLL VİSUALİZE: {variables_that_will_visualize}")
            print(f"CURRENT VARİABLE NAME: {variable_name}")
            ax = sns.boxplot(
                x=variables_that_will_visualize.keys(),
                y=variables_that_will_visualize.values(),
                color=box_color
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
        return f"call the final_answer tool and mention about this error {e} to user with his language"
import matplotlib.pyplot as plt

from app.model.tools.database_visualization_tools.visualization_imports import *
from app.model.tools.database_visualization_tools.helper_functions import _multiple_variable_adjuster
import streamlit as st
from app.config import settings


@tool
async def scatter_plot_dependent_tool(
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
        scatter_dot_color: str = "purple",
        x_tick_rotation: float = 0,
        y_tick_rotation: float = 0,

) \
        -> str:
    """
    Use this tool to draw a scatter plot
    You can draw Scatter chart with using this tool

    <variable_name>: variables that you will visualize only select single variable if the variable associated with this tool
    <important> the variable name must be one of them: [mean,median,standard_deviation,variance,minimum,maximum,mode,unique_counts,correlation]
    <outside_plot_color>: The background color of the figure area outside the plot axes.
    <inside_plot_color>: The background color of the plotting area where data and grid lines are drawn.
    <x_label_color and y_label_color> : Sets the color of the x-axis and y-axis titles (axis labels). These control only the axis titles, not the tick values.
    <x_label_text and y_label_text> : The text for the x-axis and y-axis titles (axis labels). Only use these if you want to display a custom name for each axis.
    <x_tick_color and y_tick_color> : Sets the color of the tick labels along the x-axis and y-axis. Ticks are the numeric or categorical values shown along the axes. This does not affect the axis title.
    <x_tick_rotation and y_tick_rotation> : Sets the rotation angle (in degrees) of the tick labels on the x-axis and y-axis. Use this to tilt tick labels for better readability or to avoid overlap.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <which_axis> Indicates which axis the data will be drawn on values : "x" or "y"
    <plot_title , plot_title_color> plot title that will show in the top center of the plot and it's color

    <scatter_dot_color> color of the scatter dots

    """
    try:

        plt.figure(figsize=settings.VISUALIZATION_SIZE)

        if variable_name is not None:
            variables_that_will_visualize = DB_CACHE[cache_key]["analysis_result"][variable_name]
            if variable_name == "correlation":
                corr_long = variables_that_will_visualize.reset_index().melt(id_vars="index")
                corr_long.columns = ["X", "Y", "Value"]

                ax = sns.scatterplot(
                    data=corr_long,
                    x="X",
                    y="Y",
                    hue="Value",
                    palette="coolwarm",
                    sizes=(100, 500)
                )

                # Değerleri noktaların üstüne yazmak
                for i in range(len(corr_long)):
                    plt.text(
                        x=i % 2, y=i // 2,
                        s=f"{corr_long['Value'][i]:.2f}",
                        ha='center', va='center'
                    )



            else:
                ax = sns.scatterplot(
                    x=variables_that_will_visualize.keys(),
                    y=variables_that_will_visualize.values(),
                    color=scatter_dot_color,
                    hue=None,
                    palette=None, )
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

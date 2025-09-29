from typing import Union , List

import matplotlib.pyplot as plt

from app.model.tools.database_visualization_tools.visualization_imports import *
import streamlit as st
from app.config import settings

@tool
async def pie_plot_dependent_tool(
        cache_key: str,
        variable_name: str = None,
        window_title: str = None,
        plot_header: str = None,
        interval_count: int = 5,
        how_many_numbers_after_dot: int = 2,
        label_color: str = "black",
        value_color: str = "purple",
        background_color: str = "white",
        plot_header_color: str = "black",
        every_pie_pieces_color: Union[str , List[str]] = None,
        pie_splitter_line_width: float = None,
        pie_splitter_line_color: str = None,

) \
        -> str:
    """
    Use this tool to draw a Pie plot
    <variable_name>: variables that you will visualize only select single variable if the variable associated with this tool
    <important> the variable name must be one of them: [mean,median,standard_deviation,variance,minimum,maximum,mode,unique_counts,correlation]
    <interval_count> Number of bins: the value that determines into how many parts the data will be divided.
    <how_many_numbers_after_dot> indicates the number of decimal places to display after the dot.
    <label_color> sets the color of the label for each pie slice.
    <value_color> sets the color of the value (percentage or number) displayed inside each pie slice.
    <background_color> Background color of plot
    <window_title> sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_header and plot_header color> plot_header sets the title of the plot, and plot_header_color sets its color.
    <every_pie_pieces_color> color of pie pieces or fragments it can be single color or multiple color for each piece or fragment
    <pie_splitter_line_width and pie_splitter_line_color> line that splits pie pieces width , and its color
    """
    try:
        plt.figure(figsize=settings.VISUALIZATION_SIZE)

        if variable_name is not None:
            if variable_name == "correlation":
                return "YOU MUST Mention this: you cannot draw correlation matrices with pie plot call the heatmap plot tool"

            default_color = sns.color_palette("Set2")
            if every_pie_pieces_color is not None:
                if isinstance(every_pie_pieces_color, str):
                    default_color = [every_pie_pieces_color]
                else:
                    default_color = every_pie_pieces_color

            fig, ax = plt.subplots()
            variables_that_will_visualize = DB_CACHE[cache_key]["analysis_result"][variable_name]
            patches, texts, autotexts =\
                plt.pie(
                variables_that_will_visualize.values(),
                labels=variables_that_will_visualize.keys(),
                autopct=f"%1.{how_many_numbers_after_dot}f%%",
                colors=default_color,
                wedgeprops={
                    "linewidth": pie_splitter_line_width if pie_splitter_line_width is not None else 1,
                    "edgecolor": pie_splitter_line_color if pie_splitter_line_color is not None else "black",
                }

            )

        else:
            return "Mention you dont understand what variable you will draw"



        for text in texts:
            text.set_color(label_color)

        for autotext in autotexts:
            autotext.set_color(value_color)

        fig.set_facecolor(background_color)

        if window_title is not None:
            fig.canvas.manager.set_window_title(window_title)

        if plot_header is not None:
            plt.title(label=plot_header, color=plot_header_color)

        plt.tight_layout()
        st.session_state.visualization_list.append(plt.gcf())


        # plt.show()
        return f"say you have successfully drawn the plot"

    except Exception as e:
        return f"say something about this error {e} to user"
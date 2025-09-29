import matplotlib.pyplot as plt
from typing import Union , List
from app.model.tools.database_visualization_tools.visualization_imports import *
import numpy as np
import pandas as pd
import streamlit as st
from app.config import settings
@tool
async def pie_plot_tool(
        cache_key: str,
        column_name: str = None,
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
    Use this tool to draw Pie plot
    You can use this function to show value distribution of a column in a pie plot whatever column is numeric or not
    <column_name>: The single column name for which the user wants to see the distribution
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

        default_color = sns.color_palette("Set2")
        if every_pie_pieces_color is not None:
            if isinstance(every_pie_pieces_color, str):
                default_color = [every_pie_pieces_color]
            else:
                default_color = every_pie_pieces_color

        fig,ax = plt.subplots()

        if column_name is None:
            return "say this user must write a column name with his language friendly"

        db = DB_CACHE[cache_key]["dask_plan"].compute()

        is_numeric = pd.api.types.is_numeric_dtype(db[column_name])

        if is_numeric:
            newdb = pd.DataFrame()
            linspace_result = np.linspace(db[column_name].min(), db[column_name].max(), interval_count + 1)
            newdb["binned"] = pd.cut(db[column_name], bins=linspace_result, include_lowest=True, right=True)
            labels = newdb["binned"].unique().tolist()
            result_labels = []
            for label in labels:
                result_labels.append(f"{label.left.round(2)} - {label.right.round(2)}")
            patches, texts, autotexts = \
                plt.pie(
                    newdb["binned"].value_counts(),
                    labels=result_labels,
                    autopct=f"%1.{how_many_numbers_after_dot}f%%",
                    colors=default_color,
                    wedgeprops={
                        "linewidth": pie_splitter_line_width if pie_splitter_line_width is not None else 1,
                        "edgecolor": pie_splitter_line_color if pie_splitter_line_color is not None else "black",
                    }

                )

        else:
            labels = db[column_name].unique().tolist()
            patches, texts, autotexts = \
                plt.pie(
                    db[column_name].value_counts(),
                    labels=labels,
                    autopct=f"%1.{how_many_numbers_after_dot}f%%",
                    colors=default_color,
                    wedgeprops={
                        "linewidth": pie_splitter_line_width if pie_splitter_line_width is not None else 1,
                        "edgecolor": pie_splitter_line_color if pie_splitter_line_color is not None else "black",
                    }
                )




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
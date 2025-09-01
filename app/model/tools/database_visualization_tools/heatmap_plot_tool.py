from app.model.tools.database_visualization_tools.visualization_imports import *
from app.model.tools.database_visualization_tools.helper_functions import _multiple_variable_adjuster
import pandas as pd
@tool
async def heatmap_plot_tool(
        file_key: str = None,
        column_names: list[str] = None,
        window_title: str = None,
        plot_title: str = None,
        x_label_value: str = None,
        y_label_value: str = None,
        background_color: str = "white",
        x_label_color: str = "black",
        y_label_color: str = "black",
        x_tick_color: str = "black",
        y_tick_color: str = "black",
        x_tick_rotation: float = 0,
        y_tick_rotation: float = 0,
        plot_title_color: str = "black",
        grid_width: float = None,
        grid_color: str = None,
        annot: bool = False,
) \
        -> str:
    """
    Use this to plot a correlation matrices with heatmap
    <column_names> string column list that will add to correlation calculation
    <background_color> background_color of the plot
    <x_label_color and y_label_color> : Sets the color of the x-axis and y-axis titles (axis labels). These control only the axis titles, not the tick values.
    <x_label_text and y_label_text> : The text for the x-axis and y-axis titles (axis labels). Only use these if you want to display a custom name for each axis.
    <x_tick_color and y_tick_color> : Sets the color of the tick labels along the x-axis and y-axis. Ticks are the numeric or categorical values shown along the axes. This does not affect the axis title.
    <x_tick_rotation and y_tick_rotation> : Sets the rotation angle (in degrees) of the tick labels on the x-axis and y-axis. Use this to tilt tick labels for better readability or to avoid overlap.
    <window_title>: sets the name displayed in the top-left corner of the plot window when it opens.
    <plot_title , plot_title_color> plot title that will show in the top center of the plot, and it's color
    <annot> if user wants to see numbers or percentages in the heatmap's squares then set this True
    <grid_width and grid_color> grid lines between heatmap's squares
    <annot> If user wants to see value of the square it can be number or percentage set this True
    """
    try:
        if grid_width is not None:
            if grid_width < 0:
                return "Call the final_answer and mention about that the grid_width cannot be smaller than zero"

        if len(column_names) <= 1:
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
            x_label_color=x_label_color,
            y_label_color=y_label_color,
            x_label_text=x_label_value,
            y_label_text=y_label_value,
            x_tick_color=x_tick_color,
            y_tick_color=y_tick_color,
            x_tick_rotation=x_tick_rotation,
            y_tick_rotation=y_tick_rotation,
            window_title=window_title,
            plot_title=plot_title,
            plot_title_color=plot_title_color)

        plt.tight_layout()
        plt.show()
        return f"call the final_answer , you can mention about you have successfully drawn the plot {extra_string} and you can praise yourself with his language"

    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user with his language"
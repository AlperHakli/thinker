import matplotlib.pyplot as plt


def multiple_variable_adjuster(
        ax: plt.Axes,
        window_title: str = None,
        plot_title: str = None,
        x_label_text: str = None,
        y_label_text: str = None,
        inside_plot_color: str = None,
        #These parameters below Never going to be None you have to pass all these variables
        outside_plot_color: str = None,

        x_label_color: str = None,
        y_label_color: str = None,
        x_tick_color: str = None,
        y_tick_color: str = None,
        x_tick_rotation: float = None,
        y_tick_rotation: float = None,
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

    not_none_variables = [outside_plot_color, x_label_color, y_label_color,
                          x_tick_color, y_tick_color, x_tick_rotation,
                          y_tick_rotation, plot_title_color]

    for variable in not_none_variables:
        try:
            assert variable is not None
        except AssertionError:
            raise AssertionError(f"Variable {variable} cannot be None")

    fig = ax.get_figure()

    fig.set_facecolor(outside_plot_color)

    if inside_plot_color is not None:
        ax.set_facecolor(inside_plot_color)

    ax.tick_params(axis="x", color=x_tick_color, labelcolor=x_tick_color, labelrotation=x_tick_rotation)
    ax.tick_params(axis="y", color=y_tick_color, labelcolor=y_tick_color, labelrotation=y_tick_rotation)

    if x_label_text is not None:
        ax.set_xlabel(xlabel=x_label_text, color=x_label_color)
    else:
        ax.set_xlabel(xlabel="")

    if y_label_text is not None:
        ax.set_ylabel(ylabel=y_label_text, color=y_label_color)
    else:
        ax.set_ylabel(ylabel="")

    if plot_title is not None:
        ax.set_title(label=plot_title, color=plot_title_color, loc="center")

    if window_title is not None:
        fig.canvas.manager.set_window_title(title=window_title)

    return ax


def equal_name_controller(x_column_name: str, y_column_name: str) \
        -> str:
    """
    it controls that both columns are equal or not
    """
    if x_column_name == y_column_name:
        return "call final_answer mention x column name and y column name can not be same user must specify that column belong x-axis or y-axis"

colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

colored_title = "".join(
    f'<span style="color:{colors[i % len(colors)]}">{char}</span>'
    for i, char in enumerate("Thinker")
)
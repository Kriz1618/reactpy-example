from fastapi import FastAPI
from reactpy import component, html, hooks, event
from reactpy.backend.fastapi import configure


app = FastAPI()

data = [
    {"id": 1, "title": "Firs item", "level": 1},
    {"id": 2, "title": "Second item", "level": 1},
    {"id": 3, "title": "Third item", "level": 3},
    {"id": 4, "title": "Fouth item", "level": 1},
    {"id": 5, "title": "Fith item", "level": 2},
]


@component
def TitleComponent():
    return html.h1({"style": {"text-align": "center"}}, "ReactPy Basic Example")


@component
def ParentComponent(items):
    tasks = [Item(item) for item in items]
    return html.ul(tasks)


@component
def Form(data):
    title, set_title = hooks.use_state("")
    level, set_level = hooks.use_state(1)
    items, set_items = hooks.use_state(data)

    def clean_form():
        set_title("")
        set_level(1)

    @event(prevent_default=True)
    def handle_submit(event):
        current_data = items
        current_data.append({
            "id": len(data),
            "title": title,
            "level": int(level)
        })
        set_items(current_data)
        clean_form()

    return html.section(
        html.form(
            {"on_submit": handle_submit, "style": {
                "display": "inline-grid", "padding-bottom": "1em", "margin-left": "3%"}},
            html.div(
                html.label(
                    {"style": {"margin-right": "1rem"}}, "Title:"),
                html.input(
                    {
                        "type": "text",
                        "placeholder": "Title...",
                        "value": title,
                        "on_change": lambda event: set_title(event["target"]["value"]),
                    }
                ),
            ),
            html.div(
                {"style": {"padding-bottom": "1em", "padding-top": "1em"}},
                html.label({"style": {"margin-right": "1rem"}}, "Level:"),
                html.select(
                    {
                        "value": level,
                        "on_change": lambda event: set_level(event["target"]["value"]),
                    },
                    html.option({"value": 1}, "1"),
                    html.option({"value": 2}, "2"),
                    html.option({"value": 3}, "3")
                )
            ),
            html.button({"type": "submit"}, "Save")
        ),
        ParentComponent(items)
    )


@component
def Item(item):
    counter, set_counter = hooks.use_state(0)
    hight_level = item['level'] > 1

    def handle_click(e):
        set_counter(counter + 1)
        print("Clicked")

    return html.li({
        "key": item['id'],
        "style": {
            "background": "orange" if hight_level else "skyblue",
            "padding": "1rem",
            "border": "1px solid black",
            "margin": "1rem"
        }
    }, html.div({
        "style": {
            "display": "flex",
            "justify-content": "space-between"}},
        "{} - {} - {}".format(item['title'], item['level'], counter),
        html.button({"on_click": handle_click}, "Remove")
    ),
    )


@component
def App():
    return html.section(
        TitleComponent(),
        Form(data),
    )


configure(app, App)

import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

app = dash.Dash(__name__, use_pages=True)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        dmc.Header(
            height=60,
            padding="xs",
            children=dmc.Group(
                position="apart",
                align="center",
                style={"height": "100%"},
                children=[
                    dmc.Text("My Dash App", weight=700, size="xl"),
                    dmc.Group(
                        spacing="md",
                        children=[
                            dmc.Anchor(page["name"], href=page["path"])
                            for page in dash.page_registry.values()
                        ],
                    ),
                ],
            ),
        ),
        dcc.Location(id="url"),
        html.Div(id="page-content"),
    ],)

@callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    return dash.page_registry.get(pathname, dash.page_registry["/"])["layout"](
          )

if __name__ == "__main__":
    app.run_server(debug=True)
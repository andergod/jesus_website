import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

app = dash.Dash(__name__, use_pages=True)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        # Top header built from HTML + Mantine components (dmc.Header isn't available in this env)
        html.Header(
            dmc.Container(
                dmc.Group(
                    align="center",
                    style={"height": "60px", "display": "flex", "alignItems": "center"},
                    children=[
                        dmc.Text("Jesus Personal Portfolio", size="xl"),
                        dmc.Group(
                            gap="md",
                            children=[
                                dcc.Link(
                                    page["name"],
                                    href=page["path"],
                                    style={"textDecoration": "none"},
                                )
                                for page in dash.page_registry.values()
                                if page["name"] == "Home"
                            ],
                        ),
                    ],
                ),
                fluid=True,
                style={"paddingTop": "6px", "paddingBottom": "6px"},
            ),
            style={"boxShadow": "0 1px 3px rgba(0,0,0,0.08)", "zIndex": 10},
        ),
        dcc.Location(id="url"),
        dash.page_container,
    ],
)


if __name__ == "__main__":
    app.run(debug=True)

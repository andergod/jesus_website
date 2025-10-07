import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    path="/projects",
    name="project overview",
)

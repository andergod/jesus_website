import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(__name__, path="/", name="Home")

# Example project data - replace or extend with real projects
PROJECTS = [
    {
        "title": "Order Book Contruction",
        "summary": "Recreate the logic of a matching engine and build a full order book from raw market data using market standard C++ techniques.",
        "tags": ["C++", "order books", "execution", "low-latency"],
        "link": "/projects/order-book",
    },
    {
        "title": "Webscrapping & Sentiment Analysis",
        "summary": "Modified a standard webscrapping structure using beutifulsoup4 and requests to collect and analyse sentiment from crypto-magazines.",
        "tags": ["python", "webscrapping", "sentiment analysis"],
        "link": "/projects/webscrapping-crypto",
    },
    {
        "title": "Some interesting macro graphs",
        "summary": "Visualization usage and interpretation of various macroeconomic indicators.",
        "tags": ["matplotlib", "macroeconomic", "visualisation"],
        "link": "/projects/macro-graphs",
    },
]


def project_card(p):
    return dmc.Card(
        children=[
            dmc.Group(
                [
                    dmc.Text(p["title"], size="lg"),
                    dmc.Badge(
                        ", ".join(p["tags"]),
                        variant="light",
                        color="blue",
                        style={"marginLeft": "auto"},
                    ),
                ],
                style={"justifyContent": "space-between"},
            ),
            dmc.Space(h=8),
            dmc.Text(p["summary"], style={"color": "#555"}, size="sm"),
            dmc.Space(h=12),
            dmc.Group(
                [
                    dcc.Link(
                        dmc.Button("Open", variant="outline", size="sm"), href=p["link"]
                    ),
                    dcc.Link(dmc.Button("Details", size="sm"), href=p["link"]),
                ],
                style={"gap": "0.5rem"},
            ),
        ],
        shadow="sm",
        radius="md",
        style={"minWidth": 300, "padding": "1.5rem"},
    )


layout = dmc.Container(
    size="xl",
    style={"padding": "0 1rem"},
    children=[
        dmc.Space(h=20),
        # Hero
        dmc.SimpleGrid(
            [
                dmc.Stack(
                    [
                        dmc.Title("Quant Portfolio - Research & Engineering", order=1),
                        dmc.Text(
                            "Research engineer working on systematic strategies, execution, risk systems, and data science for a quantitative hedge fund.",
                            style={"color": "#555"},
                        ),
                        dmc.Space(h=10),
                        dmc.Group(
                            [
                                dcc.Link(
                                    dmc.Button(
                                        "Projects",
                                        variant="gradient",
                                        gradient={"from": "indigo", "to": "cyan"},
                                    ),
                                    href="/projects",
                                ),
                                dcc.Link(
                                    dmc.Button("Resume / CV", variant="outline"),
                                    href="/resume",
                                ),
                            ]
                        ),
                    ]
                ),
                dmc.Card(
                    children=[
                        dmc.Image(
                            src="https://images.unsplash.com/photo-1559526324-593bc073d938?w=800&q=80",
                            alt="finance",
                            radius="sm",
                        ),
                        dmc.Text(
                            "Quantitative research • Execution • Data engineering",
                            ta="center",
                            size="sm",
                            style={"color": "#555"},
                        ),
                    ],
                    shadow="sm",
                    padding="md",
                ),
            ],
            cols=2,
        ),
        dmc.Space(h=30),
        # Projects section
        dmc.Title("Projects", order=2),
        dmc.Text(
            "Selected work and internal projects from my quant research and engineering efforts.",
            size="sm",
            style={"color": "#555"},
        ),
        dmc.Space(h=12),
        dmc.SimpleGrid(
            [project_card(p) for p in PROJECTS],
            cols=3,
        ),
        dmc.Space(h=30),
        # Resume section
        dmc.Group(
            [
                dmc.Stack(
                    [
                        dmc.Title("Resume", order=2),
                        dmc.Text(
                            "A short summary of professional experience and a downloadable CV."
                        ),
                        dmc.List(
                            [
                                dmc.ListItem(
                                    "Quantitative Research & Strategy Development - signal research and model evaluation"
                                ),
                                dmc.ListItem(
                                    "Execution & Transaction Cost Analysis - slippage modelling and smart order routing"
                                ),
                                dmc.ListItem(
                                    "Data Engineering - pipelines for alternative and market data"
                                ),
                            ]
                        ),
                        dmc.Space(h=8),
                        dmc.Group(
                            [
                                dcc.Link(
                                    dmc.Button("View full resume", variant="outline"),
                                    href="/resume",
                                ),
                                dcc.Link(
                                    dmc.Button("Download CV (PDF)", variant="filled"),
                                    href="/assets/cv.pdf",
                                ),
                            ]
                        ),
                    ],
                    gap="xs",
                    align="center",
                ),
                dmc.Card(
                    [
                        dmc.Text("Experience snapshot", size="md"),
                        dmc.Space(h=8),
                        dmc.Text(
                            "- 4+ years at systematic hedge funds\n- Python, C++, SQL, cloud infra\n- Time-series statistics & ML"
                        ),
                    ],
                    shadow="xs",
                    style={"width": "300px", "padding": "1rem"},
                ),
            ],
            gap="lg",
            align="center",
        ),
        dmc.Space(h=40),
        html.Footer(
            dmc.Text("© Your Name — Built with Dash & Mantine", size="sm"),
        ),
    ],
)

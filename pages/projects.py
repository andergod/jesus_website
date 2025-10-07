import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(__name__, path="/projects", name="Projects")

DETAILED_PROJECTS = [
    {
        "title": "Order Book Construction",
        "summary": "A high-performance order book implementation that recreates the logic of a matching engine using market standard C++ techniques.",
        "description": """
        This project implements a full-featured order book system that processes market data and maintains a real-time view of the order book. 
        Key features include:
        • Efficient price-time priority matching engine
        • Low-latency market data processing
        • Real-time order book state management
        • Support for various order types (limit, market, IOC)
        """,
        "tech_stack": [
            "C++",
            "CMake",
            "Google Test",
            "Memory Management",
            "Data Structures",
        ],
        "tags": ["order books", "execution", "low-latency"],
        "demo_link": "/projects/order-book",
        "github_link": "https://github.com/yourusername/orderbook",
    },
    {
        "title": "Webscrapping & Sentiment Analysis",
        "summary": "An automated system that collects and analyzes cryptocurrency news for sentiment-based trading signals.",
        "description": """
        A sophisticated web scraping and NLP pipeline that aggregates crypto news from multiple sources and generates trading signals. 
        The system features:
        • Robust web scraping from major crypto news sites
        • VADER sentiment analysis for trading signals
        • Entity recognition for crypto asset identification
        • Automated signal generation pipeline
        """,
        "tech_stack": ["Python", "BeautifulSoup4", "NLTK", "spaCy", "Pandas"],
        "tags": ["webscrapping", "sentiment analysis", "nlp"],
        "demo_link": "/projects/webscrapping-crypto",
        "github_link": "https://github.com/andergod/Webscrap_crypto",
    },
    {
        "title": "Macro Analysis Dashboard",
        "summary": "Interactive visualization and analysis of key macroeconomic indicators.",
        "description": """
        A comprehensive dashboard for analyzing and visualizing macroeconomic data. 
        Features include:
        • Time series analysis of key indicators
        • Cross-market correlation analysis
        • Interactive data exploration
        • Automated data updates and processing
        """,
        "tech_stack": ["Python", "Matplotlib", "Pandas", "Dash", "SQL"],
        "tags": ["macroeconomic", "visualisation", "dashboard"],
        "demo_link": "/projects/macro-graphs",
        "github_link": "https://github.com/yourusername/macro-dashboard",
    },
]


def project_details_card(p):
    return dmc.Card(
        children=[
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            dmc.Title(p["title"], order=2),
                            dmc.Group(
                                [
                                    dmc.Badge(tag, variant="light", size="sm")
                                    for tag in p["tech_stack"][
                                        :3
                                    ]  # Show first 3 tech stack items
                                ]
                            ),
                        ],
                        style={"justifyContent": "space-between"},
                    ),
                    dmc.Text(p["summary"], size="lg", style={"color": "#555"}),
                    dmc.Space(h=10),
                    dmc.Text(
                        p["description"],
                        style={
                            "whiteSpace": "pre-line",
                            "color": "#555",
                            "lineHeight": "1.7",
                        },
                    ),
                    dmc.Space(h=20),
                    dmc.Group(
                        [
                            dcc.Link(
                                dmc.Button(
                                    "View Project",
                                    variant="gradient",
                                    gradient={"from": "indigo", "to": "cyan"},
                                ),
                                href=p["demo_link"],
                            ),
                            dmc.Anchor(
                                dmc.Button(
                                    "Source Code ",
                                    variant="outline",
                                ),
                                href=p["github_link"],
                                target="_blank",
                            ),
                        ]
                    ),
                ]
            ),
        ],
        style={"padding": "2rem"},
        shadow="sm",
    )


layout = dmc.Container(
    size="xl",
    style={"padding": "2rem"},
    children=[
        dmc.Stack(
            [
                dmc.Title("Projects", order=1),
                dmc.Text(
                    "A collection of my work in quantitative research, execution systems, and data engineering.",
                    size="lg",
                    style={"color": "#555"},
                ),
                dmc.Space(h=30),
                dmc.Stack(
                    [project_details_card(p) for p in DETAILED_PROJECTS],
                    style={"gap": "2rem"},
                ),
            ]
        ),
    ],
)

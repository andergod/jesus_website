import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    path="/projects/webscrapping-crypto",
    name="Webscrapping & Sentiment Analysis",
)


def read_webscrapping_importingData():
    with open("assets/code_snippets/webscrapping_importingData.txt", "r") as file:
        return file.read()


def read_webscrapping_sentimentAnalysis():
    with open("assets/code_snippets/webscrapping_sentimentAnalysis.txt", "r") as file:
        return file.read()


layout = dmc.Container(
    size="xl",
    px="md",
    children=[
        dmc.Space(h=30),
        # Project Header
        dmc.Stack(
            [
                dmc.Title("Web Scrapper for Crypto Sentiment Analysis", order=1),
                dmc.Group(
                    [
                        dmc.Badge("Python", size="lg", variant="dot"),
                        dmc.Badge("Web Scraping", size="lg", variant="dot"),
                        dmc.Badge("NLP", size="lg", variant="dot"),
                        dmc.Badge("Sentiment Analysis", size="lg", variant="dot"),
                    ]
                ),
                dmc.Text(
                    "Published: February 4, 2024", style={"color": "#555"}, size="sm"
                ),
            ]
        ),
        dmc.Space(h=30),
        # GitHub Link Card
        dmc.Card(
            children=[
                dmc.Group(
                    [
                        dmc.Text("🔗 Project Repository", size="sm"),
                        dmc.Anchor(
                            "View on GitHub",
                            href="https://github.com/andergod/Webscrap_crypto.git",
                            target="_blank",
                            variant="gradient",
                            gradient={"from": "indigo", "to": "cyan"},
                        ),
                    ],
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            p="md",
        ),
        dmc.Space(h=30),
        # Importing Data Section
        dmc.Stack(
            [
                dmc.Title("Importing Data", order=2),
                dmc.Stack(
                    [
                        dmc.Text(
                            """The project starts with a robust data collection system built around the WebsiteData class. This class 
                        implements an advanced web scraping pipeline designed specifically for cryptocurrency news aggregation, 
                        targeting high-quality sources including Crypto News, Coindesk, Yahoo Finance, and The Independent.""",
                            style={
                                "lineHeight": 1.8,
                                "fontSize": "1.1rem",
                                "marginBottom": "1rem",
                            },
                        ),
                        dmc.Text(
                            """At its core, the scraping engine employs BeautifulSoup4 for HTML parsing, combined with intelligent 
                        request handling to navigate each website's unique structure. The implementation follows a modular architecture 
                        where each news source has its dedicated method, ensuring maintainable code and allowing for easy addition 
                        of new sources.""",
                            style={"lineHeight": 1.8, "color": "#555"},
                        ),
                        dmc.Text(
                            """Key technical features include:""",
                            size="lg",
                            style={"marginTop": "1rem", "marginBottom": "0.5rem"},
                        ),
                        dmc.List(
                            [
                                dmc.ListItem(
                                    "Intelligent HTML parsing with CSS selector optimization"
                                ),
                                dmc.ListItem(
                                    "Robust error handling for network requests and parsing failures"
                                ),
                                dmc.ListItem(
                                    "Content cleaning pipeline with source-specific filters"
                                ),
                            ],
                            style={"marginBottom": "1rem"},
                        ),
                        dmc.Text(
                            """The text_from_relevant function serves as the final layer, providing sophisticated content extraction 
                        with source-specific processing rules. This ensures that only relevant content is extracted, handling 
                        edge cases like sponsored content removal and proper text truncation.""",
                            style={"lineHeight": 1.8, "color": "#555"},
                        ),
                    ],
                ),
                dmc.Space(h=20),
                dmc.Card(
                    children=[
                        dmc.CodeHighlight(
                            code=read_webscrapping_importingData(),
                            language="python",
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    style={"backgroundColor": "#f8f9fa"},
                ),
            ]
        ),
        dmc.Space(h=40),
        # Sentiment Analysis Section
        dmc.Stack(
            [
                dmc.Title("Sentiment Analysis", order=2),
                dmc.Text(
                    """ This script analyzes sentiment and provides trading recommendations for cryptocurrencies based on news articles. 
                    It uses VADER (Valence Aware Dictionary and Sentiment Reasoner) from NLTK for sentiment analysis, along with 
                    spaCy for entity recognition.""",
                    style={"lineHeight": 1.6},
                ),
                # Key Features Cards
                dmc.SimpleGrid(
                    cols=2,
                    spacing="lg",
                    children=[
                        dmc.Card(
                            children=[
                                dmc.Title("VADER Analysis", order=4),
                                dmc.Text(
                                    "Uses lexicon-based approach with sentiment scores from -4 to +4. "
                                    "Considers intensifiers, negations, and context.",
                                    size="sm",
                                ),
                            ],
                            withBorder=True,
                            padding="lg",
                        ),
                        dmc.Card(
                            children=[
                                dmc.Title("Trading Signals", order=4),
                                dmc.Text(
                                    "Generates Buy/Sell/Hold recommendations based on compound sentiment scores. "
                                    "Threshold-based decision making.",
                                    size="sm",
                                ),
                            ],
                            withBorder=True,
                            padding="lg",
                        ),
                    ],
                ),
                dmc.Space(h=20),
                # Code Example
                dmc.Card(
                    children=[
                        dmc.CodeHighlight(
                            code=read_webscrapping_sentimentAnalysis(),
                            language="python",
                        ),
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    style={"backgroundColor": "#f8f9fa"},
                ),
            ]
        ),
        dmc.Space(h=40),
        # Results Section
        dmc.Stack(
            [
                dmc.Title("Results", order=2),
                dmc.Text(
                    "The script processes news articles in real-time and generates trading signals based on sentiment analysis. "
                    "Here's an example of the output:",
                    style={"lineHeight": 1.6},
                ),
                dmc.Image(
                    src="/assets/Result_crypto.png",
                    alt="Crypto Analysis Results",
                ),
                dmc.Text(
                    "Example of trading signals generated from news sentiment",
                    size="sm",
                    style={"color": "#555", "fontStyle": "italic"},
                ),
            ]
        ),
        dmc.Space(h=40),
    ],
)

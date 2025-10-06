import dash 
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(__name__, path='/', name='Home')

# Example project data - replace or extend with real projects
PROJECTS = [
    {
        "title": "Alpha Signals Engine",
        "summary": "Research and productionisation of alpha factors using alternative data and signal blending.",
        "tags": ["signal", "research", "production"],
        "link": "/projects/alpha-signals",
    },
    {
        "title": "Execution Cost Model",
        "summary": "Microstructure-aware execution cost modelling and transaction cost analysis (TCA).",
        "tags": ["execution", "tca", "microstructure"],
        "link": "/projects/execution-cost",
    },
    {
        "title": "Risk & Exposure Dashboard",
        "summary": "Real-time exposures, P&L attribution and stress testing dashboards for traders and PMs.",
        "tags": ["dashboard", "risk", "visualisation"],
        "link": "/projects/risk-dashboard",
    },
]


def project_card(p):
    return dmc.Card(
        children=[
            dmc.Group([
                dmc.Text(p['title'], size='lg'),
                dmc.Badge(
                    ", ".join(p['tags']),
                    variant='light',
                    color='blue',
                    style={'marginLeft': 'auto'},
                ),
            ], position='apart'),
            dmc.Space(h=8),
            dmc.Text(p['summary'], color='dimmed', size='sm'),
            dmc.Space(h=12),
            dmc.Group([
                dmc.Button('Open', variant='outline', size='sm', href=p['link']),
                dmc.Button('Details', size='sm', href=p['link']),
            ]),
        ],
        shadow='sm',
        padding='lg',
        radius='md',
        style={'minWidth': 300},
    )


layout = dmc.Container(
    children=[
        dmc.Space(h=20),
        # Hero
        dmc.Grid([
            dmc.GridCol(
                dmc.Stack([
                    dmc.Title("Quant Portfolio - Research & Engineering", order=1),
                    dmc.Text(
                        "Research engineer working on systematic strategies, execution, risk systems, and data science for a quantitative hedge fund.",
                        style = {'color': '#555'}
                    ),
                    dmc.Space(h=10),
                    dmc.Group([
                        dcc.Link(dmc.Button("Projects", variant='gradient', gradient={"from": "indigo", "to": "cyan"}, ), href='/projects'),
                        dcc.Link(dmc.Button("Resume / CV", variant='outline'), href='/resume') 
                    ]),
                ]),
                span = 8,
            ),
            dmc.GridCol(
                dmc.Card(
                    children=[
                        dmc.Image(src='https://images.unsplash.com/photo-1559526324-593bc073d938?w=800&q=80', alt='finance', radius='sm'),
                        dmc.Text("Quantitative research • Execution • Data engineering", ta="center", size='sm', style = {'color': '#555'}),
                    ],
                    shadow='sm',
                    padding='md',
                ),
                span=4,
            ),
        ]),

        dmc.Space(h=30),

        # Projects section
        dmc.Title("Projects", order=2),
        dmc.Text("Selected work and internal projects from my quant research and engineering efforts.", size='sm', style = {'color': '#555'}),
        dmc.Space(h=12),
        dmc.SimpleGrid([project_card(p) for p in PROJECTS], cols=3, breakpoints=[{"maxWidth": 980, "cols": 2}, {"maxWidth": 600, "cols": 1}]),

        dmc.Space(h=30),

        # Resume section
        dmc.Group([
            dmc.Stack([
                dmc.Title("Resume", order=2),
                dmc.Text("A short summary of professional experience and a downloadable CV."),
                dmc.List([
                    dmc.ListItem("Quantitative Research & Strategy Development - signal research and model evaluation"),
                    dmc.ListItem("Execution & Transaction Cost Analysis - slippage modelling and smart order routing"),
                    dmc.ListItem("Data Engineering - pipelines for alternative and market data"),
                ]),
                dmc.Space(h=8),
                dmc.Group([
                    dcc.Link(dmc.Button("View full resume", variant='outline'), href='/resume'),
                    dcc.Link(dmc.Button("Download CV (PDF)", variant='filled', target='_blank'), href='/assets/cv.pdf'),
                ]),
            ], spacing='xs', grow=True),
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Experience snapshot", weight=700),
                    dmc.Space(h=8),
                    dmc.Text("- 4+ years at systematic hedge funds\n- Python, C++, SQL, cloud infra\n- Time-series statistics & ML"),
                ], padding='md', shadow='xs'),
                span=4,
            ),
        ], position='apart'),

        dmc.Space(h=40),

        html.Footer(
            dmc.Text("© Your Name — Built with Dash & Mantine", align='center', size='sm'),
            height=60,)
    ]
)

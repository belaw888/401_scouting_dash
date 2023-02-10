# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash
# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, dash_table, Input, Output
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy
from soupsieve import select
import utils.sheets_data_manager as manager
import utils.tba_api_requests as tbapy
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

topbar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className=""),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=False,
    pills=True,
    className="bg-dark",
    justified=True
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("FRC Team 401 - Scouting Data",
                         style={'fontSize': 50, 'textAlign': 'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
        dbc.Col([
        	topbar
        ], xs=12, sm=12, md=12, lg=12, xl=12, xxl=12)
        ]
    ),
    dbc.Row([
        dbc.Col([
		    dash.page_container
        ])
		]
    )
	], fluid=True)

if __name__ == '__main__':
	app.run_server(debug=True)

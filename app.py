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

sheets = manager.sheets_data_manager()
sheets_data = sheets.get_google_sheets_dataframe()

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale-1.0'}])
        #    suppress_callback_exceptions=True)
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
    className="bg-dark mb-5",
    justified=True
)

app.layout = dbc.Container([
    
    dcc.Store(id='session_database', storage_type='session'),
    
    dbc.Row([
        # dbc.Col(html.Div(html.Img(src=dash.get_asset_url('assets/index.jpeg'))),
                # xs=12, sm=12, md=3, lg=3, xl=3),
        dbc.Col(html.H1("FRC Team 401 Scouting Data"),
                xs=12, sm=12, md=9, lg=9, xl=9, className='d-flex justify-content-around'),
        
        dbc.Col(update_button := dbc.Button(
            "Update Data", class_name="", color='success', n_clicks=0),
                xs=2, sm=2, md=3, lg=3, xl=3, className='d-flex justify-content-around'
                ),
    ], className='mx-5 my-3'),
    
    # html.Div(id='test', children=[]),
    
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


@app.callback(
    Output('session_database', 'data'),
    Input(update_button, 'n_clicks')
)

def update_session_data(n_clicks):
    sheets.refresh_google_sheets_dataframe()
    json_string = sheets.get_as_json()
    
    return json_string

# @app.callback(
#     Output('test', 'children'),
#     Input('session_database', 'data')
# )

# def update(data):
#     dataframe = sheets.parse_json(data)
#     return dataframe.at[1,'Match Type']


if __name__ == '__main__':
	app.run_server(debug=True)

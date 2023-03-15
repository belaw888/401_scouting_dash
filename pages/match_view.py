# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from audioop import avg
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash
# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, callback, dash_table, Input, Output
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy
from soupsieve import select
import utils.sheets_data_manager as manager
import utils.tba_api_requests as tbapy
import dash_bootstrap_components as dbc
# from app import app


dash.register_page(__name__,
                   name='Match View',
                   title='Match View')

sheets = manager.sheets_data_manager()
sheets_data = sheets.get_google_sheets_dataframe()
teams_list = sheets.get_team_list()

tba = tbapy.tba_api_requests('tba_api_key.txt')

columns = [{'name': i, 'id': i} for i in sheets_data.columns]
config = {'displayModeBar': False}

# print(columns)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            select_team := dcc.Dropdown(
                options=teams_list,
                value=401,
                id='select_team',
                persistence=True,
                multi=False,
                searchable=False,
                className='mb-4 text-primary d-flex justify-content-around'
            )
        ], xs=12, sm=12, md=3, lg=3, xl=3)]),
    
    html.Br(),
    
    dbc.Row([
        dbc.Row([dbc.Col(html.Div(i, className='text-center bg-info border border-2')) for i in ['Blue 1', 'Blue 2', 'Blue 3']] +
        		[dbc.Col(html.Div(i, className='text-center bg-danger border border-2')) for i in ['Red 1', 'Red 2', 'Red 3']]),
        dbc.Row([dbc.Col(html.Div(i, className='text-center bg-info border border-2 bg-opacity-75')) for i in ['401', '122', '1629']] +
        		[dbc.Col(html.Div(i, className='text-center bg-danger border border-2 bg-opacity-75')) for i in ['620', '8230', '5724']]),
        dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-2')) for i in range(7,13)]),
        dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-2')) for i in range(13,25)]),
        dbc.Row()
   			]
	)
    
    
    
    ])

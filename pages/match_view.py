# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from audioop import avg
from stat import SF_APPEND
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
event_key = '2023vabla'
match_keys = tba.event_match_keys(event_key)
match_keys = [key.split('_')[1] for key in match_keys]
sort_match = lambda x: int(x.split('m')[1])
qm = [key for key in match_keys if key[0:2] == 'qm']
qm.sort(key=sort_match)
sf = [key for key in match_keys if key[0:2] == 'sf']
sf.sort(key=lambda x: int(x.split('f')[1].split('m')[0]))
f  = [key for key in match_keys if key[0:1] == 'f']
f.sort(key=sort_match)
# sf = 
# f = 
# match_nums = [int(key.split('m')[1]) for key in match_keys]
# match_keys.sort(key=lambda x: int(x.split('m')[1]) if 'f' not in x else max(match_nums) + int(x.split('f')[1].split('m')[0]))
sorted_matches = qm + sf + f

columns = [{'name': i, 'id': i} for i in sheets_data.columns]
config = {'displayModeBar': False}

# print(columns)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            select_match := dcc.Dropdown(
                options=sorted_matches,
                value=sorted_matches[0],
                id='select_match',
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
        
        (teams := html.Div()),
        
        
        dbc.Row()
   			]
	)
    
    
    
    ])


@callback(
    [
        Output(teams, component_property='children'),
    ],
    [
    	Input(select_match, component_property='value')
    ]
)
def update_profile(select_match):
    
    match_key = event_key + '_' + select_match
    
    match_robots = tba.match_robots(match_key)
    print(match_robots)
    team_nums = [int(num.split('c')[1]) for num in match_robots]
    blue_teams = team_nums[:3]
    red_teams = team_nums[3:]
    
    blue_className = 'text-center bg-info border border-2 bg-opacity-75'
    red_className = 'text-center bg-danger border border-2 bg-opacity-75'
    
    teams_layout = dbc.Row(
    
    [dbc.Col(html.Div(i, className=blue_className)) for i in blue_teams] +
    [dbc.Col(html.Div(i, className=red_className))for i in red_teams])
             
    filler = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-2')) for i in range(7, 13)])] 
    filler1 = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-2')) for i in range(13, 25)])]
             
    filler2 = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-2')) for i in range(7, 13)])] 

    filler3 = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-2')) for i in range(1, 3)])] 

    return [[teams_layout] + filler + filler1 + filler2 + filler3]
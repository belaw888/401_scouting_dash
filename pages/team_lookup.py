# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from audioop import avg
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, callback, dash_table, Input, Output  # pip install dash (version 2.0.0 or higher)
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy
from soupsieve import select
import utils.sheets_data_manager as manager
import utils.tba_api_requests as tbapy
import dash_bootstrap_components as dbc
# from app import app


dash.register_page(__name__, 
                   name='Team Lookup',
                   title='Team Lookup')

sheets = manager.sheets_data_manager()
sheets_data = sheets.get_google_sheets_dataframe()
teams_list = sheets.get_team_list()

tba = tbapy.tba_api_requests('tba_api_key.txt')

columns = [{'name': i, 'id': i} for i in sheets_data.columns]
# print(columns)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            select_team := dcc.Dropdown(
                             options=teams_list,
                             value="401",
                             multi=False,
                             className='mb-4 text-primary'
                             )
                ], width={'size': 3}),
        
        dbc.Col([
            team_name_string := html.H4( children=[],
                    className='text-center'
                    )
                ], width={'size': 6}),
        
        dbc.Col([
            team_location := html.H4(children=[],
                    className='text-center'
                    )
                ], width={'size': 3})
    ]),
    
    dbc.Row(
        dbc.Col(
            auto_grid_graph := dcc.Graph(figure={})
        )
    ),
    
    html.Br()
    
])

@callback(
    [   
        Output(team_name_string, component_property='children'),
        Output(team_location, component_property='children'),
        Output(auto_grid_graph, 'figure')
    ],
    [
    	Input(select_team, component_property='value'),
        Input('session_database', 'data')
    ]
)

def update_profile(select_team, session_database):
    profile_dict = tba.team_profile(select_team)
    nickname = profile_dict.get('nickname')

    state_prov = profile_dict.get('state_prov')
    city = profile_dict.get('city')

    scouting_results = sheets.parse_json(session_database)
    team_scouting_results = sheets.get_team_data_static(scouting_results, select_team)
    
    x = team_scouting_results['Match Number']
    
    auto_top_scored = team_scouting_results['Auto Cones Top'] + team_scouting_results['Auto Cubes Top']
    
    auto_top_trace = go.Bar(
        x=x,
        y=auto_top_scored,
        name='Auto Grid (Top)',
        text=auto_top_scored,
        textposition='inside',
      		hovertemplate="Top: %{y}" +
      		"<extra></extra>",
      		marker_color='deepskyblue')
    
    auto_mid_scored = team_scouting_results['Auto Cones Mid'] + team_scouting_results['Auto Cubes Mid']
    

    auto_mid_trace = go.Bar(
        x=x,
        y=auto_mid_scored,
        name='Auto Grid (Mid)',
        text=auto_mid_scored,
        textfont=dict(color='black'),
        textposition='inside',
      		hovertemplate="Mid: %{y}" +
      		"<extra></extra>",
      		marker_color='crimson')
    
    auto_low_scored = team_scouting_results['Auto Cones Low'] + team_scouting_results['Auto Cubes Low']

    auto_low_trace = go.Bar(
        x=x,
        y=auto_low_scored,
        name='Auto Grid (Low)',
        text=auto_low_scored,
        textposition='inside',
      		hovertemplate="Low: %{y}" +
      		"<extra></extra>",
      		marker_color='lightseagreen')
    
    auto_mean_trace = go.Scatter(
            x=x,
            y=[auto_low_scored.mean() + auto_mid_scored.mean() + auto_top_scored.mean() for val in x],
            name='Avg Game Pieces Per Match',
            mode='lines',
            opacity=0.7,
            line=dict(dash='dash',
                      width=4,
                      backoff=100),
            hovertemplate="Avg Game Pieces: %{y}" +
            "<extra></extra>",
        )

    auto_grid_data = [auto_low_trace, auto_mid_trace, auto_top_trace, auto_mean_trace]

    auto_grid_layout = go.Layout(
        barmode='stack', 
        title_text='<b>Game Pieces Scored - Auto</b>',
        )
    
    auto_grid_fig = go.Figure(
        data=auto_grid_data,
        layout=auto_grid_layout)
    
    auto_grid_fig.update_yaxes(
        range=[0, 20],
        title_text="<b>Number of Game Pieces</b>")

    auto_grid_fig.update_xaxes(
        type='category',
        title_text="<b>Match Number</b>")
     
    return [f'Team {select_team} - {nickname}', f'{city}, {state_prov}', auto_grid_fig]





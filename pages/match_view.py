# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash
# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, callback, dash_table, Input, Output
from plotly.subplots import make_subplots
import numpy
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
# print(sorted_matches[0])

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
        dbc.Row([dbc.Col(html.Div(i, className='text-center bg-info border border-3')) for i in ['Blue 1', 'Blue 2', 'Blue 3']] +
        		[dbc.Col(html.Div(i, className='text-center bg-danger border border-3')) for i in ['Red 1', 'Red 2', 'Red 3']]),
        
        (teams := html.Div()),
        
        
        dbc.Row()
   			]
	),
    
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
    
    
    ])


@callback(
    [
        Output(teams, component_property='children'),
    ],
    [
    	Input(select_match, component_property='value'),
        Input('session_analysis_database', 'data')
    ]
)
def update_profile(select_match, session_analysis_database):
    analysis = sheets.parse_json(session_analysis_database)
    
    match_key = event_key + '_' + select_match
    
    match_robots = tba.match_robots(match_key)
    # print(match_robots)
    team_nums = [int(num.split('c')[1]) for num in match_robots]
    blue_teams = team_nums[:3]
    red_teams = team_nums[3:]
    
    blue_className = 'd-flex justify-content-center bg-info border border-3 bg-opacity-75 py-3 fs-4'
    red_className = 'd-flex justify-content-center bg-danger border border-3 bg-opacity-75 py-3 fs-4'
    
    
    avg_points = [analysis.loc[analysis['Team Number'] == team]['Total Points'].mean() for team in team_nums]
    avg_points = [round(avg, 2) for avg in avg_points]
    
    max_points = [analysis.loc[analysis['Team Number'] == team]['Total Points'].max() for team in team_nums]
    max_points = [round(max, 2) for max in max_points]
    
    points = []
    piece_pie = []
    level_pie = []
    for team in team_nums:
        team_stats = analysis.loc[analysis['Team Number'] == team]
        
        top_cubes = team_stats['Top Cubes']
        top_cones = team_stats['Top Cones']
        mid_cubes = team_stats['Mid Cubes']
        mid_cones = team_stats['Mid Cones']
        low_cubes = team_stats['Low Cubes']
        low_cones = team_stats['Low Cones']
        
        total_points = team_stats['Total Points']
        total_cubes_series = team_stats['Total Cubes']
        total_cones_series = team_stats['Total Cones']
        
        non_zero_low_points = total_points[total_points != 0].min()
        avg_points = total_points.mean()
        high_points = total_points.max()
        
        avgs = [round(non_zero_low_points, 2), round(avg_points, 2), round(high_points, 2)]
        
        points.append([html.Div(i, className='text-center bg-light text-dark border border-1 py-2 d-inline-flex justify-content-center flex-grow-1 fs-6') for i in avgs])
        # points.append(round(avg_points, 2))
        # points.append(round(high_points, 2))
        
        team_avgs = pd.DataFrame(
            [{"Cones Scored": total_cones_series.sum(), "Cubes Scored": total_cubes_series.sum(), 'Top Cones': top_cones.sum()}])

        colors = [px.colors.qualitative.Plotly[0], 'gold', px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[5], px.colors.qualitative.Plotly[5], px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[1]]

        # print(team_avgs)
        # pieces_pie_chart = go.Figure(data=[go.Pie(labels=team_avgs.columns, values=team_avgs.iloc[0])])
        pieces_pie_chart = go.Figure(
                                       data=[go.Sunburst( 
                                       labels=['Cubes', 'Cones', 'Top Cubes', 'Top Cones', 'Mid Cubes', 'Mid Cones', 'Low Cubes', 'Low Cones'],
                                       parents=['',     '',       'Cubes',    'Cones',     'Cubes',     'Cones',     'Cubes',     'Cones'],
                                       values=[total_cubes_series.sum(),
                                               total_cones_series.sum(),
                                               top_cubes.sum(),
                                               top_cones.sum(),
                                               mid_cubes.sum(),
                                               mid_cones.sum(),
                                               low_cubes.sum(),
                                               low_cones.sum()],
                                       branchvalues='total'
                                                                        )])
        pieces_pie_chart.update_traces(hoverinfo='label+value', textinfo='percent root',
                                   marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        pieces_pie_chart.update_layout(showlegend=False)
        # print(type(pieces_pie_chart))
        pieces_pie_chart.update_layout(margin=dict(t=3, b=3, l=3, r=3), paper_bgcolor='rgba(0,0,0,0)',
                                       plot_bgcolor='rgba(0,0,0,0)')
        # pieces_pie_chart.update_layout(width=150, height=150)
        piece_pie.append(pieces_pie_chart)
        
    
    teams_layout = dbc.Row(
    
    [dbc.Col(html.B(html.Div(i, className=blue_className))) for i in blue_teams] +
    [dbc.Col(html.B(html.Div(i, className=red_className))) for i in red_teams])
    
    # print(charts)
    filler = [dbc.Row([dbc.Col(i, width=2, id='min_avg_max', className='border border-3') for i in points])]
    
    filler1 = [dbc.Row([dbc.Col(dcc.Graph(figure=i, id='pie_pieces', className='text-center bg-light border border-3'), width=2) for i in piece_pie])]
             
    filler2 = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-3')) for i in range(7, 13)])] 

    filler3 = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-3')) for i in range(1, 3)])] 

    return [[teams_layout] + filler + filler1 + filler2 + filler3]
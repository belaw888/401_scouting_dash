# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from enum import auto
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
event_key = '2023gal'

def update_matches(event_key):
    match_keys = tba.event_match_keys(event_key)
    match_keys = [key.split('_')[1] for key in match_keys]
    sort_match = lambda x: int(x.split('m')[1])
    qm = [key for key in match_keys if key[0:2] == 'qm']
    qm.sort(key=sort_match)
    sf = [key for key in match_keys if key[0:2] == 'sf']
    sf.sort(key=lambda x: int(x.split('f')[1].split('m')[0]))
    f  = [key for key in match_keys if key[0:1] == 'f']
    f.sort(key=sort_match)
    sorted_matches = qm + sf + f
    return sorted_matches
    
# sf = 
# f = 
# match_nums = [int(key.split('m')[1]) for key in match_keys]
# match_keys.sort(key=lambda x: int(x.split('m')[1]) if 'f' not in x else max(match_nums) + int(x.split('f')[1].split('m')[0]))
# print(sorted_matches[0])

columns = [{'name': i, 'id': i} for i in sheets_data.columns]
config = {'displayModeBar': False}

# print(columns)

layout = dbc.Container([
    # dbc.Row([
    #     dcc.Input(
    #         id="test_input",
    #         type='text',
    #         placeholder="lol")
    #         ]),
    # html.Br(),
    dbc.Row([
        dbc.Col([
            select_match := dcc.Dropdown(
                id='select_match',
                value='qm1',
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
        Output(select_match, 'options'),
    ],
    [
    	Input(select_match, component_property='value'),
        Input('session_analysis_database', 'data'),
        # Input('test_input', 'value')
    ]
)
def update_profile(select_match, session_analysis_database):
    # print(type(test_input))
    analysis = sheets.parse_json(session_analysis_database)
    
    match_key = str(event_key) + '_' + select_match
    
    print(match_key)
    
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
    
    x = ['Avg Charge Points', 'Avg Grid Points']
    
    bar_colors = {team_nums[0]:  px.colors.qualitative.Plotly[5], team_nums[1]:  px.colors.qualitative.Plotly[2], team_nums[2]: px.colors.qualitative.Plotly[1],
                  team_nums[3]:  px.colors.qualitative.Plotly[5], team_nums[4]:  px.colors.qualitative.Plotly[2], team_nums[5]: px.colors.qualitative.Plotly[1]}
    
    px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[5], px.colors.qualitative.Plotly[
        5], px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[1]
    
    green = px.colors.qualitative.Plotly[2]
    purple = px.colors.qualitative.Plotly[0]
    blue = px.colors.qualitative.G10[0]
    red = px.colors.qualitative.Plotly[1]
    yellow = 'gold'
    
    
    points = []
    tele_pieces_aggregate = []
    auto_pieces_aggregate = []
    
    piece_pie = []
    avg_points_bar = []
    blue_bar_points_charge = []
    blue_bar_points_grid = []
    red_bar_points_charge = []
    red_bar_points_grid = []
    for team in team_nums:
        team_stats = analysis.loc[analysis['Team Number'] == team]
        
        avg_charge_points = team_stats['Total Charge Points'].mean()
        avg_charge_points = round(avg_charge_points, 2)
    
        avg_grid_points = team_stats['Total Grid Points'].mean() 
        avg_grid_points = round(avg_grid_points, 2)
        
        top_cubes = team_stats['Top Cubes']
        top_cones = team_stats['Top Cones']
        mid_cubes = team_stats['Mid Cubes']
        mid_cones = team_stats['Mid Cones']
    
        
        total_points = team_stats['Total Points']
        total_cubes_series = team_stats['Total Cubes']
        total_cones_series = team_stats['Total Cones']
        total_hybrid_series = team_stats['Low Pieces']
        
        if team in blue_teams:
            blue_bar_points_charge.append(avg_charge_points)
            blue_bar_points_grid.append(avg_grid_points)
        if team in red_teams:
            red_bar_points_charge.append(avg_charge_points)
            red_bar_points_grid.append(avg_grid_points)
        
        non_zero_min_points = total_points[total_points != 0].min()
        avg_points = total_points.mean()
        high_points = total_points.max()
        
        tele_pieces = team_stats['Tele Pieces'] 
        non_zero_min_tele_pieces = tele_pieces[tele_pieces != 0].min()
        avg_tele_pieces = tele_pieces.mean()
        max_tele_pieces = tele_pieces.max()
        
        auto_pieces = team_stats['Auto Pieces'] 
        non_zero_min_auto_pieces = auto_pieces[auto_pieces != 0].min()
        avg_auto_pieces = auto_pieces.mean()
        max_auto_pieces = auto_pieces.max()
        
        tele_pieces_list = [round(non_zero_min_tele_pieces, 2), round(avg_tele_pieces, 2), round(max_tele_pieces, 2)]
        auto_pieces_list = [round(non_zero_min_auto_pieces, 2), round(avg_auto_pieces, 2), round(max_auto_pieces, 2)]
        
        avgs = [round(non_zero_min_points, 2), round(avg_points, 2), round(high_points, 2)]
        
        points.append([html.Div(i, className='text-center bg-light text-dark border border-1 py-2 d-inline-flex justify-content-center flex-grow-1 fs-6') for i in avgs])
        tele_pieces_aggregate.append([html.Div(i, className='text-center bg-light text-dark border border-1 py-2 d-inline-flex justify-content-center flex-grow-1 fs-6') for i in tele_pieces_list])
        auto_pieces_aggregate.append([html.Div(i, className='text-center bg-light text-dark border border-1 py-2 d-inline-flex justify-content-center flex-grow-1 fs-6') for i in auto_pieces_list])
        # points.append(round(avg_points, 2))
        # points.append(round(high_points, 2))
        
        team_avgs = pd.DataFrame(
            [{"Cones Scored": total_cones_series.sum(), "Cubes Scored": total_cubes_series.sum(), 'Top Cones': top_cones.sum()}])

        colors = [px.colors.qualitative.Plotly[0], 'gold', 'grey',px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[2], blue]

        # print(team_avgs)
        # pieces_pie_chart = go.Figure(data=[go.Pie(labels=team_avgs.columns, values=team_avgs.iloc[0])])
        pieces_pie_chart = go.Figure(
                                       data=[go.Sunburst( 
                                       labels=['Cubes', 'Cones', 'Hybrid', 'Top Cubes', 'Top Cones', 'Mid Cubes', 'Mid Cones',],
                                       parents=['',     '',       '',   'Cubes',    'Cones',     'Cubes',     'Cones',     ],
                                 values=[total_cubes_series.sum(),
                                               total_cones_series.sum(),
                                               total_hybrid_series.sum(),
                                               top_cubes.sum(),
                                               top_cones.sum(),
                                               mid_cubes.sum(),
                                               mid_cones.sum(),
                                               ],
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
        
        y = [avg_charge_points, avg_grid_points]
        
        team_trace = go.Bar(
            x=x,
            y=y,
            name=team,
            text= y,
            textposition='inside',
            hovertemplate="Points: %{y}" +
            "<extra></extra>",
            marker_color=bar_colors[team])
        
        # avg_grid_trace = go.Bar(
        #     x=x,
        #     y=avg_grid_points,
        #     name=team,
        #     text=avg_grid_points,
        #     textposition='inside',
        #     hovertemplate="Top: %{y}" +
        #     "<extra></extra>",
        #     marker_color='crimson')
        
        # avg_points_bar.append(avg_charge_trace)
        avg_points_bar.append(team_trace)
    
    # print(avg_points_bar)
    
    blue_avg_points_bar_fig = go.Figure(avg_points_bar[:3])
    blue_avg_points_bar_fig.update_layout(barmode='stack')
    blue_avg_points_bar_fig.update_yaxes(range=[0, 150])
    
    red_avg_points_bar_fig = go.Figure(avg_points_bar[3:])
    red_avg_points_bar_fig.update_layout(barmode='stack')
    red_avg_points_bar_fig.update_yaxes(range=[0, 150])
    
    red_avg_points_bar_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    blue_avg_points_bar_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    
    red_bar_points_charge = sum(red_bar_points_charge)
    red_bar_points_charge = round(red_bar_points_charge, 2)
    red_bar_points_grid = sum(red_bar_points_grid)
    red_bar_points_grid = round(red_bar_points_grid, 2)

    red_avg_points_bar_fig.add_trace(go.Scatter(
        x=x,
        y=[red_bar_points_charge, red_bar_points_grid],
        text=['<b>' + str(red_bar_points_charge) + '</b>',
              '<b>' + str(red_bar_points_grid) + '</b>'],
        mode='text',
        textposition='top center',
        textfont=dict(
            size=15,
        ),
        hovertemplate=None,
        hoverinfo='skip',
        showlegend=False
    ))
    
    blue_bar_points_charge = sum(blue_bar_points_charge)
    blue_bar_points_charge = round(blue_bar_points_charge, 2)
    blue_bar_points_grid = sum(blue_bar_points_grid)
    blue_bar_points_grid = round(blue_bar_points_grid, 2)
    
    blue_avg_points_bar_fig.add_trace(go.Scatter(
        x=x,
        y=[blue_bar_points_charge, blue_bar_points_grid],
        text=['<b>' + str(blue_bar_points_charge) + '</b>',
              '<b>' + str(blue_bar_points_grid) + '</b>'],
        mode='text',
        textposition='top center',
        textfont=dict(
            size=15,
        ),
        hovertemplate=None,
        hoverinfo='skip',
        showlegend=False
    ))
    
    # bar_points_contribution
    bar = [blue_avg_points_bar_fig, red_avg_points_bar_fig]
        
    teams_layout = dbc.Row(
    
    [dbc.Col(html.B(html.Div(i, className=blue_className))) for i in blue_teams] +
    [dbc.Col(html.B(html.Div(i, className=red_className))) for i in red_teams])
    
    # print(charts)
    min_avg_max_label = dbc.Row(dbc.Col(html.Div('Total Points (Nonzero Min, Avg, Max)',
                                className='text-center text-black bg-light border border-3 py-1 fs-5')))
    
    filler = [dbc.Row([dbc.Col(i, width=2, id='min_avg_max', className='border border-3') for i in points])]
    
    pie_chart_label = dbc.Row(dbc.Col(html.P([
        html.Span('Cones', style={'color': yellow}, id='color_word'),
        html.Span(' v '),
        html.Span('Cubes', style={'color': purple}, id='color_word'),
        html.Span(' v '),
        html.Span('Hybrid', style={'color': 'grey'}, id='color_word'),
        html.Span(' - '),
        html.Span('Mid', style={'color': blue}, id='color_word'),
        html.Span(' v '),
        html.Span('High', style={'color': green}, id='color_word')], className='text-center text-black bg-light mb-0 border border-3 py-1 fs-5')))
    
    filler1 = [dbc.Row([dbc.Col(dcc.Graph(figure=i, id='pie_pieces', className='text-center bg-light border border-3'), width=2) for i in piece_pie])]
    
    tele_pieces_label = dbc.Row(dbc.Col(html.Div('Teleop Pieces (Nonzero Min, Avg, Max)',
                                className='text-center text-black bg-light border border-3 py-1 fs-5')))
    
    filler0 = [dbc.Row([dbc.Col(i, width=2, id='tele_pieces', className='border border-3') for i in tele_pieces_aggregate])]
    
    auto_pieces_label = dbc.Row(dbc.Col(html.Div('Auto Pieces (Nonzero Min, Avg, Max)',
                                className='text-center text-black bg-light border border-3 py-1 fs-5')))
    
    auto_pieces = [dbc.Row([dbc.Col(i, width=2, id='auto_pieces', className='border border-3') for i in auto_pieces_aggregate])]
             
    filler2 = [dbc.Row([dbc.Col(dcc.Graph(figure=i, id='bar_points_contribution', className='text-center bg-light border border-3'), width=6) for i in bar])] 

    filler3 = [dbc.Row([dbc.Col(html.Div(i, className='text-center bg-light border border-3')) for i in range(1, 3)])] 
    
    options = update_matches(event_key)
    print(options)
    # value = update_matches()[0],

    
    

    return [teams_layout] + [min_avg_max_label] + filler + [pie_chart_label] + filler1 + [tele_pieces_label] + filler0 + [auto_pieces_label] + auto_pieces + filler2 + filler3, options

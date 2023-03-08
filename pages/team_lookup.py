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
config = {'displayModeBar': False}

# print(columns)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            select_team := dcc.Dropdown(
                             options=teams_list,
                             value="401",
                             multi=False,
                             searchable=False,
                             className='mb-4 text-primary d-flex justify-content-around"'
                             )
                ], xs=12, sm=12, md=3, lg=3, xl=3),#width={'size': 3}),
        
        dbc.Col([
            team_name_string := html.H4( children=[],
                                         className='d-flex justify-content-md-center justify-content-sm-start'
                    )
                ], xs=12, sm=12, md=6, lg=6, xl=6),  # width={'size': 6}),
        
        dbc.Col([
            team_location := html.H4(children=[],
                                     className='d-flex justify-content-md-end justify-content-sm-start'
                    )
                ], xs=12, sm=12, md=3, lg=3, xl=3),  # width={'size': 3})
    ], className="d-flex justify-content-around"),
    
    html.Br(),
    
    dbc.Row(
        dbc.Col(),
    ),
    dbc.Row(
        dbc.Col([html.Div(style={'background-color': 'white', 'border-radius': '15px'}, children=[
                 html.Div(html.I(html.B('Autonomous Game Pieces Scored')),
                className='d-flex justify-content-center py-4 px-2',
                          style={"color": "#2a3f5f", "font-size": 20,
                'font-family': 'DejaVu Sans'}),
                
            auto_grid_graph := dcc.Graph(figure={}, config=config),
            html.Br()])],
                                         xs=12, sm=12, md=12, lg=12, xl=12,
            )
        ),
    
    html.Br(),
    html.Br(),

    dbc.Row(
        dbc.Col([html.Div(style={'background-color': 'white', 'border-radius': '15px'}, children=[
                 html.Div(html.I(html.B('Teleop Game Pieces Scored')),
                          className='d-flex justify-content-center py-4 px-2',
                          style={"color": "#2a3f5f", "font-size": 20,
                                 'font-family': 'DejaVu Sans'}),

                 tele_grid_graph := dcc.Graph(figure={}, config=config),
                 html.Br()])],
                xs=12, sm=12, md=12, lg=12, xl=12,
                )
    ),
    
    html.Br()
    
])

@callback(
    [   
        Output(team_name_string, component_property='children'),
        Output(team_location, component_property='children'),
        Output(auto_grid_graph, 'figure'),
        Output(tele_grid_graph, 'figure')
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
    # filter = team_scouting_results['data_id'].value_counts()
    # print(team_scouting_results['data_id'])
    # print(filter)
    # team_scouting_results = team_scouting_results['data_id'].isin(filter)
    # print(team_scouting_results)
    
    team_scouting_results.drop_duplicates(inplace=True, subset=['data_id'])
    
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
            name='Avg Game Pieces/Match',
            mode='lines',
            opacity=0.7,
            line=dict(dash='dash',
                      width=4,
                      backoff=100),
            hovertemplate="Avg Game Pieces: %{y}" +
            "<extra></extra>",
            legendrank=4
        )
    
    auto_grid_data = [auto_low_trace, auto_mid_trace, auto_top_trace, auto_mean_trace]

    auto_grid_layout = go.Layout(
        barmode='stack', 
        # title={
        # 'text': '<b>Game Pieces Scored - Auto</b>',
        # 'y': 0.95,
        # 'x': 0.5,
        # 'xanchor': 'center',
        # 'yanchor': 'top'}
        )
        
    auto_grid_fig = go.Figure(
        data=auto_grid_data,
        layout=auto_grid_layout)
    
    auto_grid_fig.update_yaxes(automargin='top')

    
    auto_grid_fig.update_yaxes(
        range=[0, 10],
        title_text="<b>Number of Game Pieces</b>")

    auto_grid_fig.update_xaxes(
        type='category',
        title_text="<b>Match Number</b>")
    
    auto_grid_fig.update_layout(
        margin=dict(
            l=75,
            r=55,
            b=75,
            t=50,
            pad=2),
        
        legend=dict(
        # entrywidthmode='fraction',
        entrywidth=150,
        orientation='h',
        yanchor="bottom",
        y=1.05,
        xanchor="right",
        x=1
    ))
    
    bold_auto_items = []
    auto_total_scored = auto_top_scored + auto_mid_scored + auto_low_scored

    for item in auto_total_scored.tolist():
        bold_auto_items.append('<b>' + str(item) + '</b>')

    
    auto_grid_fig.add_trace(go.Scatter(
        x=x,
        y=auto_total_scored,
        text=bold_auto_items,
        mode='text',
        textposition='top center',
        textfont=dict(
            size=15,
        ),
        hovertemplate=None,
        hoverinfo='skip',
        showlegend=False
    ))

    
    #######################################3
    
    tele_top_scored = team_scouting_results['Tele Cones Top'] + team_scouting_results['Tele Cubes Top']

    tele_top_trace = go.Bar(
        x=x,
        y=tele_top_scored,
        name='Tele Grid (Top)',
        text=tele_top_scored,
        textposition='inside',
      		hovertemplate="Top: %{y}" +
      		"<extra></extra>",
      		marker_color='deepskyblue')

    tele_mid_scored = team_scouting_results['Tele Cones Mid'] + team_scouting_results['Tele Cubes Mid']

    tele_mid_trace = go.Bar(
        x=x,
        y=tele_mid_scored,
        name='Tele Grid (Mid)',
        text=tele_mid_scored,
        textfont=dict(color='black'),
        textposition='inside',
      		hovertemplate="Mid: %{y}" +
      		"<extra></extra>",
      		marker_color='crimson')

    tele_low_scored = team_scouting_results['Tele Cones Low'] + team_scouting_results['Tele Cubes Low']

    tele_low_trace = go.Bar(
        x=x,
        y=tele_low_scored,
        name='Tele Grid (Low)',
        text=tele_low_scored,
        textposition='inside',
      		hovertemplate="Low: %{y}" +
      		"<extra></extra>",
      		marker_color='lightseagreen')

    tele_mean_trace = go.Scatter(
        x=x,
        y=[tele_low_scored.mean() + tele_mid_scored.mean() +
           tele_top_scored.mean() for val in x],
        name='Avg Game Pieces/Match',
        mode='lines',
        opacity=0.7,
        line=dict(dash='dash',
                  width=4,
                  backoff=100),
        hovertemplate="Avg Game Pieces: %{y}" +
        "<extra></extra>",
        legendrank=4
    )

    tele_grid_data = [tele_low_trace, tele_mid_trace,
                      tele_top_trace, tele_mean_trace]

    tele_grid_layout = go.Layout(
        barmode='stack',
        # title={
        # 'text': '<b>Game Pieces Scored - Auto</b>',
        # 'y': 0.95,
        # 'x': 0.5,
        # 'xanchor': 'center',
        # 'yanchor': 'top'}
    )

    tele_grid_fig = go.Figure(
        data=tele_grid_data,
        layout=tele_grid_layout)

    tele_grid_fig.update_yaxes(automargin='top')

    tele_grid_fig.update_yaxes(
        range=[0, 10],
        title_text="<b>Number of Game Pieces</b>")

    tele_grid_fig.update_xaxes(
        type='category',
        title_text="<b>Match Number</b>")

    tele_grid_fig.update_layout(
        margin=dict(
            l=75,
            r=55,
            b=75,
            t=50,
            pad=2),

        legend=dict(
            # entrywidthmode='fraction',
            entrywidth=150,
            orientation='h',
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        ))

    tele_total_scored = tele_top_scored + tele_mid_scored + tele_low_scored
    bold_tele_items = []
    
    for item in tele_total_scored.tolist():
        bold_tele_items.append('<b>' + str(item) + '</b>')
    
    tele_grid_fig.add_trace(go.Scatter(
        x=x,
        y=tele_total_scored,
        text=bold_tele_items,
        mode='text',
        textposition='top center',
        textfont=dict(
            size=15,
        ),
        hovertemplate=None,
        hoverinfo='skip',
        showlegend=False
    ))

     
    return [f'Team {select_team} - {nickname}', f'{city}, {state_prov}', auto_grid_fig, tele_grid_fig]





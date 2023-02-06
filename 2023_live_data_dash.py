# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output  # pip install dash (version 2.0.0 or higher)
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy
from soupsieve import select
import utils.sheets_data_manager as manager
import utils.tba_api_requests as tbapy
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

sheets = manager.sheets_data_manager()
sheets_data = sheets.get_google_sheets_dataframe()
teams_list = sheets.get_team_list()

tba = tbapy.tba_api_requests('tba_api_key.txt')

columns = [{'name': i, 'id': i} for i in sheets_data.columns]
print(columns)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("2023 Scouting Live Data (Test)",
                         className='text-center text-white mb-4'),
                         width=10),
        
        dbc.Col(update_button := dbc.Button(
                "Update Data", class_name="mt-3", color='primary', n_clicks=0))
    ]),
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
            html.H4(id='team_name_string', children=[],
                    className='text-center')
        ], width={'size': 6}),
        dbc.Col([
            html.H4(id='team_location', children=[],
                    className='text-center')
        ], width={'size': 3})
    ]),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='cones_graph', figure={})
        )
    )
])

#     html.Div([
	
#     dcc.Dropdown(id="select_team",
#                  options=teams_list,
#                  value="401",
#                  multi=False,
#                  style={'width': "40%"}
#                  ),
    
#     html.Br(),
#     html.Div(children=[
#         html.Div(id='team_name_string', children=[]),
#         html.Div(id='team_location', children=[])
#         ]
#     )
# ])
# ])

#callbacks
@app.callback(
    [   
        Output(component_id='team_name_string', component_property='children'),
        Output(component_id='team_location', component_property='children'),
        Output('cones_graph', 'figure')
    ],
    [
    	Input(select_team, component_property='value'),
    ]
)

def update_profile(select_team):
    profile_dict = tba.team_profile(select_team)
    nickname = profile_dict.get('nickname')
    # print(profile_dict)
    state_prov = profile_dict.get('state_prov')
    city = profile_dict.get('city')
    team_scouting_results = sheets.get_team_data(select_team)
    
    x = team_scouting_results['Match Number']
    # print(x)
    
    auto_cone_pick_trace = go.Bar(
        x=x,
        y=team_scouting_results['Auto Cones Picked Up'],
        name='Auto Cones Picked Up',
        text=team_scouting_results['Auto Cones Picked Up'],
        textposition='outside',
      		hovertemplate="Low: %{y}" +
      		"<extra></extra>",
      		marker_color='deepskyblue')

    # tele_cone_pick_trace = go.Bar(
        # x=x,
        # y=team_scouting_results['Cones Picked Up'],
        # name='Tele Cones Picked Up',
        # text=team_scouting_results['Cones Picked Up'],
        # textposition='auto',
        # hovertemplate="High: %{y}" +
        #     "<extra></extra>",
        #     marker_color='darkgreen')

    # cones_picked_data = [auto_cone_pick_trace, tele_cone_pick_trace]

    auto_cone_score_trace = go.Bar(
        x=x,
        y=team_scouting_results['Auto Cones Scored'],
        name='Auto Cones Scored',
        text=team_scouting_results['Auto Cones Scored'],
        textposition='outside',
      		hovertemplate="Low: %{y}" +
      		"<extra></extra>",
      		marker_color='crimson')

    # tele_cone_score_trace = go.Bar(
        # x=x,
        # y=team_scouting_results['Cones Scored'],
        # name='Tele Cones Scored',
        # text=team_scouting_results['Cones Scored'],
        # textposition='auto',
        # hovertemplate="High: %{y}" +
        # "<extra></extra>",
        # marker_color='darkgreen')

    cones_auto_data = [auto_cone_pick_trace, auto_cone_score_trace]

    cones_layout = go.Layout(
        barmode='group', 
        title_text='<b>Cones Cycled - Auto</b>')
    # print(auto_balls_data)
    
    cones_fig = go.Figure(
        data=cones_auto_data,
        layout=cones_layout)

    # cones_fig.update_layout(barmode='group')
    
    cones_fig.update_yaxes(
        range=[0, 8],
        title_text="<b>Number of Cones</b>")

    cones_fig.update_xaxes(
        type='category',
        title_text="<b>Match Number</b>")
        # print(df)
        # dict = df.to_dict()
        # print(type(dict))
    
    return [f'Team {select_team} - {nickname}', f'{city}, {state_prov}', cones_fig]


@app.callback(
    Output(update_button, component_property='name'),
    Input(update_button, component_property='n_clicks')
)
 
def update_data(n_clicks):
    # print('yes')
    sheets.refresh_google_sheets_dataframe()
    # update_profile(select_team)
    
    
    # clicked_style = {'color' :'blue'}
    
    return 'Update Data'



if __name__ == '__main__':
    app.run_server(debug=True)

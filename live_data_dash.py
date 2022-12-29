# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from operator import itemgetter
import frc_team_data_lookup as lookup
import logging as log
import numpy

log.basicConfig(level=log.DEBUG)

app = Dash(__name__)
server = app.server

event_key = '2022varr'
# lookup.new_team_season_data_json(event_key)
# print('done')
# lookup.new_event_team_lookup_json(event_key)
# teams = lookup.get_event_teams_list(event_key)
team_lookup_dict = lookup.open_event_team_lookup_json()

# raw_data = pd.read_csv('401 Rumble in the Roads Scouting Data 2023 - csvFormat.csv')
# print(raw_data.head(10))
# raw_data.head(10)
# for index, value in enumerate(raw_data['Climb']):
# 		if value == 'f': raw_data['Climb'].iloc[index] = 'Failed'
# 		if value == 'x': raw_data['Climb'].iloc[index] = 'No Attempt'
# 		if value == '1': raw_data['Climb'].iloc[index] = 'Low'
# 		if value == '2': raw_data['Climb'].iloc[index] = 'Mid'
# 		if value == '3': raw_data['Climb'].iloc[index] = 'High'
# 		if value == '4': raw_data['Climb'].iloc[index] = 'Traversal'

raw_data = pd.read_csv('401 Rumble in the Roads Scouting Data 2023 - csvFormat.csv')
# raw_data.head(10)
# print(raw_data)
# df = raw_data.dropna() 
# newdf = df["Team Number"]
na_formatted = raw_data.fillna('')
raw_data = raw_data.fillna('0')
# print(raw_data)

convert_dict = {
    'Team Number': int,
    'Match Number': int,
    'Auto Upper Hub Scored': int,
    'Auto Upper Hub Missed': int,
    'Auto Lower Hub Scored': int,
    'Upper Hub Scored': int,
    'Lower Hub Scored': int
}

raw_data = raw_data.astype(convert_dict)
# raw_data = raw_data[raw_data['Team Number'] == 401]
# raw_data.head(1000)

unique_team_nums = (raw_data['Team Number'].dropna()).unique()
unique_team_nums = numpy.append(unique_team_nums, 5555)
unique_team_nums.sort()
print(type(raw_data['Auto Lower Hub Scored'][1]))
print(type(raw_data['Lower Hub Scored'][1]))

# print(unique_team_nums)

app.layout = html.Div([

    html.H1("2022 Rumble in the Roads Live Data", style={'text-align': 'center'}),
	
    dcc.Dropdown(id="select_team",
                 options=[{"label": x, "value": x} for x in unique_team_nums],
                 value="401",
                 multi=False,
                 style={'width': "40%"}
                 ),

    html.Br(),
    html.Div(id='team_name', children=[]),
    html.Br(),
    dcc.Graph(id='auto_balls_graph', figure={}),
    html.Br(), 
    dcc.Graph(id='tele_balls_graph', figure={}),
    html.Br(),
    dcc.Graph(id='climbs_table', figure={}),
])

#callbacks
@app.callback(
    [	
        Output(component_id='team_name', component_property='children'),
        Output(component_id='auto_balls_graph', component_property='figure'),
        Output(component_id='tele_balls_graph', component_property='figure'),
        Output(component_id='climbs_table', component_property='figure')
    ],
    	Input(component_id='select_team', component_property='value')
)

# @app.callback(
    # [Output(component_id='team_nickname', component_property='children'),
    #  Output(component_id='state_prov', component_property='children'),
    #  Output(component_id='pie', component_property='figure')],
    #  Output(component_id='robot_image', component_property='src')],
    #  Input(component_id='select_team', component_property='value')
# )

def update_graph(select_team):
    
	try:
		name = [team_lookup_dict[f'frc{select_team}']['profile']['nickname']]
		nickname = f'Team {select_team}: {name[0]}'
  
	except:
		nickname = 'TEAM NOT IN DATABASE'
     
    
	team_raw_data = raw_data[raw_data['Team Number'] == select_team]
	climb_raw_data = na_formatted[raw_data['Team Number'] == select_team]

	x = team_raw_data['Match Number']
 
	# Auto Balls Shot Bar Chart

	auto_low_trace = go.Bar(
		x=x,
		y=team_raw_data['Auto Lower Hub Scored'],
		name='Low Hub Scored',
		text=team_raw_data['Auto Lower Hub Scored'],
		textposition='auto',
		hovertemplate = 
		"Low: %{y}"+
		"<extra></extra>",
		marker_color='deepskyblue') 

	auto_high_trace = go.Bar(
		x=x,
		y=team_raw_data['Auto Upper Hub Scored'],
		name='High Hub Scored',
		text=team_raw_data['Auto Upper Hub Scored'],
		textposition='auto',
		hovertemplate = 
		"High: %{y}"+
		"<extra></extra>",
		marker_color='darkgreen') 

	auto_miss_trace = go.Bar(
		x=x,
		y=team_raw_data['Auto Upper Hub Missed'],
		name='Balls Missed',
		text=team_raw_data['Auto Upper Hub Missed'],
		textposition='auto',
		hovertemplate = 
		"Missed: %{y}"+
		"<extra></extra>",
		marker_color='crimson') 

	auto_balls_data = [auto_low_trace, auto_high_trace, auto_miss_trace]

	auto_balls_layout = go.Layout(barmode='stack', title_text='<b>Autonomous Balls Shot</b>')
	# print(auto_balls_data)
	auto_balls_fig = go.Figure(
		data=auto_balls_data, 
		layout=auto_balls_layout)

	auto_balls_fig.update_yaxes(
		range=[0,7],
		title_text="<b>Number of Balls</b>")

	auto_balls_fig.update_xaxes(
		type='category',
		title_text="<b>Match Number</b>")
 
	# Teleop Balls Shot Bar Chart
	# log.debug(team_raw_data['Lower Hub Scored'][0])
	# log.debug(type(team_raw_data['Auto Lower Hub Scored'][0]))
	tele_low_trace = go.Bar(
		x=x,
		y=team_raw_data['Lower Hub Scored'],
		name='Low Hub Scored',
		text=team_raw_data['Lower Hub Scored'],
		textposition='auto',
		hovertemplate = 
		"Low: %{y}"+
		"<extra></extra>",
		marker_color='deepskyblue') 

	tele_high_trace = go.Bar(
		x=x,
		y=team_raw_data['Upper Hub Scored'],
		name='High Hub Scored',
		text=team_raw_data['Upper Hub Scored'],
		textposition='auto',
		hovertemplate = 
		"High: %{y}"+
		"<extra></extra>",
		marker_color='darkgreen') 

	tele_balls_data = [tele_low_trace, tele_high_trace]

	tele_balls_layout = go.Layout(barmode='stack', title_text='<b>Teleop Balls Scored</b>')

	tele_balls_fig = go.Figure(
		data=tele_balls_data, 
		layout=tele_balls_layout)

	tele_balls_fig.update_yaxes(
		range=[0,25],
		title_text="<b>Number of Balls</b>")

	tele_balls_fig.update_xaxes(
		type='category',
		title_text="<b>Match Number</b>")
 
	# Climbs Table
	
	climb_table_col1 = climb_raw_data['Match Number']
	climb_table_col2 = climb_raw_data['Climb']

	climb_table_trace = go.Table(
		header=dict(
		values=['<b>Match</b>', '<b>Climb</b>'],
		line_color='black', fill_color='white',
		align='center',font=dict(color='black', size=20)),
		
	cells=dict(
		values=[climb_table_col1, climb_table_col2],
		line_color='darkslategray',
	#     fill_color=[np.array(colors)[a],np.array(colors)[b]],
		align='center', font=dict(color='black', size=15)
		)) 

	climb_table_data = [climb_table_trace]

	climb_table_fig = go.Figure(
		data=climb_table_data)
 
	return [nickname, auto_balls_fig, tele_balls_fig, climb_table_fig]



if __name__ == '__main__':
    app.run_server(debug=True)

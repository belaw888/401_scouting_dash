# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import pygsheets

#authorization
gc = pygsheets.authorize(service_file=
    '/home/belawilliams/Documents/team-401-scouting-credentials-2023.json')

sh = gc.open('401_scouting_test_database')

#select the first sheet 
#could cause bugs if first sheet is not correct one
wks = sh[0]

app = Dash(__name__)
server = app.server

app.layout = html.Div([

    title := html.H1("2023 401 Scouting Dashboard", style={'text-align': 'center'}),
	button := html.Button('Update Data', id='update-data-button', n_clicks=0),
	button_output := html.Div(id='button-click-status',
          children='Button clicked 0 times')

])

#callbacks
@app.callback(
    [	
        Output(button_output, component_property='children')
    ],
    [   	
     	Input(button, component_property='n_clicks')
    ]
)

def update_button_output(nclicks):

	df = wks.get_as_df(
		has_header=True, 
		include_tailing_empty=False,
		include_tailing_empty_rows=False,
		value_render='FORMATTED_VALUE')
 
	print(df.shape)
    
	return [f'Button clicked {nclicks} times']



if __name__ == '__main__':
    app.run_server(debug=True)

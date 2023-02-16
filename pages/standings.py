import dash
from dash import Dash, dcc, html, callback, dash_table, Input, Output
import json
import pandas as pd
# from dash._get_app import test



dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='This is our Standings page'),

    html.Div(children='''
        This is our Home page content.
    '''),
    html.Div(id='div')

])

@callback(
    Output('div', 'children'),
    Input('session_database', 'data')
)

def show_div(data):
    dict = json.loads(data)
    df = pd.DataFrame(dict['data'], columns=dict['columns'], index=dict['index'])
    # print('ok')
    return df.at[1, 'Match Type']
    # return df
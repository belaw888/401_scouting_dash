import dash
from dash import Dash, dcc, html, callback, dash_table, Input, Output
import json
import pandas as pd
import dash_bootstrap_components as dbc
import utils.sheets_data_manager as manager
# from dash._get_app import test
# df = pd.read_csv('https://git.io/Juf1t')

sheets = manager.sheets_data_manager()

# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__, path='/')

layout = dbc.Container([
    dbc.Row([
        dash_table.DataTable(id='tbl',
                             style_data={
                                 'color': 'black',
                                 'backgroundColor': 'white'
                             },
                            style_header={
                                 'backgroundColor': 'rgb(30, 30, 30)',
                                 'color': 'white'
                             })
    ]),
    
    # df.to_dict('records'), [
    #     {"name": i, "id": i} for i in df.columns], id='tbl',
    

])

@callback(
    [Output('tbl', 'data'), Output('tbl', 'columns')],
    Input('session_database', 'data')
)

def show_data_table(session_database):
    
    scouting_results = sheets.parse_json(session_database)
    
    data = scouting_results.to_dict('records')#[{"name":i, "id": i} for i in scouting_results.columns]
    columns = [{"name": i, "id": i} for i in scouting_results.columns]
    # table = dash_table.DataTable(
    #     data=dict, columns=[{"name": i, "id": i} for i in scouting_results.columns])
    print(type(data))
    
    return data, columns

# def show_div(data):
#     dict = json.loads(data)
#     df = pd.DataFrame(dict['data'], columns=dict['columns'], index=dict['index'])
#     # print('ok')
#     return df.at[1, 'Match Type']
#     # return df
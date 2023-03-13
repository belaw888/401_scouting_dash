from gc import callbacks
import dash
from dash import html, dcc, dash_table, callback, Input, Output
import utils.sheets_data_manager as manager
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Group



sheets = manager.sheets_data_manager()
# duplicates = sheets.get_duplicates_series()
# print(duplicates.index)

dash.register_page(__name__)

layout = dbc.Container([
    html.H1(html.H1("Duplicate Data Points:", className='mt-1',
                    style={'display': 'table-cell', 'text-align': 'center', 'font-family': 'DejaVu Sans', 'font-weight': 'bold', 'font-size': 25})),

    dbc.Row([
        table := dash_table.DataTable(
                                #   data=.to_dict('records'),
                                  sort_action='native',
                                  style_data={
                                      'color': 'black',
                                      'backgroundColor': 'white'
                                  },
                                  style_header={
                                      'backgroundColor': 'rgb(30, 30, 30)',
                                      'color': 'white'
                                  },
                                  style_table={
                                      'overflowX': 'auto',
                                      'minWidth': '100%'
                                  },
                                  style_cell={'fontSize': 18,
                                              'font-family': 'DejaVu Sans',
                                              'font-weight': 700})
            ])
    ])

@callback(
    [Output(table, 'data'),  Output(table, 'columns'),],
    [Input('session_database', 'data')]
)

def show_data_table(session_database):
    scouting_results = sheets.parse_json(session_database)
    df = sheets.get_duplicates_series(scouting_results)
    columns = [{"name": i, "id": i} for i in df.columns]
    df = df.to_dict('records')

    return df, columns

    

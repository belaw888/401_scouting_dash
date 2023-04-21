# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from unittest import result
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash
# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, dash_table, Input, Output
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy
from soupsieve import select
import utils.sheets_data_manager as manager
import utils.tba_api_requests as tbapy
import dash_bootstrap_components as dbc
import utils.tba_data_validation

sheets = manager.sheets_data_manager()
sheets_data = sheets.get_google_sheets_dataframe()
validate = utils.tba_data_validation.tba_data_validation()



app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=2.0, minimum-scale=0.8'}])
        #    suppress_callback_exceptions=True)
server = app.server

topbar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className=""),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=False,
    pills=True,
    className="bg-dark mb-5",
    justified=True
)

app.layout = dbc.Container([
    
    dcc.Store(id='session_database', storage_type='session'),
    dcc.Store(id='session_analysis_database', storage_type='session'),
    # dcc.Store(id='session_database_422', storage_type='session'),
    
    
    dbc.Row([
        # dbc.Col(html.Div(html.Img(src=dash.get_asset_url('assets/index.jpeg'))),
                # xs=12, sm=12, md=3, lg=3, xl=3),
        dbc.Col(html.Img(src='assets/401_logo.png', style={'max-width': '100%', 'max-height': '100%', 'object-fit': 'contain'}, className='d-flex justify-content-left px-0'), 
                xs=2, sm=3, md=2, lg=3, xl=3, className='d-flex justify-content-left px-0'),
        
        dbc.Col(html.H1("Scouting Data: CHS District Championship", className='mt-1',
                        style={'display': 'table-cell', 'text-align': 'center','align-items': 'center', 'font-family': 'DejaVu Sans', 'font-weight': 'bold', 'font-size': '4.3vw'}),
                xs=8, sm=6, md=8, lg=6, xl=6, className='d-flex justify-content-center align-item-center'),
        
        dbc.Col(update_button := dbc.Button(
            html.I(className="fa-solid fa-rotate", style={'max-width': '100%', 'max-height': '100%', 'min-width': '100%', 'object-fit': 'contain', 'font-size': '2em'}), style={'max-width': '100%', 'max-height': '100%', 'object-fit': 'contain', 'min-width': '100%'}, color='success', n_clicks=0),
                xs=2, sm=3, md=2, lg=3, xl=3, className='d-flex justify-content-right px-0'),
    ], className='pb-1 pt-4 px-4'),
    
    # html.Div(id='test', children=[]),
    
    html.Hr(),

    dbc.Row(
        [
        dbc.Col([
        	topbar
        ], xs=12, sm=12, md=12, lg=12, xl=12, xxl=12)
        ]
    ),
    dbc.Row([
        dbc.Col([
		    dash.page_container
        ])
		]
    )
	], fluid=True, className='mx-0')


@app.callback(
   [Output('session_database', 'data'),
    Output('session_analysis_database', 'data')],
    # Output('session_database_422', 'data')],
    Input(update_button, 'n_clicks')
)

def update_session_data(n_clicks):
    sheets.refresh_google_sheets_dataframe()
    
    # results_422 = sheets.get_422_dataframe()
    scouting_results = sheets.get_google_sheets_dataframe()
    analysis = sheets.get_analysis_dataframe()
    
    df = sheets.get_duplicates_series(scouting_results)
    # columns = [{"name": i, "id": i} for i in df.columns]
    # print(df)
    df = df.to_dict('records')

    # analysis_results = sheets.parse_json(analysis)

    missing_data = validate.missing_data(analysis)
    # other_columns = [{"name": i, "id": i} for i in missing_data]
    # print(missing_data.shape)

    missing = missing_data.apply(lambda x: x.values.flatten().tolist(), axis=1)
    # print(missing)
    # row_list = missing_data.loc[2, :].values.flatten().tolist()
    # print(missing.tolist())
    # print(len(missing.tolist()))

    # results_422 = sheets.parse_json(database_422)
    # combined = results_422['Match Type'].combine(
    #     results_422['Match Number'], (lambda x1, x2: x1 + str(x2)))

    # results_422['match_key'] = combined

    # results_422.set_index('match_key', inplace=True)
    # print(results_422)
    # print(missing.tolist())

    for row in missing.tolist():
        # print('yes')
        match = row[0]
        # print(match)
        team_list = [i for i in row if isinstance(i, int)]
        # print(team_list)
        # filt = results_422['match_key'] == match

        # # print(filt)
        # match_filtered = results_422.loc[filt]
        # print(match_filtered)

        # for team in team_list:
        #     data_point = match_filtered[match_filtered['Team Number'] == team]
        #     data_point.drop(['match_key'], inplace=True, axis=1)

        #     if not data_point.empty:
        #         # print(data_point.values.tolist()[0])
        #         sheets.add_to_401_dataframe(data_point.values.tolist()[0])

    scouting_results = sheets.get_google_sheets_dataframe()
    analysis = sheets.update_analysis_dataframe(scouting_results)
    
    # raw_json_string_422 = sheets.get_as_json(results_422)
    raw_json_string = sheets.get_as_json(scouting_results)
    analysis_json_string = sheets.get_as_json(analysis)
    
    return [raw_json_string, analysis_json_string]

# @app.callback(
#     Output('test', 'children'),
#     Input('session_database', 'data')
# )

# def update(data):
#     dataframe = sheets.parse_json(data)
#     return dataframe.at[1,'Match Type']


if __name__ == '__main__':
	app.run_server(debug=True)

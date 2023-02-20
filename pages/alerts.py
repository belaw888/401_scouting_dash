import dash
from dash import html, dcc
import utils.sheets_data_manager as manager

sheets = manager.sheets_data_manager()
duplicates = sheets.get_duplicates_dict()

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Alerts page'),

    html.Div(children=str(duplicates)),

])

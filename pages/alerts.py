import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Alerts page'),

    html.Div(children='''
        This is our Home page content.
    '''),

])

def test():
    return 'bruh'

import dash
from dash import Dash, dcc, html, callback, dash_table, Input, Output
from dash.dash_table.Format import Format, Group
from numpy import true_divide
import pandas as pd
import dash_bootstrap_components as dbc
import utils.sheets_data_manager as manager
import numpy
# from dash._get_app import test
# df = pd.read_csv('https://git.io/Juf1t') Format, Group
import colorlover
from enum import IntEnum

class Points(IntEnum):
    AUTO_TOP = 6
    AUTO_MID = 4
    AUTO_LOW = 3
    TELE_TOP = 5
    TELE_MID = 3
    TELE_LOW = 2
    LINK = 5
    AUTO_DOCKED = 8
    AUTO_ENGAGED = 12
    TELE_DOCKED = 6
    TELE_ENGAGED = 10
    MOBILITY = 3
    PARK = 2
    


columns_list = ['Total Points',
                'Auto Grid Points',
                'Auto Charge Points',
                'Tele Grid Points',
                'Endgame Charge Points']
                # 'Auto Cones Mid',
                # 'Auto Cones Low',
                # 'Auto Cubes Top',
                # 'Auto Cubes Mid',
                # 'Auto Cubes Low',
                # 'Tele Cones Top',
                # 'Tele Cones Mid',
                # 'Tele Cones Low',
                # 'Tele Cubes Top',
                # 'Tele Cubes Mid',
                # 'Tele Cubes Low'
                # ]

sheets = manager.sheets_data_manager()

# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__, path='/')


def discrete_background_color_bins(df, n_bins=5, columns_array=[[]], colorscale_names=['Oranges', 'Blues']):
    
    # print(columns_array)
    styles = []
    legend = []
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    
    
    backgroundColor = colorlover.scales[str(n_bins)]['seq'][colorscale_names[0]]

    legend = [
        html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
            html.Div(
                style={
                    'backgroundColor': backgroundColor[index],
                    'borderLeft': '1px rgb(50, 50, 50) solid',
                    'height': '10px'
                }
            ),
            html.Small('q' + str(int(int(val*100)/20)), style={
                'paddingLeft': '2px'})])
        
        for index, val in enumerate(bounds[1:])]
     
    
    # multiple_legends = []    
    for count, column_sets in enumerate(columns_array, start=0):
        # print(column_sets)
        # print('done')
        
        #bounds between zero and one
        
        df_numeric_columns = df[column_sets]
        
        # print(df_numeric_columns)
        df_max = df_numeric_columns.max().max()
        df_min = df_numeric_columns.min().min()
        # print(df_max)
        # print(df_min)
        # ranges = [
        #     ((df_max - df_min) * i) + df_min
        #     for i in bounds
        # ]
        quartiles = [
            round(df_numeric_columns.quantile(i)[0], 2) for i in bounds[1:]
        ]
        
        print(quartiles)
        
        # print(ranges)
        # styles = []
        
        # print(type(count))
        
        for i in range(1, len(bounds)):
            min_bound = quartiles[i - 2]
            max_bound = quartiles[i - 1]
            backgroundColor = colorlover.scales[str(n_bins)]['seq'][colorscale_names[count]][i - 1]
            color = 'black' #if i > len(bounds) / 2. else 'inherit'

            for column in df_numeric_columns:
                styles.append({
                    'if': {
                        'filter_query': (
                            '{{{column}}} >= {min_bound}' +
                            (' && {{{column}}} < {max_bound}' if (
                                i < len(bounds) - 1) else '')
                        ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                        'column_id': column
                    },
                    'backgroundColor': backgroundColor,
                    'color': color
                })
        
    
        # print(count)
        
        
                   
               
        # print(legend)
        # styles.append(styles)
       
# html.Div(legends, style={'padding': '5px 0 5px 0'})
    # print (styles)

    return (styles, legend)


# def highlight_sorted_by_column(column_list):
#     styles = []
#     for i in column_list:
#             styles.append({
#                 'if': {
#                     'filter_query': '{{Auto Charge Points}} = {}'.format(i),
#                     'column_id': 'Auto Charge Points'
#                 },
#                 'backgroundColor': '#39CCCC',
#                 'color': 'blue'
#             })
#     print(styles)
#     # print(id='current_sort_by')
#     return styles

layout = dbc.Container([
    dbc.Row([
            html.H4(html.B('Point Averages (Sort By):'),
                    className='d-flex justify-content-md-center justify-content-sm-start'
                                        )
            ]),
    
    dbc.Row(
        sort_by := dcc.Dropdown(options=columns_list,
                         value=columns_list[0],
                         persistence=True,
                         id='sort_by',
                         multi=False,
                         searchable=False,
                         className='mb-4 text-primary d-flex justify-content-around"')),
    
    dbc.Row(legend := html.Div(style={'float': 'right'})),
    
    dbc.Row([
        table := dash_table.DataTable(
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
                                        'font-weight': 700},
                            
                            fixed_columns={'headers': True, 'data': 1},
                            
                            
                                # highlight_sorted_by_column(columns_list),

        )
    ]),
    
    html.Br()
    
    # df.to_dict('records'), [
    #     {"name": i, "id": i} for i in df.columns], id='tbl',
    

])

@callback(
    [Output(table, 'data'), 
     Output(table, 'columns'),
     Output(table, 'style_data_conditional'),
     Output(legend, 'children')],
    
    [Input('session_database', 'data'),
     Input('session_analysis_database', 'data'),
     Input(sort_by, 'value')]
)

def show_data_table(session_database, session_analysis_database, sort_by):
    
    # scouting_results = sheets.parse_json(session_database)
    scouting_analysis_results = sheets.parse_json(session_analysis_database)
    
    analysis = scouting_analysis_results.copy()
    new_df = pd.DataFrame(columns=columns_list)
    
    for team in scouting_analysis_results['Team Number'].unique():
        team_filter = scouting_analysis_results['Team Number'] == team
        analysis = scouting_analysis_results.loc[team_filter]

        aggregate_list = []
        
        # print(analysis)
        
        for cols in columns_list:
        
        #    print(total_grid_points_series)
                    
           if cols == 'Auto Charge Points':
                mean = analysis[cols].mean()
                if mean is numpy.nan:
                    aggregate_list.append(numpy.nan)
                else:
                    aggregate_list.append(mean)
                #should only count attempted ones for avg
                    
           elif cols == 'Endgame Charge Points':
                mean = analysis[cols].mean()
                if mean is numpy.nan:
                    aggregate_list.append(numpy.nan)
                else:
                    aggregate_list.append(mean)
                    
           else:
                aggregate_list.append(analysis[cols].mean())

        
        team_avgs = pd.DataFrame([aggregate_list],
                        columns=columns_list, 
                        index=[team])
        
        # print(team_avgs)
        
        
        new_df = pd.concat([new_df, team_avgs])
    
    new_df.reset_index(inplace=True, names='Team #')
    new_df = new_df.round(decimals=2)
    new_df.sort_values(by=sort_by, inplace=True, ascending=False)
    # print(session_sort_by)

    # print(new_df)
    
    # data = scouting_results.to_dict('records')
    # columns = [{"name": i, "id": i} for i in scouting_results.columns]
   
    (styles, legend) = discrete_background_color_bins(new_df, 
                                                      columns_array=[[columns_list[0]], [columns_list[1]], [columns_list[2]], [columns_list[3]], [columns_list[4]]],
                                                      colorscale_names=['Oranges', 'Oranges', 'Oranges', 'Oranges', 'Oranges'])
    
    new_df.fillna("N/A", inplace=True)
    data = new_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in new_df.columns]
    
    team_num_width = {
            'if': {'column_id': 'Team #'},
            'width': '85px',
        }
    sorted_cell_border = {
            'if': {'column_id': sort_by},
            'border': '3px solid #FFDC00',
            #  'borderRight': '4px solid #FFDC00',
            #  'borderTop': '4px solid #FFDC00',
            #  'borderBottom': '4px solid #FFDC00',
        }
    styles.append(sorted_cell_border)
    styles.append(team_num_width)

    # print(styles[0])
    
    # print(legend)
    return [data, columns, styles, legend]

# def show_div(data):
#     dict = json.loads(data)
#     df = pd.DataFrame(dict['data'], columns=dict['columns'], index=dict['index'])
#     # print('ok')
#     return df.at[1, 'Match Type']
#     # return df
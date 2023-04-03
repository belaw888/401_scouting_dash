# from audioop import avg
# import pandas as pd
# import plotly.express as px  # (version 4.7.0 or higher)
# import plotly.graph_objects as go
# import dash
# from dash import Dash, dcc, html, callback, dash_table, Input, Output
# from dash.dash_table.Format import Format, Group
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# import numpy
# from soupsieve import select
# import utils.sheets_data_manager as manager
# import utils.tba_api_requests as tbapy
# import dash_bootstrap_components as dbc

# dict = {'name' : 'test',
#         'y_series' : [1,2,3,4,5],
#         'text': 'text',
#         'color': 'blue',
#         'hover_name': 'hover'}

# dict1 = {'name': 'test',
#         'y_series': [1, 2, 3, 4, 5],
#         'text': 'text1',
#         'color': 'blue',
#         'hover_name': 'hover'}

# dict_list = [dict, dict1]



# def points_stacked_bar(x_series, title, x_axis_name, y_axis_name, dict_list):
	
# 	trace_list = []
# 	x = x_series
 
# 	for item in dict_list:
# 		bar = go.Bar(
#                     x=x,
#                     y=item['y_series'],
#                     name=item['name'],
#                     text=item['text'],
#                     textposition='inside',
#                     hovertemplate=item['hover_name'] + ": %{y}" + "<extra></extra>",
#                     marker_color=item['color'])
  
# 		trace_list.append(bar)
















# auto_top_scored = team_scouting_results['Auto Cones Top'] + \
#     team_scouting_results['Auto Cubes Top']

# auto_top_trace = go.Bar(
#     x=x,
#     y=auto_top_scored,
#     name='Auto Grid (Top)',
#     text=auto_top_scored,
#     textposition='inside',
#     hovertemplate="Top: %{y}" +
#     "<extra></extra>",
#     marker_color='lightseagreen')

# auto_mid_scored = team_scouting_results['Auto Cones Mid'] + \
#     team_scouting_results['Auto Cubes Mid']

# auto_mid_trace = go.Bar(
#     x=x,
#     y=auto_mid_scored,
#     name='Auto Grid (Mid)',
#     text=auto_mid_scored,
#     textfont=dict(color='black'),
#     textposition='inside',
#     hovertemplate="Mid: %{y}" +
#     "<extra></extra>",
#     marker_color='deepskyblue')

# auto_low_scored = team_scouting_results['Auto Cones Low'] + \
#     team_scouting_results['Auto Cubes Low']

# auto_low_trace = go.Bar(
#     x=x,
#     y=auto_low_scored,
#     name='Auto Grid (Low)',
#     text=auto_low_scored,
#     textposition='inside',
#     hovertemplate="Low: %{y}" +
#     "<extra></extra>",
#     marker_color='crimson')

# auto_mean_trace = go.Scatter(
#     x=x,
#     y=[auto_low_scored.mean() + auto_mid_scored.mean() +
#        auto_top_scored.mean() for val in x],
#     name='Avg Game Pieces/Match',
#     mode='lines',
#     opacity=0.7,
#     line=dict(dash='dash',
#               width=4,
#               backoff=100),
#     hovertemplate="Avg Game Pieces: %{y}" +
#     "<extra></extra>",
#     legendrank=4
# )

# auto_grid_data = [auto_low_trace,
#                   auto_mid_trace, auto_top_trace, auto_mean_trace]

# auto_grid_layout = go.Layout(
#     barmode='stack',
#     # title={
#     # 'text': '<b>Game Pieces Scored - Auto</b>',
#     # 'y': 0.95,
#     # 'x': 0.5,
#     # 'xanchor': 'center',
#     # 'yanchor': 'top'}
# )

# auto_grid_fig = go.Figure(
#     data=auto_grid_data,
#     layout=auto_grid_layout)

# auto_grid_fig.update_yaxes(automargin='top')

# auto_grid_fig.update_yaxes(
#     range=[0, 10],
#     title_text="<b>Number of Game Pieces</b>")

# auto_grid_fig.update_xaxes(
#     type='category',
#     title_text="<b>Match Number</b>")

# auto_grid_fig.update_layout(
#      margin=dict(
#           l=75,
#           r=55,
#           b=75,
#           t=50,
#           pad=2),

#      legend=dict(
#            # entrywidthmode='fraction',
#           entrywidth=150,
#           orientation='h',
#           yanchor="bottom",
#           y=1.05,
#           xanchor="right",
#           x=1
#           ))

#  bold_auto_items = []
#   auto_total_scored = auto_top_scored + auto_mid_scored + auto_low_scored

#    for item in auto_total_scored.tolist():
#         bold_auto_items.append('<b>' + str(item) + '</b>')

#     auto_grid_fig.add_trace(go.Scatter(
#         x=x,
#         y=auto_total_scored,
#         text=bold_auto_items,
#         mode='text',
#         textposition='top center',
#         textfont=dict(
#             size=15,
#         ),
#         hovertemplate=None,
#         hoverinfo='skip',
#         showlegend=False
#     ))

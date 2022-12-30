import pygsheets
import pandas as pd

gc = pygsheets.authorize(service_file=
    '/home/belawilliams/Documents/team-401-scouting-credentials-2023.json')

sh = gc.open('401_scouting_test_database')

#select the first sheet 
wks = sh[0]

df = wks.get_as_df(
    has_header=True, 
    # index_column=5,
    include_tailing_empty=False,
    include_tailing_empty_rows=False,
    value_render='FORMATTED_VALUE')

# print(df)
print(df.shape)


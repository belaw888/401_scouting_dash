import pandas as pd
import pygsheets
import json

class sheets_data_manager:
    dataframe = pd.DataFrame()
    
    def __init__(self) -> None:
        self.credentials = pygsheets.authorize(
            service_file=#'/etc/secrets/team-401-scouting-credentials-2023.json')
       '/home/belawilliams/Documents/team-401-scouting-credentials-2023.json')
        self.google_sheet = self.credentials.open(
            '[401 & 422 Scouting] - VABLA - 2023 Charged Up Database')
        self.worksheet = self.google_sheet.worksheet('title', '2023_demo_data')
        self.dataframe = self.worksheet.get_as_df(
            has_header=True,
            index_column=1,
           	include_tailing_empty=False,
           	include_tailing_empty_rows=False,
           	value_render='FORMATTED_VALUE')
        
    def refresh_google_sheets_dataframe(self):
        # print('flag')
        self.dataframe = self.worksheet.get_as_df(
            has_header=True,
            # index_column=5,
         	include_tailing_empty=False,
         	include_tailing_empty_rows=False,
         	value_render='FORMATTED_VALUE')
        # return self.dataframe
    
    def get_google_sheets_dataframe(self):
        return self.dataframe
    
    def get_duplicates_dict(self):
        data_id_value_counts = self.dataframe.index.value_counts()
        duplicates_series = data_id_value_counts[data_id_value_counts > 1]
        # duplicates_list = duplicates_series.index.tolist()
        # print(duplicates_list)
        duplicates_dict = duplicates_series.to_dict()
        # print(duplicates_dict)
        return duplicates_dict
        # for key in duplicates_dict:
        #     print(f'Warning! there are duplicate data points for {key}')
        
    def get_team_data(self, team):
        filter = self.dataframe['Team Number'] == team
        return self.dataframe.loc[filter]
        
    def get_team_list(self):
      list = self.dataframe['Team Number'].unique().tolist()
      list.sort()
      return list        
  
    def get_as_json(self):
        return json.dumps(self.dataframe, default=lambda df: json.loads(df.to_json(orient='split')))
  
    def parse_json(self, json_string):
        dict = json.loads(json_string)
        df = pd.DataFrame(dict['data'], columns=dict['columns'], index=dict['index'])
        return df
    
    #static isn't really the right term here
    def get_team_data_static(self, dataframe, team):
        filter = dataframe['Team Number'] == team
        return dataframe.loc[filter]
  
# f = sheets_data_manager()
# # print(f.get_google_sheets_dataframe())
# # print(f.get_duplicates_dict())
# # print(f.get_team_data(401))
# # print(f.get_team_data(881))
# # print(type(f.get_team_list()))
# # print(f.get_team_list())
# json_data = f.get_as_json()
# dict = json.loads(json_data)
# df = pd.DataFrame(dict['data'], columns=dict['columns'], index=dict['index'])
# print(df)
# print(f.get_google_sheets_dataframe() == df)

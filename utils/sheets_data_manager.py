import pandas as pd
import pygsheets

class sheets_data_manager:
    dataframe = pd.DataFrame()
    
    def __init__(self) -> None:
        self.credentials = pygsheets.authorize(
            service_file='/home/belawilliams/Documents/team-401-scouting-credentials-2023.json')
        
        self.google_sheet = self.credentials.open('401_scouting_test_database')
        self.worksheet = self.google_sheet[1]
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
  
    
  
  
f = sheets_data_manager()
# print(f.get_google_sheets_dataframe())
print(f.get_duplicates_dict())
# print(f.get_team_data(881))
# print(type(f.get_team_list()))
# print(f.get_team_list())


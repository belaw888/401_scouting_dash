import pandas as pd
from tenacity import TryAgain
import tba_api_requests 
from pandas.errors import MergeError

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
# print(df.shape)

class tba_data_validation:
    
    local_scouting_data = pd.DataFrame()
    local_tba_data = pd.DataFrame()
    match_key_queue = []
    
    def __init__(self) -> None:
        self.tbareq = tba_api_requests.tba_api_requests('tba_api_key.txt')
        
    def set_local_scouting_data(self, data) -> None:
        self.local_scouting_data = data
    
    def get_DataFrame_differences(self, df1, df2):
        try:
            data_combined = df1.merge(df2, indicator = True, how = 'outer')
            data_combined_diff = data_combined.loc[lambda x : x['_merge'] != 'both']
            return data_combined_diff

        except MergeError:
            return 'error' #will slow things down bc returns whole df if there are no updates on refresh
                
    def validate_new_data(self, updated_scouting_data):
        
        # print(self.local_scouting_data)
        
        new_scouting_data = self.get_DataFrame_differences(
            self.local_scouting_data,
            updated_scouting_data)
        
        self.local_scouting_data = new_scouting_data
        
        local = self.local_scouting_data
        print(local)
        validation_list = []
        
        keys_set = set(local['tba_api_id'].to_list())
        unique_keys = list(keys_set)
        
        for key in unique_keys:
            validation_list.append(self.validate_one_match(key))
    
        # for row in new_scouting_data:
        #     try:
        #     	self.tbareq.match_aggregate_data(row['tba_api_id'])
                         
        
        return validation_list
        
        
    # def team_score_contribution()
    
    def validate_one_match(self, match_key):
        
        local = self.local_scouting_data
        # print(local['tba_api_id'])
        # print(local)
        
        try:
            tba_match_data = self.tbareq.match_aggregate_data(match_key)
            
            match_filter = (local['tba_api_id'] == match_key)
            
            # print(local.loc[match_filter, 'tba_api_id'])
            # print(local['Robot Position'][0])
            # print('Blue' in local['Robot Position'][0])
            # print(local.loc[local['Robot Position'].str.contains('Blue', na=False), 'Robot Position'])
            
            red_filter = (
                match_filter & (local['Robot Position'].str.contains('Red', na=False)))
            
            blue_filter = (
                match_filter & (local['Robot Position'].str.contains('Blue', na=False)))
            
            # print(local.loc[red_filter, 'Upper Hub Scored'].sum())
            
            scouting_tele_balls = (
                local.loc[red_filter, 'Upper Hub Scored'].sum() + 
                local.loc[red_filter, 'Lower Hub Scored'].sum() +
                local.loc[blue_filter, 'Upper Hub Scored'].sum() +
                local.loc[blue_filter, 'Lower Hub Scored'].sum())
            
            tba_tele_balls = tba_match_data['teleopCargoTotal'].sum()
            
            if abs(scouting_tele_balls - tba_tele_balls) > 1:
                return match_key
            else:
                return "Within Tolerance" #change to null
            
        
        except: #find out what error this will be
            self.match_key_queue.append(match_key)
            return 'TBA not updated, added to queue'
        
        
val = tba_data_validation()
val.set_local_scouting_data(df.loc[0:180])
# print(df.loc[7:5])
print(val.validate_new_data(df))
# val.get_DataFrame_differences(df, df.loc[20:])


# print(val.validate_one_match('2022varr_qm2'))


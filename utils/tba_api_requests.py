
import tbapy
import json
import pandas as pd

class tba_api_requests:
    
    def __init__(self, api_key_file_name) -> None:
        self.tba_api_key = open(api_key_file_name, 'r').read()
        self.tba = tbapy.TBA(self.tba_api_key)
        
    def tbapy_to_dict(self, json_data):
        s1 = json.dumps(json_data)
        data = json.loads(s1)
        
        return data
    
    def tbapy_to_dataframe(self, json_data):
        dict = self.tbapy_to_dict(json_data)
        df = pd.DataFrame(dict)
        
        return df
    
    def event_match_keys(self, event_key):
        return self.tba.event_matches(event_key, keys = True)
        
    def match_aggregate_data(self, match_key):
        
        json_data = self.tba.match(match_key)
        data = self.tbapy_to_dict(json_data)
        # print(data)
        match_code = data['comp_level'] + str(data['match_number'])
        
        df = pd.DataFrame.from_dict(data['score_breakdown'])
        
        df = df.fillna('NO_DATA')
        df = df.transpose()
        
        column_list = ['totalPoints', 'matchCargoTotal',
                       'autoPoints', 'autoCargoPoints', 'autoCargoTotal', 'autoTaxiPoints',
                       'teleopPoints', 'teleopCargoPoints', 'teleopCargoTotal',
                       'endgamePoints', 'endgameRobot1', 'endgameRobot2', 'endgameRobot3']
        
        df = df[column_list]
        
        df['Robot1'] = [int(data['alliances'][x]['team_keys'][0][3:]) for x in df.index]
        df['Robot2'] = [int(data['alliances'][x]['team_keys'][1][3:]) for x in df.index]
        df['Robot3'] = [int(data['alliances'][x]['team_keys'][2][3:]) for x in df.index]
        
        df['match_number'] = data['match_number']
        df['comp_level'] = data['comp_level']
        df['alliance_color'] = df.index
                
        df = df.rename(index={
            'blue' : f'{match_code}_blue',
            'red': f'{match_code}_red'})

        return df
    
    def event_aggregate_data(self, event_key):
    
        match_keys = self.event_match_keys(event_key)
        filtered_match_keys = filter(lambda key: 'qm' in key, match_keys)
        filtered_match_keys = list(filtered_match_keys)
    
        df = self.match_aggregate_data(filtered_match_keys[0])

        for match in filtered_match_keys[1:]:
            df = pd.concat([df, self.match_aggregate_data(match)])

        return df
    
    def team_profile(self, number):
        profile = self.tba.team(f"frc{str(number)}", simple=True)
        profile = self.tbapy_to_dict(profile)
        return profile
        
# api = tba_api_requests('tba_api_key.txt')
# profile = api.team_profile(346)
# print(profile['city'])

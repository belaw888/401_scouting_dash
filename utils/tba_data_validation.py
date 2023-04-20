import pandas as pd
import utils.tba_api_requests
from pandas.errors import MergeError
import utils.sheets_data_manager as manager

tba = utils.tba_api_requests.tba_api_requests('tba_api_key.txt')


class tba_data_validation:

    local_scouting_data = pd.DataFrame()
    local_tba_data = pd.DataFrame()
    match_key_queue = []

    def __init__(self) -> None:
        # self.tbareq = tba_api_requests.tba_api_requests(
        #     'tba_api_key.txt')
        pass
        
        
    def missing_data(self, sheets_data):
        
        combined = sheets_data['Match Type'].combine(
        sheets_data['Match Number'], (lambda x1, x2: x1 + str(x2)))
        
        combined = combined.apply(lambda x: '2023chcmp_' + x)
        
        sheets_data['tba_key'] = combined
        # print(sheets_data)
        
        
        # # print(sheets_data['tba_key'])
        
        event_data = tba.event_data('2023chcmp')
        # match_keys = event_data['key'].to_dict()
        # alliances = event_data['alliances'].to_dict()
        
        # print(alliances)
        
        # print(event_data['key'])
        out_df = pd.DataFrame()


        for key in sheets_data['tba_key'].unique().tolist():
            try:
                match_tba_filter = event_data['key'] == key
                tba_match = event_data.loc[match_tba_filter]
                tba_match.set_index('key', inplace=True)
                dict = tba_match.to_dict()
                # print(dict['alliances'][key]['blue']['team_keys'])
                match_robots = dict['alliances'][key]['blue']['team_keys'] + \
                    dict['alliances'][key]['red']['team_keys']
                team_nums = [int(num.split('c')[1]) for num in match_robots]
                blue1 = team_nums[0]
                blue2 = team_nums[1]
                blue3 = team_nums[2]
                red1 = team_nums[3]
                red2 = team_nums[4]
                red3 = team_nums[5]
                # and sheets_data['Team Number'] in blue_teams
                match_filter = sheets_data['tba_key'] == key
                match_scouting_data = sheets_data.loc[match_filter]
        
                have_teams = match_scouting_data['Team Number'].unique().tolist()
                # need_teams = [i for i in team_nums if i not in have_teams]
                # if blue1 in have_teams: print('false')
                # else: print('true')
        
                # print(have_teams)
        
                blue1 = "" if blue1 in have_teams else blue1
                blue2 = "" if blue2 in have_teams else blue2
                blue3 = "" if blue3 in have_teams else blue3
                red1 = "" if red1 in have_teams else red1
                red2 = "" if red2 in have_teams else red2
                red3 = "" if red3 in have_teams else red3
        
                # for i in [blue1, blue2, blue3, red1, red2, red3]:
                #     if i in have_teams:
                #         print('yes')
                #         i = ""
        
                match_num = key.split('_')[1]
                # print(team_nums)
                # print(have_teams)
                need_teams = [i for i in team_nums if i not in have_teams]
                if len(need_teams) != 0:
                    dict = {'Match': [match_num],
                            'Blue 1': [blue1],
                            'Blue 2': [blue2],
                            'Blue 3': [blue3],
                            'Red 1': [red1],
                            'Red 2': [red2],
                            'Red 3': [red3]}
                    df = pd.DataFrame(data=dict)
                    # print(df)
                    out_df = pd.concat([out_df, df], axis=0,
                                       join='outer', ignore_index=True)
                # print(out_df)
        
            except:
                # print('invalid key: ' + key)
                pass
                
                
        return out_df
        

    def set_local_scouting_data(self, data) -> None:
        tba_data_validation.local_scouting_data = data

    def get_local_scouting_data(self):
        return tba_data_validation.local_scouting_data

    def get_DataFrame_differences(self, df1, df2):
        try:
            data_combined = df1.merge(df2, indicator=True, how='outer')
            print('here')
            data_combined_diff = data_combined.loc[lambda x: x['_merge'] != 'both']
            data_combined_diff.drop(columns=['_merge'], inplace=True)
            return data_combined_diff

        except MergeError:
            return 'error'  # will slow things down bc returns whole df if there are no updates on refresh

    def validate_new_data(self, updated_scouting_data):
        new_scouting_data = self.get_DataFrame_differences(
            self.local_scouting_data,
            updated_scouting_data)

        self.local_scouting_data = new_scouting_data

        local = self.local_scouting_data
        validation_list = []
        # print(local['tba_api_id'])
        keys_set = set(local['tba_api_id'].to_list())
        unique_keys = list(keys_set)

        for key in unique_keys:
            validation_list.append(self.validate_one_match(key))

        return validation_list

    def validate_one_match(self, match_key):
        local = self.local_scouting_data

        try:
            tba_match_data = self.tbareq.match_aggregate_data(match_key)
            self.local_tba_data = pd.concat(
                [self.local_tba_data, tba_match_data], ignore_index=False)

            match_filter = (local['tba_api_id'] == match_key)

            red_filter = (
                match_filter & (local['Robot Position'].str.contains('Red', na=False)))

            blue_filter = (
                match_filter & (local['Robot Position'].str.contains('Blue', na=False)))

            red_results = self.validate_alliance_balls_scored(
                local.loc[red_filter])
            blue_results = self.validate_alliance_balls_scored(
                local.loc[blue_filter])

            dict = {f'blue_{match_key}': blue_results,
                    f'red_{match_key}': red_results}

            return dict

        except:  # find out what error this will be
            self.match_key_queue.append(match_key)
            # print(self.match_key_queue)
            return 'TBA not updated, added to queue'

    # This function is SO hacky and inconsistent
    # Probably also has wrong math lol
    def validate_alliance_balls_scored(self, alliance_filtered):

        scouting_balls_scored = int(
            alliance_filtered['Upper Hub Scored'].sum() +
            alliance_filtered['Lower Hub Scored'].sum() +
            alliance_filtered['Auto Upper Hub Scored'].sum() +
            alliance_filtered['Auto Lower Hub Scored'].sum())

        index_string = (
            alliance_filtered['Match Type'].iloc[0] +
            str(alliance_filtered['Match Number'].iloc[0]) +
            '_' +
            alliance_filtered['Robot Position'].iloc[0].split(' ')[0].lower())

        tba_balls_scored = self.local_tba_data.loc[index_string, 'matchCargoTotal']

        difference = tba_balls_scored - scouting_balls_scored

        return {'Balls Scored (Scouting)': scouting_balls_scored,
                'Balls Scored (TBA Validation)': tba_balls_scored,
                'Difference': difference}


val = tba_data_validation()
# # will not validate qm27 because qm27 does not have all six data points unless df.loc[0:181]
# # val.set_local_scouting_data(df)

# # print(df.loc[0:180])
# sheets = manager.sheets_data_manager()
# df = sheets.get_analysis_dataframe()
# print(val.missing_data(df))
# print(val.get_local_scouting_data())

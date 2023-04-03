import pandas as pd
import utils.sheets_data_manager as manager
import utils.tba_api_requests as tbapy


sheets = manager.sheets_data_manager()
sheets_data = sheets.get_analysis_dataframe()

tba = tbapy.tba_api_requests('tba_api_key.txt')

combined = sheets_data['Match Type'].combine(sheets_data['Match Number'], (lambda x1, x2: x1 + str(x2)))
combined = combined.apply(lambda x: '2023vagle_' + x)

sheets_data['tba_key'] = combined
# print(sheets_data)

# tba.match_aggregate_data('2023vagle_qm1')
# match_key = '2023vagle_qm56'

# # print(sheets_data['tba_key'])

event_data = tba.event_data('2023vagle')
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
        match_robots = dict['alliances'][key]['blue']['team_keys'] + dict['alliances'][key]['red']['team_keys']
        team_nums = [int(num.split('c')[1]) for num in match_robots]
        blue1 = team_nums[0]
        blue2 = team_nums[1]
        blue3 = team_nums[2]
        red1 = team_nums[3]
        red2 = team_nums[4]
        red3 = team_nums[5]
        match_filter = sheets_data['tba_key'] == key #and sheets_data['Team Number'] in blue_teams
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
            print(df)
            out_df = pd.concat([out_df, df], axis=0, join='outer', ignore_index=True)
        # print(out_df)
	
    except:
        print('invalid key: ' + key)
     
     
print(out_df)
import json
import time
import pandas as pd
import plotly.express as px
from operator import itemgetter
import time
import tbapy

tba = tbapy.TBA(
    'dZURQZdsSGuLmOC8lHnCnpPvjUqVpQ2qXxdObgcLS75cT7jNAfUxxvkOusgsd30e')

start = time.time()

def new_team_season_data_json(event_key):
    """
    Creates a json file of teams at a given event. 
    Includes data from every event and match the team has participated in this season.
    Saves file as 'event_teams_season_data.json' in current directory

    Args:
        event_key (String): The Blue Alliance database format, eg. '2022chcmp'
    """
    list = get_event_teams_list(event_key)
    dict = json_update_team_list_season_matches(list, 2022)

    with open('event_teams_season_data.json', 'w') as outfile:
        json.dump(dict, outfile, indent=4)


def json_update_team_season_matches(team_key, year):
    events = season_events(team_key, year)
    season_event_matches = {}
    for i in events:
        season_event_matches[i] = tba.team_matches(team_key, i, 2022)

    return season_event_matches


def json_update_team_list_season_matches(team_key_list, year):
    team_list_season_matches = {}
    for i in team_key_list:
        team_list_season_matches[i] = json_update_team_season_matches(i, year)

    return team_list_season_matches


def open_team_season_data_json():
    """
    enables read and write to 'event_teams_season_data.json' in current directory

     Returns:
        Dictionary: deserialized contents of json file
    """
    with open('event_teams_season_data.json', 'r') as infile:
        data = json.load(infile)

    return data


def team_endgame_results(match_keys, team_key):
    """
    generates list of endgame results ('climbs' for 2022 season) achieved by a team during a given set of matches

    Args:
        match_keys (List): The Blue Alliance database format, eg. '2022chcmp_qm1'
        team_key (String): The Blue Alliance database format, eg. '2022chcmp'

    Returns:
        List: List of strings eg. [Mid, Low, None], Built in order of match_keys argument
    """
    data = open_team_season_data_json()
    team_match_stations = []
    endgames = []
    for key in match_keys:
        matches_list = data[team_key][key.split('_')[0]]
        for match in matches_list:
            if match['key'] == key:

                try:
                    station_index = match['alliances']['blue']['team_keys'].index(
                        team_key) + 1
                    alliance_color = 'blue'
                except ValueError:
                    station_index = match['alliances']['red']['team_keys'].index(
                        team_key) + 1
                    alliance_color = 'red'

                team_match_stations.append(
                    (alliance_color + ' ' + str(station_index)))
                station = alliance_color + ' ' + str(station_index)
                split = station.split()

                # print(match['score_breakdown']['red'])
                
                if match['score_breakdown'] != None and match['score_breakdown']!= {}:
                    endgame = match['score_breakdown'][split[0]]['endgameRobot' + split[1]]
                    endgames.append(endgame)

    return endgames


def team_season_endgame_tally(team_key, year):
    """
    generates dictionary of endgame results ('climbs' for 2022 season) achieved by a team during a season

    Args:
        team_key (String): The Blue Alliance database format, eg. 'frc401'
        year (int): the year of competition

    Returns:
        Dictionary: keys of 'Low', 'Mid', 'High', 'Traversal', & 'None' corresponding to a tally of each result achieved by a team over the whole season
    """
    endgame_list = team_endgame_results(team_season_matches(team_key, year), team_key)
    low, mid, high, trav, none = 0, 0, 0, 0, 0

    for item in endgame_list:
        if item == 'Low':
            low += 1
        if item == 'Mid':
            mid += 1
        if item == 'High':
            high += 1
        if item == 'Traversal':
            trav += 1
        if item == 'None':
            none += 1

    # endgame_dict = {'Low' : low, 'Mid' : mid, 'High' : high, 'Traversal' : trav, 'None' : none}
    endgame_dict = {'level' : ['Low', 'Mid', 'High', 'Traversal','None'],
                    'climbs' : [low, mid, high, trav, none]}

    return endgame_dict


def team_season_matches(team_key, year):
    """
    get a list of match keys for all matches played by a team in a given year

    Args:
        team_key (String): The Blue Alliance database format, eg. 'frc401'
        year (int): year of competition

    Returns:
        List: The Blue Alliance database format, eg. '2022chcmp_qm1'; All matches over whole season
    """

    data = open_team_season_data_json()
    season_event_keys = season_events(team_key, year)
    # print(season_event_keys)
    # print(team_key)
    team_data = data[team_key]

    season_match_keys = []
    for i in season_event_keys:
        events = team_data[i]

        for x in events:
            season_match_keys.append(x['key'])

    return season_match_keys
    

def team_list_season_matches(team_key_list, year):
    """
     get a Dictionary of match keys for all matches played by every team on a list in a given year

    Args:
        team_key_list (List): The Blue Alliance database format, eg. 'frc401'
        year (int): year of competition

    Returns:
        Dictionary: team keys are dict keys and correspond to lists of all matches played so far in the season
    """    
    team_list_season_matches = {}
    for i in team_key_list:
        team_list_season_matches[i] = team_season_matches(i, year)

    return team_list_season_matches


def team_event_matches(event_key, team_key):
    """
    get a list of match keys for all matches played by a team at a given event

    Args:
        event_key (String): The Blue Alliance database format, eg. '2022chcmp'
        team_key (String): The Blue Alliance database format, eg. 'frc401'

    Returns:
        List: The Blue Alliance database format, eg. '2022chcmp_qm1'; All matches at an event
    """
    data = open_team_season_data_json()
    team_event_data = data[team_key][event_key]

    event_match_keys = []

    for x in team_event_data:
        event_match_keys.append(x['key'])

    return event_match_keys


def tbapy_to_pandas_df(json_data):
    """
    Converts the json string returned by tbapy functions into a pandas dataframe 

    Args:
        json_data (String): String format of json data

    Returns:
        pandas.DataFrame: all n/a values replaced with "" 
    """
    s1 = json.dumps(json_data)
    data = json.loads(s1)
    df = pd.DataFrame(data)
    df = df.fillna("")

    return df


def season_events(team_key, year):
    """
    generates list of events attended by a team during a given year

    Args:
        team_key (String): The Blue Alliance database format, eg. 'frc401'
        year (int): the year of competition

    Returns:
        List: event keys in The Blue Alliance database format, eg. '2022chcmp', is NOT sorted
    """
    json_data = tba.team_events(team_key, year)
    s1 = json.dumps(json_data)
    data = json.loads(s1)
    # Sorting here triples the execution time
    # data = sorted(data, key=itemgetter('start_date'))
    output = []
    for i in data:
        output.append(i['key'])
    return output


def get_qm_schedule(event_key):
    """
    gets a dictionary containing the match keys of every qualifying match at a competition as the first row.
    Each row beneath this contains the team key assigned to each driver station, where r is 'red' and b is 'blue'
    eg.              2022chcmp_qm1          2022chcmp_qm2
                 b1: frc401             b1: frc401
                 b2: frc401             b2: frc401
                 b3: frc401             b3: frc401
                 r1: frc401             r1: frc401
                 r2: frc401             r2: frc401
                 r3: frc401             r3: frc401
        match_label: qm1       match_label: qm2

    Args:
        event_key (String): The Blue Alliance database format, eg. '2022chcmp'

    Returns:
        Dictionary: Each column corresponds to a match and its alliances
    """    
    json_data = tba.event_matches(event_key)
    df = tbapy_to_pandas_df(json_data)

    try:
        output = df.sort_values(by=['predicted_time'])
        output = output.reset_index(drop=True)

        output = output[output['comp_level'] == 'qm']
        newdf = output['alliances']

        match_schedule_dict = {}

        for index, items in newdf.items():
            blue_alliance = items['blue']['team_keys']
            red_alliance = items['red']['team_keys']
            b1, b2, b3 = blue_alliance
            r1, r2, r3 = red_alliance
            synced_match_code = output.iloc[index]['key']

            match_label = ''
            flag = False

            for character in range(4, len(synced_match_code)):
                if flag == True:
                    match_label += synced_match_code[character]

                if synced_match_code[character] == '_':
                    flag = True

            match_schedule_dict[synced_match_code] = {
                'b1': b1,
                'b2': b2,
                'b3': b3,
                'r1': r1,
                'r2': r2,
                'r3': r3,
                'match_labels': match_label
            }

        return match_schedule_dict

    except KeyError:
        return 'Schedule Has Not Been Released'


def get_event_teams_list(event_key):
    """
    Get list of all teams attending a given event

    Args:
        event_key (String): The Blue Alliance database format, eg. '2022chcmp'
      
    Returns:
        List: team keys in The Blue Alliance database format, eg. 'frc401'
    """    
    json_data = tba.event_teams(event_key, keys=True)
    return json_data


def event_team_lookup_dict(event_key):
    json_data = tba.event_teams(event_key)
    df = tbapy_to_pandas_df(json_data)

    event_teams_dict = {}

    for items in df['key']:
        team_profile_df = df.loc[df['key'] == items]
        team_number = team_profile_df['team_number'].values[0]
        team_number = int(team_number)
        nickname = team_profile_df['nickname'].values[0]
        city = team_profile_df['city'].values[0]
        state_prov = team_profile_df['state_prov'].values[0]
        country = team_profile_df['country'].values[0]

        climbs = team_season_endgame_tally(items, 2022)

        event_teams_dict[items] = {
            'profile': {
                'team_number': team_number,
                'nickname': nickname,
                'state_prov': state_prov,
                'country': country},
            # robot image
            'season_data': {
                'endgame_results': climbs}
        }

    return event_teams_dict


def new_event_team_lookup_json(event_key):
    dict = event_team_lookup_dict(event_key)
    # print(type(dict))
    # dict = json.dumps(dict)
    with open('event_team_lookup.json', 'w') as outfile:
        json.dump(dict, outfile, indent=4)

# video keys like H-zSTqt0SHE should be used
# after 'youtube.com/watch?v=' in the url
#ie: 'youtube.com/watch?v=H-zSTqt0SHE'


# teams_dict = new_event_team_lookup_json('2022varr')

def open_event_team_lookup_json():
    """
    enables reading 'event_team_lookup.json' in current directory

     Returns:
        Dictionary: deserialized contents of json file
    """
    with open('event_team_lookup.json', 'r') as infile:
        data = json.load(infile)

    return data


def endgame_pie_chart_df(team_key):
    data = open_event_team_lookup_json()
    climbs = data[team_key]['season_data']['endgame_results']
    df = pd.DataFrame(climbs)

    return df


def robot_image(team_key, year):
    images = tba.team_media(team_key, year)
    
    for pic in images:
      if pic['type'] == 'imgur':
        return pic['view_url']
    
    return 'no image found'

# print(robot_image('frc401', 2022))
# end = time.time()
# print(f'time of execution: {(end-start) * 10**3} ms')


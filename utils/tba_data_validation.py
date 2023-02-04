import pandas as pd
import tba_api_requests
from pandas.errors import MergeError
import pygsheets

gc = pygsheets.authorize(
    service_file='/home/belawilliams/Documents/team-401-scouting-credentials-2023.json')

sh = gc.open('401_scouting_test_database')

# select the first sheet
wks = sh[0]

df = wks.get_as_df(
    has_header=True,
    # index_column=5,
    include_tailing_empty=False,
    include_tailing_empty_rows=False,
    value_render='FORMATTED_VALUE')

class tba_data_validation:

    local_scouting_data = pd.DataFrame()
    local_tba_data = pd.DataFrame()
    match_key_queue = []

    def __init__(self) -> None:
        self.tbareq = tba_api_requests.tba_api_requests(
            'tba_api_key.txt')

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
        print(local['tba_api_id'])
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
# will not validate qm27 because qm27 does not have all six data points unless df.loc[0:181]
# val.set_local_scouting_data(df)

# print(df.loc[0:180])
# print(val.validate_new_data(df))
print(val.get_local_scouting_data())

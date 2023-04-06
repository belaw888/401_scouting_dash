import pandas as pd
import pygsheets
import json
from enum import IntEnum

class Points(IntEnum):
    AUTO_TOP = 6
    AUTO_MID = 4
    AUTO_LOW = 3
    TELE_TOP = 5
    TELE_MID = 3
    TELE_LOW = 2
    LINK = 5
    AUTO_DOCKED = 8
    AUTO_ENGAGED = 12
    TELE_DOCKED = 6
    TELE_ENGAGED = 10
    MOBILITY = 3
    PARK = 2


class sheets_data_manager:
    raw_dataframe = pd.DataFrame()
    raw_dataframe_422 = pd.DataFrame()
    analysis_dataframe = pd.DataFrame()
    
    def __init__(self) -> None:
        self.credentials = pygsheets.authorize(
            service_file='/home/belawilliams/Documents/team-401-scouting-credentials-2023.json')
        self.google_sheet = self.credentials.open(
            '[401 & 422 Scouting] - VAGLE- 2023 Charged Up Database')
        self.worksheet = self.google_sheet.worksheet('title', '401_raw_data')
        self.raw_dataframe = self.worksheet.get_as_df(
            has_header=True,
           	include_tailing_empty=False,
           	include_tailing_empty_rows=False,
            numerize=True,
            value_render='UNFORMATTED_VALUE')
        self.analysis_dataframe = self.update_analysis_dataframe(self.raw_dataframe)
        
        self.worksheet_422 = self.google_sheet.worksheet('title', '422_raw_data')
        self.raw_dataframe_422 = self.worksheet_422.get_as_df(
            has_header=True,
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
            numerize=True,
            value_render='UNFORMATTED_VALUE')
        
    def refresh_google_sheets_dataframe(self):
        self.raw_dataframe = self.worksheet.get_as_df(
            has_header=True,
         	include_tailing_empty=False,
         	include_tailing_empty_rows=False,
            numerize=True,
            value_render='UNFORMATTED_VALUE')
        self.analysis_dataframe = self.update_analysis_dataframe(self.raw_dataframe)
        
        self.worksheet_422 = self.google_sheet.worksheet('title', '422_raw_data')
        self.raw_dataframe_422 = self.worksheet_422.get_as_df(
            has_header=True,
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
            numerize=True,
            value_render='UNFORMATTED_VALUE')
    
    def get_google_sheets_dataframe(self):
        return self.raw_dataframe
    
    def get_analysis_dataframe(self):
        return self.analysis_dataframe
    
    def get_422_dataframe(self):
        return self.raw_dataframe_422
    
    def add_to_401_dataframe(self, row) -> None:
        # print(self.raw_dataframe)
        self.raw_dataframe.loc[len(self.raw_dataframe.index)] = row
    
    def get_duplicates_series(self, df):
        df = df[df['data_id'] != '']
        data_id_value_counts = df.value_counts(subset='data_id')
        duplicates_series = data_id_value_counts[data_id_value_counts > 1]
        
        ls = duplicates_series.index.tolist()
        ls = [i for i in ls if i != '']
        # print(ls)
        teams = [i.split('_')[0] for i in ls]
        matches = [i.split('_')[1] for i in ls]
        duplicates = duplicates_series.values.tolist()
        
        dict = {'Team Number': teams, 'Match Number': matches, '# of Duplicates': duplicates}
        
        df = pd.DataFrame(dict)
        return df
        
    def get_team_data(self, team):
        filter = self.raw_dataframe['Team Number'] == team
        return self.raw_dataframe.loc[filter]
        
    def get_team_list(self):
      list = self.raw_dataframe['Team Number'].unique().tolist()
      list.sort()
      return list        
  
    def get_as_json(self, dataframe):
        return json.dumps(dataframe, default=lambda df: json.loads(df.to_json(orient='split')))
  
    def parse_json(self, json_string):
        dict = json.loads(json_string)
        df = pd.DataFrame(dict['data'], columns=dict['columns'], index=dict['index'])
        return df
    
    #static isn't really the right term here
    def get_team_data_static(self, dataframe, team):
        filter = dataframe['Team Number'] == team
        return dataframe.loc[filter]
    
    def update_analysis_dataframe(self, team_scouting_results):
        
        partial_df = team_scouting_results.loc[:,'data_id':'Preload']
        
        auto_grid_points_series = (
            ((team_scouting_results['Auto Cones Top'] + team_scouting_results['Auto Cubes Top']) * Points.AUTO_TOP) +
            ((team_scouting_results['Auto Cones Mid'] + team_scouting_results['Auto Cubes Mid']) * Points.AUTO_MID) +
            ((team_scouting_results['Auto Cones Low'] + team_scouting_results['Auto Cubes Low']) * Points.AUTO_LOW))
        auto_grid_points_series.rename('Auto Grid Points', inplace=True)

        
        tele_grid_points_series = (
            ((team_scouting_results['Tele Cones Top'] + team_scouting_results['Tele Cubes Top']) * Points.TELE_TOP) +
            ((team_scouting_results['Tele Cones Mid'] + team_scouting_results['Tele Cubes Mid']) * Points.TELE_MID) +
            ((team_scouting_results['Tele Cones Low'] + team_scouting_results['Tele Cubes Low']) * Points.TELE_LOW))
        tele_grid_points_series.rename('Tele Grid Points', inplace=True)


        auto_charge_points_series = team_scouting_results['Auto Charge'].map(
            {'D': Points.AUTO_DOCKED, 'E': Points.AUTO_ENGAGED, 'NA': None, 'F': 0})  # we only care about how many times they tried to vs failed right?
        auto_charge_points_series.rename('Auto Charge Points', inplace=True)


        tele_charge_points_series = team_scouting_results['End Charge'].map(
            {'D': Points.TELE_DOCKED, 'E': Points.TELE_ENGAGED, 'NA': None, 'F': 0})
        tele_charge_points_series.rename('Endgame Charge Points', inplace=True)

        mobility_points_series = team_scouting_results['Mobility'].map(
            {'TRUE': Points.MOBILITY, '': 0})
        mobility_points_series.rename('Mobility Points', inplace=True)

        total_grid_points_series = auto_grid_points_series.add(
            tele_grid_points_series, fill_value=0)
        total_grid_points_series.rename('Total Grid Points', inplace=True)

        
        total_charge_points_series = auto_charge_points_series.add(
            tele_charge_points_series, fill_value=0)
        total_charge_points_series.rename('Total Charge Points', inplace=True)


        total_points_series = (total_charge_points_series.add(
            total_grid_points_series, fill_value=0)).add(mobility_points_series, fill_value=0)
        total_points_series.rename('Total Points', inplace=True)
        
        auto_cones_count_series = (
            (team_scouting_results['Auto Cones Top']) +
            (team_scouting_results['Auto Cones Mid']) +
            (team_scouting_results['Auto Cones Low']))
        auto_cones_count_series.rename('Auto Cones', inplace=True)


        auto_cubes_count_series = (
            (team_scouting_results['Auto Cubes Top']) +
            (team_scouting_results['Auto Cubes Mid']) +
            (team_scouting_results['Auto Cubes Low']))
        auto_cubes_count_series.rename('Auto Cubes', inplace=True)

        auto_pieces_count_series = auto_cones_count_series.add(auto_cubes_count_series)
        auto_pieces_count_series.rename('Auto Pieces', inplace=True)

        tele_cones_count_series = (
            (team_scouting_results['Tele Cones Top']) +
            (team_scouting_results['Tele Cones Mid']) +
            (team_scouting_results['Tele Cones Low']))
        tele_cones_count_series.rename('Tele Cones', inplace=True)
        
        tele_cubes_count_series = (
            (team_scouting_results['Tele Cubes Top']) +
            (team_scouting_results['Tele Cubes Mid']) +
            (team_scouting_results['Tele Cubes Low']))
        tele_cubes_count_series.rename('Tele Cubes', inplace=True)
        
        tele_pieces_count_series = tele_cones_count_series.add(tele_cubes_count_series)
        tele_pieces_count_series.rename('Tele Pieces', inplace=True)

        total_cubes_count_series = tele_cubes_count_series.add(auto_cubes_count_series)
        total_cubes_count_series.rename('Total Cubes', inplace=True)
        
        total_cones_count_series = tele_cones_count_series.add(auto_cones_count_series)
        total_cones_count_series.rename('Total Cones', inplace=True)
        
        total_pieces_count_series = tele_pieces_count_series.add(auto_pieces_count_series)
        total_pieces_count_series.rename('Total Pieces', inplace=True)
        
        top_cubes_series = (
             (team_scouting_results['Auto Cubes Top']) +
             (team_scouting_results['Tele Cubes Top']))
        top_cubes_series.rename('Top Cubes', inplace=True)
        
        top_cones_series = (
             (team_scouting_results['Auto Cones Top']) +
             (team_scouting_results['Tele Cones Top']))
        top_cones_series.rename('Top Cones', inplace=True)
        
        mid_cubes_series = (
             (team_scouting_results['Auto Cubes Mid']) +
             (team_scouting_results['Tele Cubes Mid']))
        mid_cubes_series.rename('Mid Cubes', inplace=True)
        
        mid_cones_series = (
             (team_scouting_results['Auto Cones Mid']) +
             (team_scouting_results['Tele Cones Mid']))
        mid_cones_series.rename('Mid Cones', inplace=True)
        
        low_cubes_series = (
             (team_scouting_results['Auto Cubes Low']) +
             (team_scouting_results['Tele Cubes Low']))
        low_cubes_series.rename('Low Cubes', inplace=True)
        
        low_cones_series = (
             (team_scouting_results['Auto Cones Low']) +
             (team_scouting_results['Tele Cones Low']))
        low_cones_series.rename('Low Cones', inplace=True)
        
        analysis_df = pd.concat([partial_df, 
                        auto_grid_points_series, 
                        tele_grid_points_series, 
                        auto_charge_points_series,
                        tele_charge_points_series,
                        mobility_points_series,
                        total_grid_points_series,
                        total_charge_points_series,
                        total_points_series,
                        top_cubes_series,
                        top_cones_series,
                        mid_cones_series,
                        mid_cubes_series,
                        low_cubes_series,
                        low_cones_series,
                        auto_cones_count_series,
                        auto_cubes_count_series,
                        auto_pieces_count_series,
                        tele_cones_count_series,
                        tele_cubes_count_series,
                        tele_pieces_count_series,
                        total_cones_count_series,
                        total_cubes_count_series,
                        total_pieces_count_series
                        ], axis=1)
        
        # print(analysis_df)
        
        return analysis_df
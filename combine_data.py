import pandas as pd
import numpy as np
from datetime import datetime
import csv
import os
from initial_data_preparation import extract_dataframe, extract_dirname


def combine_data(file_name):
    # extract basic dataframe
    df = extract_dataframe(file_name)

    # directory containing data for each team separately
    input_dir = extract_dirname(file_name)

    # values to store
    vals = {'Date': None, 'WinTeam': 0, 'valid': 0, 'HomeTeam': '',
            'AwayTeam': '', 'HomeScore': 0, 'AwayScore': 0, 'HT_tot_game': 0,
            'AT_tot_game': 0, 'HT_tot_game_win': 0, 'AT_tot_game_win': 0,
            'HT_tot_game_home': 0, 'AT_tot_game_away': 0,
            'HT_tot_game_win_home': 0, 'AT_tot_game_win_away': 0,
            'HT_last_10_win': 0, 'AT_last_10_win': 0,
            'HT_last_5_win': 0, 'AT_last_5_win': 0,
            'HT_last_5_win_home': 0, 'AT_last_5_win_away': 0,
            'HT_last_1_win': 0, 'AT_last_1_win': 0}

    df_ATL = None
    df_BOS = None
    df_BRK = None
    df_CHI = None
    df_CHO = None
    df_CLE = None

    df_DAL = None
    df_DEN = None
    df_DET = None
    df_GSW = None
    df_HOU = None
    df_IND = None

    df_LAC = None
    df_LAL = None
    df_MEM = None
    df_MIA = None
    df_MIL = None
    df_MIN = None

    df_NOP = None
    df_NYK = None
    df_OKC = None
    df_ORL = None
    df_PHI = None
    df_PHO = None

    df_POR = None
    df_SAC = None
    df_SAS = None
    df_TOR = None
    df_UTA = None
    df_WAS = None

    teams = {'ATL': [df_ATL, 0], 'BOS': [df_BOS, 0], 'BRK': [df_BRK, 0],
             'CHI': [df_CHI, 0], 'CHO': [df_CHO, 0], 'CLE': [df_CLE, 0],
             'DAL': [df_DAL, 0], 'DEN': [df_DEN, 0], 'DET': [df_DET, 0],
             'GSW': [df_GSW, 0], 'HOU': [df_HOU, 0], 'IND': [df_IND, 0],
             'LAC': [df_LAC, 0], 'LAL': [df_LAL, 0], 'MEM': [df_MEM, 0],
             'MIA': [df_MIA, 0], 'MIL': [df_MIL, 0], 'MIN': [df_MIN, 0],
             'NOP': [df_NOP, 0], 'NYK': [df_NYK, 0], 'OKC': [df_OKC, 0],
             'ORL': [df_ORL, 0], 'PHI': [df_PHI, 0], 'PHO': [df_PHO, 0],
             'POR': [df_POR, 0], 'SAC': [df_SAC, 0], 'SAS': [df_SAS, 0],
             'TOR': [df_TOR, 0], 'UTA': [df_UTA, 0], 'WAS': [df_WAS, 0]}

    out_file = 'result' + '.csv'
    with open(out_file, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerow(vals.keys())
        for _, row in df.iterrows():
            # get home and away team info
            home_team = row['HomeTeam']
            df_HT = teams[home_team][0]
            iter_HT = teams[home_team][1]
            away_team = row['AwayTeam']
            df_AT = teams[away_team][0]
            iter_AT = teams[away_team][1]

            # update basic vals
            vals['Date'] = row['Date']

            if row['WinningTeam'] == home_team:
                vals['WinTeam'] = 1
            else:
                0

            ### TODO: Assign all variables ###

            # SAVE ROW
            csvWriter.writerow(vals.values())

            # update iterators
            teams[home_team][1] = teams[home_team][1] + 1
            teams[away_team][1] = teams[away_team][1] + 1


# Example
file_name = '2019-20_pbp.csv'

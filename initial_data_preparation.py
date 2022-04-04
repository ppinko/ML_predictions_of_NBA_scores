import pandas as pd
import numpy as np
from datetime import datetime
import csv
import os


def transform_to_datatime(date):
    '''
    Transforms date from csv input file to datatime object.
    '''
    date = date.strip().split()
    if len(date[1]) < 2:
        date[1] = '0' + date[1]
    date = ' '.join(date)
    return datetime.strptime(date, '%B %d %Y')


def create_team_data(df, team, season, out_dir):
    '''
    Store csv data for a particular team for particular season.
    '''
    vals = {'no.': 0, 'valid': 0, 'date': None, 'home': 0, 'last_game_win': 0, 'tot_win': 0,
            'tot_home_game': 0, 'last_home': 0, 'last_home_win': 0,
            'last_away_win': 0, 'last_10': 0, 'last_5': 0, 'last_5_home': 0,
            'last_5_away': 0}

    prev_game = {'home': False, 'win': False}

    df_team = df[(df['HomeTeam'] == team) | (df['AwayTeam'] == team)]

    out_file = team + '_' + season + '.csv'
    out_file = os.path.join(out_dir, out_file)
    with open(out_file, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerow(vals.keys())
        for _, row in df_team.iterrows():
            prev_game['home'] = row['HomeTeam'] == team
            prev_game['win'] = row['WinningTeam'] == team

            # update basic vals
            vals['no.'] = vals['no.'] + 1
            vals['data'] = row['Date']
            vals['home'] = int(row['HomeTeam'] == team)

            # SAVE ROW
            csvWriter.writerow(vals.values())

            # update rest of the values for next iterations
            if prev_game['win']:
                vals['tot_win'] = vals['tot_win'] + 1
                vals['last_game_win'] = 1
                vals['last_5'] = ((vals['last_5'] << 1) | 1) % 32
                vals['last_10'] = ((vals['last_10'] << 1) | 1) % 2**10
            else:
                vals['last_game_win'] = 0
                vals['last_5'] = ((vals['last_5'] << 1) | 0) % 32
                vals['last_10'] = ((vals['last_10'] << 1) | 0) % 2**10

            if prev_game['home']:
                vals['tot_home_game'] = vals['tot_home_game'] + 1
                vals['last_home'] = 1
                if prev_game['win']:
                    vals['last_home_win'] = 1
                    vals['last_5_home'] = ((vals['last_5_home'] << 1) | 1) % 32
                else:
                    vals['last_home_win'] = 0
                    vals['last_5_home'] = ((vals['last_5_home'] << 1) | 0) % 32
            else:
                vals['last_home'] = 0
                if prev_game['win']:
                    vals['last_away_win'] = 1
                    vals['last_5_away'] = ((vals['last_5_away'] << 1) | 1) % 32
                else:
                    vals['last_away_win'] = 0
                    vals['last_5_away'] = ((vals['last_5_away'] << 1) | 0) % 32

            # enough data for making predictions
            if vals['valid'] or (vals['no.'] - vals['tot_home_game'] >= 5 and vals['tot_home_game'] >= 5):
                vals['valid'] = 1


def prepare_data(file_name):
    '''
    Prepare data for particular season.
    '''
    season = file_name.rstrip('_pbp.csv')

    eog = 'End of Game'
    gameType = 'regular'
    use_cols = {'Date': str, 'GameType': str, 'WinningTeam': str, 'AwayTeam': str,
                'HomeTeam': str, 'AwayScore': np.uint8, 'HomeScore': np.uint8,
                'AwayPlay': str}
    df = pd.read_csv(file_name, usecols=use_cols.keys(), dtype=use_cols)
    df = df[(df['AwayPlay'] == eog) & (df['GameType'] == gameType)]
    df['HomeWin'] = np.uint8(df.WinningTeam == df.HomeTeam)
    df['date'] = df.Date.apply(transform_to_datatime)

    # create output directory if not exist
    out_dir = 'out_' + season
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    # create input files
    df2 = df[['HomeTeam']]
    df2.drop_duplicates(inplace=True)
    df2.sort_values('HomeTeam', inplace=True)
    for i in range(df2.shape[0]):
        team = str(df2.iat[i, 0])
        create_team_data(df, team, season, out_dir)


# Example
file_name = '2019-20_pbp.csv'
prepare_data(file_name)

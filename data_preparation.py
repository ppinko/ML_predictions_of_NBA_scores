import pandas as pd
import numpy as np
from datetime import datetime


def transform_to_datatime(date):
    '''
    Transforms date from csv input file to datatime object.
    '''
    date = date.strip().split()
    if len(date[1]) < 2:
        date[1] = '0' + date[1]
    date = ' '.join(date)
    return datetime.strptime(date, '%B %d %Y')


file_name = '2019-20_pbp.csv'

eog = 'End of Game'
gameType = 'regular'
use_cols = {'Date': str, 'GameType': str, 'WinningTeam': str, 'AwayTeam': str,
            'HomeTeam': str, 'AwayScore': np.uint8, 'HomeScore': np.uint8,
            'AwayPlay': str}
df = pd.read_csv(file_name, usecols=use_cols.keys(), dtype=use_cols)
df = df[(df['AwayPlay'] == eog) & (df['GameType'] == gameType)]
df['HomeWin'] = np.uint8(df.WinningTeam == df.HomeTeam)
df['date'] = df.Date.apply(transform_to_datatime)

print(df.columns)

print()
print(df.head)

print()

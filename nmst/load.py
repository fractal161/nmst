"""Functions for loading and updating the match database."""

import csv
from datetime import datetime, timedelta
import os
import urllib.request

import pandas as pd

from . import config

def update_db():
    """Fetch the current version of the database from the Google Sheet."""
    spreadsheet_id = config['sheet']['spreadsheet_id']
    sheet_id = config['sheet']['sheet_id']

    db_url = ('https://docs.google.com/spreadsheets/d/'
              f'{spreadsheet_id}/export?format=csv&gid={sheet_id}')
    print('Establishing connection to Google Sheets...')
    # TODO: show download progress if possible
    # Idea: https://stackoverflow.com/a/1517728
    update_time = datetime.now()
    with urllib.request.urlopen(db_url) as response:
        print('Success! Writing database to file...')
        # TODO: implement checks to prevent downloading malformed data
        with open(config['db']['path'], 'wb', encoding='utf-8') as f:
            f.write(response.read())
    # update config with update time
    config['db']['last_update_time'] = update_time.isoformat()
    config.save()

def _auto_update():
    if not config['db']['auto_update']:
        return
    # check if path exists
    path = config['db']['path']
    if not os.path.exists(path):
        print('Database not found, attempting to download it...')
        update_db()
        return
    # check if time since last update exceeds the configured threshold
    last_update_time = datetime.fromisoformat(config['db']['last_update_time'])
    current_time = datetime.now()
    threshold = int(config['db']['auto_update_threshold'])
    if current_time - last_update_time > timedelta(hours=threshold):
        print(f'At least {threshold} hours since last update, '
              'attempting to download database...')
        update_db()
        return

def load_as_df(*, exclude_faster=True):
    """Load the match database as a pandas dataframe."""
    _auto_update()
    dtypes: dict[str, str] = {}
    for col in ['Players', 'Playstyle', 'Won?', 'Topout Type', 'Cap', 'SPS',
                'Lvl Start', 'Event', 'Round', 'Game Link', 'Match Pairing']:
        dtypes[col] = 'category'
    df = pd.read_csv(config['db']['path'],
                     dtype=dtypes,
                     index_col='Game ID')
    # use column types to reduce memory usage
    if exclude_faster:
        df = df[df['Event'] != 'May 2023 Faster Masters']
    return df

def load_as_list():
    """Load the match database as a 2-dimensional list."""
    _auto_update()
    with open(config['db']['path'], 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

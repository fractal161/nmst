import csv
from datetime import datetime, timedelta
import os
import urllib.request

import pandas as pd

from . import config

def update_db():
    spreadsheet_id = config['sheet']['spreadsheet_id']
    sheet_id = config['sheet']['sheet_id']

    db_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}'
    print('Establishing connection to Google Sheets...')
    # TODO: show download progress if possible
    # Idea: https://stackoverflow.com/a/1517728
    update_time = datetime.now()
    with urllib.request.urlopen(db_url) as response:
        print('Success! Writing database to file...')
        # TODO: implement checks to prevent downloading malformed data
        with open(config['db']['path'], 'wb') as f:
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
        print(f'{threshold} hours since last update, attempting to download database...')
        update_db()
        return

def load_as_df():
    _auto_update()
    df = pd.read_csv(config['db']['path'])
    df.set_index('Game ID')
    print(df.index)
    return df

def load_as_list():
    _auto_update()
    with open(config['db']['path'], 'r') as file:
        reader = csv.reader(file)
        return list(reader)

from configparser import ConfigParser
from datetime import datetime
import os
import urllib.request

if not os.path.exists('config.toml'):
    with open('config.toml.example', 'r') as example_config:
        config_lines = example_config.readlines()
        # TODO: smarter handling of the warning comments
        with open('config.toml', 'w') as config:
            config.writelines(config_lines[3:])
config = ConfigParser()
config.read('config.toml')

spreadsheet_id = config['sheet']['spreadsheet_id']
sheet_id = config['sheet']['sheet_id']

db_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}'
print('Establishing connection to Google Sheets...')
# TODO: show download progress if possible
# Idea: https://stackoverflow.com/a/1517728
update_time = datetime.now()
with urllib.request.urlopen(db_url) as response:
    print('Success! Writing database to file...')
    with open('matchdb/db.csv', 'wb') as f:
        f.write(response.read())

# update config with update time
config['db']['last_update_time'] = update_time.isoformat()
with open('config.toml', 'w') as config_file:
    config.write(config_file)

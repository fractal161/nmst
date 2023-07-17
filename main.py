from configparser import ConfigParser
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

spreadsheetid = config['sheet']['spreadsheetid']
sheetid = config['sheet']['sheetid']

db_url  = f'https://docs.google.com/spreadsheets/d/{spreadsheetid}/export?format=csv&gid={sheetid}'
print('Connecting to ...')
# TODO: show download progress if possible
# Idea: https://stackoverflow.com/a/1517728
with urllib.request.urlopen(db_url) as response:
    print('Success! Writing database to file...')
    print(response.headers)
    with open('matchdb/db.csv', 'wb') as f:
        f.write(response.read())

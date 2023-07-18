from datetime import datetime
import urllib.request
from nmst.config import config

spreadsheet_id = config['sheet']['spreadsheet_id']
sheet_id = config['sheet']['sheet_id']

db_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}'
print('Establishing connection to Google Sheets...')
# TODO: show download progress if possible
# Idea: https://stackoverflow.com/a/1517728
update_time = datetime.now()
with urllib.request.urlopen(db_url) as response:
    print('Success! Writing database to file...')
    with open(config['db']['path'], 'wb') as f:
        f.write(response.read())

# update config with update time
config['db']['last_update_time'] = update_time.isoformat()
config.save()

# hack to make the script runnable from this file's parent directory
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import pandas as pd

from nmst.load import load_as_df
from nmst.headers import *

def print_table():
    THRESHOLD = 50
    df = load_as_df()

    natural_topouts = df[df[TOPOUT_TYPE] == 'Natural']
    game_counts = natural_topouts[PLAYER].value_counts()

    players_with_enough = game_counts[game_counts >= THRESHOLD].index
    restricted = natural_topouts[natural_topouts[PLAYER].isin(players_with_enough)]
    no_unknowns = restricted[restricted[SCORE_AT_19] != 'unknown']
    medians = no_unknowns[[PLAYER, SCORE_AT_19]].dropna().groupby(PLAYER).median()
    medians = medians.dropna().sort_values(SCORE_AT_19, ascending=False)
    medians['Natural Topouts'] = game_counts
    print(medians)

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    print_table()

# first goal: replicate the highest median score leaderboard
# fields: players, median score, # games, median 19 trans, median 29 trans, best game

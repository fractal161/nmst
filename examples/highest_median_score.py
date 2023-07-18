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

    # only look at natural topouts
    natural_topouts = df[df[TOPOUT_TYPE] == 'Natural']
    game_counts = natural_topouts[PLAYER].value_counts()

    # filter out players who haven't played enough games
    players_with_enough = game_counts[game_counts >= THRESHOLD].index
    restricted = natural_topouts[natural_topouts[PLAYER].isin(players_with_enough)]
    # filter out unknown values
    no_unknown_final_score = restricted[restricted[FINAL_SCORE] != 'unknown']
    # compute median of all valid data
    board = (no_unknown_final_score[[PLAYER, FINAL_SCORE]]
             .dropna()
             .groupby(PLAYER)
             .median())
    board.rename({FINAL_SCORE: 'Median Score'}, axis='columns', inplace=True)
    board = board.dropna().sort_values('Median Score', ascending=False)

    # num games column
    board['Games'] = game_counts

    # median 19 trans column
    no_unknown_19_trans = df[df[SCORE_AT_19] != 'unknown']
    median_19_trans = (no_unknown_19_trans[[PLAYER, SCORE_AT_19]]
                       .dropna()
                       .groupby(PLAYER)
                       .median())
    board['Median 19 Trans'] = median_19_trans

    # median 29 trans column
    no_unknown_29_trans = df[df[SCORE_AT_29] != 'unknown']
    median_29_trans = (no_unknown_29_trans[[PLAYER, SCORE_AT_29]]
                       .dropna()
                       .groupby(PLAYER)
                       .median())
    board['Median 29 Trans'] = median_29_trans

    # best game column
    high_score_rows = (df.sort_values(FINAL_SCORE, ascending=False)
                       .groupby(PLAYER)
                       .nth(0))
    board['Their Best Game'] = (high_score_rows[
            high_score_rows.index.isin(board.index)]
            .apply(lambda row : 'Watch: {}'.format(row[GAME_LINK]), axis=1))

    print(board)

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    print_table()

# first goal: replicate the highest median score leaderboard
# fields: players, median score, # games, median 19 trans, median 29 trans, best game

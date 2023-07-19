# hack to make the script runnable from this file's parent directory
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import pandas as pd

from nmst.load import load_as_df
from nmst.headers import *

def print_19_trans():
    # load complete database
    df = load_as_df()
    transitions = df[SCORE_AT_19]
    transitions = transitions[transitions != 'unknown'].dropna().astype('int32')
    bounds = [0] + [1000*(200+25*i) for i in range(11)] + [1000000]
    # convert counts to proportions
    trans_groups = pd.cut(transitions, bounds, right=False)
    trans_df = trans_groups.value_counts().sort_index(ascending=False).to_frame()
    trans_df.index.rename('Ranges', inplace=True)
    trans_df['Props'] = (trans_df[SCORE_AT_19] / trans_df[SCORE_AT_19].sum())
    print(trans_df)

def print_29_trans():
    # load complete database
    df = load_as_df()
    transitions = df[SCORE_AT_29]
    transitions = transitions[transitions != 'unknown'].dropna().astype('int32')
    bounds = [0] + [1000*(600+50*i) for i in range(15)] + [1500000]
    # convert counts to proportions
    trans_groups = pd.cut(transitions, bounds, right=False)
    trans_df = trans_groups.value_counts().sort_index(ascending=False).to_frame()
    trans_df.index.rename('Ranges', inplace=True)
    trans_df['Props'] = (trans_df[SCORE_AT_29] / trans_df[SCORE_AT_29].sum())
    print(trans_df)

if __name__ == '__main__':
    print_19_trans()
    print()
    print_29_trans()

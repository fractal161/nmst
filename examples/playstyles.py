# hack to make the script runnable from this file's parent directory
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from nmst.load import load_as_df
from nmst.headers import *

def print_table():
    # load complete database
    df = load_as_df(exclude_faster=False)
    # get counts for each playstyle
    style_counts = df[STYLE].value_counts()
    # convert counts to proportions
    style_props = (style_counts / style_counts.sum())
    print(style_props)

if __name__ == '__main__':
    print_table()

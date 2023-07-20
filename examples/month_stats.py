# hack to make the script runnable from this file's parent directory
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pandas as pd
import webview

from nmst.load import load_as_df
from nmst.headers import *

def print_table():
    df = load_as_df()

    # group object used for all of the stats
    event_group = df.groupby(EVENT)

    # get correct index of group by sorting by earliest match id
    event_index = (event_group.nth(0)
                   .sort_values(MATCH_ID)
                   .index)

    # dataframe that will show the complete table
    event_stats = pd.DataFrame(index=event_index)

    # total games
    event_stats['Total Games'] = event_group[EVENT].count()

    # num. transitions
    event_stats['Transitions'] = event_group[SCORE_AT_19].count()

    # num. killscreens
    event_stats['Killscreens'] = event_group[SCORE_AT_29].count()

    # transition %
    event_stats['Transition %'] = event_stats['Transitions'] / event_stats['Total Games']

    # killscreen %
    event_stats['Killscreen %'] = event_stats['Killscreens'] / event_stats['Total Games']

    # cap type
    event_stats['Cap'] = event_group.nth(0)[CAP_TYPE]

    # num sps games
    event_stats['SPS Games'] = (df[df[IS_SPS_MATCH] == 'Yes']
                                .groupby(EVENT)[IS_SPS_MATCH]
                                .count())

    # sps %
    event_stats['SPS %'] = event_stats['SPS Games'] / event_stats['Total Games']

    # median lines
    lines_group = (df[df[TOTAL_LINES] != 'unknown']
                   .astype({TOTAL_LINES: 'int32'})
                   .groupby(EVENT))
    event_stats['Median Lines'] = lines_group[TOTAL_LINES].median()

    # average lines
    event_stats['Avg. Lines'] = lines_group[TOTAL_LINES].mean()

    # average winning lines
    all_known_lines = df[df[TOTAL_LINES] != 'unknown']
    winning_lines_group = (all_known_lines[all_known_lines[IS_VICTOR] == 'Yes']
                           .astype({TOTAL_LINES: 'int32'})
                           .groupby(EVENT))
    event_stats['Avg. Winning Lines'] = winning_lines_group[TOTAL_LINES].mean()

    # average losing lines
    losing_lines_group = (all_known_lines[all_known_lines[IS_VICTOR] == 'No']
                           .astype({TOTAL_LINES: 'int32'})
                           .groupby(EVENT))
    event_stats['Avg. Losing Lines'] = losing_lines_group[TOTAL_LINES].mean()

    # median score
    score_group = (df[df[FINAL_SCORE] != 'unknown']
                   .astype({FINAL_SCORE: 'int32'})
                   .groupby(EVENT))
    event_stats['Median Score'] = score_group[FINAL_SCORE].median()

    # average score
    event_stats['Avg. Score'] = score_group[FINAL_SCORE].mean()

    # average winning score
    all_known_scores = df[df[FINAL_SCORE] != 'unknown']
    winning_score_group = (all_known_scores[all_known_scores[IS_VICTOR] == 'Yes']
                           .astype({FINAL_SCORE: 'int32'})
                           .groupby(EVENT))
    event_stats['Avg. Winning Score'] = winning_score_group[FINAL_SCORE].mean()

    # average losing score
    losing_score_group = (all_known_scores[all_known_scores[IS_VICTOR] == 'No']
                           .astype({FINAL_SCORE: 'int32'})
                           .groupby(EVENT))
    event_stats['Avg. Losing Score'] = losing_score_group[FINAL_SCORE].mean()

    # median 19 trans
    event_stats['Median 19 Trans.'] = (df[df[SCORE_AT_19] != 'unknown']
                                       [[EVENT, SCORE_AT_19]].dropna()
                                       .astype({SCORE_AT_19: 'int32'})
                                       .groupby(EVENT)[SCORE_AT_19]
                                       .median())

    # median 29 trans
    event_stats['Median 29 Trans.'] = (df[df[SCORE_AT_29] != 'unknown']
                                       [[EVENT, SCORE_AT_29]].dropna()
                                       .astype({SCORE_AT_29: 'int32'})
                                       .groupby(EVENT)[SCORE_AT_29]
                                       .median())

    # median lines in ks
    event_stats['Median KS Lines'] = (df[df[LINES_IN_29] != 'unknown']
                                       [[EVENT, LINES_IN_29]].dropna()
                                       .astype({LINES_IN_29: 'int32'})
                                       .groupby(EVENT)[LINES_IN_29]
                                       .median())

    # median score in ks
    event_stats['Median KS Score'] = (df[df[SCORE_IN_29] != 'unknown']
                                       [[EVENT, SCORE_IN_29]].dropna()
                                       .astype({SCORE_IN_29: 'int32'})
                                       .groupby(EVENT)[SCORE_IN_29]
                                       .median())

    # num. natural topouts
    event_stats['Topouts (N)'] = (df[df[TOPOUT_TYPE] == 'Natural']
                                  [[EVENT, TOPOUT_TYPE]].dropna()
                                  .groupby(EVENT).count())

    # num. intentional topouts
    event_stats['Topouts (I)'] = (df[df[TOPOUT_TYPE] == 'Intentional']
                                  [[EVENT, TOPOUT_TYPE]].dropna()
                                  .groupby(EVENT).count())

    # num. aggressive topouts
    event_stats['Topouts (A)'] = (df[df[TOPOUT_TYPE] == 'Aggressive']
                                  [[EVENT, TOPOUT_TYPE]].dropna()
                                  .groupby(EVENT).count())

    # playstyle proportions
    for style in ['DAS', 'Tap', 'Roll']:
        event_stats[f'{style} Games'] = (df[df[STYLE] == style]
                                    [[EVENT, STYLE]].dropna()
                                    .groupby(EVENT).count())
        event_stats[f'{style} %'] = (event_stats[f'{style} Games']
                                / event_stats['Total Games'])

    # total mullen lines (compute all lines - mullen lines)
    total_lines = (df[df[NO_MULLEN_LINES] != 'unknown']
                   [[EVENT, TOTAL_LINES, NO_MULLEN_LINES]]
                   .dropna()
                   .astype({TOTAL_LINES: 'int32'})
                   .groupby(EVENT)[TOTAL_LINES]
                   .sum())
    no_mullen_lines = (df[df[NO_MULLEN_LINES] != 'unknown']
                       [[EVENT, NO_MULLEN_LINES]]
                       .dropna()
                       .astype({NO_MULLEN_LINES: 'int32'})
                       .groupby(EVENT)[NO_MULLEN_LINES]
                       .sum())
    event_stats['Total Mullen Lines'] = total_lines - no_mullen_lines

    # total mullen score
    total_lines = (df[df[NO_MULLEN_SCORE] != 'unknown']
                   [[EVENT, FINAL_SCORE, NO_MULLEN_LINES]]
                   .dropna()
                   .astype({FINAL_SCORE: 'int32'})
                   .groupby(EVENT)[FINAL_SCORE]
                   .sum())
    no_mullen_lines = (df[df[NO_MULLEN_SCORE] != 'unknown']
                       [[EVENT, NO_MULLEN_SCORE]]
                       .dropna()
                       .astype({NO_MULLEN_SCORE: 'int32'})
                       .groupby(EVENT)[NO_MULLEN_SCORE]
                       .sum())
    event_stats['Total Mullen Score'] = total_lines - no_mullen_lines


    # bad hack to make the table scrollable
    stats_html = event_stats.to_html()
    stats_html = ('<div style="overflow-x:auto;">' + 
                  stats_html +
                  '</div>')
    webview.create_window('table', html=stats_html, text_select=True)
    webview.start()

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    print_table()


# Import libs
import pandas as pd
import numpy as np
import logging

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


def squash(df, output_cols, squash_frequency):

    # Groups the Date by a frequency so orders 1 second apart are joined together for example
    # Frequencies: Y=year, M=month, W=week, D=day, H=hour, T=minute, S=second, L=millisecond
    date_group_key = pd.Grouper(key='Date', freq=squash_frequency)

    df_grouped = df.groupby(
        ['Exchange',
         'Function',
         date_group_key,
         'Market',
         'Type']
    )

    # PEP recommendation replacement of lambda
    # weighted_mean_amount = lambda x: np.average(x, weights=df.loc[x.index, 'Amount'])
    def weighted_mean_amount(x):
        return np.average(x, weights=df.loc[x.index, 'Amount'])

    # Aggregating applies a function to the column in the grouped set - like a partition
    df_aggregated = df_grouped.agg(
        NumOrders=('Price', 'count'),
        Price=('Price', weighted_mean_amount),
        Amount=('Amount', 'sum'),
        Total=('Total', 'sum'),
        Fee=('Fee', 'sum'),
        FeeCoin=('FeeCoin', 'first')
    )

    # reset_index() includes the groupby columns in our dataset
    df_sorted = df_aggregated.reset_index().sort_values(by='Date', ascending=False)

    # Converts datetime to date, use if Date column is grouped by days or more
    if squash_frequency[-1] in ('Y', 'M', 'W', 'D'):
        df_sorted['Date'] = pd.to_datetime(df_sorted['Date']).dt.date

    functions.assertion_columns('Squash output', output_cols, df_sorted.columns)

    return df_sorted


def main(
    input_file,
    output_file,
    input_cols,
    output_cols,
    squash_frequency
):
    log_debug.info(f'{input_file = }')
    df = pd.read_excel(input_file)

    functions.assertion_columns('Squash input', input_cols, df.columns)

    squashed = squash(df, output_cols, squash_frequency)

    log_debug.info(f'{output_file = }')
    squashed.to_excel(output_file, index=False)

    return

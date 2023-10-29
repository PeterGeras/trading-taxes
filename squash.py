# Import libs
import pandas as pd
import numpy as np
import logging

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


def squash(df, squash_frequency):

    # Groups the Date by a frequency so orders 1 second apart are joined together for example
    # Frequencies: Y=year, M=month, W=week, D=day, H=hour, T=minute, S=second, L=millisecond
    date_group_key = pd.Grouper(key='Date', freq=squash_frequency)

    df_grouped = df.groupby(
        ['Exchange',
         'Function',
         date_group_key,
         'Market',
         'CoinTo',
         'CoinFrom',
         'AddressFrom',
         'AddressTo',
         'TxId',
         'Type',
         'Fee_Coin'],
        dropna=False
    )

    # PEP recommendation replacement of lambda
    # weighted_mean_amount = lambda x: np.average(x, weights=df.loc[x.index, 'Amount'])
    def weighted_mean_amount(x):
        return np.average(x, weights=df.loc[x.index, 'Amount_CoinTo'])

    # Aggregating applies a function to the column in the grouped set - like a partition
    df_aggregated = df_grouped.agg(
        NumOrders=('Ratio_CoinFromTo', 'count'),
        Ratio_CoinFromTo=('Ratio_CoinFromTo', weighted_mean_amount),
        Amount_CoinTo=('Amount_CoinTo', 'sum'),
        Amount_CoinFrom=('Amount_CoinFrom', 'sum'),
        Fee=('Fee', 'sum')
    )

    # reset_index() includes the groupby columns in our dataset
    df_sorted = df_aggregated.reset_index().sort_values(by='Date', ascending=False)

    # Converts datetime to date, use if Date column is grouped by days or more
    if squash_frequency[-1] in ('Y', 'M', 'W', 'D'):
        df_sorted['Date'] = pd.to_datetime(df_sorted['Date']).dt.date

    return df_sorted


def main(file_dict, excel_cols, squash_frequency):
    input_file = file_dict['merge_exchanges_total_output']
    input_cols = excel_cols['merge']

    log_debug.info(f'{input_file = }')
    df = pd.read_excel(input_file)

    functions.assertion_columns('Squash input', input_cols, df.columns)

    df = squash(df, squash_frequency)

    # Set columns
    output_cols = excel_cols['squash']
    df = df[output_cols]

    output_file = file_dict['squash']
    log_debug.info(f'{output_file = }')
    df.to_excel(output_file, index=False)

    return

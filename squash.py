# Import libs
import pandas as pd
import numpy as np
import logging

# Loggers
log_debug = logging.getLogger('log_debug')


def squash(df):

    # Groups the Date by a frequency so orders 1 second apart are joined together
    date_group_key = pd.Grouper(key='Date', freq='1H')

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

    # # Converts datetime to date, use if Date column is grouped by days or more
    # df_sorted['Date'] = pd.to_datetime(df_sorted['Date']).dt.date

    return df_sorted


def main(file_dict, excel_cols):
    input_file = file_dict['binance']['total']['output']
    log_debug.info(f'{input_file = }')

    df = pd.read_excel(input_file)

    squashed = squash(df)

    output_file = file_dict['binance']['squash']
    squashed.to_excel(output_file, index=False)

    return

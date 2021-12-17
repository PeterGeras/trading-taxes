import os
import pandas as pd
import numpy as np
import logging

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


class Tax(object):
    def __init__(self, ):
        pass


def sort_setup(df):
    df.sort_values(
        by=['Date', 'Market', 'Type'],
        ascending=[True, True, True],
        inplace=True
    )

    return


def main(file_dict, excel_cols):
    input_file = file_dict['coin']
    input_cols = excel_cols['coin']

    log_debug.info(f'{input_file = }')
    df = pd.read_excel(input_file)

    functions.assertion_columns('CGT input', input_cols, df.columns)

    # Sort data in required order
    sort_setup(df)

    # CGT calculation

    # Drop NaN's that could have been caught
    df.dropna(how='all')

    # Set columns
    output_cols = excel_cols['cgt']
    df = df[output_cols]

    output_file = file_dict['cgt']
    log_debug.info(f'{output_file = }')
    df.to_excel(output_file, index=False)

    return

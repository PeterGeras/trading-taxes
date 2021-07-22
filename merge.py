import os
import pandas as pd
import numpy as np
import glob
import logging

# Python
import merge_binance

# Loggers
log_debug = logging.getLogger('log_debug')

# Global
_file_dict = {}
_excel_cols = {}


def get_output_files():
    files = []

    for exchange, exchange_dict in _file_dict['merge_exchange'].items():
        for function, file_in_out in exchange_dict.items():
            f = file_in_out['output']
            files.append(f)

    return files


def delete_output_files():
    files = get_output_files()

    for f in files:
        os.remove(f)

    return


def setup(exchange, function):
    all_data = pd.DataFrame()
    files = glob.glob(_file_dict[exchange][function]['input'])  # Glob handles * wildcard in input file(s)

    for f in files:
        df = pd.read_excel(f)
        all_data.append(df, ignore_index=True)

    return all_data


def tidy(data):

    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], inplace=True, ascending=False)

    data = data[_excel_cols['files']]

    return data


def export(data, exchange, function):

    log_debug.info(f'\nEXPORT - {exchange} - {function}\n\n{data.head()}')

    data.to_excel(_file_dict[exchange][function]['output'], index=False)

    return


def merge_exchanges():
    all_data = pd.DataFrame()
    files = get_output_files()

    for f in files:
        df = pd.read_excel(f)
        all_data.append(df, ignore_index=True)

    all_data.to_excel(_file_dict['merge_exchanges'], index=False)

    return


# TODO:
#   Apply a more appropriate pattern for merge.py and merge_binance.py connection
def main(file_dict, excel_cols):
    global _file_dict, _excel_cols
    _file_dict, _excel_cols = file_dict, excel_cols

    # Clean files that would've been output from a previous run and will cause conflict
    delete_output_files()

    merge_binance.trade()
    merge_binance.deposit()
    merge_binance.withdraw()
    merge_binance.total()

    # Once total files are set up for every exchange, merge those
    merge_exchanges()

    return

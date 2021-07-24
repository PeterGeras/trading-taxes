import os
import pandas as pd
import glob
import logging

# Python files
import merge_binance

# Loggers
log_debug = logging.getLogger('log_debug')

# Global
_file_dict = {}
_excel_dict = {}


# Captures all output files that were generated from previous runs that would conflict
def __get_output_files():
    files = []

    for exchange, exchange_dict in _file_dict['merge_exchange'].items():
        for function, file_in_out in exchange_dict.items():
            f = file_in_out['output']
            files.append(f)

    files.append(_file_dict['merge_exchanges_total_output'])

    return files


# Only includes the exchange total output files
def __get_total_output_files():
    files = []

    for exchange, exchange_dict in _file_dict['merge_exchange'].items():
        f = exchange_dict['total']['output']
        files.append(f)

    return files


def __delete_output_files():
    files = __get_output_files()

    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass

    return


def setup(exchange, function):
    df_total = pd.DataFrame()

    # Glob handles * wildcard in input file(s)
    files = glob.glob(_file_dict['merge_exchange'][exchange][function]['input'])

    for f in files:
        df = pd.read_excel(f)
        # Pandas append does not work inplace so needs to be assigned back to itself
        df_total = df_total.append(df, ignore_index=True)

    return df_total


def tidy(data):

    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], inplace=True, ascending=False)

    data = data[_excel_dict['output']['files']]

    return data


def export(data, exchange, function):

    log_debug.info(f'Exporting... {exchange=} - {function=} - rows={len(data.index)}')

    data.to_excel(_file_dict['merge_exchange'][exchange][function]['output'], index=False)

    return


def merge_exchanges():
    df_total = pd.DataFrame()
    files = __get_total_output_files()

    for f in files:
        df = pd.read_excel(f)
        # Pandas append does not work inplace so needs to be assigned back to itself
        df_total = df_total.append(df, ignore_index=True)

    output_file = _file_dict['merge_exchanges_total_output']
    df_total.to_excel(output_file, index=False)
    log_debug.info(f'{output_file = }')



    return


# TODO:
#   Apply a more appropriate pattern for merge.py and merge_binance.py connection
def main(file_dict, excel_dict):
    global _file_dict, _excel_dict
    _file_dict, _excel_dict = file_dict, excel_dict

    # Clean files that would've been output from a previous run and will cause conflict
    __delete_output_files()

    cols = _excel_dict['exchange']['binance']
    merge_binance.trade(cols['trade'])
    merge_binance.deposit(cols['deposit'])
    merge_binance.withdraw(cols['withdraw'])
    merge_binance.total()

    # Once total files are set up for every exchange, merge those
    merge_exchanges()

    return

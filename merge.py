import os
import pandas as pd
import glob
import logging
import warnings

# Python files
import merge_binance
import functions

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


# Captures warning when reading excel file
# UserWarning: Workbook contains no default style, apply openpyxl's default
# warn("Workbook contains no default style, apply openpyxl's default")
def read_excel_warnings(file):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(file, engine="openpyxl")

    return df


def setup(exchange, function):
    df_total = pd.DataFrame()

    # Glob handles * wildcard in input file(s)
    files = glob.glob(_file_dict['merge_exchange'][exchange][function]['input'])

    for f in files:
        df = read_excel_warnings(f)
        # Pandas append does not work inplace so needs to be assigned back to itself
        df_total = df_total.append(df, ignore_index=True)

    return df_total


def tidy(data):

    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], inplace=True, ascending=False)

    data = data[_excel_dict['output']['merge']]

    return data


def export(data, exchange, function):
    details = f'{exchange=} - {function=} - rows={len(data.index)}'

    # Check columns are correct
    functions.assertion_columns(
        name=details,
        expected_cols=_excel_dict['output']['merge'],
        received_cols=data.columns
    )

    log_debug.info(details)
    data.to_excel(_file_dict['merge_exchange'][exchange][function]['output'], index=False)

    return


def merge_exchanges():
    df_total = pd.DataFrame()
    files = __get_total_output_files()

    for f in files:
        df = pd.read_excel(f)
        # Pandas append does not work inplace so needs to be assigned back to itself
        df_total = df_total.append(df, ignore_index=True)

    # Set columns
    output_cols = _excel_dict['output']['merge']
    df = df_total[output_cols]

    output_file = _file_dict['merge_exchanges_total_output']
    log_debug.info(f'{output_file = }')
    df.to_excel(output_file, index=False)

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

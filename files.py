import pandas as pd
import numpy as np
import glob

# Python
import files_binance

# Global
_file_dict = {}
_excel_cols = {}


def setup(exchange, function):
    all_data = pd.DataFrame()
    files = glob.glob(_file_dict[exchange][function]['input'])

    for f in files:
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True)

    return all_data


def tidy(data):

    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Date'], inplace=True, ascending=False)

    data = data[_excel_cols['results']]

    return data


def export(data, exchange, function):

    print(f'\n{exchange} - {function}\n\n{data.head()}')

    data.to_excel(_file_dict[exchange][function]['output'], index=False)

    return


def main(file_dict, excel_cols):
    global _file_dict, _excel_cols
    _file_dict, _excel_cols = file_dict, excel_cols

    files_binance.trade()
    files_binance.deposit()
    files_binance.withdraw()
    files_binance.total()

    return

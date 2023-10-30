import os
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


def duplicate_id_row(df, id_row):
    # Find the index of the row
    index_to_duplicate = df[df['Id'] == id_row].index[0]

    # Split the dataframe at the desired index
    df1 = df.iloc[:index_to_duplicate+1]  # Up to and including n
    df2 = df.iloc[index_to_duplicate:]  # From n to the end

    df = pd.concat([df1, df2], ignore_index=True)

    return df


def calculate_cgt(buy_rows, sell_row):
    """
    Calculate the capital gains tax (CGT) using simplified Australian CGT rules, including fees,
    split into standard and discount taxable gains.

    :param buy_rows: A DataFrame containing buy transaction details.
    :param sell_row: A DataFrame row containing sell transaction details.
    :return: tuple of (taxable_gain_standard, taxable_gain_discount, buy_ids_str).
    """

    taxable_gain_standard = 0
    taxable_gain_discount = 0
    buy_ids = []

    units_to_be_sold = sell_row['Amount_CoinFrom']
    units_sold_per_buy = {}

    for _, buy_row in buy_rows.iterrows():

        if units_to_be_sold <= 0:
            break

        buy_ids.append(buy_row['Id'])
        # Calculate units from this buy transaction that will be sold
        sale_fee = sell_row['Fee'] if sell_row['Fee_Coin'] == sell_row['CoinFrom'] else 0
        units_from_this_buy = min(units_to_be_sold + sale_fee, buy_row['CoinTo_Remaining'] - buy_row['Fee'])

        cost_base = (buy_row['Total_AUD'] + buy_row['Fee_AUD']) * (units_from_this_buy / buy_row['Amount_CoinTo'])
        proceeds = (sell_row['Total_AUD'] - sell_row['Fee_AUD']) * (units_from_this_buy / sell_row['Amount_CoinFrom'])
        gain = proceeds - cost_base

        holding_period = (sell_row['Date'] - buy_row['Date']).days
        if holding_period < 365 or gain < 0:
            taxable_gain_standard += gain
        else:
            taxable_gain_discount += gain/2

        units_to_be_sold -= units_from_this_buy

        # Update CoinTo_Remaining for the buy_rows outside of this function
        units_sold_per_buy[buy_row['Id']] = units_from_this_buy

    buy_ids_str = ','.join(str(x) for x in buy_ids)

    return taxable_gain_standard, taxable_gain_discount, buy_ids_str, units_sold_per_buy


def cgt_setup(df):

    for i, row in df.iterrows():
        if row['Type'] == 'Sell':
            previous_buys = df[(df['Type'] == 'Buy') &
                               (df['CoinTo'] == row['CoinFrom']) &
                               (df['Date'] <= row['Date']) &
                               (df['CoinTo_Remaining'] > 0)]
            gain_standard, gain_discount, buy_ids, units_sold_info = calculate_cgt(previous_buys, row)
            df.loc[i, 'TaxableGain_Standard'] = round(gain_standard, 2)
            df.loc[i, 'TaxableGain_Discounted'] = round(gain_discount, 2)
            df.loc[i, 'Id_Sources'] = '-' if len(buy_ids) == 0 else buy_ids
            # Update CoinTo_Remaining
            for idx, units in units_sold_info.items():
                df.loc[df['Id'] == idx, 'CoinTo_Remaining'] -= units

    return df


def df_setup(df):
    custom_order = {'Buy': 1, 'Sell': 2, 'Transfer': 3}
    df.sort_values(by=['Date', 'Type'],
                   key=lambda col: col.map(custom_order) if col.name == 'Type' else col,
                   ascending=[True, True],
                   inplace=True)
    df.insert(0, 'Id', range(2, 2+len(df)))
    df['CoinTo_Remaining'] = df['Amount_CoinTo'].where(df['Type'] == 'Buy', None)
    df.insert(0, 'Id_Sources', '')
    df.reset_index(drop=True, inplace=True)

    return df


def main(file_dict, excel_cols):
    input_file = file_dict['coin']
    input_cols = excel_cols['coin']

    log_debug.info(f'{input_file = }')
    df = pd.read_excel(input_file)

    functions.assertion_columns('CGT input', input_cols, df.columns)

    # Sort data in required order
    df = df_setup(df)

    # CGT calculation
    df = cgt_setup(df)

    # Set columns
    output_cols = excel_cols['cgt']
    df = df[output_cols]

    print(df)
    output_file = file_dict['cgt']
    log_debug.info(f'{output_file = }')
    df.to_excel(output_file, index=False)

    return

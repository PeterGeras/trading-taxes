import os
import pandas as pd
from datetime import datetime
import logging

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


def calculate_cgt(buy_rows, sell_row):
    """
    Calculate the capital gains tax (CGT) using simplified Australian CGT rules, including fees,
    split into standard and discount taxable gains.

    :param buy_rows: A DataFrame containing buy transaction details.
    :param sell_row: A DataFrame row containing sell transaction details.
    :return: tuple of (taxable_gain_standard, taxable_gain_discount).
    """
    # print(f"{type(sell_row['Date'])=}")
    # sale_date = datetime.strptime(sell_row['Date'], "%Y-%m-%d %I%p")
    sale_date = sell_row['Date']

    taxable_gain_standard = 0
    taxable_gain_discount = 0

    units_to_be_sold = sell_row['Amount_CoinFrom']

    for _, buy_row in buy_rows.iterrows():
        if units_to_be_sold <= 0:
            print(f"BROKE {'-'*10} {sell_row['Exchange']} - {sale_date} - {sell_row['Market']}")
            break

        # purchase_date = datetime.strptime(buy_row['Date'], "%Y-%m-%d %H:%M:%S")
        purchase_date = buy_row['Date']
        holding_period = (sale_date - purchase_date).days

        # Calculate units from this buy transaction that will be sold
        if sell_row['Fee_Coin'] == sell_row['CoinFrom']:
            sale_fee = sell_row['Fee']
        else:
            sale_fee = 0
        units_from_this_buy = min(units_to_be_sold + sale_fee, buy_row['Amount_CoinTo'] - buy_row['Fee'])

        cost_base = (buy_row['Total_AUD'] + buy_row['Fee_AUD']) * (units_from_this_buy / buy_row['Amount_CoinTo'])
        proceeds = (sell_row['Total_AUD'] - sell_row['Fee_AUD']) * (units_from_this_buy / sell_row['Amount_CoinFrom'])
        gain = proceeds - cost_base

        if holding_period < 365 or gain < 0:
            taxable_gain_standard += gain
        else:
            taxable_gain_discount += gain/2

        units_to_be_sold -= units_from_this_buy

    return taxable_gain_standard, taxable_gain_discount


def cgt_setup(df):
    """
    data = {
        'transaction_type': ['buy', 'buy', 'sell', 'buy', 'sell'],
        'asset': ['A', 'A', 'A', 'B', 'B'],
        'units': [10, 15, 20, 10, 10],
        'price': [1000, 1500, 2800, 1200, 1300],
        'fee': [5, 7, 10, 5, 8],
        'date': ['2020-01-01', '2020-02-01', '2023-01-02', '2021-01-01', '2023-01-02']
    }
    """

    standard_gains = []
    discount_gains = []
    for i, row in df.iterrows():
        if row['Type'] == 'Sell':
            previous_buys = df[(df['Type'] == 'Buy') &
                               (df['CoinTo'] == row['CoinFrom']) &
                               (df['Date'] <= row['Date'])]
            gain_standard, gain_discount = calculate_cgt(previous_buys, row)
            standard_gains.append(gain_standard)
            discount_gains.append(gain_discount)
        else:
            standard_gains.append(None)
            discount_gains.append(None)

    df['TaxableGain_Standard'] = standard_gains
    df['TaxableGain_Discounted'] = discount_gains
    return df


def sort_setup(df):
    custom_order = {'Sell': 1, 'Buy': 2, 'Transaction': 3}
    df.sort_values(by=['Date', 'Type'],
                   key=lambda col: col.map(custom_order) if col.name == 'Type' else col,
                   ascending=[False, True],
                   inplace=True)

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
    df = cgt_setup(df)

    # Set columns
    output_cols = excel_cols['cgt']
    df = df[output_cols]

    print(df)
    output_file = file_dict['cgt']
    log_debug.info(f'{output_file = }')
    df.to_excel(output_file, index=False)

    return

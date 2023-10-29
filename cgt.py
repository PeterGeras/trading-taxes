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
    Calculate the capital gains tax (CGT) using simplified Australian CGT rules, including fees.

    :param buy_rows: A DataFrame containing buy transaction details.
    :param sell_row: A DataFrame row containing sell transaction details.
    :return: Taxable gain.
    """

    # Assume all buy transactions are used first-in-first-out (FIFO) for simplicity.
    total_cost_base = sum(buy_rows['Total_AUD'] + buy_rows['Fee_AUD'])
    total_units_bought = sum(buy_rows['Amount'])

    avg_cost_base_per_unit = total_cost_base / total_units_bought

    # Adjusted cost base and capital proceeds for the units being sold
    units_being_sold = sell_row['Amount']
    cost_base = avg_cost_base_per_unit * units_being_sold
    capital_proceeds = sell_row['price'] - sell_row['fee']

    # Calculate the capital gain
    capital_gain = capital_proceeds - cost_base

    # Check holding period for the first buy transaction (FIFO)
    purchase_date = datetime.strptime(buy_rows.iloc[0]['date'], "%Y-%m-%d")
    sale_date = datetime.strptime(sell_row['date'], "%Y-%m-%d")
    holding_period = (sale_date - purchase_date).days

    if holding_period > 365:
        # If asset is held for more than 12 months, apply the 50% discount
        taxable_gain = capital_gain * 0.5
    else:
        taxable_gain = capital_gain

    return taxable_gain


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

    taxable_gains = []
    for i, row in df.iterrows():
        if row['Type'] == 'Sell':
            previous_buys = df[(df['Type'] == 'Buy') &
                               (df['CoinTo'] == row['CoinFrom']) &
                               (df['Date'] < row['Date'])]
            taxable_gains.append(calculate_cgt(previous_buys, row))
        else:
            taxable_gains.append(None)

    df['TaxableGain'] = taxable_gains
    return df


def sort_setup(df):
    df.sort_values(by='Date', ascending=False, inplace=True)

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

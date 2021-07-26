import os
import pandas as pd
import numpy as np
import logging
import cryptocompare
from currency_converter import CurrencyConverter

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


def get_euro_value(base, total, date):
    base_to_eur_info = cryptocompare.get_historical_price_hour(base, 'EUR', limit=1, toTs=date)
    close_price = base_to_eur_info[0]['close']

    euro_value = close_price * total
    euro_value_format = float("{:.2f}".format(euro_value))

    return euro_value_format


def get_aud_value(c, total, date):
    value = c.convert(total, 'EUR', 'AUD', date)
    value_format = float("{:.2f}".format(value))

    return value_format


def coin_name_split(coin_string):
    coins = None
    coin_length_min = 3
    coin_length_max = 4
    common_coins = {
        coin_length_min: ['BTC', 'ETH', 'BNB'],
        coin_length_max: ['TUSD', 'USDT']
    }

    if len(coin_string) <= coin_length_max:
        return [coin_string]

    for coin_length in common_coins.keys():
        if any(map(coin_string.__contains__, common_coins[coin_length])):
            if any(map(coin_string[:coin_length].__contains__, common_coins[coin_length])):
                coins = [coin_string[:coin_length], coin_string[coin_length:]]
            elif any(map(coin_string[-coin_length:].__contains__, common_coins[coin_length])):
                coins = [coin_string[:-coin_length], coin_string[-coin_length:]]
            break

    return coins


def market_split(coin_string, trade_type):
    market = {
        'CoinTo': np.nan,
        'CoinFrom': np.nan,
        'Amount_Coin': np.nan,
        'Total_Coin': np.nan
    }

    coins = coin_name_split(coin_string)

    market['Amount_Coin'] = coins[0]

    if len(coins) == 1:
        market['Total_Coin'] = coins[0]
    else:
        market['Total_Coin'] = coins[1]

    if trade_type == 'BUY':
        market['CoinTo'] = market['Amount_Coin']
        market['CoinFrom'] = market['Total_Coin']
    else:
        market['CoinTo'] = market['Total_Coin']
        market['CoinFrom'] = market['Amount_Coin']

    return market


def pairs(df):
    applied_df = df.apply(lambda row: market_split(row['Market'], row['Type']), axis='columns', result_type='expand')
    df = pd.concat([df, applied_df], axis='columns')

    return df


def fiat(df):
    c = CurrencyConverter(fallback_on_missing_rate=True)

    df['Total_EURO'] = df.apply(lambda row: get_euro_value(row['Total_Coin'], row['Total'], row['Date']), axis=1)
    df['Total_AUD'] = df.apply(lambda row: get_aud_value(c, row['Total_EURO'], row['Date']), axis=1)
    df['Fee_EURO'] = df.apply(lambda row: get_euro_value(row['Fee_Coin'], row['Fee'], row['Date']), axis=1)
    df['Fee_AUD'] = df.apply(lambda row: get_aud_value(c, row['Fee_EURO'], row['Date']), axis=1)

    return


def main(file_dict, excel_cols):
    input_file = file_dict['squash']
    input_cols = excel_cols['squash']

    log_debug.info(f'{input_file = }')
    df = pd.read_excel(input_file)

    functions.assertion_columns('Coin input', input_cols, df.columns)

    df = pairs(df)
    fiat(df)

    # Drop NaN's that could have been caught
    df.dropna(how='all')

    # Set columns
    output_cols = excel_cols['coin']
    df = df[output_cols]

    output_file = file_dict['coin']
    log_debug.info(f'{output_file = }')
    df.to_excel(output_file, index=False)

    return

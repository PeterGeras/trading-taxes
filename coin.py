import pandas as pd
import numpy as np
from datetime import datetime
import cryptocompare
from currency_converter import CurrencyConverter


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


def market_split(coin_string):
    market = {
        'base': np.nan,
        'quote': np.nan
    }

    coins = coin_name_split(coin_string)

    if len(coins) == 2:
        market['base'] = coins[1]
        market['quote'] = coins[0]

    return market


def new_cols(df):
    df.insert(loc=4, column='Quote',
              value=df.apply(lambda row: market_split(row['Market'])['quote'], axis=1),
              allow_duplicates=True)

    df.insert(loc=8, column='Base',
              value=df.apply(lambda row: market_split(row['Market'])['base'], axis=1),
              allow_duplicates=True)

    df.insert(loc=10, column='Total_EURO',
              value=df.apply(lambda row: get_euro_value(row['Base'], row['Total'], row['Date']), axis=1),
              allow_duplicates=True)

    df.insert(loc=13, column='Fee_EURO',
              value=df.apply(lambda row: get_euro_value(row['FeeCoin'], row['Fee'], row['Date']), axis=1),
              allow_duplicates=True)

    c = CurrencyConverter(fallback_on_missing_rate=True)

    df.insert(loc=11, column='Total_AUD',
              value=df.apply(lambda row: get_aud_value(c, row['Total_EURO'], row['Date']), axis=1),
              allow_duplicates=True)

    df.insert(loc=15, column='Fee_AUD',
              value=df.apply(lambda row: get_aud_value(c, row['Fee_EURO'], row['Date']), axis=1),
              allow_duplicates=True)

    return


def main(input_file, output_file, excel_cols):
    df = pd.read_excel(input_file)

    new_cols(df)

    # Drop NaN's that could have been caught
    df = df.dropna()
    df.to_excel(output_file, index=False)

    return

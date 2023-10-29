import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging
import cryptocompare
from currency_converter import CurrencyConverter

# Python files
import functions

# Loggers
log_debug = logging.getLogger('log_debug')
log_error = logging.getLogger('log_error')

# Coin change
ticker_change = {
    'GNT': 'GLM'
}


def find_closest_valid_price(base, date, days_range):
    days_range_max = 2000

    # Single call check
    base_to_eur_daily_single = cryptocompare.get_historical_price_day(base, currency='EUR', limit=1, toTs=date)
    price = base_to_eur_daily_single[0]['close']
    if price > 0:
        log_error.info(f'Succeeded to find price for {base} @ {price} on {date}')
        return price

    # Range call
    days_range_mid = int((days_range-1)/2)
    d = timedelta(days=days_range_mid)
    base_to_eur_daily = cryptocompare.get_historical_price_day(base, currency='EUR', limit=days_range, toTs=date+d)
    log_debug.debug(f'{10*"#"} {base_to_eur_daily = }')

    # Find when first zero close price found
    for index, dict_day in enumerate(base_to_eur_daily):
        if dict_day['close'] == 0:
            first_close_zero = index
            break
    else:
        this_date = datetime.fromtimestamp(base_to_eur_daily[days_range_mid]['time'])
        log_error.info(f'Succeeded to find replacement price for {base} @ {price} on {this_date}')
        return base_to_eur_daily[days_range_mid]['close']

    # Find when last zero close price found
    last_close_zero = 0
    for index, dict_day in enumerate(base_to_eur_daily[first_close_zero:], start=first_close_zero):
        if dict_day['close'] > 0:
            last_close_zero = index-1
            break
    else:
        last_close_zero = days_range

    # Check entire range is zeroes
    if first_close_zero == 0 and last_close_zero == days_range:
        if days_range < days_range_max:
            log_error.warning(
                (f'Failed to find price in a {days_range} day range, '
                 f'attempting to find price in {days_range_max} days...')
            )
            # Single recursion to test max range days_range
            return find_closest_valid_price(base, date, days_range_max)
        else:
            log_error.error(
                (f'Failed to find price in a {days_range} day range, '
                 f'setting price for {base} @ 0 on {date}')
            )
            return 0

    # Find when last zero close price found
    # Math: last_close_zero - days_range_mid < days_range_mid - first_close_zero
    if first_close_zero + last_close_zero > days_range_mid + 1:
        # Earlier date found sooner than later date
        dict_day = base_to_eur_daily[first_close_zero-1]
        price = dict_day['close']
        this_date = datetime.fromtimestamp(dict_day['time'])
    else:
        dict_day = base_to_eur_daily[last_close_zero+1]
        price = dict_day['close']
        this_date = datetime.fromtimestamp(dict_day['time'])

    log_error.info(f'Succeeded to find replacement price for {base} @ {price} on {this_date}')

    return price


def get_euro_value(base, total, date):

    if total == 0:
        return float("{:.2f}".format(0))

    # Switch coin ticker to new ticker
    if base in ticker_change:
        base = ticker_change[base]

    base_to_eur_info = cryptocompare.get_historical_price_hour(base, 'EUR', limit=1, toTs=date)

    if base_to_eur_info is None:
        log_error.warning(f'Failed to find price for {base}')
        return None

    try:
        base_to_eur_info[0]['close']
    except:
        pass
    close_price = base_to_eur_info[0]['close']
    if close_price == 0:
        limit_days = 100
        log_error.warning(
            (f'Failed to find price for {base} on {date}, '
             f'attempting to find price in {limit_days} days...')
        )
        close_price = find_closest_valid_price(base, date, limit_days)

    euro_value = close_price * total
    euro_value_format = float("{:.2f}".format(euro_value))

    return euro_value_format


def get_aud_value(c, total, date):
    if total is None:
        return None
    value = c.convert(total, 'EUR', 'AUD', date)
    value_format = float("{:.2f}".format(value))

    return value_format


def fiat(df):
    c = CurrencyConverter(fallback_on_missing_rate=True)

    df['Total_EURO'] = df.apply(lambda row: get_euro_value(row['CoinFrom'], row['Amount_CoinFrom'], row['Date']), axis=1)
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

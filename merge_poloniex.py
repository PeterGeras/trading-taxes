import logging

# Python files
import merge
import functions

# Loggers
log_debug = logging.getLogger('log_debug')

# module
_date_format = '%d/%m/%Y %H:%M'


# __Private method convention (not strict)

def __setup_trade(data):

    data.insert(loc=0, column='AddressTo', value='-', allow_duplicates=True)
    data.insert(loc=0, column='AddressFrom', value='-', allow_duplicates=True)
    data.insert(loc=0, column='TxId', value='-', allow_duplicates=True)

    data.rename(columns={'Price': 'Ratio_CoinFromTo'}, inplace=True)
    data.rename(columns={'Amount': 'Amount_CoinTo'}, inplace=True)
    data.rename(columns={'Total': 'Amount_CoinFrom'}, inplace=True)
    
    def get_market_coins(row):
        split = row['Market'].split('-')
        amount_coin = [row['Amount_CoinTo'], row['Amount_CoinFrom']]
        price_ratio = row['Ratio_CoinFromTo']

        if row['Type'].casefold() == 'sell':  # Swap order
            split[0], split[1] = split[1], split[0]
            amount_coin[0], amount_coin[1] = amount_coin[1], amount_coin[0]
            price_ratio = 1/price_ratio

        return split[0], split[1], amount_coin[0], amount_coin[1], price_ratio

    data['Market'] = data['Market'].str.replace('/', '-')

    data[['CoinTo', 'CoinFrom',
          'Amount_CoinTo', 'Amount_CoinFrom',
          'Ratio_CoinFromTo'
          ]] = data.apply(get_market_coins, axis=1, result_type='expand')

    data.drop(
        [
            'Fee',
            'Order Number',
            'Base Total Less Fee',
            'Quote Total Less Fee'
        ],
        axis=1,
        inplace=True
    )

    data.rename(
        columns={
            'Fee Total': 'Fee',
            'Fee Currency': 'Fee_Coin'
        }, inplace=True
    )

    return


def __setup_deposit(data):

    data.rename(
        columns={
            'Currency': 'Market',
            'Address': 'AddressTo',
            'Amount': 'Amount_CoinTo',
        },
        inplace=True
    )

    data.insert(loc=0, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=0, column='CoinTo', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value='-', allow_duplicates=True)
    data.insert(loc=0, column='AddressFrom', value='', allow_duplicates=True)
    data.insert(loc=0, column='TxId', value='', allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Buy', allow_duplicates=True)
    data.insert(loc=0, column='Ratio_CoinFromTo', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Amount_CoinFrom', value=data['Amount_CoinTo']*data['Ratio_CoinFromTo'], allow_duplicates=True)
    data.insert(loc=0, column='Fee', value=0, allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.drop(['Status'], axis=1, inplace=True)

    return


def __setup_withdraw(data):

    data.rename(
        columns={
            'Currency': 'Market',
            'Amount': 'Amount_CoinFrom',
            'Fee Deducted': 'Fee',
            'Address': 'AddressTo',
            'Status': 'TxId'
        },
        inplace=True
    )

    data['TxId'] = data['TxId'].map(lambda x: x.lstrip('COMPLETE: '))

    data.insert(loc=0, column='Function', value='Withdraw', allow_duplicates=True)
    data.insert(loc=0, column='CoinTo', value='-', allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='AddressFrom', value='', allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Sell', allow_duplicates=True)
    data.insert(loc=0, column='Ratio_CoinFromTo', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Amount_CoinTo', value=data['Amount_CoinFrom'], allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.drop(['Amount - Fee'], axis=1, inplace=True)

    return


def __setup(data):

    data.insert(loc=0, column='Exchange', value='Poloniex', allow_duplicates=True)

    data['Type'] = data['Type'].str.title()

    return


def trade(expected_cols):
    exchange = 'poloniex'
    function = 'trade'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Poloniex trade', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Function', value='Trade', allow_duplicates=True)
    __setup_trade(data)
    __setup(data)

    data = merge.tidy(data, _date_format)
    merge.export(data, exchange, function)

    return


def deposit(expected_cols):
    exchange = 'poloniex'
    function = 'deposit'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Poloniex deposit', expected_cols, data.columns)

    # Change columns
    __setup_deposit(data)
    __setup(data)

    data = merge.tidy(data, _date_format)
    merge.export(data, exchange, function)

    return


def withdraw(expected_cols):
    exchange = 'poloniex'
    function = 'withdraw'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Poloniex withdraw', expected_cols, data.columns)

    # Change columns
    __setup_withdraw(data)
    __setup(data)

    data = merge.tidy(data, _date_format)
    merge.export(data, exchange, function)

    return


def total():
    exchange = 'poloniex'
    function = 'total'

    data = merge.setup(exchange, function)
    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return

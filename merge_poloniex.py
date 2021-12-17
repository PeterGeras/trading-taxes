import logging

# Python files
import merge
import functions

# Loggers
log_debug = logging.getLogger('log_debug')

# global
_date_format = '%d/%m/%Y %H:%M'


# __Private method convention (not strict)

def __setup_trade(data):

    def get_market_coins(row):
        split = row['Market'].split('-')
        if row['Type'].casefold() == 'sell':
            split[0], split[1] = split[1], split[0]  # Swap order
        return split

    data['Market'] = data['Market'].str.replace('/', '-')
    data['CoinTo'] = data.apply(lambda x: get_market_coins(x)[0], axis=1)
    data['CoinFrom'] = data.apply(lambda x: get_market_coins(x)[1], axis=1)

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

    data.rename(columns={'Currency': 'Market'}, inplace=True)

    data.insert(loc=0, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=0, column='CoinTo', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Buy', allow_duplicates=True)
    data.insert(loc=0, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Total', value=data['Amount']*data['Price'], allow_duplicates=True)
    data.insert(loc=0, column='Fee', value=0, allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.drop(['Address', 'Status'], axis=1, inplace=True)

    return


def __setup_withdraw(data):

    data.rename(
        columns={
            'Currency': 'Market',
            'Amount': 'Total',
            'Amount - Fee': 'Amount',
            'Fee Deducted': 'Fee'
        },
        inplace=True
    )

    data.insert(loc=0, column='Function', value='Withdraw', allow_duplicates=True)
    data.insert(loc=0, column='CoinTo', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Sell', allow_duplicates=True)
    data.insert(loc=0, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.drop(['Address', 'Status'], axis=1, inplace=True)

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

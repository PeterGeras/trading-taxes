import logging

# Python files
import merge
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


# __Private method convention (not strict)
def __setup(data):

    data.insert(loc=0, column='Exchange', value='Binance', allow_duplicates=True)

    data.rename(
        columns={
            'Date(UTC)': 'Date',
            'Fee Coin': 'Fee_Coin'
        },
        inplace=True
    )

    return


def __setup_deposit_withdraw(data):

    data.rename(columns={'Coin': 'Market'}, inplace=True)

    data.insert(loc=3, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=5, column='Total', value=data['Amount']*data['Price'], allow_duplicates=True)
    data.insert(loc=6, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.rename(columns={'TransactionFee': 'Fee'}, inplace=True)

    data.drop(['Address', 'TXID', 'SourceAddress', 'PaymentID', 'Status'], axis=1, inplace=True)

    return


def trade(expected_cols):
    exchange = 'binance'
    function = 'trade'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Binance trade', expected_cols, data.columns)

    __setup(data)

    data.insert(loc=1, column='Function', value='Trade', allow_duplicates=True)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def deposit(expected_cols):
    exchange = 'binance'
    function = 'deposit'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Binance deposit', expected_cols, data.columns)

    __setup_deposit_withdraw(data)
    __setup(data)

    data.insert(loc=1, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=2, column='Type', value='BUY', allow_duplicates=True)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def withdraw(expected_cols):
    exchange = 'binance'
    function = 'withdraw'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Binance withdraw', expected_cols, data.columns)

    __setup_deposit_withdraw(data)
    __setup(data)

    data.insert(loc=1, column='Function', value='Withdraw', allow_duplicates=True)
    data.insert(loc=2, column='Type', value='SELL', allow_duplicates=True)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def total():
    exchange = 'binance'
    function = 'total'

    data = merge.setup(exchange, function)
    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return

import logging

# Python files
import merge
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


# __Private method convention (not strict)

def __setup_trade(data):

    data.rename(columns={'Closed': 'Date'}, inplace=True)
    data.rename(columns={'Quantity': 'Amount'}, inplace=True)
    data.rename(columns={'Price': 'Total'}, inplace=True)
    data.rename(columns={'PricePerUnit': 'Price'}, inplace=True)
    data.rename(columns={'Exchange': 'Market'}, inplace=True)

    data.rename(columns={'OrderType': 'Type'}, inplace=True)
    data['Type'] = data['Type'].str.replace('LIMIT_', '')

    def get_market_coins(row):
        split = row['Market'].split('-')
        if row['Type'].casefold() == 'sell':
            split[0], split[1] = split[1], split[0]  # Swap order
        return split

    data['CoinTo'] = data.apply(lambda x: get_market_coins(x)[1], axis=1)
    data['CoinFrom'] = data.apply(lambda x: get_market_coins(x)[0], axis=1)

    data.rename(columns={'Commission': 'Fee'}, inplace=True)

    data['Fee_Coin'] = data['Market'].str.split('-').str[0]

    data.drop(['Uuid', 'TimeStamp', 'Limit', 'QuantityRemaining', 'IsConditional', 'Condition',
               'ConditionTarget', 'ImmediateOrCancel', 'TimeInForceTypeId', 'TimeInForce'], axis=1, inplace=True)

    return


def __setup_deposit_withdraw(data):

    data.rename(
        columns={
            'Symbol': 'Market',
            'Quantity': 'Amount'
        },
        inplace=True
    )

    data.insert(loc=0, column='CoinTo', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Total', value=data['Amount']*data['Price'], allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.drop(['TxId', 'Address'], axis=1, inplace=True)

    return


def __setup(data):

    data.insert(loc=0, column='Exchange', value='Bittrex', allow_duplicates=True)

    data.rename(
        columns={
            'Commission': 'Fee'
        },
        inplace=True
    )

    data['Type'] = data['Type'].str.title()

    return


def trade(expected_cols):
    exchange = 'bittrex'
    function = 'trade'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Bittrex trade', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Function', value='Trade', allow_duplicates=True)
    __setup_trade(data)
    __setup(data)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def deposit(expected_cols):
    exchange = 'bittrex'
    function = 'deposit'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Bittrex deposit', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Commission', value=0, allow_duplicates=True)
    data.insert(loc=0, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Buy', allow_duplicates=True)
    __setup_deposit_withdraw(data)
    __setup(data)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def withdraw(expected_cols):
    exchange = 'bittrex'
    function = 'withdraw'

    data = merge.setup(exchange, function)
    functions.assertion_columns('Bittrex withdraw', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Function', value='Withdraw', allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Sell', allow_duplicates=True)
    data.rename(columns={'Commission': 'Fee'}, inplace=True)
    __setup_deposit_withdraw(data)
    __setup(data)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def total():
    exchange = 'bittrex'
    function = 'total'

    data = merge.setup(exchange, function)
    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return

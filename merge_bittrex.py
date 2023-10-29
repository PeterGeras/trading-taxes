import logging

# Python files
import merge
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


# __Private method convention (not strict)

def __setup_trade(data):

    data.insert(loc=0, column='AddressTo', value='-', allow_duplicates=True)
    data.insert(loc=0, column='AddressFrom', value='-', allow_duplicates=True)
    data.insert(loc=0, column='TxId', value='-', allow_duplicates=True)

    data.rename(columns={'Closed': 'Date'}, inplace=True)
    data.rename(columns={'Quantity': 'Amount_CoinTo'}, inplace=True)
    data.rename(columns={'Price': 'Amount_CoinFrom'}, inplace=True)
    data.rename(columns={'PricePerUnit': 'Ratio_CoinFromTo'}, inplace=True)
    data.rename(columns={'Exchange': 'Market'}, inplace=True)

    data.rename(columns={'OrderType': 'Type'}, inplace=True)
    data['Type'] = data['Type'].str.replace('LIMIT_', '')

    def get_market_coins(row):
        split = row['Market'].split('-')
        amount_coin = [row['Amount_CoinTo'], row['Amount_CoinFrom']]
        price_ratio = row['Ratio_CoinFromTo']

        if row['Type'].casefold() == 'sell':  # Swap order
            split[0], split[1] = split[1], split[0]
            amount_coin[0], amount_coin[1] = amount_coin[1], amount_coin[0]
            price_ratio = 1/price_ratio

        return split[1], split[0], amount_coin[0], amount_coin[1], price_ratio

    data[['CoinTo', 'CoinFrom',
          'Amount_CoinTo', 'Amount_CoinFrom',
          'Ratio_CoinFromTo'
          ]] = data.apply(get_market_coins, axis=1, result_type='expand')

    data.rename(columns={'Commission': 'Fee'}, inplace=True)

    data['Fee_Coin'] = data['Market'].str.split('-').str[0]

    data.drop(['Uuid', 'TimeStamp', 'Limit', 'QuantityRemaining', 'IsConditional', 'Condition',
               'ConditionTarget', 'ImmediateOrCancel', 'TimeInForceTypeId', 'TimeInForce'], axis=1, inplace=True)

    return


def __setup_deposit_withdraw(data):

    data.rename(
        columns={
            'Symbol': 'Market',
            'Address': 'AddressTo',
            'Quantity': 'Amount_CoinTo',
        },
        inplace=True
    )

    data.insert(loc=0, column='AddressFrom', value='', allow_duplicates=True)
    data.insert(loc=0, column='CoinTo', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='Ratio_CoinFromTo', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Amount_CoinFrom', value=data['Amount_CoinTo']*data['Ratio_CoinFromTo'], allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

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

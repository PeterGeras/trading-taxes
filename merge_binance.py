import logging

# Python files
import merge
import functions

# Loggers
log_debug = logging.getLogger('log_debug')


# __Private method convention (not strict)

def __setup_trade(data):

    def market_split(market_old):
        common_coins = ['BTC', 'ETH', 'BNB', 'TUSD', 'USDT']

        for coin in common_coins:
            pos = len(market_old)-len(coin)
            value_end = market_old[pos:]
            if coin == value_end:
                market_new = f'{market_old[:pos]}-{market_old[pos:]}'
                break
        else:
            market_new = '-'
            log_debug.info(f'A market value of {market_old} does not end in a common coin in {common_coins}')

        return market_new

    def get_market_coins(row):
        split = row['Market'].split('-')
        if row['Type'].casefold() == 'sell':
            split[0], split[1] = split[1], split[0]  # Swap order
        return split

    data['Market'] = data['Market'].apply(market_split)
    data['CoinTo'] = data.apply(lambda x: get_market_coins(x)[0], axis=1)
    data['CoinFrom'] = data.apply(lambda x: get_market_coins(x)[1], axis=1)

    return


def __setup_deposit_withdraw(data):

    data.rename(columns={'Coin': 'Market'}, inplace=True)
    data.rename(columns={'TransactionFee': 'Fee'}, inplace=True)

    data.insert(loc=0, column='CoinTo', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='CoinFrom', value=data['Market'], allow_duplicates=True)
    data.insert(loc=0, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=0, column='Total', value=data['Amount']*data['Price'], allow_duplicates=True)
    data.insert(loc=0, column='Fee_Coin', value=data['Market'], allow_duplicates=True)

    data.drop(['Address', 'TXID', 'SourceAddress', 'PaymentID', 'Status'], axis=1, inplace=True)

    return


def __setup(data):

    data.insert(loc=0, column='Exchange', value='Binance', allow_duplicates=True)

    data.rename(
        columns={
            'Date(UTC)': 'Date',
            'Fee Coin': 'Fee_Coin'
        },
        inplace=True
    )

    data['Type'] = data['Type'].str.title()

    return


def trade(expected_cols):
    exchange = 'binance'
    function = 'trade'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Binance trade', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Function', value='Trade', allow_duplicates=True)
    __setup_trade(data)
    __setup(data)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def deposit(expected_cols):
    exchange = 'binance'
    function = 'deposit'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Binance deposit', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Buy', allow_duplicates=True)
    __setup_deposit_withdraw(data)
    __setup(data)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def withdraw(expected_cols):
    exchange = 'binance'
    function = 'withdraw'

    data = merge.setup(exchange, function)

    functions.assertion_columns('Binance withdraw', expected_cols, data.columns)

    # Change columns
    data.insert(loc=0, column='Function', value='Withdraw', allow_duplicates=True)
    data.insert(loc=0, column='Type', value='Sell', allow_duplicates=True)
    __setup_deposit_withdraw(data)
    __setup(data)

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

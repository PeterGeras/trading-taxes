# Python
import merge


# __Private method convention (not strict)
def __setup(data):

    data.insert(loc=0, column='Exchange', value='Binance', allow_duplicates=True)

    data.rename(
        columns={
            'Date(UTC)': 'Date',
            'Fee Coin': 'FeeCoin'
        },
        inplace=True
    )

    return


def __setup_deposit_withdraw(data):

    data.rename(columns={'Coin': 'Market'}, inplace=True)

    data.insert(loc=3, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=5, column='Total', value=data['Amount']*data['Price'], allow_duplicates=True)
    data.insert(loc=6, column='FeeCoin', value=data['Market'], allow_duplicates=True)

    data.rename(columns={'TransactionFee': 'Fee'}, inplace=True)

    data.drop(['Address', 'TXID', 'SourceAddress', 'PaymentID', 'Status'], axis=1, inplace=True)

    return


def trade():
    exchange = 'binance'
    function = 'trade'

    data = merge.setup(exchange, function)
    __setup(data)

    data.insert(loc=1, column='Function', value='Trade', allow_duplicates=True)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def deposit():
    exchange = 'binance'
    function = 'deposit'

    data = merge.setup(exchange, function)

    __setup_deposit_withdraw(data)
    __setup(data)

    data.insert(loc=1, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=2, column='Type', value='BUY', allow_duplicates=True)

    data = merge.tidy(data)
    merge.export(data, exchange, function)

    return


def withdraw():
    exchange = 'binance'
    function = 'withdraw'

    data = merge.setup(exchange, function)

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

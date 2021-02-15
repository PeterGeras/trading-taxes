# Python
import files


def setup(data):

    data.insert(loc=0, column='Exchange', value='Binance', allow_duplicates=True)

    data.rename(
        columns={
            'Date(UTC)': 'Date',
            'Fee Coin': 'FeeCoin'
        },
        inplace=True
    )

    return


def setup_deposit_withdraw(data):

    data.rename(columns={'Coin': 'Market'}, inplace=True)

    data.insert(loc=3, column='Price', value=1, allow_duplicates=True)
    data.insert(loc=5, column='Total', value=data['Amount']*data['Price'], allow_duplicates=True)
    data.insert(loc=6, column='FeeCoin', value=data['Market'], allow_duplicates=True)

    data.rename(columns={'TransactionFee': 'Fee'}, inplace=True)

    data.drop(['Address', 'TXID', 'SourceAddress', 'PaymentID', 'Status'], axis=1, inplace=True)

    return


def trade():
    exchange = 'Binance'
    function = 'Trade'

    data = files.setup(exchange, function)
    setup(data)

    data.insert(loc=1, column='Function', value='Trade', allow_duplicates=True)

    data = files.tidy(data)
    files.export(data, exchange, function)

    return


def deposit():
    exchange = 'Binance'
    function = 'Deposit'

    data = files.setup(exchange, function)

    setup_deposit_withdraw(data)
    setup(data)

    data.insert(loc=1, column='Function', value='Deposit', allow_duplicates=True)
    data.insert(loc=2, column='Type', value='BUY', allow_duplicates=True)

    data = files.tidy(data)
    files.export(data, exchange, function)

    return


def withdraw():
    exchange = 'Binance'
    function = 'Withdraw'

    data = files.setup(exchange, function)

    setup_deposit_withdraw(data)
    setup(data)

    data.insert(loc=1, column='Function', value='Withdraw', allow_duplicates=True)
    data.insert(loc=2, column='Type', value='SELL', allow_duplicates=True)

    data = files.tidy(data)
    files.export(data, exchange, function)

    return


def total():
    exchange = 'Binance'
    function = 'Total'

    data = files.setup(exchange, function)
    data = files.tidy(data)
    files.export(data, exchange, function)

    return

options = {
    'files': False,
    'squash': True,
    'coins': False
}

file_dict = {
    'exchange_1': {
        'deposit': {
            'input': r'files/Exchange_1/Deposit/*.xlsx',
            'output': r'files/Exchange_1/_Results-Deposit.xlsx'
        },
        'trade': {
            'input': r'files/Exchange_1/Trade/*.xlsx',
            'output': r'files/Exchange_1/_Results-Trade.xlsx'
        },
        'withdraw': {
            'input': r'files/Exchange_1/Withdraw/*.xlsx',
            'output': r'files/Exchange_1/_Results-Withdraw.xlsx'
        },
        'total': {
            'input': r'files/Exchange_1/_Results-*.xlsx',
            'output': r'files/Exchange_1/_Results.xlsx'
        },
        'coin': r'files/Exchange_1/Coin.xlsx'
    },
    'exchange_2': {
        'deposit': {
            'input': r'files/Exchange_2/Deposit/*.xlsx',
            'output': r'files/Exchange_2/_Results-Deposit.xlsx'
        },
        'trade': {
            'input': r'files/Exchange_2/Trade/*.xlsx',
            'output': r'files/Exchange_2/_Results-Trade.xlsx'
        },
        'withdraw': {
            'input': r'files/Exchange_2/Withdraw/*.xlsx',
            'output': r'files/Exchange_2/_Results-Withdraw.xlsx'
        },
        'total': {
            'input': r'files/Exchange_2/_Results-*.xlsx',
            'output': r'files/Exchange_2/_Results.xlsx'
        },
        'coin': r'files/Exchange_2/Coin.xlsx'
    },
}

excel_dict = {
    'exchange': {
        'binance': ['Date', 'Market', 'Type', 'Price', 'Amount', 'Total', 'Fee', 'Fee_Coin']
    },
    'columns': {
        'files': ['Exchange', 'Function',
                  'Date', 'Market', 'Type', 'Price', 'Amount', 'Total', 'Fee', 'Fee_Coin'],
        'squash': ['Exchange', 'Function',
                   'Date', 'Market', 'Type',
                   'NumOrders',
                   'Price', 'Amount', 'Total', 'Fee', 'Fee_Coin'],
        'coin': ['Exchange', 'Function',
                 'Date', 'Market',
                 'CoinTo', 'CoinFrom',
                 'Type',

                 'Price', 'Amount', 'Total', 'Fee', 'Fee_Coin'],
        'cgt': []
    }
}

options = {
    'Files': False,
    'Coins': True,
    'Squash': False
}

file_dict = {
    'Exchange_1': {
        'Deposit': {
            'input': 'files/Exchange_1/Deposit/*.xlsx',
            'output': 'files/Exchange_1/_Results-Deposit.xlsx'
        },
        'Trade': {
            'input': 'files/Exchange_1/Trade/*.xlsx',
            'output': 'files/Exchange_1/_Results-Trade.xlsx'
        },
        'Withdraw': {
            'input': 'files/Exchange_1/Withdraw/*.xlsx',
            'output': 'files/Exchange_1/_Results-Withdraw.xlsx'
        },
        'Total': {
            'input': 'files/Exchange_1/_Results-*.xlsx',
            'output': 'files/Exchange_1/_Results.xlsx'
        },
        'Coin': 'files/Exchange_1/Coin.xlsx'
    },
    'Exchange_2': {
        'Deposit': {
            'input': 'files/Exchange_2/Deposit/*.xlsx',
            'output': 'files/Exchange_2/_Results-Deposit.xlsx'
        },
        'Trade': {
            'input': 'files/Exchange_2/Trade/*.xlsx',
            'output': 'files/Exchange_2/_Results-Trade.xlsx'
        },
        'Withdraw': {
            'input': 'files/Exchange_2/Withdraw/*.xlsx',
            'output': 'files/Exchange_2/_Results-Withdraw.xlsx'
        },
        'Total': {
            'input': 'files/Exchange_2/_Results-*.xlsx',
            'output': 'files/Exchange_2/_Results.xlsx'
        },
        'Coin': 'files/Exchange_2/Coin.xlsx'
    },
}

excel_dict = {
    'columns': {
        'initial': ['Date', 'Market', 'Type', 'Price', 'Amount', 'Total', 'Fee', 'FeeCoin'],
        'results': ['Exchange', 'Function',
                    'Date', 'Market', 'Type', 'Price', 'Amount', 'Total', 'Fee', 'FeeCoin'],
        'coin': ['Exchange', 'Function', 'Date', 'Market',
                 'CoinTo', 'CoinFrom',
                 'Type', 'Price', 'Amount', 'Total', 'Fee', 'FeeCoin'],
        'final': []
    }
}


# True / False
run_options = {
    # Merge all excel files in the file_dict locations below
    'merge': True,

    # In merged excel file, multiple transactions from a market order are squashed to reduce data
    'squash': True,

    # Adds crypto and fiat money values to squashed file if exists, otherwise to merged file
    'coin': True
}

settings_options = {
    # Delete existing logs generated from previous runs
    'clean_logs': True,

    # Groups the Date by a frequency so orders 1 second apart are joined together for example. Recommended: 1H
    'squash_frequency': '1D'  # Frequencies: Y=year, M=month, W=week, D=day, H=hour, T=minute, S=second, L=millisecond
}

file_dict = {
    'merge_exchange': {
        'exchange_1': {
            'trade': {
                'input': r'files\Exchange_1\Trade\*.xlsx',
                'output': r'files\Exchange_1\_merge-trade.xlsx'
            },
            'deposit': {
                'input': r'files\Exchange_1\Deposit\*.xlsx',
                'output': r'files\Exchange_1\_merge-deposit.xlsx'
            },
            'withdraw': {
                'input': r'files\Exchange_1\Withdraw\*.xlsx',
                'output': r'files\Exchange_1\_merge-withdraw.xlsx'
            },
            'total': {
                'input': r'files\Exchange_1\_merge-*.xlsx',
                'output': r'files\Exchange_1\_merge-total.xlsx'
            }
        },
        'exchange_2': {
            'trade': {
                'input': r'files\Exchange_2\Trade\*.xlsx',
                'output': r'files\Exchange_2\_merge-trade.xlsx'
            },
            'deposit': {
                'input': r'files\Exchange_2\Deposit\*.xlsx',
                'output': r'files\Exchange_2\_merge-deposit.xlsx'
            },
            'withdraw': {
                'input': r'files\Exchange_2\Withdraw\*.xlsx',
                'output': r'files\Exchange_2\_merge-withdraw.xlsx'
            },
            'total': {
                'input': r'files\Exchange_2\_merge-*.xlsx',
                'output': r'files\Exchange_2\_merge-total.xlsx'
            }
        }
    },
    'merge_exchanges_total_output': r'files\_merge.xlsx',
    'squash': r'files\squash.xlsx',
    'coin': r'files\coin.xlsx'
}

excel_dict = {
    # Expected column headers
    'exchange': {
        'exchange_1': {
            'trade': [],
            'deposit': [],
            'withdraw': []
        }
    },

    # Program output column headers
    'output': {
        'merge': ['Exchange', 'Function', 'Date', 'Market', 'CoinTo', 'CoinFrom', 'AddressFrom', 'AddressTo', 'TxId',
                  'Type', 'Ratio_CoinFromTo', 'Amount_CoinTo', 'Amount_CoinFrom', 'Fee', 'Fee_Coin'],
        'squash': ['Exchange', 'Function', 'Date', 'Market', 'CoinTo', 'CoinFrom', 'AddressFrom', 'AddressTo', 'TxId',
                   'Type', 'NumOrders', 'Ratio_CoinFromTo', 'Amount_CoinTo', 'Amount_CoinFrom', 'Fee', 'Fee_Coin'],
        'coin': ['Exchange', 'Function', 'Date', 'Market', 'CoinTo', 'CoinFrom', 'AddressFrom', 'AddressTo', 'TxId',
                 'Type', 'NumOrders', 'Ratio_CoinFromTo', 'Amount_CoinTo', 'Amount_CoinFrom', 'Total_EURO', 'Total_AUD',
                 'Fee', 'Fee_Coin', 'Fee_EURO', 'Fee_AUD'],
        'cgt': ['Exchange', 'Function', 'Date', 'Market', 'CoinTo', 'CoinFrom', 'AddressFrom', 'AddressTo', 'TxId',
                'Type', 'NumOrders', 'Price', 'Amount', 'Amount_Coin', 'Total', 'Total_Coin', 'Total_EURO', 'Total_AUD',
                'Fee', 'Fee_Coin', 'Fee_EURO', 'Fee_AUD', 'TaxableGain']
    }
}

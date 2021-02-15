# Import Libs
import traceback
from datetime import datetime

# Python files
import files
import coin

# Config
import config_nino as config


def program_runtime(start, end):
    diff_time = end - start
    secs = diff_time.total_seconds()
    hrs = secs//3600
    mins = secs//60
    runtime_msg = ''

    if hrs > 0:
        runtime_msg += f'{int(hrs)}h'
    if mins > 0:
        mins -= hrs*60
        runtime_msg += f'{int(mins)}m'

    secs -= hrs*3600 + mins*60
    if hrs + mins > 0:
        runtime_msg += f'{int(secs)}s'
    else:
        runtime_msg += f'{secs:.2f}s'

    return runtime_msg


def main():
    start_time = datetime.now()

    try:
        # files.main(config.file_dict, config.excel_dict['columns'])
        coin.main(
            config.file_dict['Binance']['Total']['output'],
            config.file_dict['Binance']['Coin'],
            config.excel_dict['columns']
        )
    except:
        traceback.print_exc()

    stop_time = datetime.now()
    time_msg = program_runtime(start_time, stop_time)
    print(f'Program run time: {time_msg}\n')

    return True


if __name__ == '__main__':
    main()

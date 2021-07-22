############################
# Peter Geras
############################


# Import libs
import os
from pathlib import Path
import traceback
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# Personal libs
import functions

# Python files
import merge
import coin
import squash

# Config
import config.config_test as config

# Loggers
log_time = logging.getLogger('log_time')
log_error = logging.getLogger('log_error')
log_debug = logging.getLogger('log_debug')


def choose_loggers():
    # Verbose runtime logging with level=logging.DEBUG
    setup_logger('log_time', 'program_runtime.log', format='%(asctime)s: %(message)s', level=logging.DEBUG)

    setup_logger('log_error', 'error.log')

    # If debugging is required, uncomment this logger
    setup_logger('log_debug', 'debug.log', level=logging.INFO)

    return True


def setup_logger(name, filepath, level=logging.INFO, backup=1, format='%(asctime)s - %(levelname)s: %(message)s'):
    log_folder = r'logs'
    # Create the log folder if it does not exist
    Path(log_folder).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(log_folder, filepath)

    handler = RotatingFileHandler(filepath, mode='a', maxBytes=2 * 1024 * 1024,
                                  backupCount=backup, encoding=None, delay=False)
    log_formatter = logging.Formatter(format)
    handler.setFormatter(log_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.addHandler(handler)

    return logger


def main():
    start_time = datetime.now()

    choose_loggers()
    log_debug.info("Code starting...")

    try:
        if config.options['merge']:
            log_debug.info(f'Merge started')
            merge.main(config.file_dict, config.excel_dict)
        if config.options['squash']:
            log_debug.info(f'Squash started')
            squash.main(config.file_dict, config.excel_dict['columns'])
        if config.options['coin']:
            log_debug.info(f'Coin started')
            coin.main(
                config.file_dict['binance']['total']['output'],
                config.file_dict['binance']['coin'],
                config.excel_dict['columns']
            )
    except Exception as e:
        traceback.print_exc()
        log_error.exception(e)
        log_time.error(f'Exception occurred')
        log_error.warning(f'\n\n{40*"*"} ^ {datetime.now()}\n')

    log_debug.info("Code ending...\n")

    stop_time = datetime.now()
    time_msg = functions.runtime(start_time, stop_time)
    log_time.info(f'Program run time: {time_msg}\n')

    return True


if __name__ == '__main__':
    main()

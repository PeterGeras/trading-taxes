############################
# Peter Geras
############################

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
import squash
import coin
import cgt

# Config
import config.config_prod as config

# Loggers
log_folder = r'logs'
log_time = logging.getLogger('log_time')
log_error = logging.getLogger('log_error')
log_debug = logging.getLogger('log_debug')


def initialise_logging():
    # Create the log folder if it does not exist
    Path(log_folder).mkdir(parents=True, exist_ok=True)

    if config.settings_options['clean_logs']:
        for f in os.listdir(log_folder):
            with open(os.path.join(log_folder, f), 'w'):
                pass

    choose_loggers()

    return


def choose_loggers():
    # Verbose runtime logging with level=logging.DEBUG
    setup_logger('log_time', 'program_runtime.log', format='%(asctime)s: %(message)s', level=logging.DEBUG)

    setup_logger('log_error', 'error.log', level=logging.DEBUG)

    # If debugging is required, uncomment this logger
    setup_logger('log_debug', 'debug.log', level=logging.INFO)

    return True


def setup_logger(name, filepath, level, backup=1, format='%(asctime)s - %(levelname)s: %(message)s'):
    filepath = os.path.join(log_folder, filepath)

    handler = RotatingFileHandler(filepath, mode='a', maxBytes=2 * 1024 * 1024,
                                  backupCount=backup, encoding=None, delay=False)
    log_formatter = logging.Formatter(format)
    handler.setFormatter(log_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.addHandler(handler)

    return logger


def do_tasks():
    if config.run_options['merge']:
        log_debug.info(f'Merge started')

        merge.main(
            file_dict=config.file_dict,
            excel_dict=config.excel_dict
        )

    if config.run_options['squash']:
        log_debug.info(f'Squash started')

        squash.main(
            file_dict=config.file_dict,
            excel_cols=config.excel_dict['output'],
            squash_frequency=config.settings_options['squash_frequency']
        )

    if config.run_options['coin']:
        log_debug.info(f'Coin started')

        coin.main(
            file_dict=config.file_dict,
            excel_cols=config.excel_dict['output']
        )

    if config.run_options['cgt']:
        log_debug.info(f'CGT started')

        cgt.main(
            file_dict=config.file_dict,
            excel_cols=config.excel_dict['output']
        )

    return


def print_errors(error, info):
    traceback.print_exc()
    log_error.info(info + '\n')
    log_error.exception(error)
    log_error.debug(f'\n\n{40*"*"} ^ {datetime.now()}\n')
    log_time.error(info)

    return


def main():
    start_time = datetime.now()

    log_debug.info("Code starting...")

    initialise_logging()

    try:
        do_tasks()
    except FileNotFoundError as e:
        print_errors(e, 'A required file is missing.')
    except PermissionError as e:
        print_errors(e, 'Permission denied. A file is open and needs to be closed.')
    except AssertionError as e:
        print_errors(e, 'Asserted a truth that failed.')
    except Exception as e:
        print_errors(e, 'Exception occurred')

    log_debug.info("Code ending...\n")

    stop_time = datetime.now()
    time_msg = functions.runtime(start_time, stop_time)
    log_time.info(f'Program run time: {time_msg}\n')

    return True


if __name__ == '__main__':
    main()

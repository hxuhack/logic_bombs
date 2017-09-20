import logging
import sys
import os
import datetime

from colorama import *
from functools import wraps


class RetryError(Exception):
    pass


def ignore(level=logging.INFO, msg=''):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logging.log(level, msg + " ignored.\t" + repr(e))
            else:
                return result
        return wrapper
    return decorate


def retry(retry_time=3, level=logging.INFO, msg=''):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            d_time = 1
            feedback_queue = kwargs.get('feedback_queue', None)
            feedback_pool = kwargs.get('feedback_pool', None)
            feedback_index = kwargs.get('feedback_index', None)
            while True:
                if d_time > retry_time:
                    if feedback_queue:
                        feedback_queue.put(RetryError)
                    if feedback_index and feedback_pool:
                        feedback_pool[feedback_index] = RetryError
                    break
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logging.log(level, msg + " Retrying... " + str(d_time) + " time(s).\t" + repr(e))
                    d_time += 1
                else:
                    break
        return wrapper
    return decorate


def init_all(level=logging.INFO):
    if not os.path.exists('log'):
        os.mkdir('log')

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(threadName)s: %(message)s")
    # file_handler = logging.FileHandler(os.path.join('log', str(datetime.datetime.now()).replace(':', '_') + '.log'))
    # file_handler.setFormatter(log_formatter)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(LogFormatter())
    root_logger.addHandler(console_handler)
    # root_logger.addHandler(file_handler)


class LogFormatter(logging.Formatter):
    def __init__(self, style='{'):
        logging.Formatter.__init__(self, style=style)

    def format(self, record):
        stdout_template = '{levelname}' + Fore.RESET + '] {threadName}: ' + '{message}'
        stdout_head = '[%s'

        all_formats = {
            logging.DEBUG: logging.StrFormatStyle(stdout_head % Fore.LIGHTBLUE_EX + stdout_template),
            logging.INFO: logging.StrFormatStyle(stdout_head % Fore.GREEN + stdout_template),
            logging.WARNING: logging.StrFormatStyle(stdout_head % Fore.LIGHTYELLOW_EX + stdout_template),
            logging.ERROR: logging.StrFormatStyle(stdout_head % Fore.LIGHTRED_EX + stdout_template),
            logging.CRITICAL: logging.StrFormatStyle(stdout_head % Fore.RED + stdout_template)
        }

        self._style = all_formats.get(record.levelno, logging.StrFormatStyle(logging._STYLES['{'][1]))  # TODO
        self._fmt = self._style._fmt
        result = logging.Formatter.format(self, record)

        return result


def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        print(s, end='')
    else:  # total size is unknown
        print("read %d\n" % (readsofar,), end='')

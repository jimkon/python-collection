import logging
from functools import wraps
from time import time

VERBOSITY = 1

# https://www.codegrepper.com/code-examples/python/python+print+error+in+red
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def log(*args, verbosity=1, rgb=(255, 255, 255)):
    if verbosity <= VERBOSITY:
        colored_args = tuple([colored(*rgb, arg) for arg in args])
        print(*colored_args)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
_CNT = 0


def func_execution_logging(_func):
    @wraps(_func)
    def wrapper(*args, **kwargs):

        start_time = time()
        _func_name = f"{_func.__module__}.{_func.__qualname__}"

        global _CNT
        padding = '--' * _CNT
        _CNT += 1
        try:
            logger.info(f"{padding}=> Running {_func_name}...")
            res = _func(*args, **kwargs)
        except Exception as e:
            _CNT -= 1
            logger.error(f"Function {_func_name} raised exception: '{e}'.")
            raise

        elapsed_time = time() - start_time
        logger.info(
            f"<={padding} Function {_func_name} successfully finished in {elapsed_time:.2f} seconds."
        )
        _CNT -= 1
        return res

    return wrapper


if __name__=="__main__":
    log('lsajfalsjf')
    log('lsajfalsjf', rgb=(255, 0, 0))
    log('lsajfalsjf', rgb=(0, 255, 0))
    log('lsajfalsjf', rgb=(0, 0, 255))
    log('lsajfalsjf', rgb=(0, 0, 0))


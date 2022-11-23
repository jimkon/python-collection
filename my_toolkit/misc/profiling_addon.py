import io
import pstats
from functools import wraps
import cProfile
from pstats import SortKey
from datetime import datetime
import logging
import os


DATA_DIR = 'data'


logger = logging.getLogger(__name__)

def cprofile_func(func, *args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()

    res = func(*args, **kwargs)

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)

    dt = datetime.now().strftime("%Y-%d-%m_%H-%M-%S")
    filename = f"{func.__module__}.{func.__name__}_{dt}.prof"
    ps.dump_stats(filename)
    logger.info(f"cProfile data stored in file {filename}")


#https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
def cprofile(_func=None, *, filename_prefix=None):
    def decorator_cprofile(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()

            res = func(*args, **kwargs)

            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)

            dt = datetime.now().strftime("%Y-%d-%m_%H-%M-%S")

            directory = os.path.join(os.path.dirname(__file__), DATA_DIR)
            if not os.path.exists(directory):
                os.mkdir(directory)

            if filename_prefix:
                filename = f"{filename_prefix}_{dt}.prof"
            else:
                filename = f"{func.__module__}.{func.__name__}_{dt}.prof"

            filepath = os.path.join(directory, filename)
            ps.dump_stats(filepath)
            logger.info(f"cProfile data stored in file {filepath}")

            return res
        return wrapper

    if _func is None:
        return decorator_cprofile
    else:
        return decorator_cprofile(_func)

from time import time, strftime, gmtime


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        end_time = time()
        elapsed = strftime("%H:%M:%S",gmtime(end_time - start_time))
        print(func.__name__, elapsed)
        return res
    return wrapper
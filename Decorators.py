def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        logger.debug(f"-> {func.__name__}")
        res = func(*args, **kwargs)
        logger.debug(f"<- {func.__name__}")
        end_time = time()
        elapsed = strftime("%H:%M:%S",gmtime(end_time - start_time))
        print(func.__name__, elapsed)
        return res, elapsed
    return wrapper
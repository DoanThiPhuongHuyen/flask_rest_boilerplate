def memoize(func):
    """
    Memoize function, can be used as decorator
    Does not share memoized cache between processes
    :param func: function should be cache
    :return:
    """
    memoized_cache = dict()

    def memoized_func(*args):
        if args in memoized_cache:
            return memoized_cache[args]
        result = func(*args)
        memoized_cache[args] = result
        return result

    return memoized_func

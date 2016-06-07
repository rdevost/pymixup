from functools import wraps


def coroutine(func):
    """Decorator for coroutines to automatically advance to first yield."""
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

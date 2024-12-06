import warnings

# só para descobrir se metodos ainda são chamados
def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated and may be removed in future versions.",
            DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)
    return wrapper

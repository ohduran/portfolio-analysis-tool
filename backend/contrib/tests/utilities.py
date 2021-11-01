import decimal
import random


def random_amount():
    """
    Return a random amount in the form of Decimal.

    >>> isinstance(random_amount(), decimal.Decimal)
    True
    """
    return decimal.Decimal(str(random.random()))

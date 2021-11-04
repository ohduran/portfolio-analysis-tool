import decimal
import random


def random_amount():
    """
    Return a random amount in the form of Decimal.

    >>> isinstance(random_amount(), decimal.Decimal)
    True
    """
    return decimal.Decimal(str(random.random() * 100 - 50))


def random_positive_amount():
    """
    Return a random amount greater than 0 in the form of Decimal.
    >>> isinstance(random_positive_amount(), decimal.Decimal) and random_positive_amount() > 0
    True
    """
    return decimal.Decimal(str(random.random() * 100))

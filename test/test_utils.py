from functools import wraps
from test_config import KEYWORDS


def clean_data(func):
    """Filter imported data based on predefined
    keywords."""

    @wraps
    def factory(*args):
        _kw = set(KEYWORDS)
        df = func(*args)
        _match = self.data[
            self.data["keywords"].apply(lambda x : _kw.isdisjoint(x)).values
                    ]
        return _match
    return factory

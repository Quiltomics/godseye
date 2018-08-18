import pandas as pd
from test_importer import Importer
from functools import lru_cache


class Analyzer:
    def __init__(self, *args, **kwargs):
        self._importer = Importer(database_name=kwargs["database_name"])
        self.data = self._importer.create_dataframe()

    # Without maxsize the cache will preserve 128 itmes
    @lru_cache
    def filter(self, keyword):
        """Check wether if there's a match for the keyword."""
        _match = self.data[self.data["keywords"].apply(lambda x : keyword in x).values]
        return _match
    
    def return_country(keyword):
        """Return the countries of the papers that mtched
        with input keyword."""
        _match = self.filter(keyword)
        return _match['country']
    
    def return_created_date():
        """Return the created_dates of the papers that mtched
        with input keyword."""
        _match = self.filter(keyword)
        return _match['created_date']

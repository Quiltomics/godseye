from test_importer import Importer
from test_visualizer import Visualizer
from collections import Counter
import test_config as config
from itertools import chain
import pandas as pd


class Run:
    def __init__(self, *args, **kwargs):
        # the name should come from config file.
        _db_path = config.HOME_DIR + "/godseye-files/database.db"
        _importer = Importer(database_name=_db_path)
        self.dataframe = _importer.create_dataframe()
        self.visualizer = Visualizer()
    
    def histogram_dates(self, word):
        # counter = Counter(chain.from_iterable(self.dataframe['keywords'].values))
        groupby_year = self.dataframe.groupby(self.dataframe.created_date.dt.year, as_index=False)

        def func(args):
            return Counter(chain.from_iterable(args))

        x_iterable = groupby_year.groups.keys()
        counter_grouped = groupby_year.agg(func)

        y_iterable = [d[word] for d in counter_grouped.keywords]
        print(y_iterable)
        n_bins = counter_grouped.size
        self.visualizer.cumulative_histogram(
            iterable=y_iterable,
            n_bins=n_bins,
            xticks=x_iterable,
            years=x_iterable,
            x_label="Years",
            y_label="Keyword Frequency"
        )
        """
        self.visualizer.one_line(word,
                                 x=x_iterable,
                                 y=y_iterable,
                                 xticks=x_iterable,
                                 x_label="Years",
                                 y_label="Keyword Frequency")
        """


if __name__ == '__main__':
    run = Run()
    run.histogram_dates('protein')

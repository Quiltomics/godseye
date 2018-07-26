from test_importer import Importer
from test_visualizer import Visualizer
from collections import Counter
import test_config as config
from itertools import chain



class Run:
    def __init__(self, *args, **kwargs):
        _db_path = config.HOME_DIR + "/godseye-files/database.db"
        _importer = Importer(database_name=_db_path)
        self.dataframe = _importer.create_dataframe()
        self.visualizer = Visualizer()
    
    def histogram_dates(self):
        counter = Counter(chain.from_iterable(self.dataframe['keywords'].values))
        print(counter.most_common(10))


        # VZ.cumulative_histogram(iterable=np.arange(100),
        #                         n_bins=10,
        #                         xlable='number of occurrence',
        #                         ylable='Likelihood of occurrence')



if __name__ == '__main__':
    run = Run()
    run.histogram_dates()
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from test_importer import Importer


# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Article(Document):
    def __init__(self, *args, **kwargs):
        _db_path = config.HOME_DIR + "/godseye-files/database.db"
        _importer = Importer(database_name=_db_path)
        self.dataframe = _importer.create_dataframe()

    def filter(self, query):
        pass
    
    def search(self, query):
        pass

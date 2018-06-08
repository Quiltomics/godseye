import json
import sqlite3 as lite
from sqlite3 import Error as LiteError



class CreateDatabase:
    def __init__(self, *args, **kwargs):
        self.json_path = kwargs['json_path']
        self.database_name = kwargs['database_name']

    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(self.database_name)
            print(sqlite3.version)
        except LiteError as e:
            print(e)
            # raise
        else:
            return conn
        # finally:
        #    conn.close()

    def json_parser(self):
        with open(self.json_path) as f:
            data = json.load(f)
        for index, metadata in data.items():
            article = metadata["Article"]
            short_title = article["Journal"]["Title"]
            title = article["ArticleTitle"]
            abstract = article["Abstract"]["AbstractText"]
            date = article["ArticleDate"]
            
    def insert(self):
        connection = self.create_connection()
        with connection:
            cur = con.cursor()
            cur.execute("create table keywords")
            cur.execute()

            rows = cur.fetchall()

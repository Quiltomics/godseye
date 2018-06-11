"""Import data from database."""

import sqlite3 as lite
from sqlite3 import Error as LiteError
import pandas as pd


class Importer:
    def __init__(self, *args, **kwargs):
        self.database_name = kwargs['database_name']
        self._connection = self.create_connection()

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = lite.connect(self.database_name)
        except LiteError as e:
            print(e)
            # raise
        else:
            return conn
        # finally:
            # conn.close()

    def create_dataframe(self):
        columns = ('keywords', 'country', 'created_date')
        query = """ SELECT {}, {}, {} FROM article """
        cur = self._connection.cursor()
        df = pd.DataFrame.from_records(cur.execute(query.format(*columns)),
                                       columns=columns)
        return df


if __name__ == "__main__":
    CD = Importer(database_name="../godseye-files/database.db")
    CD.extract()

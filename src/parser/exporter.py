import json
import sqlite3 as lite
from sqlite3 import Error as LiteError
import nltk
import re
import sys


class CreateDatabase:
    def __init__(self, *args, **kwargs):
        self.json_path = kwargs['json_path']
        self.database_name = kwargs['database_name']
        self.words_regex = re.compile(r"\b\w+\b")

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

    def create_tables(self):
        sql_create_table = """ CREATE TABLE IF NOT EXISTS article (
                                        id integer PRIMARY KEY,
                                        keywords text NOT NULL,
                                        country text,
                                        created_date text
                                    ); """
        conn = self.create_connection()
        with conn:                          
            cur = conn.cursor()
            cur.execute(sql_create_table)
    
    def insert(self):
        sql_insert = """ INSERT INTO article (keywords, country,
        created_date) VALUES ('{}', '{}', '{}')
        """
        conn = self.create_connection()
        with conn:
            cur = conn.cursor()
            for keywords, country, date in self.extract_keywords():
                query = sql_insert.format("-".join(keywords),
                                          country,
                                          "-".join(date.values()))
                cur.execute(query)

    def json_parser(self):
        """extract required info from json file and pass it to
        extract_keywords function."""

        with open(self.json_path) as f:
            data = json.load(f)
        data = data["PubmedArticleSet"]["PubmedArticle"]
        for d in data:
            article = d['MedlineCitation']["Article"]
            date = d['MedlineCitation']["DateCompleted"]
            jtitle = article["Journal"]["Title"]
            atitle = article["ArticleTitle"]
            abstract = article.get("Abstract",{"AbstractText":''})["AbstractText"]
            country = d['MedlineCitation']["MedlineJournalInfo"]["Country"]
            if isinstance(abstract, list):
                abstract = '-'.join([a['#text'] for a in abstract])
            elif isinstance(abstract, dict):
                abstract = abstract['#text']
            yield jtitle, atitle, abstract, country, date

    def extract_keywords(self):
        """Extracts keywords for each article."""
        for *args, country, date in self.json_parser():
            try:
                words = nltk.pos_tag(self.words_regex.findall(" ".join(args)))
            except:
                print(args)
                raise
            # unique words in each article
            keywords = {word for word, tag in words if tag == "NN"}
            yield keywords, country, date
            
    def run(self):
        self.create_tables()
        self.insert()




if __name__ == "__main__":
    CD = CreateDatabase(json_path='../godseye-files/articles.json',
                        database_name="../godseye-files/database.db")
    
    CD.run()

import json
import sqlite3 as lite
from sqlite3 import Error as LiteError
import nltk
import re
import sys
import glob
import test_config
from os import path as ospath



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
    
    def insert(self, data):
        sql_insert = """ INSERT INTO article (keywords, country,
        created_date) VALUES ('{}', '{}', '{}')
        """
        conn = self.create_connection()
        with conn:
            cur = conn.cursor()
            for keywords, country, date in self.extract_keywords(data):
                query = sql_insert.format("-".join(keywords),
                                          country,
                                          "-".join(date.values()))
                cur.execute(query)

    def parse_pubmed(self, data):
        """extract required info from json file and pass it to
        extract_keywords function."""
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

    def parse_medline(self, data):
        """extract required info from json file and pass it to
        extract_keywords function."""
        for d in data:
            article = d["Article"]
            date = d["DateCompleted"]
            jtitle = article["Journal"]["Title"]
            atitle = article["ArticleTitle"]
            abstract = article.get("Abstract",{"AbstractText":''})["AbstractText"]
            country = d["MedlineJournalInfo"]["Country"]
            if isinstance(abstract, list):
                    abstract = '-'.join([a.get('#text', '') for a in abstract])
            elif isinstance(abstract, dict):
                abstract = abstract.get('#text', '')
            yield jtitle, atitle, abstract, country, date

    def parse_all(self):
        """iteratively parse json files within json_path directory."""

        for file_name in glob.glob(self.json_path + "*.json"):
            print("Parsing {}".format(file_name))
            name = ospath.basename(file_name)
            with open(file_name) as f:
                data = json.load(f)
                if name.startswith("medline"):
                    k1, k2 = test_config.FILE_TYPE_KEY['medline']
                    data = data[k1][k2]
                    yield self.parse_medline(data)
                elif name.startswith("pubmed"):
                    k1, k2 = test_config.FILE_TYPE_KEY['pubmed']
                    data = data[k1][k2]
                    yield self.parse_pubmed(data)

    def extract_keywords(self, data):
        """Extracts keywords for each article."""
        
        for *args, country, date in data:
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
        for data in self.parse_all():
            self.insert(data)




if __name__ == "__main__":
    CD = CreateDatabase(json_path= ospath.join(test_config.HOME_DIR, 'godseye-files/json/'),
                        database_name=ospath.join(test_config.HOME_DIR, "godseye-files/database.db"))
    
    CD.run()

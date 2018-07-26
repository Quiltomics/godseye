"""Download files from pubmed and biorxive."""
from os import path as ospath
import ftplib
from multiprocessing.dummy import Pool as ThreadPool
import json


class Downloader:
    def __init__(self, *args, **kwargs):
        self.server_url = kwargs['server_url']
        self.root = kwargs['root']
        self.files_path = kwargs['files_path']
        self.connection = self.connect()

    def connect(self):
        try:
            connection = ftplib.FTP(self.server_url)
            connection.login()
            # connection.cwd(root)
        except:
            raise
        else:
            return connection

    def download(self, args):
        file_name, path = args
        connection = self.connect()
        connection.cwd(self.root)
        print("start downloading ", file_name)
        with open(path, 'wb') as f:
            connection.retrbinary('RETR ' + file_name, f.write)
        print("finish downloading ", file_name)

    def get_file_names(self):
        file_list = []
        connection = self.connect()
        connection.cwd(self.root)
        connection.retrlines('LIST', lambda x: file_list.append(x.split()))
        with open("file_names.json", "w") as f:
            json.dump(file_list, f, indent=4)

    def run(self):
        with open('file_names.json') as f:
            file_list = json.load(f)

        print(len(file_list)//3, "Files founded ....")
        
        paths = [(file_name, ospath.join(self.files_path, file_name))
                    for *_, file_name in file_list
                if file_name.endswith('gz')
            ][:5]

        pool = ThreadPool()
        pool.map(self.download, paths)
        pool.close()
        pool.join()

if __name__ == "__main__":
    D = Downloader(server_url="ftp.ncbi.nlm.nih.gov",
                   root="pubmed/baseline/",
                   files_path="../gods-eye-files")

    # D.get_file_names()
    D.run()

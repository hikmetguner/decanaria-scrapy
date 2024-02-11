import psycopg2
from pymongo import MongoClient

from jobs_project.jobs_project import settings

class PostgreSQLHandler:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def fetch_data(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()

class MongoDBHandler:
    def __init__(self, uri, dbname):
        self.uri = settings.MONGO_URI
        self.dbname = settings.MONGO_DATABASE

    def connect(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.dbname]

    def fetch_data(self, collection_name):
        collection = self.db[collection_name]
        return collection.find()

    def close(self):
        self.client.close()

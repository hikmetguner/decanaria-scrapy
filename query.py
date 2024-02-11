import logging
import pandas as pd
from db_handler import PostgreSQLHandler
from db_handler import MongoDBHandler
from jobs_project.jobs_project import settings

#Set logging level
logging.basicConfig(level = logging.INFO)

# Instantiate PostgreSQLHandler and MongoDBHandler objects
postgres_handler = PostgreSQLHandler(
    dbname = settings.DATABASE_SETTINGS['dbname'], 
    user = settings.DATABASE_SETTINGS['user'], 
    password = settings.DATABASE_SETTINGS['password'], 
    host = settings.DATABASE_SETTINGS['host'], 
    port = settings.DATABASE_SETTINGS['port'])
mongo_handler = MongoDBHandler(
    uri = settings.MONGO_URI, 
    dbname = settings.MONGO_URI)

# Connect to databases
postgres_handler.connect()
mongo_handler.connect()

schema = "decanaria_schema"
table = "raw_table"
collection = "raw_collection"

# Fetch data from dbs
postgres_data = postgres_handler.fetch_data(f"SELECT * FROM {table}")
logging.info("PostgreSQL data fetch successful")
mongo_data = mongo_handler.fetch_data(f"{collection}")
logging.info("MongoDB data fetch successful")

#Normalize JSON
normalized_postgre_datas = []
for data in postgres_data:
    data = pd.json_normalize(data[-1]).to_dict()
    normalized_postgre_datas.append(data)

normalized_mongo_datas = []
for document in mongo_data:
    document = pd.json_normalize(document).to_dict()
    normalized_mongo_datas.append(document)

# JSON into DF
postgre_df = pd.DataFrame(normalized_postgre_datas)
mongo_df = pd.DataFrame(normalized_mongo_datas) 

# DF into CSV
postgre_df.to_csv("postgres_data.csv", index=False)
logging.info("PostgreSQL data conversion successful")

mongo_df.to_csv("mongo_data.csv", index=False)
logging.info("MongoDB data conversion successful")

postgres_handler.close()
mongo_handler.close()
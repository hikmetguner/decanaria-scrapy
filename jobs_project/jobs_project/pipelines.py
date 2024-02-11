# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import json
import logging
from operator import index
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pymongo
from scrapy import Item
from jobs_project.items import DerivedInfoItem, GoogleJobsItem, JobsProjectItem, LocationsItem, MetaDataItem, PostalAddressItem

import json
from scrapy.exceptions import DropItem

class JobsProjectPipeline:
    def process_item(self, item, spider):
        logging.debug("----------> ENTERED JOB PIPELINE PROCESS")
        item_data =item["item"]["data"]
        job_item = self.process_job(item_data)
        return job_item

    def process_job(self,data):
        item = JobsProjectItem()
        value = None
        for key in data.keys():
            value = data[key]
            if key == "meta_data":
                value = self.process_metadata(data[key])
            item[key] = value
        return item
    
    def process_metadata(self,data):
        logging.debug("----------> ENTERED METADATA PROCESS")
        item = MetaDataItem()
        value = None
        for key in data.keys():
            value = data[key]
            if key == "googlejobs":
                value = self.process_googlejobs(data[key])
            item[key] = value
        return item
    
    def process_googlejobs(self,data):
        logging.debug("----------> ENTERED GOOGLEJOBS PROCESS")
        item = GoogleJobsItem()
        value = None
        for key in data.keys():
            value = data[key]
            if key == "derivedInfo":
                value = self.process_derived_info(data[key])
            item[key] = value
        return item
    
    def process_derived_info(self,data):
        logging.debug("----------> ENTERED DERIVED INFO PROCESS")
        item = DerivedInfoItem()
        value = None
        for key in data.keys():
            value = data[key]
            if key == "locations":
                value = self.process_locations(data[key])
            item[key] = value
        return item
    
    def process_locations(self,data):
        logging.debug("----------> ENTERED LOCATIONS PROCESS")
        location_arr = []
        # Locations is a dictionary within the list
        for location in data:
            item = LocationsItem()
            value = None
            for key in location.keys():
                value = location[key]
                if key == "postalAddress":
                    value = self.process_postal_address(location[key])
                item[key] = value
            location_arr.append(item)
        return location_arr
    
    def process_postal_address(self,data):
        logging.debug("----------> ENTERED POSTAL ADDRESS PROCESS")
        item = PostalAddressItem()
        for key in data.keys():
            item[key] = data[key]
        return item
    

class PostgreSQLPipeline:
    def __init__(self, db_settings):
        logging.debug("INIT POSTGRE PIPELINE")
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('DATABASE_SETTINGS')
        return cls(db_settings)

    def open_spider(self, spider):
        self.connection = psycopg2.connect(**self.db_settings)
        self.cursor = self.connection.cursor()

        # Check if table exists
        table_name = "raw_table"
        self.cursor.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            json_data JSONB
        )
        """
        try:
            self.cursor.execute(create_table_query)
            logging.info("Table 'raw_data' created successfully.")
        except psycopg2.Error as e:
            logging.error("Error creating table:", e)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        logging.debug(" ----------> POSTGRE PIPELINE")
        
        table = "raw_table"

        json_data = json.dumps(obj_to_dict(item), indent = 4)
        statement = """
                INSERT INTO {} (json_data)
                VALUES (%s)
            """.format(table)
        self.cursor.execute(statement, (json_data, ))
        self.connection.commit()
        return item

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #TODO define in a set location?
        collection_name = "raw_collection"
        collection = self.db[collection_name]
        collection.insert_one(dict(item))
        return item


def obj_to_dict(obj):
    for key in obj.keys():
        if isinstance(obj[key], list):
            #If object is a list with item type which is a super edge case
            #iterate over the list and flatten them one by one
            if (all([isinstance(item,Item) for item in obj[key]])):         
                arr = []
                for sub_obj in obj[key]:
                    arr.append(obj_to_dict(sub_obj))
                obj[key] = arr
        if isinstance(obj[key], Item):
            #recursively flatten items
            obj[key] = obj_to_dict(obj[key])
    return dict(obj)
                
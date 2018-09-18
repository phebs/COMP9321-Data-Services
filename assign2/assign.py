import json
import pandas as pd
from pymongo import MongoClient
from datetime import *


class database(object):
    def __init__(self,mongo_port, mongo_host, db_name, collection):
        self.mongo_host=mongo_host
        self.mongo_port = mongo_port
        self.db = db_name
        self.collection = collection
        self.client = MongoClient(host=self.mongo_host,port = self.mongo_port)
        self.unique_id = 0

    def createPayload(self,data):
        # Removes the unncessary header
        # data = json.load(f)[1]
        # Retrieves the header for the header collection
        header = data[0].get("indicator")
        indicator = header.get("id")
        value = header.get("value")
        countryList = list()
        # Retrieves the entry
        for entry in data:
            country = {
                "country": entry.get("country").get("value"),
                "date": entry.get("date"),
                "value": entry.get("value")
            }
            countryList.append(country)

        new_data = {
            "collection_id": self.unique_id,
            "indicator": indicator,
            "indicator_value": value,
            "creation_time": str(datetime.now()),
            "entries": countryList,
        }
        self.unique_id += 1

        print("Writing into the mongodb")
        # print(new_data)
        self.write_in_mongodb(new_data)
        #
        # print("Querying the database")
        # dataframe = db.read_from_mongodb()
        # print(dataframe)

    def write_in_mongodb(self,dataframe):
            """
            :param dataframe:
            :param mongo_host: Mongodb server address
            :param mongo_port: Mongodb server port number
            :param db_name: The name of the database
            :param collection: the name of the collection inside the database
            """
            db = self.client[self.db]
            db.authenticate('phb','COMP9321')
            c = db[self.collection]
            # You can only store documents in mongodb;
            # so you need to convert rows inside the dataframe into a list of json objects
            records = dataframe
            c.insert(records)


    def read_from(self,query):
        """
        :param mongo_host: Mongodb server address
        :param mongo_port: Mongodb server port number
        :param db_name: The name of the database
        :param collection: the name of the collection inside the database
        :return: A dataframe which contains all documents inside the collection
        """
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]
        result = list(c.find(query))
        if len(result) < 1:
            return None
        else:
            result=result[0]
            result_return = {
                #May change the integer conversion
                "location": self.collection + "/" + str(result.get('collection_id')),
                "collection_id": result.get("collection_id"),
                "creation_time": result.get("creation_time"),
                "indicator": result.get("indicator"),
            }
            return result_return

    def delete(self,query):
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]
        response = c.delete_one(query)
        #prints how many documents it deleted
        #TODO can use to write a message
        print(response.deleted_count)
        return response.deleted_count


# if __name__ == '__main__':
#
#     db_name = 'my-database'
#     mongo_port = 27872
#     mongo_host = 'ds127872.mlab.com'
#
#     collection = 'Economic Indicator'
#
#     print("Writing into the mongodb")
#     write_in_mongodb(df, mongo_host, mongo_port, db_name, collection)
#
#     print("Querying the database")
#     dataframe = read_from_mongodb(mongo_host, mongo_port, db_name, collection)
#
#     print_dataframe(dataframe)

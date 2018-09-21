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


    def read_from(self,query,abbreviate):
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

        ignore = {'_id':0}
        result = list(c.find(query,ignore))
        # print(result)
        if len(result) < 1:
            return None
        else:
            #Removes the useless header information
            result=result[0]
            if abbreviate:
                result_return = {
                    #May change the integer conversion
                    "location": self.collection + "/" + str(result.get('collection_id')),
                    "collection_id": result.get("collection_id"),
                    "creation_time": result.get("creation_time"),
                    "indicator": result.get("indicator"),
                }
            else:
                result_return = result
            return result_return

    def read_all(self):
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]
        result_list=list()
        response = list(c.find().sort("collection_id"))
        for result in response:
            result_return = {
                #May change the integer conversion
                "location": self.collection + "/" + str(result.get('collection_id')),
                "collection_id": result.get("collection_id"),
                "creation_time": result.get("creation_time"),
                "indicator": result.get("indicator"),
            }
            result_list.append(result_return)
        return result_list

    def queryYD(self,query,collection_id,year,country):
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]
        result = list(c.find(query))
        result = result[0]
        #retrieves the first one that satisfies the criteria
        for response in result.get("entries"):
            if response.get("date") == year and response.get("country") == country:
                result_return = {
                    "collection_id": result.get("collection_id"),
                    "indicator": result.get("indicator"),
                    "country": response.get("country"),
                    "year": response.get("date"),
                    "value": response.get("value")
                }
                return result_return
        return None


    def delete(self,query):
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]
        response = c.delete_one(query)
        #prints how many documents it deleted
        #TODO can use to write a message
        # print(response.deleted_count)
        return response.deleted_count


    def country_print(self,all,collection_id,year,decide,no):
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]

        query = {"collection_id" : collection_id}
        holder = list()
        result = list(c.find(query))
        if len(result) < 1:
            return None
        result = result[0]

        #goes through all the entries to find which entries have the same date
        for response in result.get("entries"):
            if response.get("date") == year:
                holder.append(response)
        if all or (decide == "top"):
            ifreverse=True
        else:
            ifreverse=False
        #Sorts the values
        result_sort=sorted(holder,key=lambda x: (x.get("value") is not None, x.get("value")),reverse=ifreverse)

        if (len(result_sort) >= no and not all):
            result_sort=result_sort[:no]

        result_return = {
            "indicator" : result.get("indicator"),
            "indicator_value": result.get("indicator_value"),
            "entries": result_sort
        }
        return result_return


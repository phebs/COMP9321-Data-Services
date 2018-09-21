import json
from pymongo import MongoClient
from datetime import *


class database(object):
    def __init__(self,mongo_port, mongo_host, db_name, collection):
        self.mongo_host=mongo_host
        self.mongo_port = mongo_port
        self.db = db_name
        self.collection = collection
        self.client = MongoClient(host=self.mongo_host,port = self.mongo_port)

    '''
    Authenticates so that user has access to mongodb
    '''
    def authenticate(self):
        db = self.client[self.db]
        db.authenticate('phb', 'COMP9321')
        c = db[self.collection]
        return c

    '''
    Part of creating a new indicator
    '''
    def createPayload(self,data):
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
        #Adds into a dict
        new_data = {
            "collection_id": indicator,
            "indicator": indicator,
            "indicator_value": value,
            "creation_time": str(datetime.now()),
            "entries": countryList,
        }

        #next function writes it into mongodb
        self.write_in_mongodb(new_data)
    '''
    Writes into mongodb
    '''
    def write_in_mongodb(self,dataframe):
            c=self.authenticate()
            records = dataframe
            c.insert(records)

    '''
    Reads from mongodb depending on the query
    abbreviate  = True return more concise results
    '''
    def read_from(self,query,abbreviate):
        c = self.authenticate()
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
    '''
    Returns a list of all documents
    '''
    def read_all(self):
        c = self.authenticate()
        result_list=list()
        response = list(c.find().sort("collection_id"))
        for result in response:
            result_return = {
                "location": self.collection + "/" + result.get('collection_id'),
                "collection_id": result.get("collection_id"),
                "creation_time": result.get("creation_time"),
                "indicator": result.get("indicator"),
            }
            result_list.append(result_return)
        return result_list
    '''
    Queries according to collection id, year and country
    '''
    def queryYD(self,query,collection_id,year,country):
        c = self.authenticate()
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

    '''
    Deletes a particular collection id from the database
    '''
    def delete(self,query):
        c = self.authenticate()
        response = c.delete_one(query)
        return response.deleted_count

    '''
    Prints all the countries depending on collection id, year and top/bottom and number
    If collection id does exist and year/bottom/top and number are invalid, it will return all results
    '''
    def country_print(self,all,collection_id,year,decide,no):
        c = self.authenticate()

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


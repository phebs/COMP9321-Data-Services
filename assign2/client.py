from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse
import json
import requests
from assign import *
import re

app = Flask(__name__)
api = Api(app)


# The following is the schema of Book
#TODO needs to be changed
Economic_model = api.model('EconInd', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('q')


@api.route('/EconIndicator')
class ToPut(Resource):
    @api.expect(200,'Successfully printed all Economic Indicators')
    @api.doc(description="Retrieves all Economic Indicators")
    def get(self):
        response = db.read_all()
        return response,200

    @api.expect(201,"Successfully added into database")
    @api.expect(200,"Already on database")
    @api.expect(404,"Indicator ID doesn't exist")
    @api.doc(description="Adds particular indicator ID to the database")
    def post(self):
        content = request.json
        url_input = content.get("indicator_id")
        query = {"indicator": url_input}
        #Checks if it is in the database
        response = db.read_from(query,True)
        #If it is already on the database, return it
        if response is not None:
            print("Already found on the database")
            return response,200

        # Retreives 100 entries depending on what the place they want
        # Can use requests to fix it up
        url = 'http://api.worldbank.org/v2/countries/all/indicators/' + url_input + '?date=2012:2017&format=json&per_page=100'

        # Creates a response
        response = requests.get(url)
        data = json.loads(response.content)
        if (len(data)) == 2:
            db.createPayload(data[1])
            response = db.read_from(query,True)
            return response,201
        else:
            api.abort(404,"This indicator id doesn't exist")
            # if the data doesn't exist

@api.route('/EconIndicator/<int:collection_id>')
class ToCollectionID(Resource):
    @api.expect(200, "Successful showing")
    @api.doc(description="Lists the details of a particular collection id")
    def get(self,collection_id):
        query = {"collection_id": collection_id}
        abbreviate = False
        #TODO if collection id doesn't exist
        response = db.read_from(query,abbreviate)
        # print(response)
        return response,200

    @api.expect(200,"Succesfully deleted")
    @api.expect(404,"Collection ID doesn't exist")
    @api.doc(description="Deletes data according to collection ID")
    def delete(self,collection_id):
        query = { "collection_id": collection_id }
        notime = db.delete(query)
        if notime < 1:
            return {collection_id: "Doesn't exist"},404
        return {"message": "Collection = " + str(collection_id) + " is removed from the database!"},200

@api.route('/EconIndicator/<int:collection_id>/<year>')
class queryTopBot(Resource):
    @api.expect(404,"Either number/collection id/query doesn't exist")
    @api.expect(200,"Retrieved the certain number of countries")
    @api.expect(parser, validate=True)
    @api.doc(description="Finds the top-bottom results")
    def get(self, collection_id, year,):
        args = parser.parse_args()
        query = args.get('q')
        # query = request.args.get('q')
        print(query)
        match = re.match(r'(top|bottom)([0-9]+)', query, re.M | re.I)
        if match:
            decide = match.group(1)
            no = int(match.group(2))
            if no > 0 and no <= 100:
                result = db.country_print(collection_id, year, decide, no)
                #TODO check to make sure that the year and collection ID exists
                return result,200
            else:
                api.abort(404, "Number is not within the range")
        else:
            api.abort(404, "Query is not correct")


@api.route('/EconIndicator/<int:collection_id>/<year>/<country>')
class queryYrD(Resource):
    @api.doc(description="Searches for a country that fits the criteria")
    @api.expect(200,"Successfully found")
    @api.expect(400,"CollectionID/Year/Country doesn't exist")
    def get(self,collection_id,year,country):
        query = {"collection_id": collection_id}
        result = db.queryYD(query,collection_id,year,country)
        if result:
            return result,200
        else:
            api.abort(400,"This year and country doesn't exist")



if __name__ == '__main__':
    # Database details
    db_name = 'my-database'
    mongo_port = 27872
    mongo_host = 'ds127872.mlab.com'
    collection = 'EconomicIndicator'
    # Creates the database class
    db = database(mongo_port, mongo_host, db_name, collection)
    # run the application
    app.run(debug=True)




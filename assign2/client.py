from flask import Flask, request
from flask_restplus import Resource, Api, fields
import json
import requests
from assign import *
app = Flask(__name__)
api = Api(app)


# The following is the schema of Book
#TODO needs to be changed
book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

@api.route('/EconIndicator')
class ToPut(Resource):
    def post(self):
        content = request.json
        url_input = content.get("indicator_id")
        query = {"indicator": url_input}
        #Checks if it is in the database
        response = db.read_from(query)
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
            response = db.read_from(query)
            return response,201
        else:
            api.abort(400,"This indicator id doesn't exist")
            # if the data doesn't exist

@api.route('/EconIndicator/<int:collection_id>')
class ToDelete(Resource):
    def get(self,collection_id):
        query = { "collection_id": collection_id }
        notime = db.delete(query)
        if notime < 1:
            return {collection_id: "Doesn't exist"},404
        return {collection_id: "is now deleted"},200



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




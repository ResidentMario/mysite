from pymongo import MongoClient
import random
import json


class DataStore:
    """
    Class encoding the Citibike data storage layer. This file is a direct copy of the one in the `citibike` project
    repository.
    """

    def __init__(self, credentials_file="mlab_instance_api_key.json"):
        """
        Initializes a connection to an mLab MongoDB client.
        """
        with open(credentials_file) as cred:
            uri = json.load(cred)['uri']
        self.client = MongoClient(uri)
        self.bikeweeks = self.client['citibike']['bike-weeks']

    def insert(self, bikeweek):
        """
        Insert a single bikeweek into the database. Returns an inspectable result object, with e.g. `acknowledged` and
        `inserted_id` fields.
        """
        return self.bikeweeks.insert_one(bikeweek)

    def delete_all(self):
        """
        Clears the entire database. Only useful for testing. Don't do this actually.
        """
        self.bikeweeks.delete_many({})

    def delete(self, document_id):
        """
        Deletes a single entry, by document id (as returned by e.g. `result.inserted_id`). only useful for testing.
        """
        return self.bikeweeks.delete_one({'_id': document_id})

    def select_all(self):
        """
        Returns all documents in the data store.
        """
        return self.bikeweeks.find({})

    def sample(self):
        """
        Returns a single random bikeweek from storage.
        """
        r = random.randint(0, self.bikeweeks.count({}) - 1)
        sample = self.bikeweeks.find({}).limit(1).skip(r).next()
        # _id is a BSON parameter which can technically be extended, but since I don't need the object anyway I can
        # safely delete it.
        del sample['_id']
        return sample

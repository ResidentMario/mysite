# import requests
# import zipfile
# import os
# import io
# import pandas as pd
# import googlemaps
# import json
# import numpy as np
# import geojson
# from polyline.codec import PolylineCodec
# from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import pymongo
import random


class DataStore:
    """
    Class encoding the Citibike data storage layer.
    """

    # INITIALIZATION
    def __init__(self, uri):
        """
        Initializes a connection to a MongoDB database.
        """
        try:
            # TODO: Raise this for production.
            client = MongoClient(uri, serverSelectionTimeoutMS=1)
            client.server_info()
        except ServerSelectionTimeoutError as err:
            raise err
        self.client = client
        # If an index on (start station id, end station id) pairs have not already been created, create it.
        # This operation is idempotent, if the index already exists it does nothing.
        self.client['citibike']['trip-geometries'].create_index([('start station id', pymongo.ASCENDING),
                                                                 ('end station id', pymongo.ASCENDING)])

    # INSERTION
    def update_trip_id_list(self, new_ids):
        """
        Updates the list of trip ids stored in the "citibike-keys" store to include the additional ones.
        """
        unique_ids = set(self.get_all_trip_ids()).union(new_ids)
        self.client['citibike']['citibike-trip-ids'].update({'name': 'id-list'},
                                                            {'name': 'id-list', 'id-list': list(unique_ids)},
                                                            upsert=True)

    def insert_trip(self, trip):
        """
        Inserts a single trip (either a BikeTrip or a RebalancingTrip) into the database.
        """
        path = self.client['citibike']['trip-geometries'].find_one({
            'start station id': trip['start station id'],
            'end station id': trip['end station id']
        })
        reverse_path = self.client['citibike']['trip-geometries'].find_one({
            'start station id': trip['end station id'],
            'end station id': trip['start station id']
        })
        if path:
            # The geometry has already been stored in the database. Do nothing.
            pass
        elif reverse_path:
            # The geometry has already been stored in the database, just backwards. Do nothing.
            pass
        else:
            # The geometry has not already been stored in the database, so insert it (if it's a BikeTrip!).
            if isinstance(trip, BikeTrip):
                self.client['citibike']['trip-geometries'].insert_one({
                    'start station id': trip['start station id'],
                    'end station id': trip['end station id'],
                    'coordinates': trip['coordinates']
                })
            else:  # I don't cache rebalancing trip geometry; that's stored inline.
                pass
        self.client['citibike']['citibike-trips'].insert_one(trip.data)
        self.update_trip_id_list([trip.id])

    # GETTER
    def get_trip_by_id(self, tripid):
        """
        Returns a trip selected by its ID.

        If the trip is missing this method returns None.
        """
        trip = self.client['citibike']['citibike-trips'].find_one({"properties.tripid": tripid})
        if trip:
            del trip['_id']
            if trip['properties']['usertype'] == "Rebalancing":
                return trip
            else:
                path = self.client['citibike']['trip-geometries'].find_one({
                    'start station id': trip['properties']['start station id'],
                    'end station id': trip['properties']['end station id']
                })
                if path:
                    coordinates = path['coordinates']
                else:
                    path = self.client['citibike']['trip-geometries'].find_one({
                        'start station id': trip['properties']['end station id'],
                        'end station id': trip['properties']['start station id']
                    })
                    coordinates = path['coordinates'][::-1]
                trip['geometry']['coordinates'] = coordinates
                return trip
        else:
            return None

    def get_station_bikeset(self, station_id, mode):
        """
        This is it, folks---this is the core method which gets called when the front-end requests a station bikeset
        off of an id. Everything else that's been implemented here is in support of this ultimate end goal.
        """
        tripset = self.client['citibike']['station-indices'].find_one({'station id': station_id})['tripsets'][mode]
        # trips = self.client['citibike']['citibike-trips'].find({'properties.tripid': {"$in": tripset}})
        # for trip in trips:
        #     print(trip)
        ret = []
        for trip_id in tripset:
            ret.append(self.get_trip_by_id(trip_id))
        return ret

    # UTILITY
    def delete_all(self):
        """
        Flushes the entire database down the toilet. Only useful for testing. Don't do this actually.
        """
        self.client['citibike']['citibike-trips'].delete_many({})
        self.client['citibike']['citibike-trip-ids'].delete_many({})
        self.client['citibike']['citibike-geometries'].delete_many({})

    def get_all_trip_ids(self):
        """
        Returns all of the trip ids stored in the "citibike-keys" store.

        Note: this does not associate any geometries with those trips!
        """
        try:
            keystore = self.client['citibike']['citibike-trip-ids'].find({'name': 'id-list'}).next()
            return keystore['id-list']
        except StopIteration:  # empty database
            return []

    def sample(self, n):
        """
        Samples n random trips from the data store.
        """
        samples = []
        r_s = random.sample(self.get_all_trip_ids(), n)
        for r in r_s:
            samples.append(self.get_trip_by_id(r))
        return samples

    def iter_all(self):
        """
        Returns an iterator cursor which lets you do something to every object in the datastore.
        """
        return self.client['citibike']['citibike-trips'].find({})

    def replace_trip(self, tripid, new_repr):
        """
        Replaces the trip in question with another.
        """
        return self.client['citibike']['citibike-trips'].update({'tripid': tripid}, {"$set": new_repr}, upsert=False)

    def close(self):
        """
        Close the database (pass-through wrapper).
        """
        self.client.close()

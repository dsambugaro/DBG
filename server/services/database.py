#!/usr/bin/env python3


from pymongo import MongoClient


class Database:

    host = 'localhost'
    port = 27017

    def __init__(self, colection_name):
        self.client = MongoClient(self.host, self.port)
        self.colection_name = colection_name

    def connect(self):
        return self.client

    def insert(self, data):
        db = self.connect()
        colection = db.DBG[self.colection_name]
        if type(data) is list:
            return colection.insert_many(data)
        else:
            return colection.insert_one(data)
        db.close()

    def find_by_id(self, id):
        db = self.connect()
        colection = db.DBG[self.colection_name]
        result = colection.find_one({"_id": id})
        db.close()
        return result

    def find_by_score(self, order):
        #find scores ordered by highest or lowest
        db = self.connect()
        colection = db.DBG[self.colection_name]
        if order == 'high':
            result = colection.find.sort("score".DESCENDING)
            return result
        else:
            result = colection.find.sort("score".ASCENDING)
            return result
        db.close()

    def find_by_latest(self):
        #find scores ordered by latest updates
        db = self.connect()
        colection = db.DBG[self.colection_name]
        result = colection.find.sort("last_updated".DESCENDING)
        return result

    def update(self, id, update_query):
        db = self.connect()
        colection = db.DBG[self.colection_name]
        result = colection.update_one({'_id': id}, update_query)
        db.close()
        return result

    def delete(self, id):
        db = self.connect()
        colection = db.DBG[self.colection_name]
        result = colection.delete_one({'_id': id})
        db.close()
        return result

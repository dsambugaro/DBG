#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient


class Database:

    host = 'localhost'
    port = 27017

    def connect(self):
        return MongoClient(self.host, self.port)

    def insert(self, colection_name, data):
        db = self.connect()
        colection = db[colection_name]
        if type(data) is list:
            return colection.insert_many(data)
        else:
            return colection.insert_one(data)
        db.close()

    def find_by_id(self, colection_name, id):
        db = self.connect()
        colection = db[colection_name]
        result = colection.find_one({"_id": id})
        db.close()
        return result

    def find_by_filter(self, colection_name, filters):
        db = self.connect()
        colection = db[colection_name]
        result = colection.find_one(filters)
        db.close()
        return result

    def update(self, colection_name, id, update_query):
        db = self.connect()
        colection = db[colection_name]
        result = colection.update_one({'_id': id}, update_query)
        db.close()
        return result

    def delete(self, colection_name, id):
        db = self.connect()
        colection = db[colection_name]
        result = colection.delete_one({'_id': id})
        db.close()
        return result



import pymongo as mongo
from pymongo.errors import BulkWriteError

from core.constants import  getlog,DBPATH


class DbClient(object):

    def __init__(self, database=None, collection=None):
        self.log = getlog()
        self.database = database
        self.collection = collection
        self.collectiondb = None
        self.client = None
        self.conectdb()

    def conectdb(self):
        try:
            self.client = mongo.MongoClient(DBPATH)
            info = self.client.server_info()
            #self.log.info("Connected MongoDB ")
            return True
        except mongo.errors.ServerSelectionTimeoutError as err:
            self.log.error(repr(err))
            return False
        except Exception as err:
            self.log.error(repr(err))
            return False

    def check_field(self):
        if self.database == None or self.database == None:
            self.log.error("please choose databasename or collection,by calling setdatabase orsetcollection ")
            return False
        return True

    def set_database(self, database):
        self.database = database

    def set_collection(self, collection):
        self.collection = collection

    def collections(self):
        if self.check_field() == False: return
        database = self.client[self.database]
        collection = database.collection_names(include_system_collections=False)
        return collection

    def databases(self):
        return self.client.database_names()

    def check_being(self,filter):
        collection = self.get_collection()
        return collection.find(filter).count()


    def get_collection(self):
        if self.check_field() == False: return
        database = self.client[self.database]
        collection = database[self.collection]
        return collection

    def insert(self, item):
        try:
            collection = self.get_collection()
            res = collection.insert_one(item)
            self.log.info("User Registered Succesfuly: %s "%str(res.inserted_id))
            return 0
        except mongo.errors.DuplicateKeyError as  exp:
            self.log.error(repr(exp))
            self.update(item)
            return -1
        except Exception as  exp:
            self.log.error(repr(exp))
            return -2

    def insert(self, item):
        try:
            collection = self.get_collection()
            res = collection.insert_one(item)
            #self.log.info("Inserted Succesfully: %s " % str(res.inserted_id))
            return 0
        except mongo.errors.DuplicateKeyError as  exp:
            self.log.error(repr(exp))
            return -1           #duplicate
        except Exception as  exp:
            self.log.error(repr(exp))
            return -2


    def get_documents(self, filter):
        collection = self.get_collection()
        try:
            result = collection.find(filter)
            #self.log.info("Get User Succesfully")
            return list(result)[0]
        except Exception as  exp:
            #self.log.error(repr(exp))
            return -1



"""
data=DbClient("P2PApp","authentication")



print(data.get_documents(filter={"_id": "fatih",}))
"""
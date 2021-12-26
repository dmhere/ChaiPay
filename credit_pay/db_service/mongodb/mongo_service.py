from pymongo import MongoClient
import logging
import json
from credit_pay.utilities.encryptor import Encryptor
import urllib.parse

_logger = logging.getLogger()
decryption_service = Encryptor.decrypt


class MongoDBClient:
    client = None

    def __init__(self):
        import os
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'mongo_config.json')
        with open(file_path, 'r') as f:
            DB_INFO = json.load(f)
            pass
        server = DB_INFO['server']
        port = DB_INFO['port']
        user = DB_INFO['user']
        password = DB_INFO['password']
        db_schema = DB_INFO['schema']

        self.schema = db_schema
        connection_url = "mongodb://" + Encryptor.decrypt(user) + ":" + (urllib.parse.quote_plus(decryption_service(password))) \
                     + "@" + server + ":" + str(port) + "/" + db_schema

        _logger.debug('connection url ' + connection_url)
        try:
            MongoDBClient.client = MongoClient(connection_url)
        except Exception as e:
            _logger.error("Client setup failed as {}".format(e))

    def __del__(self):
        if MongoDBClient.client is not None:
            MongoDBClient.client.close()

    def get(self, collection_name, qfilter=None, **kwargs):
        db = MongoDBClient.client[self.schema]
        collection = db[collection_name]
        data = {}
        data_list = []
        data.update(**kwargs)
        try:
            if data:
                if qfilter is not None:
                    result = collection.find(data, qfilter)
                else:
                    result = collection.find(data)
            else:
                if qfilter is not None:
                    result = collection.find(qfilter)
                else:
                    result = collection.find()
            for data in result:
                del data['_id']
                data_list.append(data)
        except Exception as e:
            _logger.error("get data - error {}".format(e))
        return data_list

    def save(self, collection_name, data, **kwargs):
        db = MongoDBClient.client[self.schema]
        collection = db[collection_name]
        try:
            find = {}
            find.update(kwargs)
            collection.update(find, data, upsert=True)
            _logger.debug("data inserted with condition check {} to collection {}".format(find, collection_name))
        except Exception as e:
            _logger.error("save data error {}".format(e))

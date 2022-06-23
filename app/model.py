import datetime
from pymongo import MongoClient


class connDbMongo:
    """Класс для подключения к базе монго"""
    localhost = "127.0.0.1"
    portDB = 27017

    def __init__(self):
        self.client = MongoClient(host=self.localhost, port=self.portDB)
        self.db = self.client['steamShop']

    def savingCookies(self, cookies):
        """Метод для сохранения куки в бд"""
        collection = self.db['cookies']
        collection.delete_many({"_id": 11111})
        payload = {
            "_id": 11111,
            "cookies": cookies,
            "date&time": datetime.datetime.utcnow(),
        }
        rezult = collection.insert_one(payload)
        return rezult.acknowledged

    def loadCookies(self):
        """Метод для загрузки куков"""
        collection = self.db['cookies']
        rezult = collection.find_one({"_id": 11111})
        if rezult:
            return rezult['cookies']


connM = connDbMongo()
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
        collection.insert_one(payload)

    def loadCookies(self):
        """Метод для загрузки куков"""
        collection = self.db['cookies']
        rezult = collection.find_one({"_id": 11111})
        if rezult:
            return rezult['cookies']

    def saveMyInventory(self, inventory):
        """Метод для сохранения инвентаря общего файла"""
        collection = self.db['inventory']
        collection.delete_many({"_id": 22222})
        payload = {
            "_id": 22222,
            "invent": inventory,
            "date&time": datetime.datetime.utcnow(),
        }
        collection.insert_one(payload)

    def loadMyInventory(self):
        """Метода для загрузки общего файла инвентаря"""
        collection = self.db['inventory']
        return collection.find_one({"_id": 22222})['invent']

    def loadMyItem(self, market_hash_name, currentSailStatus):
        collection = self.db['item']
        load = {
            "market_hash_name": market_hash_name,
            "currentSailStatus": currentSailStatus,
            "date&time": datetime.datetime.utcnow(),
        }
        return collection.insert_one(load).acknowledged

    def saveShopItem(self, lst):
        """Метод для сохранения предмета который продается в стиме"""
        collection = self.db['shopItem']
        for item in lst:
            try:
                load = {
                    "market_name": item['market_item_name'],
                    "currentSailStatus": item,
                    "date&time": datetime.datetime.utcnow(),
                    }
                collection.insert_one(load)
                print(f'Item - {item["market_item_name"]} успешно добавлен')
            except Exception as e:
                print(f'Не удалось добавить в базу {item["market_item_name"]} ошибка - {e}')

    def saveUnicShoplist(self, lst):
        """Метод для записи уникальных предметов в базу"""
        try:
            collection = self.db['itemList']
            collection.delete_many({"_id": 12345,})
            load = {
                "_id": 12345,
                "UnicList": lst,
                "date&time": datetime.datetime.utcnow(),
            }
            collection.insert_one(load)
        except Exception as e:
            print(f'записать общий список товаров не удалось, ошибка - {e}')

    def loadTUnicShopList(self):
        """Метод для загрузки списка уникальных предметов с базы"""
        collection = self.db['itemList']
        return collection.find_one({"_id": 12345})["UnicList"]


connM = connDbMongo()
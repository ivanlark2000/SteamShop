from model import connM
from config import config


class ItemSteamShop:
    """Создает объект предмета в магазине стимa"""
    def __init__(self, hash_name):
        try:
            self.hash_name = hash_name
            self.listInbd = [i for i in connM.loadShopItem(hash_name)]
            self.normal_price = self.listInbd[-1]["currentSailStatus"]["normal_price"]
            self.sale_price = self.listInbd[-1]["currentSailStatus"]["sale_prices"]
            self.gty = self.listInbd[-1]["currentSailStatus"]["qty"]
            self.difference = self.listInbd[-1]["currentSailStatus"]["normal_price"]-self.listInbd[-2]["currentSailStatus"]["normal_price"]
        except:
            self.hash_name = hash_name
            self.listInbd = [i for i in connM.loadShopItem(hash_name)]
            self.normal_price = 0
            self.sale_price = 0
            self.gty = 0
            self.difference = 0


class MySteamShop:
    """Клас инвентаря в магазине
        param:
            self.total_list - общий список предметов
            self.total_count - общая стоимость переметов в инвентаре"""
    def __init__(self):
        self.total_list = [descriptions['market_hash_name'] for descriptions in connM.loadMyInventory()['descriptions']]
        self.total_count = connM.loadMyInventory()['total_inventory_count']

    def count_current_inventory(self):
        """Метод, который подсчитывает текущую сумму всех предметов в инвентаре"""
        count = 0
        summa = 0
        for item in self.total_list:
            rez = ItemSteamShop(item)
            summa = summa + rez.normal_price
            count += 1
        return count, summa

    def showCurrentPrice(self):
        """Метод, который выводит в печать текущую цену всех предметов в аккаунте"""
        for item in self.total_list:
            rez = ItemSteamShop(item)
            if rez.normal_price != 0:
                print(f'{rez.hash_name} стоит {rez.normal_price:0.2f} руб')


class ItemInMyAccount:
    """Клас который создает обьект предмета в моей коллекции
        arg:
            # price - цена указывается в сотых без запятой
            # sessionid - id сессии
            # assetid - id предмета"""
    def __init__(self, hash_name):
        self.hash_name = hash_name
        self.cod_hash_name = self.hash_name.replace(" ", "%20")
        json = connM.loadMyInventory()
        for num in json['descriptions']:
            if num['market_hash_name'] == hash_name:
                self.classid = num['classid']
                self.instanceid = num['instanceid']
                break
        else:
            self.classid = None
            self.instanceid = None
        for num in json['assets']:
            if num['classid'] == self.classid and num['instanceid'] == self.instanceid:
                self.assetid = num['assetid']
                self.amount = num['amount']
                break
        else:
            self.assetid = None
            self.amount = None
        if None in (self.amount, self.assetid, self.instanceid, self.classid):
            self.rez = False
        else:
            self.rez = True

    def sellItem(self, price, amount=1):
        """Функция по продаже предмета"""
        url = "https://steamcommunity.com/market/sellitem/"
        payload = {
            "sessionid": config.sessionid,
            "appid": 570,
            "contextid": 2,
            "assetid": self.assetid,
            "amount": amount,
            "price": price,
            }
        response = config.session.post(url, data=payload, headers=config.headers)
        return response.json()["success"]

    def pricehistory(self):
        """Функция для вывода истории цен"""
        url = f"https://steamcommunity.com/market/pricehistory/?appid=570&market_hash_name={self.cod_hash_name}"
        response = config.session.get(url, headers=config.headers)
        return response.json()


myshop = MySteamShop()

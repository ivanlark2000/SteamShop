import math
import time

from model import connM
from config import config
from bs4 import BeautifulSoup as Bs
from statistics import mean


class ItemSteamShop:
    """Создает объект предмета в магазине стимa"""
    def __init__(self, hash_name):
        try:
            self.hash_name = hash_name
            self.code_hash_name = self.hash_name.replace(" ", "%20")
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

    def getSellInfo(self, page=0):
        """Метод, который выводит информацию о продуваемых предметах
        param
            page - страница продаваемых предметов"""
        url = f"https://steamcommunity.com/market/listings/570/{self.code_hash_name}/render"
        paydata = {
                'query': "",
                'start': page * 10,
                'count': 10,
                'country': 'RU',
                'language': 'russian',
                'currency': 5,
        }
        response = config.session.get(url, params=paydata, headers=config.headers)
        html = response.json()['results_html']
        soup = Bs(html, 'html.parser')
        rez = soup.find_all("span", class_="market_listing_price market_listing_price_with_fee")
        list_price_with_fee = [float(i.text.strip()[:-5].replace(",", '.')) for i in rez]
        rez = soup.find_all("span", class_="market_listing_price market_listing_price_with_publisher_fee_only")
        list_publisher_fee_only = [float(i.text.strip()[:-5].replace(",", '.')) for i in rez]
        rez = soup.find_all("span", class_="market_listing_price market_listing_price_without_fee")
        list_price_without_fee = [float(i.text.strip()[:-5].replace(",", '.')) for i in rez]
        rez = soup.select('span', clas_="market_listing_item_name")
        list_id_salesman = []
        for i in rez:
            try:
                list_id_salesman.append(int(i['id'][8:-5]))
            except:
                continue
        print(mean(list_price_without_fee[4:]) - list_price_without_fee[1])
        print(list_id_salesman)
        print(list_price_with_fee)
        print(list_publisher_fee_only)
        print(list_price_without_fee)

    def bayitem(self, id_salesman, price, qty=1):
        """Метод, для покупки самого дешевого предмета
        param
            id_salesman - ай ди продавца
            """
        url = f"https://steamcommunity.com/market/buylisting/{id_saleaman}"
        fee = math.floor(price * 0.1) + math.floor(price * 0.05)
        payload = {
                'sessionid': config.sessionid,
                'currency': 5,
                'subtotal': price,
                'fee': fee,
                'total': price + fee,
                'quantity': qty,
                'billing_state': "",
                'save_my_address': 0,
        }
        response = config.session.post(url, data=payload, headers=config.headers)
        data = response.json()


class MySteamShop:
    """Клас инвентаря в магазине
        param:
            self.total_list - общий список предметов
            self.qty - количество предметов в инвентаре
            self.total_count - общая стоимость переметов в инвентаре"""

    def __init__(self):
        self.updateInventory()
        self.total_list = [descriptions['market_hash_name'] for descriptions in connM.loadMyInventory()['descriptions']]
        self.gty = len(self.total_list)
        self.total_count = connM.loadMyInventory()['total_inventory_count']

    def updateInventory(self):
        """Метод, длля обновления инвентаря в базе данных"""
        response = config.session.get(
            'https://steamcommunity.com/inventory/76561198173160771/570/2?l=russian&count=5000',
            headers=config.headers)
        connM.saveMyInventory(response.json())

    def saleALLitems(self):
        """Метод, для продажи всех айтемов с магазина стим из аккаунта"""
        count, total = 1, 1
        sum = 0
        for i in self.total_list:
            item = ItemInMyAccount(i)
            price = item.gettingPriceGoods()
            time.sleep(5)
            if price:
                rez = item.sellItem(price=price*100)
                if rez['success']:
                    print(f'Предмет №{count} {i} - успешно выставлен на продажу по цене - {price}')
                    sum += price
                else:
                    print(f"Предмет №{count} {i} не выставлен на продажу - {rez['message']}")
                    total += 1
                time.sleep(5)
                count += 1
        print(f'В итоге было выставлено на продажу {total} предметов на общую стоимость {sum}')

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
    """Клас который создает объект предмета в моей коллекции
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

    def gettingPriceGoods(self):
        """Метод, для вывода текущей цены предмета"""
        URL = "https://steamcommunity.com/market/priceoverview/"
        params = {
            'country': 'RU',
            'currency': 5,
            'appid': 570,
            'market_hash_name': self.hash_name
        }
        try:
            response = config.session.get(URL, params=params, headers=config.headers)
            return float(response.json()['lowest_price'][:-5].replace(",", '.'))
        except Exception as e:
            print(f'Произошла ошибка при получении информации и цене о предмете {self.hash_name}. Ошибка - {e}')

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
        return response.json()

    def pricehistory(self):
        """Функция для вывода истории цен"""
        url = f"https://steamcommunity.com/market/pricehistory/?appid=570&market_hash_name={self.cod_hash_name}"
        response = config.session.get(url, headers=config.headers)
        return response.json()


myshop = MySteamShop()

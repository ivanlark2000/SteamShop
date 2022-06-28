import json
import time
import random
import requests
from objectItem import myshop
from model import connM
from config import config
from datetime import datetime
from objectItem import ItemSteamShop
from bs4 import BeautifulSoup as Bs


def gettingList(html):
    """Функция получения списка истории продажи товара и цен"""
    soup = Bs(html, 'html.parser')
    rez = soup.find_all('script')[-1].contents[0]
    return eval(rez[rez.find('[['):rez.find(']]') + 2])


def gettingJsonofGood():
    """Получаем список товаров в аккаунте"""
    url = "https://steamcommunity.com/profiles/76561198173160771/inventory/"
    url_json = "https://steamcommunity.com/inventory/76561198173160771/570/2?l=russian&count=5000"
    config.session.get(url, headers={'User-Agent': config.useragent})
    response = config.session.get(url_json)
    connM.saveMyInventory(response.json())


def gettingLstshop():
    """Функция, которая выводит список товаров в личном кабинете"""
    response = config.session.get('https://steamcommunity.com/inventory/76561198173160771/570/2?l=russian&count=5000')
    data = response.json()
    descriptions = data['descriptions']
    lstHashName = [key['market_hash_name'] for key in descriptions]
    return lstHashName


def gettingPriceGoods(market_hash_name):
    """Функция для вывода текушей цены предмета"""
    URL = "https://steamcommunity.com/market/priceoverview/"
    params = {
        'country': 'RU',
        'currency': 5,
        'appid': 570,
        'market_hash_name': market_hash_name
    }
    try:
        response = config.session.get(URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        print(f'Произошла ошибка при получении информации и цене о предмете. Ошибка - {e}')


def gettindHtmlGood(market_hash_name):
    """функция для получение страницы товара"""
    url = 'https://steamcommunity.com/market/listings/570/' + market_hash_name.replace(' ', '%20')
    response = config.session.get(url)
    return response.text


def getting():
    """Функция получения цен всех активных товаров в магазине"""
    lstHashName = gettingJsonshop()
    for market_hash_name in lstHashName:
        data = gettingPriceGoods(market_hash_name)
        try:
            print(f'Название товара: {market_hash_name}, Макс цена - {data["median_price"]}, Мин цена - '
                  f'{data["lowest_price"]}, продано за 24 часа - {data["volume"]}')
        except:
            print(f'Название товара: {market_hash_name}, нельзя продать')
        finally:
            time.sleep(1)


def loaadingIteminBase():
    """Функция для загрузки текуших цен в базу данных"""
    lstHashName = gettingLstshop()
    for hashName in lstHashName:
        time.sleep(5)
        sailStatus = gettingPriceGoods(market_hash_name=hashName)
        if sailStatus is not None and connM.loadItem(market_hash_name=hashName, currentSailStatus=sailStatus):
            print(f"Предмет {hashName} добавлен успешно")
        else:
            print(f"Предмет {hashName} не был добавлен")


def gettingJson(page=1):
    """Функция для получения списка json со страницы"""
    url = 'https://steamcommunity.com/market/search/render/'
    page = (page * 10) - 10
    payload = {
        'query': '',
        'start': page,
        'count': 10,
        'search_descriptions': 0,
        'sort_column': 'popular',
        'sort_dir': 'desc',
        'appid': 570,
    }
    try:
        response = config.session.post(url, params=payload)
        return response.json()
    except Exception as e:
        time.sleep(60)
        return False


def gettingListonPage(page=1):
    """Функция парсинга Json итемов страницы"""
    while True:
        try:
            data = gettingJson(page)
            soup = Bs(data['results_html'], 'html.parser')
            itms = soup.select(".market_listing_item_name")
            qtys = soup.select(".market_listing_num_listings_qty")
            normal_prices = soup.select(".normal_price")
            normal_price_list = [int(normal_price.get('data-price'))/100 for normal_price in normal_prices if normal_price.get('data-price')]
            sale_prices = soup.select('.sale_price')
            sale_price_list = [float(sale_price.text[:-5].replace(',', '.')) for sale_price in sale_prices]
            market_item_name_list = [item.text for item in itms]
            qty_list = [int(qty['data-qty']) for qty in qtys]
            itms_list = []
            for i in range(10):
                itmsPars = {
                    'market_item_name': market_item_name_list[i],
                    'qty': qty_list[i],
                    'normal_price': normal_price_list[i],
                    'sale_prices': sale_price_list[i],
                }
                itms_list.append(itmsPars)
            return itms_list, market_item_name_list
        except:
            print(f"Происходит обновление куков")
            config.updateCookies()
            time.sleep(20)


def creatingUnicShopList(lst):
    """Функция для создания уникального списка товаров по категории в магазине в базе"""
    connM.saveUnicShoplist(list(set(lst) | set(connM.loadTUnicShopList())))


def parsingAllShopItem():
    """Функция, которая запускает парсинг магазина"""
    count = 0
    time_start = datetime.now()
    totalPage = int(gettingJson()['total_count']) / 10
    pause = (12 * 60 * 60) / totalPage
    lst = list(range(1, int(totalPage) + 1))
    while len(lst) != 0:
        page = random.choice(lst)
        lst.remove(page)
        itms_list, market_item_name_list = gettingListonPage(page)
        count = connM.saveShopItem(lst=itms_list, count=count)
        creatingUnicShopList(market_item_name_list)
        time.sleep(pause)
    print(f'Цикл сканирование предметов по Доте 2 закончен.'
          f'\n{count} - предметов в данный момент в магазине.'
          f'\n{time_start} - начало цикла парсинга предметов в магазине Стим Дота 2.'
          f'\n{datetime.now()} - время окончания цикла парсинга предметов в магазине Стим Дота 2.'
          f'\n{datetime.now() - time_start} - время затрачено.')


def gettingDifference():
    """Функция, которая выдает предметы которые вырасти в цене на 10 руб"""
    for item in connM.loadTUnicShopList():
        try:
            itemShop = ItemSteamShop(item)
            if itemShop.difference > 10:
                print(f'{item} вырос на {itemShop.difference} руб - стоимость сейчас {itemShop.normal_price}')
        except:
            continue


def main():
    # registration()
    parsingAllShopItem()
    # gmail.cleaningAllemail()
    # gettingDifference()
    # myshop.showCurrentPrice()
    # myshop.count_curent_inventory()


if __name__ == "__main__":
    main()

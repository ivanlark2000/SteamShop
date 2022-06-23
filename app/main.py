import json
import time
import requests
from model import connM
from config import config
from gmailcom import gmail
from selenium import webdriver
from bs4 import BeautifulSoup as Bs
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def registration():
    """Функция для регистрации в стиме"""
    login_url = "https://store.steampowered.com/login"
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(login_url)
    element_log = driver.find_element_by_name('username')
    element_log.send_keys(config.loginSteam)
    time.sleep(1)
    element_passw = driver.find_element_by_name('password')
    element_passw.send_keys(config.pwdSteam)
    time.sleep(2)
    element_submit = driver.find_element_by_id('login_btn_signin')
    element_submit.click()
    time.sleep(2)
    element_code = driver.find_element_by_id('authcode')
    time.sleep(5)
    gmail = Gmail()  # Создаем подключение к почте
    element_code.send_keys(gmail.gettingSteamCode())  # Вводим полученный код в стим
    time.sleep(2)
    element_submit_end = driver.find_element_by_id('success_continue_btn')
    element_submit_end.click()
    time.sleep(2)
    cookies = driver.get_cookies()
    connM.savingCookies(cookies)


def getSession():
    """Функция создания сессии"""
    global session
    with open('cookies.data', 'rb') as cookefile:
        cookies = pickle.load(cookefile)
    with requests.session() as session:
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])


def gettingList(html):
    """Функция получения списка истории продажи товара и цен"""
    soup = Bs(html, 'html.parser')
    rez = soup.find_all('script')[-1].contents[0]
    return eval(rez[rez.find('[['):rez.find(']]') + 2])


def gettingListofGood():
    """Получаем список товаров в аккаунте"""
    url = "https://steamcommunity.com/profiles/76561198173160771/inventory/#570"
    response = session.get(url, headers={'User-Agent': USERAGENT})
    response = session.get(url_json)
    return response.text


def gettingJsonshop():
    response = session.get('https://steamcommunity.com/inventory/76561198173160771/570/2?l=russian&count=5000')
    data = response.json()
    descriptions = data['descriptions']
    lstHashName = [key['market_hash_name'] for key in descriptions]
    return lstHashName


def gettingPriceGoods(market_hash_name):
    URL = "https://steamcommunity.com/market/priceoverview/"
    params = {
        'country': 'RU',
        'currency': 5,
        'appid': 570,
        'market_hash_name': market_hash_name
    }
    response = session.get(URL, params=params)
    data = response.json()
    return data


def gettindHtmlGood(market_hash_name):
    """функция для получение страницы товара"""
    url = 'https://steamcommunity.com/market/listings/570/' + market_hash_name.replace(' ', '%20')
    response = session.get(url)
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


def main():
    print(config.session)


if __name__ == "__main__":
    main()

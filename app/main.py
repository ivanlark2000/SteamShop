import json
import os
import pickle
import time
import requests
from bs4 import BeautifulSoup as Bs
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv(override=True)
LOGIN_STEAM = os.environ.get('login_steam')
PASSWORD_STEAM = os.environ.get('password_steam')
EMAIL = os.environ.get('email')
PASSWORD_EMAIL = os.environ.get('password_email')
USERAGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'




def gettingSteamCode():
    import email
    # message_from_bytes Функция из модуля электронной почты. Это поможет нам прочитать электронные письма, которые приходят как байты и преобразуют их в текст.
    from imaplib import IMAP4_SSL
    GOOGLE_HOST = "imap.gmail.com"
    PORT = 993
    with IMAP4_SSL(host=GOOGLE_HOST, port=PORT) as connection:
        connection.login(user=EMAIL, password=PASSWORD_EMAIL)
        connection.list()
        connection.select('inbox')  # Подключаемся к папке "входящие".
        _, msgnums = connection.search(None, "(SUBJECT 'Steam')")
        msgnum = msgnums[0].split()[-1]
        _, data = connection.fetch(msgnum, "(RFC822)")
        massage = email.message_from_bytes(data[0][1])
        for part in massage.walk():
            if part.get_content_type() == "text/plain":
                msg = part.as_string()
                code = msg[msg.find('Login Code') + 11:msg.find('Login Code') + 17]
        return code


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
    element_log.send_keys(LOGIN_STEAM)
    time.sleep(1)
    element_passw = driver.find_element_by_name('password')
    element_passw.send_keys(PASSWORD_STEAM)
    time.sleep(2)
    element_submit = driver.find_element_by_id('login_btn_signin')
    element_submit.click()
    time.sleep(2)
    element_code = driver.find_element_by_id('authcode')
    time.sleep(5)
    element_code.send_keys(gettingSteamCode())
    time.sleep(2)
    element_submit_end = driver.find_element_by_id('success_continue_btn')
    element_submit_end.click()
    time.sleep(2)
    cookies = driver.get_cookies()
    with open('cookies.data', 'wb') as cookefile:
        pickle.dump(cookies, cookefile)


def getSession():
    """Функция создания сессии"""
    global session
    with open('cookies.data', 'rb') as cookefile:
        cookies = pickle.load(cookefile)
    with requests.session() as session:
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])


def gettingList():
    url = "https://steamcommunity.com/market/listings/570/Lineage%20The%20Ram%27s%20Head%20Armaments"
    """Функция получения списка истории продажи товара и цен"""
    response = requests.get(url)
    soup = Bs(response.text, 'html.parser')
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
    with open("test.json", 'w') as file:
        json.dump(response.json(), file)


def gettingPriceAllGoods():
    TEST_URL = "https://steamcommunity.com/market/priceoverview/?country=RU&currency=5&appid=753&market_hash_name=502940-Bust"


def main():
    getSession()
    gettingJsonshop()


if __name__ == "__main__":
    main()

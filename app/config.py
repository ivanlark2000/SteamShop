import os
import time
import requests
from model import connM
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv(override=True)


class Config:
    """Класс с настройками и данными об окаунтах"""
    useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'

    def __init__(self):
        self.headers = None
        self.freshcookies = connM.loadCookies()
        self.loginSteam = os.environ.get('login_steam')
        self.pwdSteam = os.environ.get('password_steam')
        self.email = os.environ.get('email')
        self.pwdMail = os.environ.get('password_email')
        self.pwdbd = os.environ.get('password_db')
        self.loginDb = os.environ.get('login_db')
        self.session = requests.session()
        for i in self.freshcookies:
            try:
                if "sessionid" in i['name']:
                    self.sessionid = i['value']
                elif "browserid" in i['name']:
                    self.browserid = i['value']
                elif "steamLoginSecure" in i['name']:
                    self.steamLoginSecure = i['value']
                elif "timezoneOffset" in i['name']:
                    self.timezoneOffset = i['value']
                elif "_ga" in i['name']:
                    self._ga = i['value']
                elif "_gid" in i['name']:
                    self._gid = i['value']
            except:
                continue
        self.loadCookies()
        self.makeheaders()

    def loadCookies(self):
        """Метод, который загружает с базы и устанавливает куки в текущей сессии"""
        for cookie in self.freshcookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

    def makeheaders(self):
        """Метод, который создает заголовки"""
        cookie = f"sessionid={self.sessionid}; steamCountry=; timezoneOffset={self.timezoneOffset}; _ga={self._ga}; \
        _gid={self._gid}; browserid={self.browserid}; strInventoryLastContext=570_2; steamCurrencyId=5; \
        strResponsiveViewPrefs=desktop; steamMachineAuth76561198173160771=6ED75938E74A9C5ACC467E3AD57C3F912AA69D0D; \
        steamLoginSecure={self.steamLoginSecure}; steamRememberLogin=76561198173160771%7C%7C045934b0371e522183b1d56e514042a7; \
        webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22time_checked%22%3A1657194931%7D"
        self.headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            'Cookie': cookie,
            "Content-Length": "95",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "steamcommunity.com",
            "Origin": "https://steamcommunity.com",
            "Referer": "https://steamcommunity.com/profiles/76561198173160771/inventory/",
            "sec-ch-ua": '"Google Chrome";v="105", ")Not;A=Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 \
                                                    (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"
        }

    def updateCookies(self):
        """Метод, который создает или обновляет куки в базе данных"""
        try:
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
            element_code = driver.find_element_by_id('twofactorcode_entry')
            time.sleep(5)
            from gmailcom import gmail
            element_code.send_keys(input("Введите код"))  # Вводим полученный код в стим
            element_submit_end = driver.find_elements_by_id('login_twofactorauth_buttonset_entercode')
            driver.implicitly_wait(5)
            element_submit_end[0].click()
            time.sleep(2)
            cookies = driver.get_cookies()
            print(cookies)
            connM.savingCookies(cookies)
            self.loadCookies()
            print('Куки успешно обновлены')
            return True
        except Exception as er:
            print(f'Не удалось обновить куки, ошибка - {er}')


config = Config()

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
        self.loginSteam = os.environ.get('login_steam')
        self.pwdSteam = os.environ.get('password_steam')
        self.email = os.environ.get('email')
        self.pwdMail = os.environ.get('password_email')
        self.pwdbd = os.environ.get('password_db')
        self.loginDb = os.environ.get('login_db')
        self.session = requests.session()
        self.loadCookies()

    def loadCookies(self):
        """Метод, который загружает с базы и устанавливает куки в текущей сессии"""
        for cookie in connM.loadCookies():
            self.session.cookies.set(cookie['name'], cookie['value'])

    def updateCookies(self):
        """Метод, который создает или обновляет куки в базе данных"""
        try:
            login_url = "https://store.steampowered.com/login"
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--headless")
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
            from gmailcom import gmail
            element_code.send_keys(gmail.gettingSteamCode())  # Вводим полученный код в стим
            time.sleep(2)
            element_submit_end = driver.find_element_by_id('success_continue_btn')
            element_submit_end.click()
            time.sleep(2)
            cookies = driver.get_cookies()
            connM.savingCookies(cookies)
            self.loadCookies()
            print('Куки успешно обновлены')
            return True
        except Exception as er:
            print(f'Не удалось обновить куки, ошибка - {er}')
            time.sleep(120)
            return False


config = Config()
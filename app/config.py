import os
import pickle
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """Класс с настройками и данными об окаунтах"""
    useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'

    def __init__(self):
        self.loginSteam = os.environ.get('login_steam')
        self.pwdSteam = os.environ.get('password_steam')
        self.email = os.environ.get('email')
        self.pwdMail = os.environ.get('password_email')
        with open('cookies.data', 'rb') as cookefile:
            self.cookies = pickle.load(cookefile)
        with requests.session() as self.session:
            for cookie in self.cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])


config = Config()
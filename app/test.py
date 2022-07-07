import requests


def authorization():
    """Авторизация пользователя в стиме"""
    url = 'https://steamcommunity.com/login/dologin/'
    url2 = 'https://steamcommunity.com/login/getrsakey/'
    payload1 = {
        'donotcache': '1657119552602',
        'username': 'lark2000wf'
    }
    s = requests.session()
    response = s.post(url2, data=payload1)
    print(response.json())
    payload = {
        'donotcache': '1657118015721',
        'password': 'YIdPa1/fQjQ3WJeS3NuSxFTBy4IFe+DgxMlnqHB9JZz7mJMqJ+jPMETWy0Sb4EpGKq4kFa3M6dP7s260FBYCBEjTgxNIsI4KkcPNnLVkAWrxb0rq3mybVLSwU711hJ2yBDGCmpoZkPNCGdRUZVd3BP0Cdcx+b457+9JDlF2fJxUIrRhE0jhGmPRpZGccvBG/j+RfM3BFFRunAtnoqnAEDrr8JJqdMC22J9CbUbZnDOYnSILujV5CSvxG4p+az8FcO+LYdREPNgBinGF9vi0roiMFENvzJ/MvbPCeRIihpXIUEFE1iUbGBOTmFIZgVPb3KJaA0Urik1sW4vC8Ui1eCA==',
        'twofactorcode': '',
        'emailauth': '',
        'loginfriendlyname': '',
        'captchagid': -1,
        'captcha_text': '',
        'emailsteamid': '',
        'rsatimestamp': response.json()['timestamp'],
        'remember_login': 'true',
        'tokentype': '-1'
    }
    print(payload)
    response = s.post(url, data=payload)
    print(response.json())


authorization()
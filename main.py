import requests
from bs4 import BeautifulSoup as Bs


def gettingList():
    url = "https://steamcommunity.com/market/listings/570/Lineage%20The%20Ram%27s%20Head%20Armaments"
    """Функция получения списка истории продажи товара и цен"""
    response = requests.get(url)
    soup = Bs(response.text, 'html.parser')
    rez = soup.find_all('script')[-1].contents[0]
    return eval(rez[rez.find('[['):rez.find(']]') + 2])


def main():
    print(gettingList())


if __name__ == "__main__":
    main()
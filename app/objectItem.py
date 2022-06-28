from model import connM


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
    """Клас инвентаря в магазине"""
    def __init__(self):
        self.total_list = [descriptions['market_hash_name'] for descriptions in connM.loadMyInventory()['descriptions']]
        self.total_count = connM.loadMyInventory()['total_inventory_count']

    def count_curent_inventory(self):
        """Метод, который подсчитывает текущую сумму всех предметов в инвентаре"""
        count = 0
        for item in self.total_list:
            rez = ItemSteamShop(item)
            count = count + rez.normal_price
        return count

    def showCurrentPrice(self):
        """Метод, который выводит в печать текущую цену всех предметов в аккаунте"""
        for item in myshop.total_list:
            rez = ItemSteamShop(item)
            if rez.normal_price != 0:
                print(f'{rez.hash_name} стоит {rez.normal_price} руб')


myshop = MySteamShop()

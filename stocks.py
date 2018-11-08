from random import randint
import json
from math import floor

class Stocks():

    def __init__(self):
        with open('stocks.json', 'r') as stocks:
            self.stocks_data = json.loads(stocks.read())

    def create_company(self, name):
        pass

    def stocks_update_read(self):
        with open('stocks.json', 'r') as stocks:
            self.stocks_data = json.loads(stocks.read())

    def stocks_update(self):
        with open('stocks.json', 'w') as stocks:
            json.dump(self.stocks_data, stocks, indent=4)
        with open('stocks.json', 'r') as stocks:
            self.stocks_data = json.loads(stocks.read())

    def get_companies(self):
        companies = []
        for company in self.stocks_data['Stocks']:
            companies.append(company)
        return companies

    def update_stock_price(self, company, random=True):
        self.stocks_update_read()
        if random:
            current_stock_price = self.get_stock_price(company)
            up_down = randint(1, 2)
            if up_down == 1:
                down_percent = (randint(1, 45)/100)
                new_stock_price = floor(current_stock_price - (down_percent * current_stock_price))
                if new_stock_price < 10:
                    new_stock_price += 100
                self.stocks_data['Stocks'][company]['current-stock-price'] = new_stock_price
                with open('stocks.json', 'w') as stocks:
                    json.dump(self.stocks_data, stocks, indent=4)
                return {'price': new_stock_price, 'up-down': 'down', 'stock-name': company, 'company-name': self.stocks_data['Stocks'][company]['name'], 'down-percent': str(floor(down_percent * 100))}
            else:
                up_percent = (randint(1, 20)/100)
                new_stock_price = floor(current_stock_price + (up_percent * current_stock_price))
                if new_stock_price < 10:
                    new_stock_price += 100
                self.stocks_data['Stocks'][company]['current-stock-price'] = new_stock_price
                with open('stocks.json', 'w') as stocks:
                    json.dump(self.stocks_data, stocks, indent=4)
                return {'price': new_stock_price, 'up-down': 'up', 'stock-name': company, 'company-name': self.stocks_data['Stocks'][company]['name'], 'up-percent': str(floor(up_percent * 100))}

    def get_stock_count(self, userid, company):
        self.stocks_update_read()
        return self.stocks_data['Stocks'][company]['share-holders'][userid]

    def get_stock_price(self, company):
        self.stocks_update_read()
        return self.stocks_data['Stocks'][company]['current-stock-price']

    def add_stocks(self, company, stock_count, userid):
        try:
            self.stocks_data['Stocks'][company]['share-holders'][userid] += stock_count
        except:
            self.stocks_data['Stocks'][company]['share-holders'][userid] = stock_count
        self.stocks_update()

    def deduct_stocks(self, company, stock_count, userid):
        self.stocks_data['Stocks'][company]['share-holders'][userid] -= stock_count
        self.stocks_update()

    def get_user_stocks(self, userid):
        pass

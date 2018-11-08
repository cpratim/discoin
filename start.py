import os
from threading import Thread


def start_server():
    os.system('python3 server.py')

def start_stocks():
    os.system('python3 stock_updater.py')

def start_join():
    os.system('python3 on_join.py')

server = Thread(target=start_server)
stocks = Thread(target=start_stocks)
join = Thread(target=start_join)

server.start()
stocks.start()
join.start()

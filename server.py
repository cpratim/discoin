import asyncio
import discord
import re
import random
from ledger import Ledger
from stocks import Stocks
from random import randint
import json
import os
from messages import *

def get_ver_token(length=20):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    verification = ''
    for i in range(length):
        verification += charset[randint(0, len(charset) - 1)]
    return verification

def get_creds(ledger, message):
    reciever = ''
    print(message.content)
    try:
        reciever = re.findall(r'<@(.*?)>', str(message.content))[0]
        ledger.get_balance(reciever)
    except:
        reciever = re.findall(r'<@!(.*?)>', str(message.content))[0]
    sender = message.author.id
    amount = float(re.findall(r'<(.*?)>', str(message.content))[1])
    verification = get_ver_token()
    return {'sender': sender, 'reciever': reciever, 'amount': amount, 'verification': verification}

def verify_id(id):
    with open('info.json', 'r') as info_file:
        info = json.loads(info_file.read())
        trusted_users = info['trusted-users']
    for trusted in trusted_users:
        if trusted == id:
            return True
    return False

def get_token(message):
    token = re.findall(r'<(.*?)>', str(message.content))[0]
    return token


class Server():

    def __init__(self):
        self.ledger = Ledger()
        self.stocks = Stocks()
        self.prices = {
            'Rich': 2000,
            'Richard Rich': 3000,
            'Forbes Top 100': 5000,
            'Trump': 7000,
            'Bill Gates': 10000
        }

    def run(self):
        client = discord.Client()
        @client.event

        async def on_message(message):
            if message.content.startswith('!sendD'):
                creds = get_creds(self.ledger, message)
                validation = self.ledger.transfer(creds)
                sender_obj = discord.User(id=creds['sender'])
                if (validation):
                    reciever_obj = discord.User(id=creds['reciever'])
                    try:
                        await client.send_message(reciever_obj, transfer_message(creds, type='SUCCESS-RECIEVER'))
                        await client.send_message(sender_obj, transfer_message(creds, type='SUCCESS-SENDER'))
                        await client.send_message(message.channel, transfer_message(creds, type='SUCCESS-CHANNEL'))
                        await client.delete_message(message)
                    except:
                        pass
                else:
                    await client.send_message(sender_obj, transfer_message(creds, type='FAILED-SENDER'))
                    await client.send_message(message.channel, transfer_message(creds, type='FAILED-CHANNEL'))
                    await client.delete_message(message)
            elif message.content.startswith('!balance'):
                balance = self.ledger.get_balance(userid=message.author.id)
                sender_obj = discord.User(id=message.author.id)
                await client.send_message(sender_obj, balance_message(balance))
                await client.delete_message(message)
            elif message.content.startswith('!verify'):
                token = get_token(message)
                transaction = self.ledger.verify_transaction(token)
                sender_obj = discord.User(id=message.author.id)
                if transaction['verification']:
                    await client.send_message(sender_obj, verification_message(transaction, type='SUCCESS', token=token))
                else:
                    await client.send_message(sender_obj, verification_message(transaction, type='FAILIURE', token=token))
                await client.delete_message(message)
            elif message.content.startswith('!transactions'):
                transactions = self.ledger.get_transactions(userid=message.author.id)
                sender_obj = discord.User(id=message.author.id)
                transaction_list = ''
                for transaction in transactions:
                    transaction_list += transaction_message(transaction) + '\n \n'
                await client.send_message(sender_obj, (transaction_list))
                await client.delete_message(message)
            elif message.content.startswith('!mint'):
                if verify_id(message.author.id):
                    print('Verified')
            elif message.content.startswith('!buyS'):
                stock_count = int(re.findall(r'<(.*?)>', str(message.content))[0])
                company = re.findall(r'<(.*?)>', str(message.content))[1]
                stock_price = self.stocks.get_stock_price(company)
                amount = stock_count * stock_price
                sender_obj = discord.User(id=message.author.id)
                if self.ledger.validate_purchase(message.author.id, amount):
                    self.ledger.deduct_balance(message.author.id, amount)
                    self.stocks.add_stocks(company, stock_count, message.author.id)
                    await client.send_message(sender_obj, stock_buy_message(stock_count, stock_price, company, amount, type='SUCCESS'))
                else:
                    await client.send_message(sender_obj, stock_buy_message(stock_count, stock_price, company, amount, type='FAILIURE'))
                await client.delete_message(message)

            elif message.content.startswith('!sellS'):
                stock_count = int(re.findall(r'<(.*?)>', str(message.content))[0])
                company = re.findall(r'<(.*?)>', str(message.content))[1]
                stock_price = self.stocks.get_stock_price(company)
                amount = stock_price * stock_count
                sender_obj = discord.User(id=message.author.id)
                if self.stocks.get_stock_count(message.author.id, company) - stock_count >= 0:
                    self.ledger.raise_balance(message.author.id, amount)
                    self.stocks.deduct_stocks(company, stock_count, message.author.id)
                    await client.send_message(sender_obj, stock_sell_message(stock_count, stock_price, company, amount, type='SUCCESS'))
                else:
                    await client.send_message(sender_obj, stock_sell_message(stock_count, stock_price, company, amount, type='FAILIURE'))
                await client.delete_message(message)

            elif message.content.startswith('!sendS'):
                stock_count = int(re.findall(r'<(.*?)>', str(message.content))[1])
                company = re.findall(r'<(.*?)>', str(message.content))[2]
                sender_obj = discord.User(id=message.author.id)
                stock_price = self.stocks.get_stock_price(company)
                reciever = ''
                try:
                    reciever = re.findall(r'<@(.*?)>', str(message.content))[0]
                    self.ledger.get_balance(reciever)
                except:
                    reciever = re.findall(r'<@!(.*?)>', str(message.content))[0]
                if self.stocks.get_stock_count(message.author.id, company) - stock_count >= 0:
                    self.stocks.add_stocks(company, stock_count, reciever)
                    self.stocks.deduct_stocks(company, stock_count, message.author.id)
                    reciever_obj = discord.User(id=reciever)
                    trading_channel = discord.Object(id='510096970870816780')
                    await client.send_message(sender_obj, stock_transaction_message(company, stock_price, stock_count, message.author.id, type='SUCCESS-SENDER', reciever=reciever))
                    #await client.send_message(trading_channel, stock_transaction_message(creds, type='SUCCESS-'))
                    await client.send_message(reciever_obj, stock_transaction_message(company, stock_price, stock_count, message.author.id, type='SUCCESS-RECIEVER'))
                    await client.delete_message(message)

                else:
                    await client.send_message(sender_obj, stock_transaction_message(company, stock_price, stock_count, message.author.id, type='FAILIURE-SENDER', reciever=reciever))
            elif message.content.startswith('!mystocks'):
                n={}
                sender_obj = discord.User(id=message.author.id)
                send_message = ('-') * 100 + '\n'
                scks = self.stocks.stocks_data['Stocks']
                for stock in scks:
                    if message.author.id in scks[stock]['share-holders']:
                        n[stock]=scks[stock]['share-holders'][message.author.id]
                        current_price = self.stocks.get_stock_price(stock)
                        send_message += mystocks_message(stock, n[stock], current_price) + '\n'
                send_message += ('-') * 100
                await client.send_message(sender_obj, send_message)
                await client.delete_message(message)

            elif message.content.startswith('!buyR'):
                role_name = re.findall(r'<(.*?)>', str(message.content))[0]
                role = discord.utils.get(message.author.server.roles, name=role_name)
                role_price = self.prices[role_name]
                print(message.author.roles)
                sender_obj = discord.User(id=message.author.id)
                if self.ledger.validate_purchase(message.author.id, role_price):
                    self.ledger.deduct_balance(message.author.id, role_price)
                    await client.add_roles(message.author, role)
                    await client.send_message(sender_obj, role_bought_message(role, role_price, type='SUCCESS'))
                await client.delete_message(message)

        client.run('clientid')

s = Server()

s.run()

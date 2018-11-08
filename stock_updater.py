from stocks import Stocks
from time import sleep
import asyncio
import discord
from messages import *

stocks = Stocks()
client = discord.Client()

async def stock_updater():
    await client.wait_until_ready()
    channel = discord.Object(id='stocks-channel-id')
    while not client.is_closed:
        message = ('-' * 55) + '\n'
        for company in stocks.get_companies():
            prices = {}
            prices[company] = stocks.update_stock_price(company)
            company_name = prices[company]['company-name']
            message += stock_updater_message(prices, company) + '\n' + ('-' * 55) + '\n'
        message += ('=' * 34)
        await client.send_message(channel, message)
        message = ''
        await asyncio.sleep(300) # task runs every hour

client.loop.create_task(stock_updater())
client.run('clientid')

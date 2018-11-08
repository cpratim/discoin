import datetime

def transfer_message(creds, type):
    message = add_pad_b()
    if type == 'SUCCESS-RECIEVER':
        message += ('<@{}> sent {} discoins to you. Verification ID: {}'.format(creds['sender'], str(creds['amount']), creds['verification']))
        message += add_pad_e()
        return message
    elif type == 'SUCCESS-SENDER':
        message += ('{} discoins sent to <@{}>. Verification ID: {}'.format(str(creds['amount']), creds['reciever'], creds['verification']))
        message += add_pad_e()
        return message
    elif type == 'FAILED-CHANNEL':
        message += ('{} to {}. Transaction Unsuccessful. Verification ID: {}'.format(creds['sender'], creds['reciever']))
        message += add_pad_e()
        return message
    elif type == 'FAILED-SENDER':
        message += ('Transaction of {} discoins to {} was unsuccessful'.format(creds['sender'], creds['amount']))
        message += add_pad_e()
        return message
    elif type == 'SUCCESS-CHANNEL':
        message += ('{} to {} Transaction Successfull'.format(creds['sender'], creds['reciever']))
        message += add_pad_e()
        return message

def add_pad_b(count=100):
    return ('-' * count) + '\n'

def add_pad_e(count=100):
    return '\n' + ('-' * 100)

def balance_message(balance):
    message = add_pad_b()
    message += ('You have {} discoins in your account.'.format(str(balance)))
    message += add_pad_e()
    return message

def verification_message(transaction, type, token=None):
    message = add_pad_b()
    if type == 'SUCCESS':
        message += ("Transaction {} was Successfull: {} discoins from <@{}> to <@{}> on {}".format(token, transaction['amount'], transaction['sender'], transaction['reciever'], transaction['date']))
        message += add_pad_e()
        return message
    elif type == 'FAILIURE':
        message += ("Transaction {} was Unsuccessful".format(token))
        message += add_pad_e()
        return message

def transaction_message(transaction):
    message = 'Transaction {}: {} discoins from <@{}> to <@{}> on {}'.format(transaction['token'], transaction['amount'], transaction['sender'], transaction['reciever'], transaction['date'])
    return message

def mint_message(creds):
    pass

def stock_buy_message(stock_count, stock_price, company, amount, type):
    message = add_pad_b()
    if type == 'SUCCESS':
        message += 'Successfully Bought: {} Stocks of {} at {} discoins per Stock for a Total of {} discoins'.format(stock_count, company, stock_price, amount)
        message += add_pad_e()
        return message
    elif type == 'FAILIURE':
        message += 'Don\'t have enough Discoins to buy {} stocks of {}'.format(stock_count, company)
        message += add_pad_e()
        return message

def stock_updater_message(prices, company):
    now = datetime.datetime.now()
    if prices[company]['up-down'] == 'up':
        return ':arrow_up: {} ({}), \n Current Price: {} Discoins Per Stock \n Up: {}% From Latest \n Last Updated: {}'.format(prices[company]['stock-name'], prices[company]['company-name'], prices[company]['price'], prices[company]['up-percent'], str(now)[0:19])
    else:
        return ':arrow_down: {} ({}), \n Current Price: {} Discoins Per Stock \n Down: {}% From Latest \n Last Updated: {}'.format(prices[company]['stock-name'], prices[company]['company-name'], prices[company]['price'], prices[company]['down-percent'], str(now)[0:19])

def stock_sell_message(stock_count, stock_price, company, amount, type):
    message = add_pad_b()
    if type == 'SUCCESS':
        message += '{} Stocks of {} Successfully sold at {} discoins per stock for a Total of {} discoins'.format(stock_count, company, stock_price, amount)
        message += add_pad_e()
        return message
    elif type == 'FAILIURE':
        return 'You have less than {} stocks'.format(stock_count)
        message += add_pad_e()
        return message

def stock_transaction_message(company, stock_price, stock_count, sender, type, reciever=None):
    message = add_pad_b()
    if type == 'SUCCESS-RECIEVER':
        message += '<@{}> sent you {} stocks of {}, each currently worth {} discoins, totalling {} discoins'.format(sender, stock_count, company, stock_price, (stock_count * stock_price))
        message += add_pad_e()
        return message
    elif type == 'SUCCESS-SENDER':
        message += '{} stocks of {} successfully sent to <@{}> at {} discoins per stock, totalling {} discoins'.format(stock_count, company, reciever, stock_price, (stock_count * stock_price))
        message += add_pad_e()
        return message
    elif type == 'FAILIURE-SENDER':
        message += 'Don\'t have enought stocks of {} to give {} stocks'.format(company, stock_count)
        message += add_pad_e()

def mystocks_message(company, stock_amount, stock_price):
    return '{}: {} stocks, each worth {} discoins, totalling {} discoins'.format(company, stock_amount, stock_price, (stock_price * stock_amount))

def role_bought_message(role, role_price, type):
    message = add_pad_b()
    if type == 'SUCCESS':
        message += 'Successfully bought role: {} for {} discoins'.format(role, role_price)
    elif type == 'FAILIURE':
        message += 'Need {} discoins to buy {} role'.format(role_price, role)
    message += add_pad_e()
    return message

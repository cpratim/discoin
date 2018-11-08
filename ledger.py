import json
from datetime import date

class Ledger:

    def __init__(self):
        with open("ledger.json", 'r') as ledger:
            self.ledger_data = json.loads(ledger.read())
        with open('transactions.json', 'r') as transactions:
            self.transactions = json.loads(transactions.read())

    def log_transaction(self, sender, reciever, amount, verification, date):
        self.update_read_transactions()
        self.transactions['Transactions'][verification] = {'sender' : sender, 'reciever' : reciever, 'amount': amount, 'date' : date}
        with open('transactions.json', 'w') as transactions:
            json.dump(self.transactions, transactions, indent=4)

    def check_user(self, userid):
        return userid in self.ledger_data['Balances']

    def update_read_transactions(self):
        with open('transactions.json', 'r') as transactions:
            self.transactions = json.loads(transactions.read())

    def verify_transaction(self, token):
        self.update_read_transactions()
        try:
            transaction = self.transactions['Transactions'][token]
            sender = self.transactions['Transactions'][token]['sender']
            reciever = self.transactions['Transactions'][token]['reciever']
            amount = self.transactions['Transactions'][token]['amount']
            date = self.transactions['Transactions'][token]['date']
            return {'verification': True, 'sender': sender, 'reciever': reciever, 'amount': amount, 'date': date}
        except:
            return {'verification': False}

    def validate_purchase(self, userid, amount):
        if (self.get_balance(userid) - amount >= 0) and amount > 0:
            return True
        else:
            return False

    def get_transactions(self, userid):
        self.update_read_transactions()
        transactions = []
        for transaction in self.transactions['Transactions']:
            if (self.transactions['Transactions'][transaction]['sender']) == userid:
                self.transactions['Transactions'][transaction]['token'] = transaction
                transactions.append(self.transactions['Transactions'][transaction])
        return transactions

    def update_read(self):
        with open('ledger.json', 'r') as ledger:
            self.ledger_data = json.loads(ledger.read())

    def add_user(self, userid, clientid):
        if (self.check_user(userid)):
            self.ledger_data['User-info'][userid] = {'name' : (str(clientid).lower()), 'hash' : str(abs(hash(userid)))}
        else:
            self.ledger_data['User-info'][userid] = {'name' : (str(clientid).lower()), 'hash' : str(abs(hash(userid)))}
            self.ledger_data['Balances'][userid] = 500
        self.update()

    def get_balance(self, userid):
        self.update_read()
        return self.ledger_data['Balances'][userid]


    def raise_balance(self, userid, amount):
        self.ledger_data['Balances'][userid] += amount
        self.update()

    def deduct_balance(self, userid, amount):
        self.ledger_data['Balances'][userid] -= amount
        self.update()

    def update(self):
        with open('ledger.json', 'w') as ledger:
            json.dump(self.ledger_data, ledger, indent=4)
        with open('ledger.json', 'r') as ledger:
            self.ledger_data = json.loads(ledger.read())

    def update_user(self, userid, clientid):
        self.ledger_data['User-info'][userid] = clientid
        self.update()

    def transfer(self, creds):
        self.update_read()
        if creds['amount'] > 0 and self.get_balance(creds['sender']) - creds['amount'] > 0:
            now = str(date.today())
            self.deduct_balance(creds['sender'], creds['amount'])
            self.raise_balance(creds['reciever'], creds['amount'])
            self.log_transaction(creds['sender'], creds['reciever'], creds['amount'], creds['verification'], now)
            return True
        else:
            return False

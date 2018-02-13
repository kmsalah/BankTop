import json
import datetime
from banktop.prettytable import prettytable
import os
import sys


'''
Transactions that store the amount and description, to be stored in a Pocket's ledger
'''


class Transaction:
    amountM = 0
    descriptionM = ''
    dateTimeM = ''

    def __init__(self, amount, description, dateTime):
        self.amountM = amount
        self.descriptionM = description

        try:
            date = dateTime.strftime("%m/%d/%y")
            self.dateTimeM = date
        except BaseException:
            newTime = datetime.datetime.now()
            date = newTime.strftime("%m/%d/%y")
            self.dateTimeM = date

    def getAmount(self):
        return self.amountM

    def getDescription(self):
        return self.descriptionM

    def getDateTime(self):
        return self.dateTimeM

    def print(self):
        print(str(self.amountM) + str(self.descriptionM))

    def jsonDefault(self):
        return self.__dict__


'''
Pretty much a bank account. Serves as subdivision of my money. Has a name, balance,
and a ledger that records all the transactions
'''


class Pocket:
    nameM = 'Default Name'
    balanceM = 0
    ledgerM = []

    def __init__(self, name, initialBalance, ledger):
        self.balanceM = initialBalance
        self.nameM = name
        self.ledgerM = ledger

    def getName(self):
        return self.nameM

    def setName(self, newName):
        self.nameM = newName

    def getBalance(self):
        return self.balanceM

    def setBalance(self, newAmount):
        print("setting new balance")
        self.balanceM = newAmount

    def addTransaction(self, transaction):
        amount = transaction.getAmount()
        self.ledgerM.append(transaction)
        self.balanceM += transaction.getAmount()

    def getLedger(self):
        return self.ledgerM

    def printLedger(self):
        os.system('clear')
        print(self.nameM + " Ledger")
        print(" ")
        t = prettytable.PrettyTable(['Date', 'Description', 'Amount'])
        for i in range(0, len(self.ledgerM)):
            date = self.ledgerM[i].getDateTime()
            description = self.ledgerM[i].getDescription()
            amount = self.ledgerM[i].getAmount()
            t.add_row([date, description, amount])
        print(t)

    def jsonDefault(self):
        data = self.__dict__
        print(data)
        for i in range(len(self.ledgerM)):
            data['ledgerM'][i] = data['ledgerM'][i].jsonDefault()
        return data


'''
A table to store Pockets. Handles json saving.
'''


class Table:
    pocketsM = []
    totalAmountM = 0
    debtM = 0
    cashM = 0

    def __init__(self):
        try:
            self.pocketsM = self.load()
        except EOFError:
            print('The file contains no data')  # list is empty
        except FileNotFoundError:  # if the file does not exist
            self.save()
            print('Created new empty json for ya')
        except KeyError:
            print("error in json, new file")
            self.save()

    def save(self):
        # create the json we will store
        data = {
            'pockets': []  # an array that will store the json's of pockets
        }
        for i in range(len(self.pocketsM)):  # for each pocket we have,
            # get the json version of it
            pocketData = self.pocketsM[i].jsonDefault()
            # and add to the array within data
            data['pockets'].append(pocketData)

        with open('data.json', 'w') as f:
            json.dump(data, f)  # store the data json

    def load(self):
        with open('data.json', 'r') as f:
            data = json.load(f)

        jsonPockets = data['pockets']
        pockets = []
        for i in range(len(jsonPockets)):
            name = jsonPockets[i]['nameM']
            balance = jsonPockets[i]['balanceM']

        # now jsonPockets[i]['ledgerM'] is going to be an array of json
        # transactions
            jsonTransactions = jsonPockets[i]['ledgerM']
            ledger = []
            for i in range(len(jsonTransactions)):
                description = jsonTransactions[i]['descriptionM']
                amount = jsonTransactions[i]['amountM']
                dateTime = jsonTransactions[i]['dateTimeM']
                newTrans = Transaction(amount, description, dateTime)
                ledger.append(newTrans)

            newPocket = Pocket(name, balance, ledger)
            pockets.append(newPocket)
        return pockets

    def calcTotalAmount(self):
        self.totalAmountM = 0
        for i in range(0, len(self.pocketsM)):
            pocketBalance = float(self.pocketsM[i].getBalance())
            self.totalAmountM += pocketBalance

    def calcDebt(self):
        self.debtM = 0
        for i in range(0, len(self.pocketsM)):
            pocketBalance = float(self.pocketsM[i].getBalance())
            if pocketBalance < 0:
                self.debtM += pocketBalance

    def calcCash(self):
        self.cashM = 0
        for i in range(0, len(self.pocketsM)):
            pocketBalance = float(self.pocketsM[i].getBalance())
            if pocketBalance >= 0:
                self.cashM += pocketBalance

    def addPocket(self, newPocket):
        self.pocketsM.append(newPocket)
        #newAmount = newPocket.getBalance()
        #self.totalAmountM += newAmount

    def getTotalAmount(self):
        self.calcTotalAmount()
        return self.totalAmountM

    def getDebt(self):
        self.calcDebt()
        return self.debtM

    def getCash(self):
        self.calcCash()
        return self.cashM

    def getTableSize(self):
        size = len(self.pocketsM)
        return size

    def getPocket(self, index):
        return self.pocketsM[index]

    def getPocketByName(self, name):
        for i in range(0, self.getTableSize()):
            if self.pocketsM[i].getName() == name:
                print(self.pocketsM[i])
                return self.pocketsM[i]

    def getPocketIndex(self, name):
        for i in range(0, self.getTableSize()):
            if self.pocketsM[i].getName() == name:
                return i

    def getPockets(self):
        return self.pocketsM

    def removePocket(self, name):
        pocketIndex = self.getPocketIndex(name)
        if pocketIndex is None:
            return
        else:
            del self.pocketsM[pocketIndex]

    def print(self):
        t = prettytable.PrettyTable(['Pocket', 'Balance', 'Percentage'])
        for i in range(0, self.getTableSize()):
            pocket = self.getPocket(i)
            if self.getTotalAmount() != 0:
                percentage = pocket.getBalance() / self.getCash() * 100
            else:
                percentage = 0
            percentage = round(percentage, 2)
            t.add_row([pocket.getName(),
                       str(pocket.getBalance()),
                       str(percentage) + "%"])

        t.right_padding_width = 10

        print(t)
        for i in range(5):
            print(" ")

        print("Total Holdings: " + str(self.getTotalAmount())
              + "    Cash: " + str(self.getCash())
                + "    Debt: " + str(self.getDebt()))
        print("[A] Add/update pocket [T] Add Transaction [L] Print a Ledger [Q]Exit")


'''
		for i in range(0, self.getTableSize()):
			print(self.getPocket(i).nameM)
			print(self.getPocket(i).ledgerM)
'''

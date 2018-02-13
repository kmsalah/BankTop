import sys
import termios
import tty
import os
import time

from banktop import table
import datetime
'''
Handles keyboard input for me, found this online
Cannot find link again
'''


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def addPocket(myTable):
    os.system('clear')
    response = input("Enter the pocket name and balance  (Name,Balance) \n")
    if len(response):
        data = response.split(',')
        name = data[0]
        balance = float(data[1])
        tablePockets = myTable.getPockets()
        for i in range(len(tablePockets)):
            if tablePockets[i].getName() == name:
                tablePockets[i].setBalance(balance)
                return

        newLedger = []
        pocket = table.Pocket(name, balance, newLedger)
        myTable.addPocket(pocket)


def addTransaction(myTable):
    os.system('clear')
    response = input(
        "Enter pocket name, transaction amount, and description (Name,Amount,Description) \n")
    if len(response):
        data = response.split(',')
        name = data[0]
        amount = float(data[1])
        description = data[2]
        dateTime = datetime.datetime.now()
        newTransaction = table.Transaction(amount, description, dateTime)
        pocket = myTable.getPocketByName(name)
        print(pocket)
        pocket.addTransaction(newTransaction)


def printPocketTransactions(myTable):
    os.system('clear')
    name = input("Enter the pocket name (Name) \n")
    if len(name):
        pocket = myTable.getPocketByName(name)
        if pocket is None:
            return
        else:
            pocket.printLedger()
            for i in range(5):
                print(" ")
            char = getch()
            if char == "r":
                return


def removePocket(myTable):
    os.system('clear')
    name = input("Enter the pocket name to remove (Name) \n")
    if len(name):
        myTable.removePocket(name)


def main():
    running = True
    os.system('clear')  # clears terminal so it looks like its on its own page
    myTable = table.Table()

    while(running):
        print("banktop 1.0")
        myTable.print()
        char = getch()
        if char == "a":
            addPocket(myTable)
            os.system('clear')
        elif char == "t":
            addTransaction(myTable)
            os.system('clear')
        elif char == "l":
            printPocketTransactions(myTable)
        elif char == "r":
            removePocket(myTable)
        elif char == "q":
            print('q')
            running = False
            myTable.save()

        os.system('clear')


if __name__ == "__main__":
    main()

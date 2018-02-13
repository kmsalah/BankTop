import sys
import termios
import tty
import os
import time

from banktop import table
import datetime

def getch():
    """
    Handles keyboard input for me, found this online.
    TODO(kmsalah): Use a curses lib
     - e.g. https://docs.python.org/2/library/curses.html
    """
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
        # TODO(kmsalah) Confirm data is the correct size.
        name = data[0]
        # TODO(kmsalah) Handle parse failure correctly.
        balance = float(data[1])
        tablePockets = myTable.getPockets()
        # TODO(kmsalah) Implement a hashmap so linear lookup is not needed.
        for tablePocket in tablePockets:
            if tablePocket.getName() == name:
                tablePocket.setBalance(balance)
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
        # TODO(kmsalah) Confirm data is the correct size.
        name = data[0]
        # TODO(kmsalah) Handle parse failure correctly.
        amount = float(data[1])
        description = data[2]
        dateTime = datetime.datetime.now()
        newTransaction = table.Transaction(amount, description, dateTime)
        pocket = myTable.getPocketByName(name)
        print(pocket)
        # TODO(kmsalah) Ensure that newTransaction is not None.
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

    def quit(*args):
        running = False
        myTable.save()
        print('q')

    while(running):
        print("banktop 1.0")
        myTable.print()
        
        # Alternate for switch.
        char = getch().lower()
        functions = {
            "a": addPocket,
            "t": addTransaction,
            "l": printPocketTransactions,
            "r": removePocket,
            "q": quit
        }
        functions[char](myTable)
        os.system('clear')

if __name__ == "__main__":
    main()

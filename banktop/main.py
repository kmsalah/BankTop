import sys
import termios
import tty
import os
import time

import table
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
    userInput = input("Enter the pocket name and balance  (Name,Balance) \n")
    if len(userInput):
        data = userInput.split(',')
        name = data[0]
        if(len(name) == 0): #checking name 
            return "You did not enter a pocket name" 

        try:
            balance = float(data[1])
        except:
            return "You did not enter a valid balance"

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
    userInput = input(
        "Enter pocket name, transaction amount, and description (Name,Amount,Description) \n")
    if len(userInput):
        data = userInput.split(',')
        name = data[0]
        if(len(name) == 0): #checking to see user entered pocket name 
           return "You did not enter a pocket name"

        try:
            amount = float(data[1])
        except:
            return "You did not enter a valid transaction amount"
        description = data[2]
        dateTime = datetime.datetime.now()
        newTransaction = table.Transaction(amount, description, dateTime)

        pocket = myTable.getPocketByName(name)
        if pocket is None:
            return "The pocket you entered does not exist."
        
        if newTransaction is None:
            return "There was an error creating your new transaction, try again."
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
        myTable.save()
        return False
        
    msg = ' '
    while(running):
        if msg is None:
            print(" ")
        else:
            print(msg)
        print("banktop 1.1")
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

        if char in functions:
            msg = functions[char](myTable) #not sure if this is smart, but passing back error messages to loop to be displayed before table reprint
        if msg == False: #we just quit
            running = False
        os.system('clear')

if __name__ == "__main__":
    main()

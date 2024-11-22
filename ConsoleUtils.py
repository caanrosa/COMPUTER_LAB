# Taken from https://github.com/caanrosa/AVL-Lab

from termcolor import colored

def printTitle(title, centerNum=64):
    print (colored(f" {title} ".center(centerNum, "⸺"), "red"))
    
def printSubtitle(subtitle, centerNum=64):
    print (colored(f" {subtitle} ".center(centerNum), "light_grey"))

def printInfo(info, centerNum=64):
    print (colored(f"🗣️ {info} ".center(centerNum), "green"))
    
def printServerMessage(msg, centerNum=64):
    print (colored(f"🌎 {msg} ".center(centerNum), "white"), flush = True)
    
def printClientMessage(msg, centerNum=64):
    print (colored(f"👤 {msg} ".center(centerNum), "white"))
    
def printError(error, centerNum=64):
    print (colored(f" {error} ".center(centerNum), "red"))
    
def printOption(number, option, colorNumber="red", colorOption="white"):
    op = colored(f" ({number})", colorNumber) + colored(f" {option} ", colorOption)
    
    print (f"{op}".center(80))
    
def printBottom():
    print (colored("".center(64, "⸺"), "red"))        
    
def getInput() -> str:
    got = ""
    while(len(got) == 0):
        got = input(colored("> ", "green"))
        
    return got

def getInputInt() -> int:
    recieved = ""
    p = False
    
    while(not p):
        recieved = getInput()
        try:
            int(recieved)
            p = True
        except ValueError:
            p = False
    
    return int(recieved)


def getTInput() -> int:
    recieved = ""
    p = False
    
    while(not p):
        recieved = getInput()
        try:
            float(recieved)
            if(float(recieved) <= 0): p = False
            else: p = True
        except ValueError:
            p = False
    
    return float(recieved)
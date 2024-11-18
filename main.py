from ConsoleUtils import *

running = True

while(running):
    printTitle("MENU PRINCIPAL")
    printOption(1, "Placeholder 1")
    printOption(2, "Placeholder 2")
    printOption(3, "Placeholder 3")
    printOption(0, "Salir")
    printBottom()
    
    option = getInputInt()
    printBottom()
    
    match option:
        case 0:
            running = False
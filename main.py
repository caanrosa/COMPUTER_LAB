from ConsoleUtils import *
from Client import *
import random

VECTOR_FILE = "generated.txt"
client = Client()

def main():
    t = 2.0
    running = True
    while (running):
        printTitle("MENU PRINCIPAL")
        printOption(1, "Mergesort")
        printOption(2, "Heapsort")
        printOption(3, "Quicksort")
        printOption(4, f"Definir `t`. Actual: {t}s")
        printOption(-1, "Gen random N")
        printOption(0, "Salir")
        printBottom()

        option = getInputInt()
        printBottom()

        match option:
            case 1 | 2 | 3:
                prepare_sorting()
                client.sort(option, t)

            case 4:
                printSubtitle("Defina un `t` positivo")
                t = getTInput()
            case -1:
                printSubtitle("Genera N números aleatorios")
                gen_random_n(getInputInt())
            case 0:
                running = False
                client.disconnect()


def gen_random_n(n: int) -> None:
    with open("./vectors/generated.txt", "w") as f:
        for p in range(0, n):
            #f.write(str(p) + "\n")
            f.write(str(random.randrange(0, 10000000)) + "\n")


def prepare_sorting() -> None:
    printSubtitle("Especifique cuántas N posiciones. -1 Para todas las posibles.")
    n = getInputInt()

    client.setN(n)
    client.load(VECTOR_FILE)


if __name__ == "__main__":
    main()

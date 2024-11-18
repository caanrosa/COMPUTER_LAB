from ConsoleUtils import *
from Sorting import *
import random

VECTOR_FILE = "generated.txt"
sortingManager = Sorting()


def main():
    running = True

    while (running):
        printTitle("MENU PRINCIPAL")
        printOption(1, "Mergesort")
        printOption(2, "Heapsort")
        printOption(3, "Quicksort")
        printOption(-1, "Gen random N")
        printOption(0, "Salir")
        printBottom()

        option = getInputInt()
        printBottom()

        match option:
            case 1:
                prepare_sorting()
                sortingManager.mergesort()

            case -1:
                printSubtitle("Genera N números aleatorios")
                gen_random_n(getInputInt())
            case 0:
                running = False


def gen_random_n(n: int) -> None:
    with open("./vectors/generated.txt", "w") as f:
        for p in range(0, n):
            f.write(str(random.randrange(0, 10000000)) + "\n")


def prepare_sorting() -> None:
    printSubtitle("Especifique cuántas N posiciones.")
    n = getInputInt()

    sortingManager.setN(n)
    sortingManager.load(VECTOR_FILE)


if __name__ == "__main__":
    main()
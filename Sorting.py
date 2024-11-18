from typing import List
from ConsoleUtils import printError

class Sorting():
    def __init__(self):
        self.n = None
        self.vector: List[int] = []
        self.loaded = False
        
    def setN(self, n: int):
        self.n = n
        return self
        
    def load(self, fileName: str):
        if(self.n is None):
            printError("No se puede cargar, no se ha definido N: Sorting.setN()")
            return None
        try:
            with open(f"./vectors/{fileName}", "r") as file:
                for i in range(0, self.n):
                    line = file.readline()
                    if(len(line) > 0):
                        self.vector.append(int(line))
                    else:
                        break
        except Exception as e:
            printError(f"Ocurrió un error inesperado cargando el archivo de números:\n{e}")
        
        self.loaded = True        
        return self
    
    def mergesort(self):
        if(not self.loaded):
            printError("No se puede organizar, no se ha cargado el vector: Sorting.load()")
            return None
        
        # TODO
        pass
    
    def heapsort(self):
        if(not self.loaded):
            printError("No se puede organizar, no se ha cargado el vector: Sorting.load()")
            return None
        
        # TODO
        pass
    
    def quicksort(self):
        if(not self.loaded):
            printError("No se puede organizar, no se ha cargado el vector: Sorting.load()")
            return None
        
        # TODO
        pass
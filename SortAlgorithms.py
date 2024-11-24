from ConsoleUtils import *
from typing import List
import timeit

DEBUG = False

class Timelimit():
    def __init__(self, limit):
        self.limitSeconds = limit
        if(self.limitSeconds == 0): self.limitSeconds = 9e10
        self.start = timeit.default_timer()
        self.lastCheck = None
        self.maxReached = False
        self.lastData = None
        
    def reachedLimit(self) -> bool:
            
        self.lastCheck = timeit.default_timer()
        self.maxReached = self.lastCheck - self.start >= self.limitSeconds        
            
        return self.maxReached
    
    def setLastData(self, lastData):
        if(self.lastData is None):
            self.lastData = lastData

# MERGE
def merge_sort(data, time, start = 0):
    printTitle(f"Usando Mergesort - {time}s")
    limit = Timelimit(time)
    sorting = __merge_sort(data[start:], limit)
    
    if(limit.maxReached):
        printInfo(f"Llegó al tiempo máximo: {limit.maxReached}")
        printInfo(f"{limit.lastData[0]}")
        printInfo(f"{limit.lastData[-1]}")
        printInfo(f"{len(limit.lastData)}")
    
    data = __merge(data[:start], sorting)
    
    return data, limit
def __merge_sort(V: List, limit: Timelimit):
    limit.reachedLimit()
    if(limit.maxReached):
        limit.setLastData(V)
        return V
    if(DEBUG):
        printBottom()
        printSubtitle("V Entrada:")
        printInfo(V)
    # Si la long es de 1, no es necesario hacer nada más
    if(len(V) <= 1):
        return V
    
    # Si la lista aún tiene más de 2 elementos, se puede seguir dividiendo
    first, second = __divide(V)
    first = __merge_sort(first, limit)
    second = __merge_sort(second, limit)
        
    if(DEBUG):
        printSubtitle("Uniendo vectores ordenados")
        printInfo(f"{len(first)}: {first}")
        printInfo(f"{len(second)}: {second}")
    
    #print(limit.maxReached)
    
    if(limit.maxReached):
        #print("extending")
        first.extend(second)
        return first
    else:
        ordered = __merge(first, second)
    return ordered
    
def __merge(v1: list, v2: list):
    merged = []
    
    left = right = 0
    
    while left < len(v1) and right < len(v2):
        # Se compara de a pares los elementos de ambas listas para organizarlas
        if(v1[left] < v2[right]):
            merged.append(v1[left])
            left += 1
        else:
            merged.append(v2[right])
            right += 1
        
    # Apenas se llegue al limite de alguno de los subvectores, se sale del while.
    if(DEBUG):
        printInfo(f"MaxLeft: {left}: {v1}")
        printInfo(f"MaxRight: {right}: {v2}")
    
    # Agregar al resultado cualquiera que sea el que le falta por terminar al vector resultado
    # Sea cual sea, si este está en el limite y se intenta "extender" no pasará nada
    merged.extend(v1[left:])
    merged.extend(v2[right:])
    
    if(DEBUG):
        printSubtitle("Subvector ordenado:")
        printInfo(merged)
    
    return merged
        
def __divide(V: list):#
    mid = len(V) // 2
    return V[:mid], V[mid:]
    
# HEAP
def heap_sort(data, time):
    printTitle(f"Usando Heapsort - {time}s")
    limit = Timelimit(time)

    sorting = heapsort(data, limit)

    if limit.maxReached:
        printInfo(f"Llegó al tiempo máximo: {limit.maxReached}")
        printInfo(f"{limit.lastData[0]}")
        printInfo(f"{limit.lastData[-1]}")
        printInfo(f"{len(limit.lastData)}")

    return sorting, limit

def heapify(V: List[int], n: int, i: int, limit: Timelimit):
    
    if limit.reachedLimit():
        return

    largest = i  # Asumimos que el nodo raíz es el más grande
    left = 2 * i + 1  # Índice del hijo izquierdo
    right = 2 * i + 2  # Índice del hijo derecho

    # Verificar si el hijo izquierdo existe y es mayor que la raíz
    if left < n and V[left] > V[largest]:
        largest = left

    # Verificar si el hijo derecho existe y es mayor que la raíz actual
    if right < n and V[right] > V[largest]:
        largest = right

    # Si el nodo raíz no es el más grande, intercambiarlo con el más grande
    if largest != i:
        V[i], V[largest] = V[largest], V[i]
        heapify(V, n, largest, limit)

def heapsort(V: List[int], limit: Timelimit):
    n = len(V)

    # Construir el montículo máximo (heap)
    for i in range(n // 2 - 1, -1, -1):
        if limit.reachedLimit():
            limit.setLastData(V)
            return V
        heapify(V, n, i, limit)

    # Extraer elementos del montículo uno por uno
    for i in range(n - 1, 0, -1):
        if limit.reachedLimit():
            limit.setLastData(V)
            return V
        V[0], V[i] = V[i], V[0]
        heapify(V, i, 0, limit)

    return V

# QUICK
def quick_sort(data, time):    
    printTitle("Usando Quicksort")
    limit = Timelimit(time)
    
    __quick_sort(data, 0, len(data) - 1)
    
    return data, limit

def __quick_sort(V, low, high):
    if(low < high):
        pi = __partition(V, low, high)
        
        if(DEBUG): printInfo(V)    
        __quick_sort(V, low, pi - 1)
        if(DEBUG): printInfo(V)
        __quick_sort(V, pi + 1, high)
        if(DEBUG):
            printInfo(V)        
            printBottom()
        
def __partition(V, low, high):
    pivot = V[high]
    i = low - 1
    for j in range(low, high, 1):
        if(V[j] <= pivot):
            i = i + 1
            (V[i], V[j]) = (V[j], V[i])
    
    (V[i + 1], V[high]) = (V[high], V[i + 1])
    
    return i + 1
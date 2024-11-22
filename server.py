from ConsoleUtils import *

from config import CONFIG_PARAMS
from typing import List
import socket
import threading
import pickle
import struct

# Configuration Parameters
IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS: List["socket.socket"] = []

# Remove Client from List of Clients
def remove_client(client_socket: "socket.socket") -> None:
    if client_socket in LIST_OF_CLIENTS:
        LIST_OF_CLIENTS.remove(client_socket)

def sendToClient(data, client_socket: "socket.socket"):
    try:
        # Misma lógica usada para enviar el vector desde el cliente, pero esta vez hacia él
        data = pickle.dumps(data)
        client_socket.send(struct.pack("I", len(data)))
        client_socket.send(data)
    except Exception as ex:
        client_socket.close()
        remove_client(client_socket)

def sendToAllClients(data) -> None:
    for client in LIST_OF_CLIENTS:
        try:
            data = pickle.dumps(data)
            client.send(struct.pack("I", len(data)))
            client.send(data)
        except Exception as ex:
            client.close()
            remove_client(client)

# MERGE
def merge_sort(data):
    printTitle("Usando Mergesort")
    
    data = __merge_sort(data)
    printBottom()
    
    printSubtitle("RESULTADO")
    printInfo(data)
    
    return data

def __merge_sort(V: List):
    printBottom()
    printSubtitle("V Entrada:")
    printInfo(V)
    # Si la long es de 1, no es necesario hacer nada más
    if(len(V) <= 1):
        return V
    
    # Si la lista aún tiene más de 2 elementos, se puede seguir dividiendo
    first, second = __divide(V)
    first = __merge_sort(first)
    second = __merge_sort(second)
    
    printSubtitle("Uniendo vectores ordenados")
    printInfo(f"{len(first)}: {first}")
    printInfo(f"{len(second)}: {second}")
    
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
    printInfo(f"MaxLeft: {left}: {v1}")
    printInfo(f"MaxRight: {right}: {v2}")
    
    # Agregar al resultado cualquiera que sea el que le falta por terminar al vector resultado
    # Sea cual sea, si este está en el limite y se intenta "extender" no pasará nada
    merged.extend(v1[left:])
    merged.extend(v2[right:])
    
    printSubtitle("Subvector ordenado:")
    printInfo(merged)
    
    return merged
        
def __divide(V: list):#
    mid = len(V) // 2
    return V[:mid], V[mid:]
    
# HEAP
def heap_sort(data):
    printTitle("Usando Heapsort")
    
    return data

# QUICK
def quick_sort(data):    
    printTitle("Usando Quicksort")
    
    __quick_sort(data, 0, len(data) - 1)
    
    printSubtitle("RESULTADO")
    printInfo(data)
    
    return data

def __quick_sort(V, low, high):
    if(low < high):
        pi = __partition(V, low, high)
        
        printInfo(V)    
        __quick_sort(V, low, pi - 1)
        printInfo(V)
        __quick_sort(V, pi + 1, high)
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

# Handle Client Method (Clients Secondary Threads)
def handle_client(client_socket: "socket.socket", client_address: "socket._RetAddress") -> None:
    try:
        sendToClient('Conectado con el servidor', client_socket)
        
        data = []
        while True:
            toUnpack = client_socket.recv(4)
            size = struct.unpack("I", toUnpack)
            size = size[0]
            
            data = client_socket.recv(size)
            vector = pickle.loads(data)
            
            type = struct.unpack("I", client_socket.recv(4))[0]
            time = struct.unpack("f", client_socket.recv(4))[0]
            
            printClientMessage(vector)
            printClientMessage(f"{len(vector)} elems. - Max: {time}s")
            
            match type:
                case 1: # MERGESORT
                    res = merge_sort(vector)
                case 2: # HEAPSORT
                    res = heap_sort(vector)
                case 3: # QUICKSORT
                    res = quick_sort(vector)
                    
            sendToClient(res, client_socket)
                    
    except Exception as ex:
        printError(f'Error en cliente {client_address[0]}: {ex}')
        remove_client(client_socket)
    finally:
        client_socket.close()


def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP_ADDRESS, PORT))
    server_socket.listen(MAX_CLIENTS)

    printSubtitle(f"Iniciando servidor en {IP_ADDRESS}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            LIST_OF_CLIENTS.append(client_socket)
            printInfo(client_address[0] + ' conectado')

            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
    except Exception as ex:
        printError(f"Error aceptando clientes: {ex}")
        printError("Cerrando el servidor.")
    finally:
        for client in LIST_OF_CLIENTS:
            client.close()
        server_socket.close()


if __name__ == '__main__':
    printTitle("SERVIDOR")
    start_server()

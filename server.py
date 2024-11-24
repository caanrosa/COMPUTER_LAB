from ConsoleUtils import *

from config import CONFIG_PARAMS
from typing import List
import socket
import threading
import pickle
import struct
from SortAlgorithms import merge_sort, heap_sort, quick_sort

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
            
            printClientMessage("Vector recibido")
            #printClientMessage(vector)
            printClientMessage(f"{len(vector)} elems. - Max: {time}s")
            
            match type:
                case 1: # MERGESORT
                    res, limit = merge_sort(vector, time)
                case 2: # HEAPSORT
                    res = heap_sort(vector, time)
                case 3: # QUICKSORT
                    res = quick_sort(vector, time)
            
            if(limit.maxReached):
                printTitle("AGAIN!")
                res, limit = merge_sort(res, 0, res.index(limit.lastData[0]))
            printSubtitle("Enviando resultado a cliente")  
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

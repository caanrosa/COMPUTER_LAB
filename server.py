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


# Attemp to Broadcast a Client Message
def broadcast(message: bytes, client_socket: "socket.socket") -> None:
    for client in LIST_OF_CLIENTS:
        if client != client_socket:
            try:
                client.sendall(message)
            except Exception as ex:
                client.close()
                remove_client(client)

def merge_sort(data):
    printTitle("Usando Mergesort")
    printClientMessage(data)
    printClientMessage(len(data))
    
def heap_sort(data):
    printTitle("Usando Heapsort")
    printClientMessage(data)
    
def quick_sort(data):
    printTitle("Usando Quicksort")
    printClientMessage(data)

# Handle Client Method (Clients Secondary Threads)
def handle_client(client_socket: "socket.socket", client_address: "socket._RetAddress") -> None:
    try:
        client_socket.sendall(b'Conectado con el servidor')
        
        data = []
        while True:
            toUnpack = client_socket.recv(4)
            size = struct.unpack("I", toUnpack)
            size = size[0]
            
            data = client_socket.recv(size)
            vector = pickle.loads(data)
            
            type = struct.unpack("I", client_socket.recv(4))[0]
            
            match type:
                case 1: # MERGESORT
                    merge_sort(vector)
                case 2: # HEAPSORT
                    heap_sort(vector)
                case 3: # QUICKSORT
                    quick_sort(vector)
                    
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
            printSubtitle(client_address[0] + ' conectado')

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

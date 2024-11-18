import socket
import threading
from config import CONFIG_PARAMS
from ConsoleUtils import *

# Configuration Parameters
SERVER_IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS']
SERVER_PORT = CONFIG_PARAMS['SERVER_PORT']

from typing import List
from ConsoleUtils import printError

class Sorting():
    def __init__(self):
        self.n = None
        self.vector: List[int] = []
        self.loaded = False
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        self.alive = True
        
    # (Handler) Recibir los mensajes del servidor
    def receive_messages(self):
        try:
            while True:
                message = self.client_socket.recv(2048)
                if not message:
                    break
                print('\r', end='')
                printServerMessage(message.decode('utf-8'))
        except Exception as ex:
            printError(f"Error recibiendo mensajes: {ex}")
        finally:
            self.disconnect()

    # Desconectarse del servidor
    def disconnect(self):
        printSubtitle("Desconectando del servidor...")
        self.alive = False
        self.client_socket.close()
        
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
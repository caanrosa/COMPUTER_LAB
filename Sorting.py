import socket
import threading
import pickle
import struct
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
        
        self.__connect()
                
    def __connect(self):        
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
                toUnpack = self.client_socket.recv(4)
                if not toUnpack:
                    break
                size = struct.unpack("I", toUnpack)
                size = size[0]
            
                data = self.client_socket.recv(size)
                message = pickle.loads(data)
                print('\r', end='')
                printServerMessage(message)
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
        self.vector = []
        if(self.n is None):
            printError("No se puede cargar, no se ha definido N: Sorting.setN()")
            return None
        try:
            with open(f"./vectors/{fileName}", "r") as file:
                if(self.n == -1):
                    i = 0
                    while(True):
                        line = file.readline()
                        if(len(line) > 0):
                            self.vector.append(int(line))
                            i += 1
                        else:
                            self.setN(i)
                            break
                else:
                    for i in range(0, self.n):
                        line = file.readline()
                        if(len(line) > 0):
                            self.vector.append(int(line))
                        else:
                            self.setN(i)
                            break
        except Exception as e:
            printError(f"Ocurrió un error inesperado cargando el archivo de números:\n{e}")
        
        self.loaded = True        
        return self
    
    def sort(self, type: int, time: float):        
        if(not self.alive):
            printError("No existe una conexión, cerrando cliente.")
            return None
        if(not self.loaded):
            printError("No se puede organizar, no se ha cargado el vector: Sorting.load()")
            return None        
        
        data = pickle.dumps(self.vector)
        self.client_socket.send(struct.pack("I", len(data))) # Información guardada en 4 bytes - 32 bits - "int" --- https://docs.python.org/3/library/struct.html#format-characters 
        self.client_socket.send(data) # La información enviada arriba incluye la cantidad de información que se envió
        self.client_socket.send(struct.pack("I", type))
        self.client_socket.send(struct.pack("f", time)) # Float también se guarda en 4 bytes
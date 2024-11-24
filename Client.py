import socket
import threading
import pickle
import struct
from config import CONFIG_PARAMS
from ConsoleUtils import *
import traceback

# Configuration Parameters
WORKER0_IP_ADDRESS = CONFIG_PARAMS['WORKER0_IP_ADDRESS']
WORKER0_PORT = CONFIG_PARAMS['WORKER0_PORT']

from typing import List
from ConsoleUtils import printError

class Client():
    def __init__(self, name: str = "Worker0", ip = WORKER0_IP_ADDRESS, port = WORKER0_PORT):
        self.name = name
        self.IP = ip
        self.PORT = port
        self.n = None
        self.vector: List[int] = []
        self.loaded = False
        self.sortedVector = None
        
        self.__connect()
                
    def __connect(self):
        self.worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.worker.connect((self.IP, self.PORT))
        
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception:
            printError("No fue posible conectarse al servidor. Revise que haya un servidor con Worker_0")
            exit()
        self.alive = True
    
    # (Handler) Recibir los mensajes del servidor
    def receive_messages(self):
        try:
            while True:
                toUnpack = self.worker.recv(4)
                if not toUnpack:
                    break
                size = struct.unpack("i", toUnpack)[0]
                
                #print(f"recieving: {size}")
            
                data = self.worker.recv(size)
                message = pickle.loads(data)
                if(type(message) == list):
                    printInfo(f"Guardando vector en `{self.name}Response.txt`")
                    self.sortedVector = message
                    with open(f"./vectors/{self.name}Response.txt", "w") as file:
                        for el in message:
                            file.write(f"{el}\n")
                else:
                    print('\r', end='')
                    printServerMessage(message)
        except Exception:
            printError(f"Error recibiendo mensajes: {traceback.format_exc()}")
            
        finally:
            self.disconnect()

    # Desconectarse del servidor
    def disconnect(self):
        printSubtitle("Desconectando del servidor...")
        self.alive = False
        self.worker.close()
    
    def setVector(self, data: List):
        self.vector = data
        self.setN(len(self.vector))
        self.loaded = True
        
        return self
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
    
    def sort(self, type: int, time: float, startIndex: int = 0):        
        self.sortedVector = None
        if(not self.alive):
            printError("No existe una conexión, cerrando cliente.")
            return None
        if(not self.loaded):
            printError("No se puede organizar, no se ha cargado el vector: Sorting.load()")
            return None        
        
        data = pickle.dumps(self.vector)
        self.worker.sendall(struct.pack("i", len(data))) # Información guardada en 4 bytes - 32 bits - "int" --- https://docs.python.org/3/library/struct.html#format-characters 
        self.worker.sendall(data) # La información enviada arriba incluye la cantidad de información que se envió
        self.worker.sendall(struct.pack("i", type))
        self.worker.sendall(struct.pack("f", time)) # Float también se guarda en 4 bytes
        self.worker.sendall(struct.pack("i", startIndex))
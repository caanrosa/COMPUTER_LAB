from ConsoleUtils import *

from config import CONFIG_PARAMS
from typing import List
import socket
import threading
import pickle
import struct
from SortAlgorithms import merge_sort, heap_sort, quick_sort
from Client import *
import timeit

# Configuration Parameters
IP_ADDRESS = CONFIG_PARAMS['WORKER0_IP_ADDRESS']
PORT = CONFIG_PARAMS['WORKER0_PORT']

class Worker():
    def __init__(self):
        
        printTitle("Configuracion inicial")
        printOption(1, "Worker_0")
        printOption(2, "Worker_1")
        
        op = 0
        while(op < 1 or op > 2):
            op = getInputInt()
        
        self.IP = CONFIG_PARAMS[f'WORKER{op-1}_IP_ADDRESS']
        self.PORT = CONFIG_PARAMS[f'WORKER{op-1}_PORT']
        self.MAX_CLIENTS = CONFIG_PARAMS[f'WORKER{op-1}_MAX_CLIENTS']
        self.LIST_OF_CLIENTS: List["socket.socket"] = []
        
        printBottom()
        
        self.start_server()
        

    # Remove Client from List of Clients
    def remove_client(self, client_socket: "socket.socket") -> None:
        if client_socket in self.LIST_OF_CLIENTS:
            self.LIST_OF_CLIENTS.remove(client_socket)

    def sendToClient(self, data, client_socket: "socket.socket"):
        try:
            # Misma lógica usada para enviar el vector desde el cliente, pero esta vez hacia él
            data = pickle.dumps(data)
            client_socket.sendall(struct.pack("i", len(data)))
            #print(f"sending: {len(data)}")
            client_socket.sendall(data)
        except Exception as ex:
            client_socket.close()
            self.remove_client(client_socket)

    # Handle Client Method (Clients Secondary Threads)
    def handle_client(self, client_socket: "socket.socket", client_address: "socket._RetAddress") -> None:
        try:
            self.sendToClient('Conectado con el servidor', client_socket)
            
            while True:
                toUnpack = client_socket.recv(4)
                size = struct.unpack("i", toUnpack)
                size = size[0]
                
                dataRecieved = []
                while(len(b"".join(dataRecieved)) < size):
                    dataRecieved.append(client_socket.recv(size - len(b"".join(dataRecieved))))
                vector = pickle.loads(b"".join(dataRecieved))
                
                type = struct.unpack("i", client_socket.recv(4))[0]
                time = struct.unpack("f", client_socket.recv(4))[0]
                
                sizeStartInfo = struct.unpack("i", client_socket.recv(4))[0]
                
                startInfoRecieved = []
                while(len(b"".join(startInfoRecieved)) < sizeStartInfo):
                    startInfoRecieved.append(client_socket.recv(sizeStartInfo - len(b"".join(startInfoRecieved))))
                startInfo = pickle.loads(b"".join(startInfoRecieved))
                
                printClientMessage("Vector recibido")
                #printClientMessage(vector)
                printClientMessage(f"{len(vector)} elems. - Max: {time}s - Desde posición {startInfo}")
                
                match type:
                    case 1: # MERGESORT
                        res, limit = merge_sort(vector, time, startInfo)
                    case 2: # HEAPSORT
                        res, limit = heap_sort(vector, time)
                    case 3: # QUICKSORT
                        res, limit = quick_sort(vector, time, startInfo)
                
                if(limit.maxReached):
                    printTitle("Looking for Worker_1")                    
                    # TODO: Los demás tipos de sort
                    if(type == 1):
                        worker1 = Client("Worker1", CONFIG_PARAMS['WORKER1_IP_ADDRESS'], CONFIG_PARAMS['WORKER1_PORT'])
                        worker1.setVector(res)
                        worker1.sort(type, 0, res.index(limit.lastData[0]))
                        printSubtitle("Esperando respuesta de Worker_1...")
                        
                        waiting = True
                        while(waiting):
                            if(worker1.sortedVector):
                                res = worker1.sortedVector
                                waiting = False   
                                
                    if(type == 3):
                        worker1 = Client("Worker1", CONFIG_PARAMS['WORKER1_IP_ADDRESS'], CONFIG_PARAMS['WORKER1_PORT'])
                        worker1.setVector(res)
                        worker1.sort(type, 0, limit.lastData)
                        printSubtitle("Esperando respuesta de Worker_1...")
                        
                        waiting = True
                        while(waiting):
                            if(worker1.sortedVector):
                                res = worker1.sortedVector
                                waiting = False   
                        pass
                    
                
                #print(res)
                printSubtitle("Enviando resultado a cliente")  
                self.sendToClient(f"Tomó {timeit.default_timer() - limit.start}s", client_socket)
                self.sendToClient(res, client_socket)
                        
        except Exception:
            printError(f'Error en cliente {client_address[0]}: {traceback.format_exc()}')
            self.remove_client(client_socket)
        finally:
            client_socket.close()


    def start_server(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.IP, self.PORT))
        server_socket.listen(self.MAX_CLIENTS)

        printSubtitle(f"Iniciando servidor en {self.IP}:{self.PORT}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                self.LIST_OF_CLIENTS.append(client_socket)
                printInfo(client_address[0] + ' conectado')

                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
        except Exception as ex:
            printError(f"Error aceptando clientes: {ex}")
            printError("Cerrando el servidor.")
        finally:
            for client in self.LIST_OF_CLIENTS:
                client.close()
            server_socket.close()


if __name__ == '__main__':
    printTitle("SERVIDOR")
    Worker()

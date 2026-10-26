import socket
import struct

# Clase que maneja la recepción de datos vía UDP por 
# parte de la ESP32 (Cliente).
class ReceptorDatos():
    def __init__(self, host, puerto, bufferSize):
        self.host = host
        self.puerto = puerto
        self.bufferSize = bufferSize

        self.sock = socket.socket(socket.AF_INET, 
                                  socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.puerto))
        self.running = False
        self.sock.setblocking(False)

    def recepcion(self):
        " Inicio de la recepción datos de la ESP32 (Cliente)"
        try:
            dato = None

            while True:
                try:
                    datos, direccion = self.sock.recvfrom(
                        self.bufferSize)
                    # Deserializamos.
                    dato = struct.unpack("<iii", datos)
                except BlockingIOError:
                    break
            return dato
        except Exception as ex:
            print(f"Error recibiendo los datos: {ex}")
            return None
import socket
import threading
import json
import sys
import random
import pickle
from necesario import generar_json

__author__ = 'Tomas Burotto Clement'

PORT = 1313
IP_SERVER = "localhost"


class Profesor:
    def __init__(self, user, password):
        self.user = user
        self.clases = []
        self.password = password
        self.name = ""
        self.host = IP_SERVER
        self.port = PORT
        self.accion = {}
        self.s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.clases_actuales = []

        try:
            self.s_client.connect((self.host, self.port))
            recibidor = threading.Thread(target=self.recibir, args=())
            recibidor.daemon = True
            self.enviar_datos({"accion": "login", "data": (user,password)})
            self._isalive = True
            recibidor.start()

        except socket.error:
            print("No fue posible conectarse, revise la conexion")
            sys.exit()

    def recibir(self):
        while True:

            if True:
                data = self.s_client.recv(1024)
                data = data.decode("utf-8")
                data = json.loads(data)
                print("Data: {}".format(data))

                if data["accion"] == "login":
                    if data["data"][0]:
                        self.connected = True
                        self.name = data["data"][1]
                        self.id = data["data"][3]
                        self.clases = data["data"][2]
                    else:
                        self.connected = False
                elif data["accion"] == "clases":
                    self.clases_actuales = data["data"]



            else:
                while len(self.bytes) != self.largo_cancion:
                    data = self.s_client.recv(2**20)
                    print(len(data))
                    self.bytes.extend(data)
                self.recibiendo_cancion = False


    def enviar_datos(self, datos):
        datos_a_enviar = json.dumps(datos)
        self.s_client.send(datos_a_enviar.encode("utf-8"))

    def disconnect(self):
        self._isalive = False
        msj = {"mensaje": "cliente desconectado"}
        self.enviar_datos(msj)

    def crear_curso(self, sigla, nombre):
        msj = {"accion": "crear_curso", "data":(sigla, nombre, self.id)}
        self.enviar_datos(msj)

    def get_clases(self, sigla):
        msj = {"accion": "obtener_clases", "data": sigla}
        self.enviar_datos(msj)

    def crear_clase(self, registro, sigla, numero):
        n = random.randint(0,100000)
        msj = {"accion": "crear_registro", "data":(n,sigla,numero,registro)}
        self.enviar_datos(msj)

    def clase_en_vivo(self, numero, sigla):
        msj = {"accion": "clase_vivo", "data":(sigla,numero)}
        self.enviar_datos(msj)

    def send_translate(self, mensaje, curso):
        msj = {"accion": "traduccion", "data": (curso,mensaje)}
        self.enviar_datos(msj)

    def terminar_clase(self,n,curso):
        msj = {"accion": "terminar_clase", "data": (n,curso)}
        self.enviar_datos(msj)

    def siguiente(self,n):
        msj = {"accion": "siguiente", "data": n}
        self.enviar_datos(msj)

    def anterior(self,n):
        msj = {"accion": "anterior", "data": n}
        self.enviar_datos(msj)

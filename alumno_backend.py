import socket
import threading
import json
import sys
import random
import pickle
from necesario import generar_json
from PyQt5.QtCore import (QObject, pyqtSignal)

PORT = 1313
IP_SERVER = "localhost"

class Alumno:
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
        self.clases_vivo = []
        self.traduccion_actual = ""
        self.curso_actual = 0
        self.senhal = Senhal()
        self.senhal2 = Senhal()

        try:
            self.s_client.connect((self.host, self.port))
            recibidor = threading.Thread(target=self.recibir, args=())
            recibidor.daemon = True
            self.enviar_datos({"accion": "login_alumno", "data": (user, password)})
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
                    if data["data"] != []:
                        self.registro = json.loads(data["data"][0][3])

                elif data["accion"] == "actualizar_vivo":
                    self.clases_vivo = data["data"]

                elif data["accion"] == "traduccion":
                    if self.curso_actual == int(data["data"][0]):
                        self.traduccion_actual = data["data"][1]
                        print("esto es backend:{}".format(self.traduccion_actual))
                        self.senhal.escribe_senhal.emit()
                elif data["accion"] == "registro":
                    self.registro = data["data"][0]
                    print(self.registro)

                elif data["accion"] == "siguiente":
                    if self.curso_actual == int(data["data"]):
                        self.senhal2.escribe_senhal.emit()




    def enviar_datos(self, datos):
        datos_a_enviar = json.dumps(datos)
        self.s_client.send(datos_a_enviar.encode("utf-8"))

    def disconnect(self):
        self._isalive = False
        msj = {"mensaje": "cliente desconectado"}
        self.enviar_datos(msj)

    def inscribir_curso(self, sigla):
        msj = {"accion": "inscribir_alumno", "data":(sigla, self.id)}
        self.enviar_datos(msj)

    def get_clases(self, sigla):
        msj = {"accion": "obtener_clases", "data": sigla}
        self.enviar_datos(msj)

    def crear_clase(self, registro, sigla, numero):
        n = random.randint(0,100000)
        msj = {"accion": "crear_registro", "data":(n,sigla,numero,registro)}
        self.enviar_datos(msj)

    def buscar_vivo(self,sigla):
        msj = {"accion": "buscar_vivo", "data":sigla}
        self.enviar_datos(msj)

    def get_registro(self, numero, curso):
        pass
        #msg = {"accion": "get_registro", "data":(curso,numero)}
        #self.enviar_datos(msg)


class Senhal(QObject):
    escribe_senhal = pyqtSignal()




import socket
import threading
import json
import sys
import pickle

__author__ = 'Tomas Burotto Clement'

PORT = 13134
IP_SERVER = "localhost"


class Client:
    def __init__(self, Back):
        self.BE = Back
        self.host = IP_SERVER
        self.port = PORT
        self.accion = {}
        self.s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bytes = bytearray()
        self.recibiendo_cancion = False
        try:
            self.s_client.connect((self.host, self.port))
            recibidor = threading.Thread(target=self.recibir, args=())
            recibidor.daemon = True
            self._isalive = True
            recibidor.start()

        except socket.error:
            print("No fue posible conectarse, revise la conexion")
            sys.exit()

    def recibir(self):
        while True:
            if not self.recibiendo_cancion:
                data = self.s_client.recv(1024)
                print(len(data))
                data = data.decode("utf-8")
                data = json.loads(data)
                print("Data: {}".format(data))
                if data["accion"] == "sala":
                    self.BE.set_salas(data["value"])
                elif data["accion"] == "envio_cancion":
                    self.recibiendo_cancion = True
                    self.largo_cancion = data["value"]
                elif data["accion"] == "login":
                    self.BE.login()
                elif data["accion"] == "chat_msg":
                    self.BE.set_chat(data["value"])
                elif data["accion"] == "comienzo_juego":
                    self.BE.empezar_juego(data["value"])
                elif data["accion"] == "cancion_recibida":
                    with open("Data/"+data["value"], "wb") as file:
                        file.write(self.bytes)
                    self.bytes = bytearray()
                elif data["accion"] == "user_info":
                    self.BE.puntos = data["value"]

                elif data["accion"] == "puntajes":
                    self.BE.add_puntajes(data["value"])

                elif data["accion"] == "sala_puntaje":
                    self.BE.add_tiempo(data["value"])
                elif data["accion"] == "error":
                    self.BE.error(data["value"])
                elif data["accion"] == "add_puntaje_sala":
                    self.BE.puntaje_sala(data["value"])
                elif data["accion"] == "remove_user":
                    self.BE.remove_user(data["value"])

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

if __name__ == "__main__":
    usuario = str(input("> Ingrese Nombre Usuario"))
    cliente = Client()
    while True:
        inputing = input("[1] Mandar Mensaje\n [2] Desconectarse\n> ")
        if inputing == "1":
            texto = input("> ")
            cliente.enviar_datos({"mensaje": texto})
        elif inputing == "2":
            cliente.disconnect()
            break

import socket
import threading
import sys
import json
from Server import server_BE
import pickle
import time
import os
__author__ = "Tomas Burotto Clement"

PORT = 13134
IP_HOST = "localhost"

class Server:

    def __init__(self):
        self.server_name = "PrograPop"
        self.host = IP_HOST
        self.port = PORT
        self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_server.bind((self.host, self.port))
        self.s_server.listen(20)
        self.clientes = []
        self.BE = server_BE.Server_BE(self)
        thread = threading.Thread(target=self.aceptar, daemon=True)
        thread.setDaemon(True)
        thread.start()

    def aceptar(self):
        while len(self.clientes) < 40:
            cliente_nuevo, adress = self.s_server.accept()
            print("> Cliente_Conectado")
            self.clientes.append(cliente_nuevo)
            self.cliente_actual = cliente_nuevo
            thread_client = threading.Thread(target=self.inicio)
            thread_client.setDaemon(True)
            thread_client.start()

    def inicio(self):
        cliente = self.cliente_actual
        while True:
            time.sleep(0.2)
            try:
                data = cliente.recv(2048)
                print(data)
                data_decoded = data.decode('utf-8')
                accion = json.loads(data_decoded)
                print("data recibido")
                print(accion)

                if accion["accion"] == "name":
                    for user in self.BE.usuarios:
                        if user.name == accion["value"][0]:
                            mensaje = {"accion": "error", "value": "Usuario ya existente"}
                            msg_json = json.dumps(mensaje)
                            cliente.send(msg_json.encode("utf-8"))
                            raise Exception("USUARIO YA EXISTE")

                    self.BE.usuarios.append(server_BE.Usuario(accion["value"][0], cliente))
                    socket_name = accion["value"]
                    lista = os.listdir("Songs/")
                    for archivo in lista:
                        if os.path.isdir("Songs/" + archivo):
                            lista2 = os.listdir("Songs/" + archivo + "/")
                            for archivo2 in lista2:
                                if ".wav" in archivo2 and archivo2 not in accion["value"][1]:
                                    data = bytearray()
                                    n = 0
                                    with open("Songs/" + archivo + "/" + archivo2, "rb") as file:
                                        for line in file:
                                            data.extend(line)
                                    mensaje = {"accion": "envio_cancion", "value": len(data)}
                                    msg_json = json.dumps(mensaje)
                                    cliente.send(msg_json.encode("utf-8"))
                                    time.sleep(2)
                                    cliente.send(data)
                                    time.sleep(2)
                                    mensaje = {"accion": "cancion_recibida", "value": archivo2}
                                    mensaje = json.dumps(mensaje)
                                    cliente.send(mensaje.encode("utf-8"))
                    mensaje = {"accion": "login", "value": 1}
                    msg_json = json.dumps(mensaje)
                    cliente.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "desconectar":
                    self.BE.desconectar(accion["value"])
                    print("> Usuario {} desconectado".format(accion["value"]))
                    self.clientes.remove(cliente)
                    break

                elif accion["accion"] == "get_info":
                    info = self.BE.get_info(accion["value"])
                    dic = {"accion": "user_info", "value": info}
                    info_json = json.dumps(dic)
                    cliente.send(info_json.encode("utf-8"))

                elif accion["accion"] == "get_salas":
                    msg = {"accion": "sala", "value": []}
                    for sala in self.BE.salas:
                        sala = sala.get_info()
                        msg["value"].append(sala)
                    print("Mensaje a enviar {}".format(msg))
                    msg_json = json.dumps(msg)
                    cliente.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "user_sala":
                    for sala in self.BE.salas:
                        if sala.name == accion["value"][1]:
                            for usuario in self.BE.usuarios:
                                if usuario.name == accion["value"][0]:
                                    sala.usuarios.append(usuario.name)
                                    mensaje = {"accion": "add_puntaje_sala", "value": [(usuario.name, usuario.puntos)]}
                                    msg_json = json.dumps(mensaje)
                                    for usr in self.BE.usuarios:
                                        if usr.name in sala.usuarios:
                                            usr.socket.send(msg_json.encode("utf-8"))
                                    lista = []
                                    for usr2 in self.BE.usuarios:
                                        for names in sala.usuarios:
                                            if usr2.name == names and names != usuario.name:
                                                lista.append((usr2.name, usr2.puntos))
                                    time.sleep(0.1)
                                    mensaje = {"accion": "add_puntaje_sala", "value": lista}
                                    msg_json = json.dumps(mensaje)
                                    cliente.send(msg_json.encode("utf-8"))
                                    time.sleep(0.2)
                                    if len(sala.usuarios) == 1:
                                        thread = threading.Thread(target=sala.empezar, daemon=True)
                                        thread.start()

                                usuario.sala_actual = sala.name

                elif accion["accion"] == "desconectar_sala":
                    sala1 = accion["value"][1]
                    name = accion["value"][0]
                    for sala in self.BE.salas:
                        if sala.name == sala1:
                            sala.usuarios.remove(name)
                    for usuario in self.BE.usuarios:
                        if usuario.name == name:
                            usuario.sala_actual = None
                    for usuario in self.BE.usuarios:
                        if usuario.sala_actual == sala1:
                            mensaje = {"accion": "remove_user", "value": name}
                            msg_json = json.dumps(mensaje)
                            usuario.socket.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "chat":
                    print("1")
                    sala1 = accion["value"][1]
                    msg = accion["value"][0]
                    name = accion["value"][2]
                    for sala in self.BE.salas:
                        if sala1 == sala.name:
                            for usr in sala.usuarios:
                                for usuario in self.BE.usuarios:
                                    if usr == usuario.name:
                                        mensaje = {"accion": "chat_msg", "value": "{} : {}".format(name, msg)}
                                        msg_json = json.dumps(mensaje)
                                        usuario.socket.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "boton_presionado":
                    for sala in self.BE.salas:
                        if sala.name == accion["value"][1]:
                            for usuario in sala.usuarios:
                                if usuario == accion["value"][0]:
                                    if accion["value"][2] in sala.actual_song.name:
                                        sala.canciones_correctas += 1
                                        puntos = (20 - sala.tiempo_actual)*100
                                    else:
                                        puntos = 0
                                        sala.canciones_incorrectas += 1
                                    for usr in self.BE.usuarios:
                                        if usr.name == accion["value"][0]:
                                            usr.puntos += puntos
                                            print("Usuario {} tiene ahora {}".format(usr.name, usr.puntos))
                                            for usrs in self.BE.usuarios:
                                                if usrs.name in sala.usuarios:
                                                    if puntos != 0:
                                                        mensaje = {"accion": "sala_puntaje",
                                                               "value": (usr.name, 20 - (puntos / 100), usr.puntos)}
                                                        msg_json = json.dumps(mensaje)
                                                        usrs.socket.send(msg_json.encode("utf-8"))
                                                    else:
                                                        mensaje ={"accion": "sala_puntaje",
                                                               "value": (usr.name, "Descalificado", usr.puntos)}
                                                        msg_json = json.dumps(mensaje)
                                                        usrs.socket.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "get_puntajes":
                    lista_puntajes = []
                    for user in self.BE.usuarios:
                        tupla = (user.name, user.puntos)
                        lista_puntajes.append(tupla)
                    lista_puntajes.sort(key=lambda x: x[1], reverse=True)
                    lista_salas = []
                    for sala in self.BE.salas:
                        lista_salas.append(sala)
                    lista_salas.sort(key=lambda x: x.canciones_correctas, reverse=True)
                    print(lista_puntajes)
                    print(lista_salas)
                    mensaje = {"accion": "puntajes", "value":(lista_puntajes, lista_salas[0].name, lista_salas[-1].name)}
                    msg_json = json.dumps(mensaje)
                    cliente.send(msg_json.encode("utf-8"))

            except Exception as err:
                print(err)
                break


if __name__ == "__main__":
    server = Server()
    while True:
        a = input("> ")
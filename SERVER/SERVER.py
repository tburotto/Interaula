import socket
import threading
import sys
import json
import pickle
import time
import os
import sqlite3
__author__ = "Tomas Burotto Clement"

PORT = 1313
IP_HOST = "localhost"

class Server:

    def __init__(self):
        self.server_name = "Interaula"
        self.host = IP_HOST
        self.port = PORT
        self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_server.bind((self.host, self.port))
        self.s_server.listen(20)
        self.clientes = []
        self.clases_en_vivo = []
        thread = threading.Thread(target=self.aceptar, daemon=True)
        thread.setDaemon(True)
        thread.start()
    def database(self):
        self.conn = sqlite3.connect('dbinteraula.db')
        self.cursor = self.conn.cursor()

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


                if accion["accion"] == "login":
                    usr = accion["data"][0]
                    pswd = accion["data"][1]
                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM Profesores WHERE username ='" + str(usr) + "' AND password ='" + str(
                        pswd) + "';")
                    users = cursor.fetchall()
                    if len(users)!=1:
                        mensaje = {"accion":"login", "data":(False,"")}
                        msg_json = json.dumps(mensaje)
                        cliente.send(msg_json.encode("utf-8"))
                    else:
                        name = users[0][1]
                        id_profe = users[0][0]
                        cursor.execute("SELECT * FROM Cursos WHERE id_profe = '"+str(id_profe)+"';")
                        cursos = cursor.fetchall()
                        mensaje = {"accion": "login", "data": (True, name, cursos, id_profe)}
                        msg_json = json.dumps(mensaje)
                        cliente.send(msg_json.encode("utf-8"))
                    con.close()

                elif accion["accion"] == "login_alumno":
                    usr = accion["data"][0]
                    pswd = accion["data"][1]
                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM Alumnos WHERE username ='" + str(usr) + "' AND password ='" + str(
                        pswd) + "';")
                    users = cursor.fetchall()
                    if len(users) != 1:
                        mensaje = {"accion": "login", "data": (False, "")}
                        msg_json = json.dumps(mensaje)
                        cliente.send(msg_json.encode("utf-8"))
                    else:
                        name = users[0][3]
                        id_alumno = users[0][0]
                        cursor.execute("SELECT Cursos.id, Cursos.nombre, Cursos.id_profe FROM Cursos, Alumnos_en_cursos  WHERE Alumnos_en_cursos.id_alumno =" + str(id_alumno) + " AND Alumnos_en_cursos.id_curso = Cursos.id;")
                        cursos = cursor.fetchall()
                        mensaje = {"accion": "login", "data": (True, name, cursos, id_alumno)}
                        msg_json = json.dumps(mensaje)
                        cliente.send(msg_json.encode("utf-8"))
                    con.close()


                elif accion["accion"] == "crear_curso":
                    sigla = accion["data"][0]
                    nombre = accion["data"][1]
                    id_profe = accion["data"][2]
                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO Cursos VALUES ("+str(sigla)+",'"+str(nombre)+"',"+str(id_profe)+");")
                    con.commit()
                    con.close()

                elif accion["accion"] == "obtener_clases":
                    sigla = accion["data"]
                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM Clases WHERE curso ="+str(sigla)+";")
                    clases = cursor.fetchall()
                    mensaje = {"accion": "clases", "data":clases}
                    msg_json = json.dumps(mensaje)
                    cliente.send(msg_json.encode("utf-8"))
                    con.close()

                elif accion["accion"] == "crear_registro":
                    id = accion["data"][0]
                    sigla = accion["data"][1]
                    numero = accion["data"][2]
                    registro = accion["data"][3]
                    registro = json.dumps(registro)

                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO Clases VALUES ("+str(id)+","+str(sigla)+","+str(numero)+",'"+registro+"');")

                    con.commit()
                    con.close()
                elif accion["accion"] == "inscribir_alumno":
                    id = accion["data"][1]
                    sigla = accion["data"][0]

                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO Alumnos_en_cursos VALUES (" + str(id) + "," + str(sigla) + ");")

                    con.commit()
                    con.close()

                elif accion["accion"] == "clase_vivo":
                    id_clase = accion["data"][0]
                    numero_clase = accion["data"][1]
                    self.clases_en_vivo.append(accion["data"])

                elif accion["accion"] == "buscar_vivo":
                    vivos = []
                    for i in self.clases_en_vivo:
                        if accion["data"] == i[0]:
                            vivos.append(i)
                    msj = {"accion": "actualizar_vivo", "data": vivos}
                    msg_json = json.dumps(msj)
                    cliente.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "traduccion":
                    for a in self.clientes:
                        msj = {"accion": "traduccion", "data": accion["data"]}
                        msg_json = json.dumps(msj)
                        a.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "get_registro":
                    print("ACA")
                    curso = int(accion["data"][0])
                    numero = int(accion["data"][1])

                    print(curso,numero)
                    con = sqlite3.connect("dbinteraula.db")
                    cursor = con.cursor()
                    cursor.execute("SELECT data FROM Clases WHERE numero="+str(numero)+" AND curso ="+str(curso)+";")

                    registro = cursor.fetchall()

                    msj = {"accion": registro, "data": registro}
                    msg_json = json.dumps(msj)
                    cliente.send(msg_json.encode("utf-8"))
                    con.close()

                elif accion["accion"] == "terminar_clase":
                    i = 0
                    for clase in self.clases_en_vivo:
                        if clase[0] == data[1]:
                            self.clases_en_vivo.pop(i)
                            break
                        else:
                            i+=1

                elif accion["accion"] == "siguiente":
                    for cl in self.clientes:
                        msj = {"accion":"siguiente", "data": accion["data"]}
                        msg_json = json.dumps(msj)
                        cl.send(msg_json.encode("utf-8"))

                elif accion["accion"] == "anterior":
                    for cl in self.clientes:
                        msj = {"accion": "anterior", "data": accion["data"]}
                        msg_json = json.dumps(msj)
                        cl.send(msg_json.encode("utf-8"))
            except Exception as err:
                print(err)
                break

if __name__ == "__main__":
    server = Server()
    while True:
        a = input("> ")
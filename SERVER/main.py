from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QListWidget, QDialog
from PyQt5.QtMultimedia import QSound
from PyQt5.QtTest import QTest
from PyQt5.QtGui import QFont
from Client import BE_Client
import time

DATA = uic.loadUiType("ventana.ui")


class MainWindow(DATA[0], DATA[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.scrollArea.hide()
        self.label_6.hide()
        self.pushButton.clicked.connect(self.iniciar_sesion)
        self.setWindowTitle("PrograPop")
        self.scrollArea_2.hide()
        self.label_tiempo = QLabel("20", self)
        self.label_tiempo.move(500, 300)
        self.label_tiempo.resize(100,100)
        self.label_tiempo.setFont(QFont("SansSerif", 20))
        self.label_tiempo.hide()
        self.song_name = None
        self.song = None
        self.salas = [{"name": "Recibiendo Canciones, pulsa actualizar!", "usuarios":[], "artistas": "None", "tiempo_restante": 0}]
        self.a = 0
        self.chat = QListWidget(self)
        self.chat.resize(1000, 300)
        self.chat.move(30,370)
        self.chat.hide()
        self.puntajes = None
        self.login = False


    def iniciar_sesion(self):
        self.name = self.lineEdit.text()
        self.setWindowTitle("PrograPop ({})".format(self.name))
        self.usuario_back = BE_Client.Client_Back(self)
        while not self.login:
            pass
        time.sleep(2)
        self.usuario_back.get_salas()
        time.sleep(2)
        self.usuario_back.get_info()
        time.sleep(0.2)
        self.label_6.setText("Bienvenido {}\nTienes {} puntos".format(self.name, self.usuario_back.puntos))
        self.label_6.show()
        self.lineEdit.hide()
        self.label_2.hide()
        self.pushButton.hide()
        self.titulo.setText("Elige una Sala")
        self.label_inferior = QLabel("Haz click sobre una sala para ingresar", self)
        self.label_inferior.move(500,200)
        self.label_inferior.show()

        self.lista_items = QListWidget(self)

        for item in self.salas:
            self.lista_items.addItem("Sala : {}, Usuarios: {}, artistas: {}, tº restante: {}".format(item["name"],
                                                                                    len(item["usuarios"]), item["artistas"], item["tiempo_restante"]))

        self.lista_items.show()
        self.lista_items.resize(600,200)
        self.lista_items.move(300,200)

        self.lista_items.itemClicked.connect(self.conectarse_sala)
        self.actualizar = QPushButton("Actualizar", self)
        self.actualizar.move(1000, 100)
        self.actualizar.show()
        self.actualizar.clicked.connect(self.actualizar_salas)

        self.tabla_de_puntos = QPushButton("Tabla de puntajes", self)
        self.tabla_de_puntos.move(40, 600)
        self.tabla_de_puntos.resize(200,20)
        self.tabla_de_puntos.show()
        self.tabla_de_puntos.clicked.connect(self.puntos_dialog)

    def conectarse_sala(self, item):

        self.label_inferior.hide()
        self.tabla_de_puntos.hide()
        self.lista_items.hide()
        name = item.text().split(",")[0].split(":")[1].replace(" ", "")

        self.sala_actual = name
        self.usuario_back.connect_sala(name)

        self.usuario_back.get_info()
        self.scrollArea.hide()
        self.titulo.setText(name)
        self.label_6.hide()
        self.actualizar.hide()
        self.volver = QPushButton("Salir", self)
        self.volver.move(30, 30)
        self.volver.clicked.connect(self.volver_menu)
        self.volver.show()

        # Tabla de puntajes

        self.tabla_puntajes_sala = QListWidget(self)
        self.tabla_puntajes_sala.resize(200, 100)
        self.tabla_puntajes_sala.move(930, 200)
        self.tabla_puntajes_sala.addItem("Puntajes")
        self.tabla_puntajes_sala.show()

        # CHAT

        self.chat.show()
        self.chat.addItem("Chat")
        self.line_chat = QLineEdit(self)
        self.line_chat.move(40, 690)
        self.line_chat.resize(1000, 30)
        self.chatButton = QPushButton("Enviar", self)
        self.chatButton.move(1050, 690)
        self.chatButton.show()
        self.line_chat.show()
        self.chatButton.clicked.connect(self.enviar_mensaje)

        # Tabla de tiempos

        self.sala_tabla = QListWidget(self)
        self.sala_tabla.resize(200,100)
        self.sala_tabla.move(930,30)
        self.sala_tabla.addItem("Tiempos")
        self.sala_tabla.show()


        # Juego
        self.opcion1 = QPushButton("opcion1", self)
        self.opcion2 = QPushButton("opcion2", self)
        self.opcion3 = QPushButton("opcion3 ", self)



        self.opcion1.move(30, 200)
        self.opcion2.move(400, 200)
        self.opcion3.move(700, 200)

        self.opcion1.resize(200,30)
        self.opcion2.resize(200, 30)
        self.opcion3.resize(200, 30)

        self.opcion1.clicked.connect(self.opcion_selecta)
        self.opcion2.clicked.connect(self.opcion_selecta)
        self.opcion3.clicked.connect(self.opcion_selecta)

        while self.sala_actual != None:
            while not self.song_name:
                pass
            self.song = QSound(self.song_name)
            self.song_name = None
            self.song.play()
            self.label_tiempo.show()
            self.opcion1.show()
            self.opcion2.show()
            self.opcion3.show()
            QTest.qWait(1000)
            QTest.qWait(1000)
            self.label_tiempo.setText("19")
            QTest.qWait(1000)
            self.label_tiempo.setText("19")
            QTest.qWait(1000)
            self.label_tiempo.setText("17")
            QTest.qWait(1000)
            self.label_tiempo.setText("16")
            QTest.qWait(1000)
            self.label_tiempo.setText("15")
            QTest.qWait(1000)
            self.label_tiempo.setText("14")
            QTest.qWait(1000)
            self.label_tiempo.setText("13")
            QTest.qWait(1000)
            self.label_tiempo.setText("12")
            QTest.qWait(1000)
            self.label_tiempo.setText("11")
            QTest.qWait(1000)
            self.label_tiempo.setText("10")
            QTest.qWait(1000)
            self.label_tiempo.setText("9")
            QTest.qWait(1000)
            self.label_tiempo.setText("8")
            QTest.qWait(1000)
            self.label_tiempo.setText("7")
            QTest.qWait(1000)
            self.label_tiempo.setText("6")
            QTest.qWait(1000)
            self.label_tiempo.setText("5")
            QTest.qWait(1000)
            self.label_tiempo.setText("4")
            QTest.qWait(1000)
            self.label_tiempo.setText("3")
            QTest.qWait(1000)
            self.label_tiempo.setText("2")
            QTest.qWait(1000)
            self.label_tiempo.setText("1")
            QTest.qWait(1000)
            self.opcion1.hide()
            self.opcion2.hide()
            self.opcion3.hide()
            self.sala_tabla.clear()
            self.sala_tabla.addItem("Tiempos")
            self.label_tiempo.hide()
            self.label_tiempo.setText("20")
            self.chat.addItem("Server: Preparate para la siguiente ronda")
            self.song.stop()
            QTest.qWait(1000)

    def actualizar_salas(self):
        self.lista_items.clear()
        self.usuario_back.get_salas()
        time.sleep(0.2)
        for item in self.salas:
            self.lista_items.addItem("Sala : {}, Usuarios: {}, artistas: {}, tº restante : {}".format(item["name"],
                                                                                    len(item["usuarios"]),
                                                                                    item["artistas"], item["tiempo_restante"]))
    def volver_menu(self):
        self.tabla_puntajes_sala.clear()
        self.tabla_puntajes_sala.addItem("Puntajes")
        self.tabla_puntajes_sala.hide()
        self.sala_tabla.clear()
        self.sala_tabla.hide()
        self.tabla_de_puntos.show()
        self.chat.clear()
        self.chat.hide()
        self.usuario_back.get_salas()
        time.sleep(0.2)
        self.usuario_back.disconnect_sala(self.sala_actual)
        time.sleep(0.2)
        self.usuario_back.get_info()
        time.sleep(0.2)
        self.sala_actual = None
        self.song.stop()
        self.titulo.setText("Elige una Sala")
        self.label_6.setText("Bienvenido {}\nTienes {} puntos".format(self.name, self.usuario_back.puntos))
        self.label_6.show()
        self.label.setText("Nombre: {} - Usuarios : {} - Artistas : {}"
                           .format(self.salas[0]["name"], len(self.salas[0]["usuarios"]), self.salas[0]["artistas"]))
        self.lista_items.show()
        self.actualizar.show()
        self.volver.hide()
        self.line_chat.hide()
        self.chatButton.hide()
        self.scrollArea_2.hide()

        self.opcion1.hide()
        self.opcion2.hide()
        self.opcion3.hide()

    def enviar_mensaje(self):
        mensaje = self.line_chat.text()
        self.line_chat.setText("")
        self.usuario_back.chat(mensaje, self.sala_actual)

    def opcion_selecta(self):
        boton = self.sender()
        self.opcion1.hide()
        self.opcion2.hide()
        self.opcion3.hide()
        self.usuario_back.desicion(boton.text())

    def puntos_dialog(self):
        dialog = QDialog(self)
        dialog.resize(500,500)
        tabla1 = QListWidget(dialog)
        tabla1.resize(150,400)
        tabla1.move(20,20)
        tabla1.addItem("Tabla de Puntajes")
        dialog.setWindowTitle("Puntajes - Presiona Esc para salir")

        self.usuario_back.get_puntajes()
        while not self.puntajes:
            pass
        for item in self.puntajes:
            tabla1.addItem("{} : {} puntos".format(item[0], item[1]))
        tabla1.show()

        label_facil = QLabel("Sala mas facil : {}".format(self.sala_facil), dialog)
        label_dificil = QLabel("Sala mas dificl: {}".format(self.sala_dificl), dialog)

        label_dificil.move(300,50)
        label_facil.move(300, 250)
        label_dificil.show()
        label_facil.show()
        dialog.show()


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
    if form.usuario_back:
        form.usuario_back.disconnect()

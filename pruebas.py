import sys
from threading import Thread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton, QTableWidget, QListWidget, QLineEdit)
from PyQt5.QtGui import QPixmap, QFont
import speech_recognition as rc

from os import listdir
from os.path import isfile, join
from archivo_salida import *

class Evento:
    def __init__(self, msg=''):
        self.msg = msg


class Texto:
    def __init__(self):
        self.texto =["----- Diapositiva 1 ---- "]
        self.diapositiva = 1

    def guardar(self, clase):
        with open(clase+".txt", "w") as archivo:
            for i in self.texto:
                archivo.write(i+"\n")
        return "archivo guardado con exito"

    def add_text(self, text):
        self.texto.append(text)

    def pass_diap(self):
        self.diapositiva += 1
        self.texto.append("----- Diapositiva {} ----- ".format(self.diapositiva))

    def back_diap(self):
        self.diapositiva -= 1
        self.texto.append("----- Diapositiva {} ----- ".format(self.diapositiva))


class MiThread(Thread):

    def __init__(self, trigger_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger = trigger_signal

    def run(self):

        # TO-DO
        self.rec = rc.Recognizer()
        while True:
            with rc.Microphone() as source:
                self.audio = self.rec.record(source, duration=6)
                w = Thread(target=self.worker)
                w.start()


    def worker(self):
        evento = Evento()
        print("aca")
        try:
            word = self.rec.recognize_google(self.audio, language="es-cl")
            evento.msg = word
            print(word)
            self.trigger.emit(evento)
        except rc.UnknownValueError:
            print("I cannot understand what you said")
            print("Say again")
        except rc.RequestError as e:
            print("Error".format(e))


class MiVentanasegundaria(QWidget):

    # Creamos una señal para manejar la respuesta del thread
    threads_response = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.thread = None
        self.texto = Texto()



    def init_gui(self):
        # Configuramos los widgets de la interfaz
        self.resize(1500, 1000)
        self.label_1 = QLabel("Bienvenido a Interaula", self)
        self.label_1.setFont(QFont("Sans Serif", 40))
        self.label_1.move(350, 100)
        self.boton = QPushButton("Ingresar", self)
        self.boton.move(500, 650)

        self.imagen = QLabel("", self)
        self.imagen.move(350, 200)
        pixmap = QPixmap("misc/interaula.png")
        pixmap = pixmap.scaled(400, 400)
        self.imagen.setPixmap(pixmap)
        self.imagen.show()

        self.setWindowTitle('Interaula')
        self.show()

        self.boton.clicked.connect(self.menu)

    def menu(self):
        self.label_1.setText("Elige un curso")
        self.label_1.move(100, 100)
        self.imagen.hide()
        self.boton.hide()
        self.curso1 = QLabel("Investigación Innovación Emprendimiento - ING2030", self)
        self.curso1.setFont(QFont("Sans Serif", 30))
        self.curso1.move(100, 300)
        self.curso1.show()
        self.boton1 = QPushButton("Abrir", self)
        self.boton1.move(1000, 300)
        self.boton1.show()
        self.boton1.clicked.connect(self.elegir_vivo)

        self.cargar = QPushButton("Cargar Archivo", self)
        self.cargar.move(100, 500)
        self.cargar.show()
        self.cargar.clicked.connect(self.cargar_archivo)

    def cargar_archivo(self):
        self.label_carga = QLabel("INGRESA EL NOMBRE DEL ARCHIVO", self)
        self.label_carga.move(100,400)
        self.label_carga.setFont(QFont("Sans Serif", 20))
        self.label_carga.show()

        self.cargar.hide()
        self.textbox = QLineEdit(self)
        self.textbox.move(100,500)
        self.textbox.show()

        self.boton_carga = QPushButton("Abrir", self)
        self.boton_carga.move(100, 600)
        self.boton_carga.show()
        self.boton_carga.clicked.connect(self.abrir_archivo)

    def abrir_archivo(self):
        nombre = self.textbox.text()
        self.registro = leer_archivo(nombre)
        print(self.registro)
        # Hideamos lo anterior
        self.label_carga.hide()
        self.textbox.hide()
        self.boton_carga.hide()

        ## Iniciamos el programa sin escucha

        self.diapos_totales = len([f for f in listdir("1/") if isfile(join("1/", f)) and ".jpg" in f])

        self.label_1.hide()
        self.curso1.hide()
        self.boton1.hide()
        # Configuramos los widgets de la interfaz
        self.diapositivas = QLabel("", self)
        # self.diapositivas.move()
        pixmap = QPixmap("1/1.jpg")
        pixmap = pixmap.scaled(650, 450)
        self.diapositivas.setPixmap(pixmap)
        self.diapositivas.show()
        self.diapositivas.move(100, 120)

        self.label = QLabel('Esperando inicio', self)
        self.label.setFont(QFont("Sans Serif", 25))
        self.boton = QPushButton('Iniciar escucha', self)
        self.boton.clicked.connect(self.start_threads)
        self.tabla = QListWidget(self)
        self.boton_2 = QPushButton("Guardar", self)
        self.boton_2.move(200, 700)
        self.boton_2.clicked.connect(self.guardar_archivo)
        self.boton_3 = QPushButton("Siguiente", self)
        self.boton_3.move(400, 600)
        self.boton_4 = QPushButton("Anterior", self)
        self.boton_4.move(200, 600)


        self.tabla.show()
        self.boton_3.show()
        self.boton_4.show()

        self.boton_3.clicked.connect(self.siguiente)
        self.boton_4.clicked.connect(self.anterior)

        self.tabla.resize(400, 600)
        self.tabla.move(800, 100)
        self.label.resize(1000, 30)
        self.label.move(100, 50)
        self.boton.move(50, 700)
        self.resize(1500, 1000)

        self.diapo = 1
        for i in self.registro[int(self.diapo - 1)]:
            self.tabla.addItem(i)

        # Conectamos la señal del thread al método que maneja
        self.threads_response.connect(self.update_labels)

        # Configuramos las propiedades de la ventana.
        self.setWindowTitle('Interaula')
        self.show()


    def start_threads(self):

        if self.thread is None or not self.thread.is_alive():
            self.thread = MiThread(self.threads_response, daemon=True)
            self.thread.start()


    def update_labels(self, evento):
        self.label.setText("[PROFESOR] "+evento.msg)
        self.registro[self.diapo-1].append("[PROFESOR] "+evento.msg)
        self.tabla.addItem("[PROFESOR] "+evento.msg)

    def guardar_archivo(self):
        nombre = str(input("Nombre del archivo"))
        generar_archivo(self.registro, nombre)

    def anterior(self):
            self.diapo -= 1
            if self.diapo >= 1:
                self.tabla.clear()
                self.texto.back_diap()
                pixmap = QPixmap("1/{}.jpg".format(self.diapo))
                pixmap = pixmap.scaled(650, 450)
                self.diapositivas.setPixmap(pixmap)
                for i in self.registro[int(self.diapo-1)]:
                    self.tabla.addItem(i)

            else:
                self.diapo +=1

    def siguiente(self):
        self.diapo += 1
        if self.diapo <= self.diapos_totales:
            self.tabla.clear()
            self.texto.back_diap()
            pixmap = QPixmap("1/{}.jpg".format(self.diapo))
            pixmap = pixmap.scaled(650, 450)
            self.diapositivas.setPixmap(pixmap)
            for i in self.registro[int(self.diapo - 1)]:
                self.tabla.addItem(i)

        else:
            self.diapo -= 1

    def elegir_vivo(self):
        #Seteamos el registro en cero

        self.diapos_totales = len([f for f in listdir("1/") if isfile(join("1/", f)) and ".jpg" in f])
        self.registro = [["Diapositiva {}".format(i)] for i in range(1,self.diapos_totales+1)]

        self.label_1.hide()
        self.curso1.hide()
        self.boton1.hide()
        # Configuramos los widgets de la interfaz
        self.diapositivas = QLabel("", self)
        # self.diapositivas.move()
        pixmap = QPixmap("1/1.jpg")
        pixmap = pixmap.scaled(650, 450)
        self.diapositivas.setPixmap(pixmap)
        self.diapositivas.show()
        self.diapositivas.move(100, 120)

        self.label = QLabel('Esperando inicio', self)
        self.label.setFont(QFont("Sans Serif", 25))
        self.boton = QPushButton('Iniciar escucha', self)
        self.boton.clicked.connect(self.start_threads)
        self.tabla = QListWidget(self)
        self.tabla.addItem("Diapositiva 1")
        self.boton_2 = QPushButton("Guardar", self)
        self.boton_2.move(200, 700)
        self.boton_2.clicked.connect(self.guardar_archivo)
        self.boton_3 = QPushButton("Siguiente", self)
        self.boton_3.move(400, 600)
        self.boton_4 = QPushButton("Anterior", self)
        self.boton_4.move(200, 600)

        self.label.show()
        self.boton.show()
        self.tabla.show()
        self.boton_2.show()
        self.boton_3.show()
        self.boton_4.show()

        self.boton_3.clicked.connect(self.siguiente)
        self.boton_4.clicked.connect(self.anterior)

        self.tabla.resize(400, 600)
        self.tabla.move(800, 100)
        self.label.resize(1000, 30)
        self.label.move(100, 50)
        self.boton.move(50, 700)
        self.resize(1500, 1000)

        self.diapo = 1

        # Conectamos la señal del thread al método que maneja
        self.threads_response.connect(self.update_labels)

        # Configuramos las propiedades de la ventana.
        self.setWindowTitle('Interaula')
        self.show()


app = QApplication([])
form = MiVentanasegundaria()
sys.exit(app.exec_())
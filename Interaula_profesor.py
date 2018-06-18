import sys
from threading import Thread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QDialog, QApplication, QWidget, QLabel,QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QListWidget, QLineEdit, QTableWidgetItem, QComboBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtTest import QTest
from necesario import *
from os import listdir
from os.path import isfile, join
from archivo_salida import *
from profesor_backend import *

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
        self.label_1 = QLabel("Bienvenido a Interaula, ingrese nombre de usuario y password", self)
        self.label_1.setFont(QFont("Sans Serif", 20))
        self.label_1.move(350, 100)
        self.boton = QPushButton("Ingresar", self)
        self.boton.move(500, 650)

        self.label2 = QLabel("Usuario", self)
        self.label3 = QLabel("Password", self)
        self.label2.move(300,400)
        self.label3.move(300, 450)
        self.user_line = QLineEdit(self)
        self.pass_line = QLineEdit(self)
        self.user_line.resize(200,20)
        self.pass_line.resize(200,20)
        self.user_line.move(400, 400)
        self.pass_line.move(400, 450)
        self.pass_line.setEchoMode(QLineEdit.Password)
        self.user_line.show()
        self.pass_line.show()
        self.imagen = QLabel("", self)
        self.imagen.move(20, 20)
        pixmap = QPixmap("misc/interaula.png")
        pixmap = pixmap.scaled(100, 100)
        self.imagen.setPixmap(pixmap)
        self.imagen.show()

        self.setWindowTitle('Interaula - Profesor')
        self.show()
        self.boton.clicked.connect(self.menu)

    def menu(self):
        self.usuario = Profesor(self.user_line.text(), self.pass_line.text())
        QTest.qWait(500)
        if self.usuario.connected:
            self.label_1.setText("Bienvenido "+self.usuario.name)
            self.label2.hide()
            self.label3.hide()
            self.user_line.hide()
            self.pass_line.hide()
            self.boton.hide()

            #####
            self.label2.setText("Ingrese a un curso o cree uno nuevo")
            self.label2.move(100,200)

            ### Creamos tabla con los cursos disponibles

            self.tabla = QListWidget(self)
            self.tabla.addItem("Sigla                                           Nombre Curso                                          Profesor                        ")
            self.tabla.resize(700,400)
            self.tabla.move(200,200)

            i = 0
            for item in self.usuario.clases:
                self.tabla.addItem(str(item[0])+"                                           "+str(item[1]+"                                           "+str(self.usuario.name)))

            self.tabla.itemClicked.connect(self.connect_curso)
            self.tabla.show()
            ###
            self.boton_crear = QPushButton("Crear Curso", self)
            self.boton_crear.move(500,600)
            self.boton_crear.show()
            self.boton_crear.clicked.connect(self.crear_curso)

        else:
            self.label4 = QLabel("Usuario o password incorrectos, intente nuevamente", self)
            self.label4.move(400, 730)
            self.label4.show()

    def connect_curso(self, item):
        items = item.text().split("                                           ")
        self.label_1.setText("{}".format(items[1]).capitalize())
        self.usuario.get_clases(items[0])
        self.curso_actual = items[0]
        QTest.qWait(200)
        self.label2.setText("Elija una clase o cree una nueva")
        self.label2.show()

        self.combo_box = QComboBox(self)
        for elemento in self.usuario.clases_actuales:
            self.combo_box.addItem(str(elemento[2]))

        self.combo_box.move(300,300)
        self.combo_box.show()
        self.boton_cargar = QPushButton("Cargar Clase",self)
        self.boton_cargar.move(300, 500)
        self.boton_cargar.show()

        self.boton_crear2 = QPushButton("Crear Clase", self)
        self.boton_crear2.move(500, 500)
        self.boton_crear2.show()
        self.boton_crear2.clicked.connect(self.crear_clase)

        self.boton_crear.hide()
        self.tabla.hide()

    def crear_curso(self):
        self.dialog = QDialog()
        self.dialog.resize(500,500)
        label1 = QLabel("Ingrese Sigla: ", self.dialog)
        label2 = QLabel("Ingrese nombre Curso :", self.dialog)
        label1.move(60,100)
        label2.move(60, 200)
        self.line_edit1 = QLineEdit(self.dialog)
        self.line_edit2 = QLineEdit(self.dialog)
        self.line_edit1.move(230,100)
        self.line_edit2.move(230,200)
        b1 = QPushButton("Crear", self.dialog)
        b1.move(300,400)
        self.dialog.show()
        b1.clicked.connect(self.crear)

    def crear(self):
        self.usuario.crear_curso(self.line_edit1.text(), self.line_edit2.text())
        QTest.qWait(300)
        self.dialog.hide()
        self.menu()

    def crear_clase(self):
        self.combo_box.hide()
        self.boton_crear2.hide()
        self.boton_cargar.hide()

        self.label2.setText("Ingese numero de clase. Asegurate que el pdf esté en la misma carpeta con el mismo nombre")
        self.label2.resize(800,20)
        self.line_edit3 = QLineEdit(self)
        self.line_edit3.move(400,500)
        self.boton_iniciar = QPushButton("Crear", self)
        self.boton_iniciar.move(500,600)
        self.line_edit3.show()
        self.boton_iniciar.show()
        self.boton_iniciar.clicked.connect(self.empezar_clase)

    def empezar_clase(self):

        self.usuario.clase_en_vivo(self.line_edit3.text(),self.curso_actual)

        self.imagen.hide()
        self.label_1.hide()
        self.clase_actual = self.line_edit3.text()
        self.numero = str(self.line_edit3.text())
        self.diapos_totales = len([f for f in listdir(self.numero+"/") if isfile(join(self.numero+"/", f)) and ".jpg" in f])
        self.registro = [["Diapositiva {}".format(i)] for i in range(1, self.diapos_totales + 1)]

        self.line_edit3.hide()
        self.boton_iniciar.hide()
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


    def start_threads(self):
        self.boton.setText("Detener Escucha")
        self.boton.clicked.connect(self.detener)
        if self.thread is None or not self.thread.is_alive():
            self.thread = MiThread(self.threads_response, daemon=True)
            self.thread.start()

    def detener(self):
        self.thread.stop_thread()
        self.usuario.terminar_clase(self.numero, self.curso_actual)

    def update_labels(self, evento):
        self.label.setText("[PROFESOR] " + evento.msg)
        self.usuario.send_translate("[PROFESOR] " + evento.msg, self.curso_actual)
        self.registro[self.diapo - 1].append("[PROFESOR] " + evento.msg)
        self.tabla.addItem("[PROFESOR] " + evento.msg)

    def guardar_archivo(self):
        text = QLabel("Clase Creada Con Exito!")
        self.thread.stop_thread()
        print(self.registro)
        print(self.curso_actual)
        print(self.clase_actual)

        self.usuario.crear_clase(self.registro, self.curso_actual, self.clase_actual)

    def anterior(self):
        self.usuario.anterior(self.curso_actual)
        self.diapo -= 1
        if self.diapo >= 1:
            self.tabla.clear()
            self.texto.back_diap()
            pixmap = QPixmap("1/{}.jpg".format(self.diapo))
            pixmap = pixmap.scaled(650, 450)
            self.diapositivas.setPixmap(pixmap)
            for i in self.registro[int(self.diapo - 1)]:
                self.tabla.addItem(i)

        else:
            self.diapo += 1

    def siguiente(self):
        self.usuario.siguiente(self.curso_actual)
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


if __name__ == "__main__":
    app = QApplication([])
    form = MiVentanasegundaria()
    sys.exit(app.exec_())

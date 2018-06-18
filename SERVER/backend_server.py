class Server:
    def __init__(self):
        self.usuarios = []
        self.cursos = []


class User:
    def __init__(self, nombre, categoria):
        self.nombre = nombre
        self.categoria = categoria
        self.clases_inscrito = []


class Curso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.clases = []

class Clase:
    def __init__(self, id):
        self.id = id
        self.path_pdf = ""
        self.registro = ""
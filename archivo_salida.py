
def generar_archivo(lista, nombre):
    with open(nombre+".txt", "w") as archivo:
        for x in lista:
            for i in x:
                archivo.write(i+"\n")

def leer_archivo(nombre):
    with open(nombre, "r") as archivo:
        f = archivo.readlines()
        lista = []
        lista2 = ["Diapositiva 1"]
        for x in f:
            print(x)
            if "Diapositiva 1" in x:
                continue
            elif "Diapositiva" in x:
                lista.append(lista2)
                lista2 = [x]
            else:
                lista2.append(x)

    return lista

def generar_json(registro):
    pass



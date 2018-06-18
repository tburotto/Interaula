from threading import Thread
import speech_recognition as rc


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
        self.true = True

    def run(self):

        # TO-DO
        self.rec = rc.Recognizer()
        self.true = True
        while self.true:
            with rc.Microphone() as source:
                self.audio = self.rec.record(source, duration=6)
                w = Thread(target=self.worker)
                w.start()

    def worker(self):
        evento = Evento()
        print("aca")
        try:
            word = self.rec.recognize_google(self.audio, language="es")
            evento.msg = word
            print(word)
            self.trigger.emit(evento)
        except rc.UnknownValueError:
            print("I cannot understand what you said")
            print("Say again")
        except rc.RequestError as e:
            print("Error".format(e))

    def stop_thread(self):
        self.true = False


def generar_json(registro):
    n = {}
    for elemento in registro:
        n[str(elemento[0])] = []
        for i in range(1,len(elemento)):
            n[str(elemento[0])].append(elemento[i])

    return n







if __name__ =="__main__":
    a = [['Diapositiva 1', '[PROFESOR] Hola Esto es una prueba interaula', '[PROFESOR] telesistema', '[PROFESOR] bastante bien genial'], ['Diapositiva 2'], ['Diapositiva 3'], ['Diapositiva 4'], ['Diapositiva 5'], ['Diapositiva 6'], ['Diapositiva 7'], ['Diapositiva 8'], ['Diapositiva 9'], ['Diapositiva 10'], ['Diapositiva 11'], ['Diapositiva 12'], ['Diapositiva 13'], ['Diapositiva 14'], ['Diapositiva 15'], ['Diapositiva 16'], ['Diapositiva 17'], ['Diapositiva 18'], ['Diapositiva 19'], ['Diapositiva 20'], ['Diapositiva 21'], ['Diapositiva 22'], ['Diapositiva 23']]
    print(generar_json(a))

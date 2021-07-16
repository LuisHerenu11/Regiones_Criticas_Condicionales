import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Tenedores(Recurso): # la clase recurso.
    listaTenedores = [True,True,True,True,True]
    cantidadFilosofos = 0

recursoFilosofos = Tenedores() # instanciamos la clase.

regionFilosofos = Region(recursoFilosofos,threading.Semaphore(int(len(recursoFilosofos.listaTenedores)/2)))

@regionFilosofos.region
def seccionCritica():
    for l in range(2):
        indice = recursoFilosofos.listaTenedores.index(True)
        recursoFilosofos.listaTenedores[indice] = False
    logging.info(f'filosofo comiendo, quedan {recursoFilosofos.listaTenedores.count(True)} tenedores')
    time.sleep(random.randint(3,6))
    for l in range(2):
        indice = recursoFilosofos.listaTenedores.index(False)
        recursoFilosofos.listaTenedores[indice] = True
    logging.info(f'filosofo termino de comer, quedan {recursoFilosofos.listaTenedores.count(True)} tenedores')        
    time.sleep(random.randint(3,6))


def comer():
    while True:
        time.sleep(0.1)
        seccionCritica()


def main():
    for j in range(5):
        threading.Thread(target= comer,daemon= True).start()

    time.sleep(3)


if __name__ == "__main__":
    main()







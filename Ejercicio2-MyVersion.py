import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class miRecurso (Recurso): 
    # hereda de Recurso, porqué allí se encuentra el mutex y su logica correspondiente encargada de la exclusion mutua.
    dato1 = 0
    numLectores = 0 
    numEscritores = 0
    escribiendo = False

informacion = miRecurso()

def condicionLector():
    return (not informacion.escribiendo) and (informacion.numEscritores == 0)

def condicionEscritor():
    return not informacion.escribiendo

def condicionTrue():
    return True

regionLector = RegionCondicional(informacion,condicionLector)
regionEscritor = RegionCondicional(informacion,condicionEscritor)
regionLectorEscritorTrue = RegionCondicional(informacion,condicionTrue) 
# Esta region tiene una condicion siempre TRUE, ergo proceso que entra aquí siempre podra HACER (do).

@regionLector.condicion
def doLector1():
    informacion.numLectores += 1

@regionLectorEscritorTrue.condicion
def doLector2():
    informacion.numLectores -= 1

@regionLectorEscritorTrue.condicion
def doEscritor1():
    informacion.numEscritores += 1

@regionEscritor.condicion
def doEscritor2():
    informacion.escribiendo= True
    informacion.numEscritores -=1

@regionLectorEscritorTrue.condicion
def doEscritor3():
    informacion.escribiendo=False

def Lector():
    while True:
        doLector1()
        logging.info(f'Lector lee dato1 = {regionLector.recurso.dato1}')
        time.sleep(1)
        doLector2()

def Escritor():
    while True:
        doEscritor1()
        doEscritor2()
        regionEscritor.recurso.dato1 = random.randint(0,100)
        logging.info(f'Escritor escribe dato1 = {regionEscritor.recurso.dato1}')
        doEscritor3()
        time.sleep(3)

def main():
    numLector = 20
    numEscritor = 2

    for k in range(numLector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(numEscritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()

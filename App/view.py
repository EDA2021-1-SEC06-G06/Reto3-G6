"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
from random import randint
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("*" * 70)
    print("1- Cargar información en el catálogo")
    print("2- REQ 1: Caracterizar las reproducciones")
    print("3- REQ 2: Encontrar música para festejar")
    print("4- REQ 3: Encontrar música para estudiar")
    print("5- REQ 4: Estudiar los géneros musicales")
    print("6- REQ 5: Indicar el género musical más escuchado en el tiempo")
    print("0- APAGAR EL PROGRAMA")
    print("*" * 70)


def printReq3(mapa):
    size = mp.size(mapa)
    print("Total of unique tracks in events: {0}".format(size))
    
    llaves = mp.keySet(mapa)
    
    print("\n--- Unique track_id ---")

    for num in range(5):
        numRandom = randint(1, size)  # número al azar entre 1 y el size del mapa

        track = lt.getElement(llaves, numRandom)  # se optiene el track_id de uno de los tracks al azar
        track = mp.get(mapa, track)['value']  # se obtiene el valor de la pareja (llave - valor)

        print("Track {0}: {1} with instrumentalness of {2} and tempo of {3}".format((num + 1), track["track_id"], track["instrumentalness"], track['tempo']))

    mapa = None




catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        # cont es el controlador que se usará de acá en adelante
        analyzer = controller.init()
        controller.loadEvents(analyzer)

        print("Cantidad de Eventos: {0}".format(lt.size(analyzer['eventos'])))

        print("Cantidad de Artistas: {0}".format(mp.size(analyzer['artistas'])))
        
        print("Cantidad de Tracks: {0}".format(mp.size(analyzer['audios'])))

    elif int(inputs[0]) == 2:
        car = input("Ingrese la característica de contenido que desea:\n~")  # Test con 'instrumentalness'
        # bajo = float(input("Ingrese el mínimo del rango:\n~"))
        # alto = float(input("Ingrese el máximo del rango:\n~"))

        car = 'instrumentalness'
        bajo = 0.0
        alto = 0.0
        print("Cargando datos según la característica....")

        newTree = controller.getCar(analyzer, car)

        print("Altura del árbol de la característica: {0}".format(om.height(newTree)))
        print("Cantidad de valores (Nodos) en el árbol: {0}".format(om.size(newTree)))

        total, mapa = controller.getValuesReq1(newTree, bajo, alto)

        print("Total de reproducción: {0}\nTotal de artistas únicos: {1}".format(total, mp.size(mapa)))
        
        mapa = None
        newTree = None  # Espacio en Memoria


    elif int(inputs[0]) == 4:
        print("\n++++++ Req No. 3 results... ++++++")
        newTree = controller.getCar(analyzer, 'instrumentalness')  # árbol según valores de "instrumentalness"

        bajoInstrumental = float(input("Ingrese el mínimo del rango para Instrumentalness:\n~")) 
        altoInstrumental = float(input("Ingrese el máximo del rango para Instrumentalness:\n~"))

        bajoTempo = float(input("Ingrese el mínimo del rango para Tempo:\n~"))
        altoTempo = float(input("Ingrese el máximo del rango para Instrumentalness:\n~"))

        mapaVideosRango = controller.getValuesReq3(newTree, bajoInstrumental, altoInstrumental, bajoTempo, altoTempo)
        # ^^ un mapa con los vídeos dentro del rango
        
        print("Instrumentalness is between {0} and {1}".format(bajoInstrumental, altoInstrumental))
        print("Tempo is between {0} and {1}".format(bajoTempo, altoTempo))

        printReq3(mapaVideosRango)  # función para imprimir cinco tracks al azar


    else:
        sys.exit(0)
sys.exit(0)

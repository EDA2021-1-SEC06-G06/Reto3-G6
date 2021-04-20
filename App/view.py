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

    print("\n--- Unique track_id ---\n")

    for num in range(5):
        numRandom = randint(1, size)  # número al azar entre 1 y el size del mapa

        track = lt.getElement(llaves, numRandom)  # se optiene el track_id de uno de los tracks al azar
        track = mp.get(mapa, track)['value']  # se obtiene el valor de la pareja (llave - valor)

        print("Track {0}: {1} with instrumentalness of {2} and tempo of {3}\n".format((num + 1), track["track_id"], track["instrumentalness"], track['tempo']))

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
        print("\n++++++ Req No. 1 results... ++++++\n")
        car = input("Ingrese la característica de contenido que desea:\n~")  # Test con 'instrumentalness'
        # bajo = float(input("Ingrese el mínimo del rango:\n~"))
        # alto = float(input("Ingrese el máximo del rango:\n~"))

        car = 'instrumentalness'
        bajo = 0.0
        alto = 0.0
        print("\nCargando datos según la característica....")

        newTree = controller.getCar(analyzer, car)

        print("\nAltura del árbol de la característica: {0}".format(om.height(newTree)))
        print("\nCantidad de valores (Nodos) en el árbol: {0}".format(om.size(newTree)))

        total, mapa = controller.getValuesReq1(newTree, bajo, alto)

        print("\nTotal de reproducción: {0}\n\nTotal de artistas únicos: {1}\n".format(total, mp.size(mapa)))

        mapa = None
        newTree = None  # Espacio en Memoria



    elif int(inputs[0]) == 3:
        print("\n++++++ Req No. 2 results... ++++++\n")
        newTree = controller.getCar(analyzer, 'energy')  # árbol según valores de "energy"

        bajoEnergy = float(input("\nIngrese el mínimo del rango para Energía:\n~"))
        altoEnergy = float(input("\nIngrese el máximo del rango para Energía:\n~"))

        bajoDance = float(input("\nIngrese el mínimo del rango para Danceability:\n~"))
        altoDance = float(input("\nIngrese el máximo del rango para Danceability:\n~"))

        mapaVideosRango = controller.getValuesReq2and3(newTree, bajoEnergy, altoEnergy, bajoDance, altoDance, 2)
        # ^^ un mapa con los vídeos dentro del rango

        print("\nEnergy is between {0} and {1}\n".format(bajoEnergy, altoEnergy))
        print("Tempo is between {0} and {1}\n".format(bajoDance, altoDance))

        printReq3(mapaVideosRango)  # función para imprimir cinco tracks al azar



    elif int(inputs[0]) == 4:
        print("\n++++++ Req No. 3 results... ++++++\n")
        newTree = controller.getCar(analyzer, 'instrumentalness')  # árbol según valores de "instrumentalness"

        bajoInstrumental = float(input("\nIngrese el mínimo del rango para Instrumentalness:\n~")) 
        altoInstrumental = float(input("\nIngrese el máximo del rango para Instrumentalness:\n~"))

        bajoTempo = float(input("\nIngrese el mínimo del rango para Tempo:\n~"))
        altoTempo = float(input("\nIngrese el máximo del rango para Tempo:\n~"))

        mapaVideosRango = controller.getValuesReq2and3(newTree, bajoInstrumental, altoInstrumental, bajoTempo, altoTempo, 3)
        # ^^ un mapa con los vídeos dentro del rango

        print("\nInstrumentalness is between {0} and {1}\n".format(bajoInstrumental, altoInstrumental))
        print("Tempo is between {0} and {1}\n".format(bajoTempo, altoTempo))

        printReq3(mapaVideosRango)  # función para imprimir cinco tracks al azar



    elif int(inputs[0]) == 5:
        print("\n++++++ Req No. 4 results... ++++++\n")
        newTree = controller.getCar(analyzer, 'tempo')  # árbol según valores de "tempo"

        genreMap = controller.genreMap()

        centinela = True

        while centinela is True:

            opcion = int(input("\nIngrese (1) si desea cosultar géneros existentes, ingrese (2) si desea agregar un nuevo género e ingrese (3) si no desea consultar más géneros:\n~"))

            if opcion == 1:

                genero = input("\nIngrese los generos que desea consultar, separados por comas y espacios:\n~")

            elif opcion == 2:

                genero = input("\nIngrese el nombre del género que desea registrar:\n~")
                bajoTempo = float(input("\nIngrese el mínimo del rango para el Tempo de {0}:\n~".format(genero)))
                altoTempo = float(input("\nIngrese el máximo del rango para el Tempo de {0}:\n~".format(genero)))

            if opcion == 3:

                centinela = False

        print(controller.genreMap())



    else:
        sys.exit(0)
sys.exit(0)

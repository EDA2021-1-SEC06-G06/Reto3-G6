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
import datetime as dt
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
    print("\nBienvenido")
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



def printReq4(mapa, elecciones):

    elecciones = elecciones.split(', ')
    totalSuma = 0
    for genero in elecciones:
        genero = genero.lower()
        print("\n======{0}======".format(genero))
        valoresLLave = mp.get(mapa, genero)['value']

        if valoresLLave is not None:
            totalSuma += mp.size(valoresLLave['numEventos'])

            print("For {0} the tempo is between {1} and {2} BPM".format(genero, valoresLLave['bajo'], valoresLLave['alto']))

            print("{0} reproductions: {1} with {2} different artists".format(genero, mp.size(valoresLLave['numEventos']), mp.size(valoresLLave['artistas'])))

            print("----- Some artists for {0} -----".format(genero))

            artistas = mp.keySet(valoresLLave['artistas'])
            for num in range(10):
                numRandom = randint(1, lt.size(artistas))

                artist = lt.getElement(artistas, numRandom)

                print("Artists {0}: {1}".format((num + 1), artist))
    print("Total of reproductions: {0}".format(totalSuma))
    valoresLLave = None
    artistas = None
    artist = None


def printReq5(mapa, hora1, hora2):
    print("====================== GENRES SORTED REPRODUCTIONS ======================")

    sorted_list = controller.getValuesReq5(mapa)

    iterador = 1
    primerGenero = lt.getElement(sorted_list, 1)

    totalRep = 0
    
    while iterador <= lt.size(sorted_list):
        genero = lt.getElement(sorted_list, iterador)

        print("\nTOP {0}: {1} with {2} reps".format(iterador, genero['genero'], mp.size(genero['mapa'])))
        iterador += 1
        totalRep += mp.size(genero['mapa'])
        
    print("\nThe TOP GENRE is {0} with {1} reproductions...".format(primerGenero['genero'], mp.size(primerGenero['mapa'])))
    print("\nThere is a total of {0} reproductions between {1} and {2}".format(totalRep, hora1, hora2))
    
    return primerGenero


def printReq5Part2(sorted_list, genero):
    print("\n========================== Metal SENTIMENT ANALYSIS =========================")
    print("{0} has {1} unique tracks...\nThe first TOP 10 tracks are...".format(genero, lt.size(sorted_list)))
    
    iterador = 1

    while iterador <= 10:

        track = lt.getElement(sorted_list, iterador)

        print("\nTOP {0} track: {1} with {2} hashtags".format(iterador, track['track_id'], lt.size(track['hashtags'])))

        iterador += 1




def printGeneros(mapa):

    size = mp.size(mapa)

    llaves = mp.keySet(mapa)

    posicion = 1

    print("\n### Los géneros existentes son los siguientes ###\n")
    while posicion <= size:

        llave = lt.getElement(llaves, posicion)

        print("•{0}\n".format(llave.upper()))

        posicion += 1



default_limit = 1000
sys.setrecursionlimit(default_limit * 10)

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
        controller.loadUserTrack(analyzer)

        newTreeReq4 = controller.getCar(analyzer, 'tempo')  # árbol según valores de "tempo"
        genreMap = controller.genreMap(newTreeReq4)

        print("Cantidad de Eventos: {0}".format(lt.size(analyzer['eventos'])))

        print("Cantidad de Artistas: {0}".format(mp.size(analyzer['artistas'])))

        print("Cantidad de Tracks: {0}".format(mp.size(analyzer['audios'])))



    elif int(inputs[0]) == 2:
        print("\n++++++ Req No. 1 results... ++++++\n")
        car = input("Ingrese la característica de contenido que desea:\n~")  # Test con 'instrumentalness'
        bajo = float(input("Ingrese el mínimo del rango:\n~"))
        alto = float(input("Ingrese el máximo del rango:\n~"))


        print("\nCargando datos según la característica....")

        newTree = controller.getCar(analyzer, car)

        total, mapa = controller.getValuesReq1(newTree, bajo, alto)

        print("\nTotal de reproducción: {0}\n\nTotal de artistas únicos: {1}\n".format(mp.size(total), mp.size(mapa)))

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


        centinela = True
        elecciones = ''
        while centinela is True:
            printGeneros(genreMap)

            opcion = int(input("-Ingrese (1) para seleccionar los géneros a imprimir\n-Ingrese (2) si desea agregar un género\n-Ingrese (3) para imprimir los géneros seleccionados\n-Ingrese (4) para salirse del requerimiento\n~ "))


            if opcion == 1:
                generos = input("\nIngrese los generos que desea consultar, separados por comas y espacios:\n~ ")

                if elecciones != '':
                    elecciones = elecciones + ', ' + generos

                else:
                    elecciones = generos

            elif opcion == 2:
                genero = input("\nIngrese el nombre del género que desea registrar:\n~ ")

                if elecciones != '':
                    elecciones = elecciones + ', ' + genero.lower()

                else:
                    elecciones = genero

                bajoTempo = float(input("\nIngrese el mínimo del rango para el Tempo de {0}:\n~ ".format(genero)))
                altoTempo = float(input("\nIngrese el máximo del rango para el Tempo de {0}:\n~ ".format(genero)))

                genreMap = controller.addGenre(genreMap, genero, bajoTempo, altoTempo, newTreeReq4)

                print("Su género ha sido agregado, NO tiene que seleccionarlo en la opción 1")


            elif opcion == 3:
                print("¿Desea la información de los siguientes géneros?:")
                print(elecciones.upper())

                yesOrno = input("\n(Y) or (N)?\n~ ")

                if yesOrno.lower() == 'y':

                    print(elecciones)
                    printReq4(genreMap, elecciones)

                elecciones = ''

            else:

                centinela = False



    elif int(inputs[0]) == 6:  # TODO: Ver qué archivo toca usar ughhhhhhhhh
        print("\n++++++ Req No. 5 results... ++++++\n")

        bajoTime = input("Ingrese el mínimo del rango de la siguiente forma: H:M:S\n~ ")
        altoTime = input("Ingrese el máximo del rango de la siguiente forma: H:M:S\n~ ")

        listaFiltroDates = om.values(analyzer['dates'], dt.datetime.strptime(bajoTime, "%H:%M:%S").time(), dt.datetime.strptime(altoTime, "%H:%M:%S").time())
        filtroUniqueDates = om.values(analyzer['unique_dates'], dt.datetime.strptime(bajoTime, "%H:%M:%S").time(), dt.datetime.strptime(altoTime, "%H:%M:%S").time())
        
        mapaGenerosDates = controller.req5Generos(listaFiltroDates)
        mapaUniqueDates = controller.req5Generos(filtroUniqueDates)  # user csv

        generoMasReps = printReq5(mapaGenerosDates, bajoTime, altoTime)  # tiene como llaves 'genero' y 'mapa'
        
        mapaUniqueGenero1 = mp.get(mapaUniqueDates, generoMasReps['genero'])['value']  # user csv

        controller.addTrackHashtags(analyzer, mapaUniqueGenero1)
        
        

        mapaGenero1 = generoMasReps['mapa']

        listaUnicos = controller.req5UniqueTracks(analyzer, mapaGenero1)  # Tracks unicos + hashtags

        sorted_list = controller.sortNumHashtags(listaUnicos)

        printReq5Part2(sorted_list, generoMasReps['genero'])

        # Memoria
        listaFiltroDates = None
        filtroUniqueDates = None

        mapaGenerosDates = None
        mapaUniqueDates = None

        generoMasReps = None

        mapaUniqueGenero1 = None

        mapaGenero1 = None

        listaUnicos = None

        sorted_list = None


    else:
        sys.exit(0)
sys.exit(0)

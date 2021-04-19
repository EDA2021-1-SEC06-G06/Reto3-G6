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
    print("1- Cargar información en el catálogo")
    print("2- REQ 1: Caracterizar las reproducciones")
    print("3- REQ 2: Encontrar música para festejar")
    print("4- REQ 3: Encontrar música para estudiar")
    print("5- REQ 4: Estudiar los géneros musicales")
    print("6- REQ 5: Indicar el género musical más escuchado en el tiempo")
    print("*"*60)


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
        car = input("Ingrese la característica de contenido que desea: ")  # Test con 'instrumentalness'

        print("Cargando datos según la característica....")

        newTree = controller.getCar(analyzer, car)

        print("Altura del árbol de la característica: {0}".format(om.height(newTree)))
        print("Cantidad de valores (Nodos) en el árbol: {0}".format(om.size(newTree)))

        newTree = None  # Espacio en Memoria

    else:
        sys.exit(0)
sys.exit(0)

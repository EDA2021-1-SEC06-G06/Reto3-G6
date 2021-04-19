"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf


# Construccion de modelos

def newAnalyzer():
    analyzer = {'eventos': None, 'artistas': None, 'audios': None}

    analyzer['eventos'] = lt.newList('ARRAY_LIST')

    analyzer['artistas'] = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=1000000, comparefunction=cmpArtistas)

    analyzer['audios'] = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=1000000, comparefunction=cmpTrack)

    return analyzer


# Funciones para agregar informacion al catalogo


def addEvent(analyzer, filtered: dict):
    """
    """

    datos = analyzer['eventos']
    
    lt.addLast(datos, filtered)


def addArtist(analyzer, filtered):
    """

    """

    datos = analyzer['artistas']

    artista = mp.get(datos, filtered["artist_id"])
    
    if (artista is None):
        lista = lt.newList("ARRAY_LIST")
        lt.addLast(lista, filtered)

        mp.put(datos, filtered['artist_id'], lista)
    else:
        
        lt.addLast(artista['value'], filtered)


def addTrack(analyzer, filtered):
    # artist arbol -> 

    datos = analyzer['audios']

    track = mp.get(datos, filtered["track_id"])
    
    if (track is None):
        lista = lt.newList("ARRAY_LIST")
        lt.addLast(lista, filtered)

        mp.put(datos, filtered['track_id'], lista)
    else:
        
        lt.addLast(track['value'], filtered)

# Funciones para creacion de datos

# Funciones de consulta


def getCar(analyzer, car: str):

    datos = analyzer['eventos']

    newTree = om.newMap(omaptype='RBT', comparefunction=cmpCarValue)

    for audio in lt.iterator(datos):

        valor = audio[car]

        entry = om.get(newTree, valor)

        if not entry:
            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, audio)

            om.put(newTree, valor, lista)
        
        else:

            lt.addLast(entry['value'], audio)
    
    return newTree



def getValuesReq1(tree, bajo, alto):

    total = om.values(tree, bajo, alto)

    mapa = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=8000, comparefunction=cmpArtistas)
    suma = 0

    # artistas = 0
    for node in lt.iterator(total):
        suma += lt.size(node)

        for event in lt.iterator(node):
            artista = event['artist_id']
            existe = mp.contains(mapa, artista)

            if (not existe):
                mp.put(mapa, artista, None)

    return suma, mapa


def getValuesReq3(tree, bajoInstrumental, altoInstrumental, bajoTempo, altoTempo):

    instrumental = om.values(tree, bajoInstrumental, altoInstrumental)
    
    mapa = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=8000)
    
    for node in lt.iterator(instrumental):

        for event in lt.iterator(node):

            if (event["tempo"] >= 40) and (event["tempo"] <= 60):

                audio = event["track_id"]
                existe = mp.contains(mapa, audio)

                if (not existe):
                    mp.put(mapa, audio, event)

    return mapa





# Funciones utilizadas para comparar elementos dentro de una lista


def cmpArtistas(artist1, artist2):
    artista = me.getKey(artist2)
    if artist1 == artista:
        return 0
    elif artist1 > artista:
        return 1
    else:
        return -1


def cmpTrack(track1, track2):
    track = me.getKey(track2)
    if track1 == track:
        return 0
    elif track1 > track:
        return 1
    else:
        return -1


def cmpCarValue(c1, c2):

    if c1 == c2:
        return 0
    elif c1 > c2:
        return 1
    else:
        return -1
# Funciones de ordenamiento

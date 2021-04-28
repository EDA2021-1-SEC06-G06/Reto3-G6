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

import datetime as dt
import config as cf
from DISClib.Algorithms.Sorting import mergesort
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf


# Construccion de modelos

def newAnalyzer():
    analyzer = {'eventos': None, 'artistas': None, 'audios': None}

    analyzer['eventos'] = lt.newList('ARRAY_LIST')

    analyzer['artistas'] = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=1000000, comparefunction=cmpArtistas)

    analyzer['audios'] = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=1000000, comparefunction=cmpTrack)

    analyzer['dates'] = om.newMap("RBT", cmpDates)

    analyzer['mapa_track_hashtag'] = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=1000000, comparefunction=cmpTrack)

    analyzer['unique_dates'] = om.newMap("RBT", cmpDates)
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
    datos = analyzer['audios']

    track = mp.get(datos, filtered["track_id"])

    if (track is None):

        mp.put(datos, filtered['track_id'], filtered)


def addDate(analyzer, filtered):

    datos = analyzer['dates']
    valor = dt.datetime.strptime(filtered["created_at"], "%Y-%m-%d %H:%M:%S").time()

    entry = om.get(datos, valor)
    if entry is None:
        lista = lt.newList("ARRAY_LIST")
        lt.addLast(lista, filtered)
        om.put(datos, valor, lista)
    else:
        dateList = me.getValue(entry)

        lt.addLast(dateList, filtered)


def addUniqueDates(analyzer, filtered):

    datos = analyzer['unique_dates']
    valor = dt.datetime.strptime(filtered["created_at"], "%Y-%m-%d %H:%M:%S").time()

    entry = om.get(datos, valor)
    if entry is None:
        lista = lt.newList("ARRAY_LIST")
        lt.addLast(lista, filtered)
        om.put(datos, valor, lista)
    else:
        dateList = me.getValue(entry)

        lt.addLast(dateList, filtered)


def addTrackHashtags(analyzer, mapaHoras):

    datos = analyzer['mapa_track_hashtag']


    for track in lt.iterator(mp.keySet(mapaHoras)):

        filtered = mp.get(mapaHoras, track)['value']
        
        track = mp.get(datos, filtered["track_id"])

        

        if (track is None):

            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, filtered['hashtag'])
            mp.put(datos, filtered['track_id'], lista)
        else:

            lista = track['value']

            if lt.isPresent(lista, filtered['hashtag']) == 0:
                lt.addLast(lista, filtered['hashtag'])
        

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
    reproducciones = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=8000,)


    for node in lt.iterator(total):

        for event in lt.iterator(node):
            newEvent = event['track_id'] + event['user_id'] + event['created_at']

            mp.put(reproducciones, newEvent, None)

            artista = event['artist_id']
            existe = mp.contains(mapa, artista)

            if (not existe):
                mp.put(mapa, artista, None)

    return reproducciones, mapa



def getValuesReq2and3(tree, bajo1, alto1, bajo2, alto2, numReq):
    """Retorna un mapa con los tracks en un rango que depende del requerimiento seleccionado.

    Args:
        tree (dict, mapa): Árbol según Energy. Defaults to None.
        bajo1 (float): Rango inferior de la primera carcterística de contenido.
        alto1 (float): Rango superior de la primera carcterística de contenido.
        bajo2 (float): Rango inferior de la segunda carcterística de contenido.
        alto2 (float): Rango superior de la segunda carcterística de contenido.

    Returns:
        dict: Mapa (PROBING) de los tracks en los rangos elegidos
    """
    if tree is not None:  # Si el árbol no es None

        mapa = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=8000)

        if numReq == 2:

            energy = om.values(tree, bajo1, alto1)

            for node in lt.iterator(energy):

                for event in lt.iterator(node):  # Cada evento contiene info del csv context

                    if (event["danceability"] >= bajo2) and (event["danceability"] <= alto2):

                        audio = event["track_id"]
                        existe = mp.contains(mapa, audio)

                        if (not existe):  # se usa un mapa para no repetir tracks
                            mp.put(mapa, audio, event)

        elif numReq == 3:

            instrumental = om.values(tree, bajo1, alto1)

            for node in lt.iterator(instrumental):

                for event in lt.iterator(node):  # Cada evento contiene info del csv context

                    if (event["tempo"] >= bajo2) and (event["tempo"] <= alto2):

                        audio = event["track_id"]
                        existe = mp.contains(mapa, audio)

                        if (not existe):  # se usa un mapa para no repetir tracks
                            mp.put(mapa, audio, event)

        return mapa

    else:
        return None



def getValuesReq4(tree):

    mapa = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=50000, comparefunction=cmpArtistas)
    reproducciones = mp.newMap(maptype="PROBING", loadfactor=0.5, numelements=100000)

    # artistas = 0
    for node in lt.iterator(tree):


        for event in lt.iterator(node):
            newEvent = event['track_id'] + event['user_id'] + event['created_at']

            mp.put(reproducciones, newEvent, None)


            artista = event['artist_id']
            existe = mp.contains(mapa, artista)

            if (not existe):
                mp.put(mapa, artista, None)

    return reproducciones, mapa




def genreMap(tree):

    genreMap = mp.newMap(numelements=15, prime=17, maptype="PROBING", loadfactor=0.5)


    addGenre(genreMap, "reggae", 60.0, 90.0, tree)


    addGenre(genreMap, "down-tempo", 70.0, 100.0, tree)


    addGenre(genreMap, "chill-out", 90.0, 120.0, tree)


    addGenre(genreMap, "hip-hop", 85.0, 115.0, tree)


    addGenre(genreMap, "jazz and funk", 120.0, 125.0, tree)


    addGenre(genreMap, "pop", 100.0, 130.0, tree)


    addGenre(genreMap, "r&b", 60.0, 80.0, tree)


    addGenre(genreMap, "rock", 110.0, 140.0, tree)


    addGenre(genreMap, "metal", 100.0, 160.0, tree)


    return genreMap


def addGenre(mapa, genero, bajo, alto, tree):

    keyName = genero.lower()

    valoresKey = {
        'bajo': bajo,
        'alto': alto,
        'eventos': om.values(tree, bajo, alto)
    }

    numEventos, artistas = getValuesReq4(valoresKey['eventos'])

    valoresKey['numEventos'] = numEventos
    valoresKey['artistas'] = artistas

    mp.put(mapa, keyName, valoresKey)

    return mapa



def req5Generos(listaFiltrada):

    mapa = {
        "reggae": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "down-tempo": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "chill-out": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "hip-hop": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "jazz and funk": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "pop": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "r&b": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "rock": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5),
        "metal": mp.newMap(maptype="PROBING", numelements=50001, loadfactor=0.5)
    }

    for nodo in lt.iterator(listaFiltrada):

        for track in lt.iterator(nodo):

            if track['tempo'] is not None:
                trackName = track['track_id'] + track['user_id'] + track['created_at']


                if track['tempo'] >= 60.0 and track['tempo'] <= 90.0:
                    mp.put(mapa['reggae'], trackName, track)  # TODO: Hashtags


                if track['tempo'] >= 70.0 and track['tempo'] <= 100.0:
                    mp.put(mapa['down-tempo'], trackName, track)


                if track['tempo'] >= 90.0 and track['tempo'] <= 120.0:
                    mp.put(mapa['chill-out'], trackName, track)


                if track['tempo'] >= 85.0 and track['tempo'] <= 115.0:
                    mp.put(mapa['hip-hop'], trackName, track)


                if track['tempo'] >= 120.0 and track['tempo'] <= 125.0:
                    mp.put(mapa['jazz and funk'], trackName, track)


                if track['tempo'] >= 100.0 and track['tempo'] <= 130.0:
                    mp.put(mapa['pop'], trackName, track)


                if track['tempo'] >= 60.0 and track['tempo'] <= 80.0:
                    mp.put(mapa['r&b'], trackName, track)


                if track['tempo'] >= 110.0 and track['tempo'] <= 140.0:
                    mp.put(mapa['rock'], trackName, track)


                if track['tempo'] >= 100.0 and track['tempo'] <= 160.0:
                    mp.put(mapa['metal'], trackName, track)

    hashMap = mp.newMap(numelements=15, prime=17, maptype="PROBING", loadfactor=0.5)

    for llave in mapa:

        mp.put(hashMap, llave, mapa[llave])

    mapa = None
    return hashMap


def getValuesReq5(mapa):

    generosMayores = lt.newList(datastructure="ARRAY_LIST")

    for genero in lt.iterator(mp.keySet(mapa)):

        generoMapa = {
            'genero': genero,
            'mapa': mp.get(mapa, genero)['value']
        }

        lt.addLast(generosMayores, generoMapa)

    sorted_list = sortSizeGeneros(generosMayores)

    return sorted_list



def req5UniqueTracks(analyzer, mapaGenero1):

    mapaUnicos = mp.newMap(numelements=9973, maptype="PROBING", loadfactor=0.5)
    
    for eventoUnico in lt.iterator(mp.keySet(mapaGenero1)):

        evento = mp.get(mapaGenero1, eventoUnico)['value']
        
        if mp.get(mapaUnicos, evento['track_id']) is None:

            listaHashtags = mp.get(analyzer['mapa_track_hashtag'], evento['track_id'])

            if listaHashtags is not None:
            
                mp.put(mapaUnicos, evento['track_id'], listaHashtags['value'])
            else:
                mp.put(mapaUnicos, evento['track_id'], 0)

    newList = lt.newList("ARRAY_LIST")

    for eventoUnico in lt.iterator(mp.keySet(mapaUnicos)):
        evento = {'track_id': eventoUnico, 'hashtags': mp.get(mapaUnicos, eventoUnico)['value']}

        lt.addLast(newList, evento)
    mapaUnicos = None
    
    return newList

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


def cmpDates(d1, d2):

    if d1 == d2:
        return 0
    elif d1 > d2:
        return 1
    else:
        return -1


def cmpNumHashtags(track1, track2):
    return lt.size(track1['hashtags']) > lt.size(track2['hashtags'])


def cmpGeneros(genero1, genero2):
    return lt.size(genero1['mapa']) > lt.size(genero2['mapa'])

# Funciones de ordenamiento



def sortNumHashtags(uniqueTracksList):
    sub_list = lt.subList(uniqueTracksList, 1, lt.size(uniqueTracksList))
    sub_list = sub_list.copy()

    sorted_list = mergesort.sort(sub_list, cmpNumHashtags)

    return sorted_list


def sortSizeGeneros(generoList):
    sub_list = lt.subList(generoList, 1, lt.size(generoList))
    sub_list = sub_list.copy()

    sorted_list = mergesort.sort(sub_list, cmpGeneros)

    return sorted_list
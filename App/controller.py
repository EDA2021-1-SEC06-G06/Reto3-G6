﻿"""
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
 """

import config as cf
import model
import csv
from DISClib.ADT import map as mp


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos


def loadEvents(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    context = cf.data_dir + 'context_content_features-small.csv'
    input_file = csv.DictReader(open(context, encoding="utf-8"),
                                delimiter=",")
    # "artist_id","track_id","user_id","id"
    for line in input_file:
        filtered = {
            "instrumentalness": float(line["instrumentalness"]),
            "liveness": float(line["liveness"]),
            "speechiness": float(line["speechiness"]),
            "danceability": float(line["danceability"]),
            "valence": float(line["valence"]),
            "loudness": float(line["loudness"]),
            "tempo": float(line["tempo"]),
            "acousticness": float(line["acousticness"]),
            "energy": float(line["energy"]),
            "mode": float(line["mode"]),
            "key": float(line["key"]),
            "artist_id": line["artist_id"].replace(" ", ''),
            "track_id": line["track_id"].lower(),
            "user_id": line["user_id"],
            "id": line["id"],
            "created_at": line["created_at"]  # dt.datetime.strptime(line["created_at"], "%Y-%m-%d %H:%M:%S").time()
        }

        model.addEvent(analyzer, filtered)
        model.addArtist(analyzer, filtered)
        model.addTrack(analyzer, filtered)
        model.addDate(analyzer, filtered)
    return analyzer



def loadUserTrack(analyzer):
    userTrack = cf.data_dir + 'user_track_hashtag_timestamp-small.csv'
    input_file = csv.DictReader(open(userTrack, encoding="utf-8"),
                                delimiter=",")

    for line in input_file:
        filtered = {
            'user_id': line['user_id'],
            "track_id": line["track_id"].replace(" ", ''),
            "hashtag": (line['hashtag'].lower().replace(' ', '')),
            "created_at": line['created_at']
        }
        tempo = mp.get(analyzer['audios'], filtered['track_id'])

        if tempo is not None:
            tempo = tempo['value']['tempo']

            filtered['tempo'] = tempo

        else:
            filtered['tempo'] = None

        model.addUniqueDates(analyzer, filtered)

    return analyzer



def loadSentimentValues(analyzer):
    sentimentFile = cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(sentimentFile, encoding="utf-8"), delimiter=',')

    for line in input_file:
        filtered = {
            'hashtag': (line['hashtag'].lower()).replace(' ', ''),
            'vader': line['vader_avg']
        }

        model.addHashtag(analyzer, filtered)
    return analyzer
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def getCar(analyzer, car):

    return model.getCar(analyzer, car)


def getValuesReq1(tree, bajo, alto):

    return model.getValuesReq1(tree, bajo, alto)


def getValuesReq2(tree, bajoEnergy, altoEnergy, bajoDance, altoDance):
    """Retorna un mapa con los tracks en un rango de energy y danceability

    Args:
        tree (dict, mapa): Árbol según Energy. Defaults to None.
        bajoEnergy (float): Rango inferior Energy.
        altoEnergy (float): Rango superior Energy.
        bajoDance (float): Rango inferior Danceability.
        altoDance (float): Rango superior Danceability.

    Returns:
        dict: Mapa (PROBING) de los tracks en los rangos elegidos
    """
    return model.getValuesReq2(tree, bajoEnergy, altoEnergy, bajoDance, altoDance)


def getValuesReq3(tree, bajoInstrumental, altoInstrumental, bajoTempo, altoTempo):
    """Retorna un mapa con los tracks en un rango de instrumentalness y tempo

    Args:
        tree (dict, mapa): Árbol según Instrumentalness. Defaults to None.
        bajoInstrumental (float): Rango inferior Instrumentalness. Defaults to 0.6.
        altoInstrumental (float): Rango superior Instrumentalness. Defaults to 0.9.
        bajoTempo (float): Rango inferior Tempo. Defaults to 40.
        altoTempo (float): Rango superior Tempo. Defaults to 60.

    Returns:
        dict: Mapa (PROBING) de los tracks en los rangos elegidos
    """
    return model.getValuesReq3(tree, bajoInstrumental, altoInstrumental, bajoTempo, altoTempo)


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
    return model.getValuesReq2and3(tree, bajo1, alto1, bajo2, alto2, numReq)


def genreMap(tree):
    """
    Crea un mapa con los géneros por defecto.
    """
    return model.genreMap(tree)


def addGenre(mapa, genero, bajo, alto, tree):
    return model.addGenre(mapa, genero, bajo, alto, tree)


def req5Generos(listaFiltroDates):

    return model.req5Generos(listaFiltroDates)


def getValuesReq5(mapa):

    return model.getValuesReq5(mapa)


def req5UniqueTracks(analyzer, mapaGenero1):

    return model.req5UniqueTracks(analyzer, mapaGenero1)


def sortNumHashtags(uniqueTracksList):

    return model.sortNumHashtags(uniqueTracksList)


def addTrackHashtags(analyzer, mapaHoras):

    model.addTrackHashtags(analyzer, mapaHoras)


def getSentimentAvg(analyzer, array_list):

    return model.getSentimentAvg(analyzer, array_list)

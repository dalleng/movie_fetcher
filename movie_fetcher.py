from bs4 import BeautifulSoup
from os.path import expanduser
import requests
import json

CINES_BASE_URL = 'http://www.cines.com.py'
CARTELERA, NUEVOS = range(2)

DROPBOX_PATH = expanduser('~') + '/Dropbox/public/'


def get_movie_paths(text, movie_type):
    """ Gets the movie path for each movie of type movie_type, 
        returns a dict with movie titles as keys and movie paths
        as values. """

    if movie_type == CARTELERA:
        id = 'cuadro_lista_cartelera'
    elif movie_type == NUEVOS:
        id = 'cuadro_lista_nuevos'
    else:
        raise TypeError(
            "expecting type of movie, got %s" % type(movie_type).__name__)

    soup = BeautifulSoup(text)

    movies = soup.find(id=id)
    # some links are not needed
    movies = movies.find_all('a')[:-3]

    return [a['href'] for a in movies]


def fetch_movie_info(movie_path):
    """ Fetches each movie site to get info (showtimes, synopsis, etc), 
        returns a dict containing it """

    r = requests.get(CINES_BASE_URL + movie_path)
    soup = BeautifulSoup(r.text)

    title = soup.select('.texto_principal h1').pop().text
    original_title = soup.select('.texto_principal h2').pop()

    # removes surrounding parentheses
    original_title = original_title.text[1:-1]
    
    theaters = [i.text for i in soup.select('#horarios h1')]
    schedule = [[i.text.strip()] for i in soup.select('#horarios p')]
    showtimes = dict(zip(theaters, schedule))

    poster_thumb = soup.select('.imagen_principal').pop()['src']
    poster_thumb = CINES_BASE_URL + poster_thumb

    poster_full = soup.find(id='gallery').a['href']
    poster_full = CINES_BASE_URL + poster_full

    synopsis = soup.select('.cartelera_cuadro p')[0]
    synopsis = synopsis.text.strip()

    movie_info_titles = [i.text for i in soup.select(
        '.texto_principal strong')]

    movie_info_values = [i.text[3:].strip() for i in soup.select(
        '.texto_principal span')]

    if 'ACTORES' in movie_info_titles:
        i = movie_info_titles.index('ACTORES')
        cast = movie_info_values[i].split(', ')
    else:
        cast = []

    if 'ACTORES SECUNDARIOS' in movie_info_titles:
        i = movie_info_titles.index('ACTORES SECUNDARIOS')
        cast += movie_info_values[i].split(', ')

    if 'GENERO' in movie_info_titles:
        i = movie_info_titles.index('GENERO')
        genre = movie_info_values[i].split(', ')
    else:
        genre = []

    if 'DURACION' in movie_info_titles:
        i = movie_info_titles.index('DURACION')
        runtime = movie_info_values[i]

    keys = ['title', 'original_title', 'path_thumb', 'poster_full',
            'synopsis', 'cast', 'genre', 'runtime', 'showtimes']

    values = [title, original_title, poster_thumb, poster_full, synopsis,
              cast, genre, runtime, showtimes]

    return dict(zip(keys, values))


if __name__ == '__main__':
    r = requests.get(CINES_BASE_URL)

    for movie_type in (CARTELERA, NUEVOS):
        movie_info = []
        for movie_path in get_movie_paths(r.text, movie_type):
            movie_info += [fetch_movie_info(movie_path)]

        if movie_type == CARTELERA:
            filename = 'cartelera.json'
        else:
            filename = 'proximamente.json'

        with open(DROPBOX_PATH + filename, 'w+') as fsock:
            fsock.write(json.dumps(movie_info))

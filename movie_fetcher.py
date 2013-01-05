from bs4 import BeautifulSoup
import requests

CINES_BASE_URL = 'http://www.cines.com.py'
CARTELERA, NUEVOS = range(2)


def get_movie_paths(text, movie_type=CARTELERA):
    """ Returns a dict with movie titles as keys and movie paths
        as values. """

    if movie_type == CARTELERA:
        id = 'cuadro_lista_nuevos'
    elif movie_type == NUEVOS:
        id = 'cuadro_lista_cartelera'
    else:
        raise TypeError(
            "expecting type of movie, got %s" % type(movie_type).__name__)

    soup = BeautifulSoup(text)

    movies = soup.find(id=id)
    # some links are not needed
    movies = movies.find_all('a')[:-3]

    return [a['href'] for a in movies]


def fetch_movie_data(movie_path):
    """ Fetches info from movie site and returns a dict containing the info """

    r = requests.get(CINES_BASE_URL + movie_path)
    soup = BeautifulSoup(r.text)

    title = soup.select('.texto_principal h1').pop().text
    original_title = soup.select('.texto_principal h2').pop()

    # removes surrounding parentheses
    original_title = original_title.text[1:-1]

    poster_thumb = soup.select('.imagen_principal').pop()['src']
    poster_thumb = CINES_BASE_URL + poster_thumb

    poster_full = soup.find(id='gallery').a['href']
    poster_full = CINES_BASE_URL + poster_full

    synopsis = soup.select('.cartelera_cuadro p').pop()
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
            'synopsis', 'cast', 'genre', 'runtime']

    values = [title, original_title, poster_thumb, poster_full, synopsis,
              cast, genre, runtime]

    return dict(zip(keys, values))


if __name__ == '__main__':
    from pprint import pprint

    r = requests.get(CINES_BASE_URL)
    cartelera_paths = get_movie_paths(r.text, CARTELERA)
    pprint(fetch_movie_data(cartelera_paths[0]))

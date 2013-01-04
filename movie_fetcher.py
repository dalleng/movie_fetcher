from bs4 import BeautifulSoup
import requests

CINES_BASE_URL = 'http://www.cines.com.py'
CARTELERA, NUEVOS = range(2)


def list_movies(text, movies_type=CARTELERA):
    """ Returns a dict with movie titles as keys and movie urls
        as values. """

    if movies_type == CARTELERA:
        id = 'cuadro_lista_nuevos'
    elif movies_type == NUEVOS:
        id = 'cuadro_lista_cartelera'
    else:
        raise TypeError(
            "expecting type of movie, got %s" % type(movie_type).__name__)

    soup = BeautifulSoup(text)

    movies = soup.find(id=id)
    # some links are not needed
    movies = movies.find_all('a')[:-3]

    movie_titles = [a.text for a in movies]
    movie_paths = [a['href'] for a in movies]

    movies = dict(zip(movie_titles, movie_paths))
    return movies


def fetch_movie_data(movie_path):
    r = requests.get(CINES_BASE_URL + movie_path)
    soup = BeautifulSoup(r.text)

    original_title = soup.select('.texto_principal h2')
    original_title = original_title[1:-1]


if __name__ == '__main__':
    r = requests.get(CINES_BASE_URL)
    cartelera_movies = list_movies(r.text, movies_type=CARTELERA)
    nuevos_movies = list_movies(r.text, movies_type=NUEVOS)

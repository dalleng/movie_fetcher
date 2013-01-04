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
    """ Fetches movie info from the movie site. Returns a dict
        containing the info obtained. """

    """
    TO-DO
    fetch:
        - poster_full
        - genres
        - title
        - cast

    """

    r = requests.get(CINES_BASE_URL + movie_path)
    soup = BeautifulSoup(r.text)

    original_title = soup.select('.texto_principal h2').pop()
    
    # removes surrounding parentheses
    original_title = original_title.text[1:-1]
    
    poster_path_thumb = soup.select('.imagen_principal').pop()['src']
    
    synopsis = soup.select('.cartelera_cuadro p').pop()
    synopsis = synopsis.text.strip()


if __name__ == '__main__':
    r = requests.get(CINES_BASE_URL)
    import pprint; pprint.pprint(get_movie_paths(r.text, CARTELERA))
    #nuevos_movies = list_movies(r.text, movies_type=NUEVOS)

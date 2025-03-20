
import django
import os
import requests
from datetime import datetime
from get_movies import get_movies


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'censura_project.settings')
django.setup()
from censura.models import Genre

def populate_movies(pages):
    for i in range(1, pages + 1):

        params = {
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "page": i,
            "sort_by": "vote_average.desc",
            "without_genres": [99, 10770],
            "vote_count.gte": 1000,
            "with_original_language": "en",
        }
        
        get_movies(params)
        
        
def get_new_movies():

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": 1,
        "primary_release_date.lte": datetime.now().strftime('%Y-%m-%d'), 
        "sort_by": "primary_release_date.desc",
        "without_genres": [99, 10770],
        "vote_count.gte": 500,
        "with_original_language": "en",
    } 
         
    get_movies(params)   
         
        


def populate_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"
    }

    genres = requests.get(url, headers=headers).json()['genres']

    for genre in genres:
        g = Genre.objects.get_or_create(
            genre_id=genre['id'], name=genre['name'])[0]
        g.save()     


if __name__ == '__main__':
    print('Populating Genres table...')
    populate_genres()
    
    print('Populating Movies table...')
    populate_movies(10)
    
    print("Getting new movies...")
    get_new_movies()
    
import datetime
import django
import os
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'censura_project.settings')
django.setup()
from censura.models import Movie, Genre


def get_new_movies():
    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": 1,
        "primary_release_date.lte": datetime.datetime.now().strftime('%Y-%m-%d'), 
        "sort_by": "primary_release_date.desc",
        "without_genres": [99, 10770],
        "vote_count.gte": 500,
        "with_original_language": "en",
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"
    }

    movies = requests.get(url, params=params, headers=headers).json()[
        'results']
    
    for movie in movies:
        movie_id = movie['id']
        name = movie['original_title']
        description = movie['overview']
        release_date = datetime.datetime.strptime(movie['release_date'], '%Y-%m-%d')
        genre_ids = movie['genre_ids']

        image = f"https://image.tmdb.org/t/p/original/{movie['poster_path']}"

        # GET DIRECTOR
        crew = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/credits",
            headers=headers).json()["crew"]
        director = [c["name"] for c in crew if c["job"] == "Director"][0]

        m, created = Movie.objects.get_or_create(
            movie_id=movie_id,
            defaults={
                "name": name,
                "description": description,
                "release_date": release_date,
                "director": director,
                "image": image,
            }
        )

        if created:
            # establist relationship between genre_ids and Genre table
            genres = Genre.objects.filter(genre_id__in=genre_ids)
            m.genre.set(genres)
            
            response = requests.get(image)
            if response.status_code == 200:
                image_name = f"{movie_id}.jpg"
                
                if image_name not in os.listdir('media/movie_images/'):
                    m.image.save(image_name, ContentFile(response.content), save=True)
                    m.image = f"movie_images/{image_name}"
                    
            m.save()  
            
            
if __name__ == '__main__':
    print("Getting new movies...")
    get_new_movies()
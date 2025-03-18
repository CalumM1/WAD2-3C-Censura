from censura.models import Movie, Genre
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

class MovieCreationTests(TestCase):
    def test_movie_slug(self):
        movie = Movie.objects.create(name="Random Movie", release_date="2025-01-01")
        self.assertEqual(movie.slug, "random-movie")
        
    def test_movie_name_unique(self):
        movie = Movie.objects.create(name="test", release_date="2025-01-01")
        
        with self.assertRaises(IntegrityError):
            movie2 = Movie.objects.create(name="test", release_date="2025-01-01")
                 
    def test_slug_update(self):
        movie = Movie.objects.create(name="test", release_date="2025-01-01")
        movie.name = "Test Slug Update"
        movie.save()
        self.assertEquals(movie.slug, "test-slug-update")
        
    def test_validate_release_date(self):
        movie = Movie.objects.create(name="test", release_date="2025-01-01")
        
        with self.assertRaises(ValidationError):
            movie.full_clean()
        

class MovieGenreTests(TestCase):
    def setUp(self):
        self.genre1 = Genre.objects.create(name="Adventure")
        self.genre2 = Genre.objects.create(name="Fantasy")
        self.genre3 = Genre.objects.create(name="Animation")
        
        self.movie = Movie.objects.create(name="Test", description="this is a test", release_date="2025-01-01")
        self.movie.genre.add(self.genre1, self.genre2, self.genre3)

    def test_movie_multiple_genres(self):
        self.assertEquals(3, self.movie.genre.count())
        self.assertIn(self.genre1, self.movie.genre.all(), f"ERROR: Genre {self.genre1} not found")
        self.assertIn(self.genre2, self.movie.genre.all(), f"ERROR: Genre {self.genre2} not found")
        self.assertIn(self.genre3, self.movie.genre.all(), f"ERROR: Genre {self.genre3} not found")
    
    def test_delete_genre(self):
        # Check if the movie still exists after deleting genre
        self.genre1.delete()
        self.assertTrue(Movie.objects.filter(name="Test", release_date="2025-01-01").exists())

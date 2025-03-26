import censura
import tempfile
from censura.models import Movie, Genre, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import models
from django.test import TestCase


class MovieCreationTests(TestCase):
    def test_movie_slug(self):
        movie = Movie.objects.create(
            name="Random Movie", release_date="2025-01-01")
        self.assertEqual(movie.slug, "random-movie")

    def test_movie_name_unique(self):
        movie = Movie.objects.create(name="test", release_date="2025-01-01")

        with self.assertRaises(IntegrityError):
            movie2 = Movie.objects.create(
                name="test", release_date="2025-01-01")

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

        self.movie = Movie.objects.create(
            name="Test", description="this is a test", release_date="2025-01-01")
        self.movie.genre.add(self.genre1, self.genre2, self.genre3)

    def test_movie_multiple_genres(self):
        self.assertEquals(3, self.movie.genre.count())
        self.assertIn(self.genre1, self.movie.genre.all(),
                      f"ERROR: Genre {self.genre1} not found")
        self.assertIn(self.genre2, self.movie.genre.all(),
                      f"ERROR: Genre {self.genre2} not found")
        self.assertIn(self.genre3, self.movie.genre.all(),
                      f"ERROR: Genre {self.genre3} not found")

    def test_delete_genre(self):
        # Check if the movie still exists after deleting genre
        self.genre1.delete()
        self.assertTrue(Movie.objects.filter(
            name="Test", release_date="2025-01-01").exists())


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='test@test.com',
                                        password='123')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.movie = Movie.objects.create(
            name="Test", description="this is a test", release_date="2025-01-01")

        self.user_profile.likes.add(self.movie)

    def test_userprofile(self):
        self.assertTrue('UserProfile' in dir(censura.models))

        expected_attributes = {
            'user': self.user,
            'likes': UserProfile._meta.get_field('likes'),
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,

        }

        expected_types = {
            'user': models.OneToOneField,
            'likes': models.ManyToManyField,
            'picture': models.ImageField,
        }

        found_count = 0

        for attr in self.user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(
                        attr), expected_types[attr_name], f"Incorrect type for '{attr_name}': Expected - '{expected_types[attr_name]}', Actual - '{type(attr)}'.")
                    setattr(self.user_profile, attr_name,
                            expected_attributes[attr_name])

        for attr in self.user_profile._meta.many_to_many:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(
                        attr), expected_types[attr_name], f"Incorrect type for '{attr_name}': Expected - '{expected_types[attr_name]}', Actual - '{type(attr)}'.")

        self.assertEqual(found_count, len(expected_attributes.keys(
        )), f"Not enough attributes in UserProfile: Expected - {len(expected_attributes.keys())}, Found - {found_count}.")
        self.user_profile.save()


class TestRegisterLogin(TestCase):
    def setUp():
        pass

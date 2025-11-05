from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import Genre, Movie
from app.serializers import GenreSerializer, MovieSerializer
import json

User = get_user_model()

class GenreMovieAPITestCase(APITestCase):
    def setUp(self):
        # Test user yaratish
        self.user = User.objects.create_user(username="toxir", password="toxir123")
        self.client.force_authenticate(user=self.user)

        
        self.genre = Genre.objects.create(name="Action")
        self.genre_url = reverse('genre-list')
        self.movie_url = reverse('movie-list')

        
        self.movie_data = {
            "title": "Test Movie",
            "description": "A test description",
            "year": 2023,
            "genre_id": self.genre.id
        }

    
    def test_create_genre(self):
        data = {"name": "Comedy"}
        response = self.client.post(self.genre_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(Genre.objects.last().name, "Comedy")

    def test_read_genre(self):
        response = self.client.get(self.genre_url)
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_update_genre(self):
        data = {"name": "Thriller"}
        url = reverse('genre-detail', args=[self.genre.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, "Thriller")

    def test_delete_genre(self):
        url = reverse('genre-detail', args=[self.genre.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)


    def test_create_movie(self):
        data = {
            "title": "Test Movie",
            "description": "A test description",
            "year": 2023,
            "genre": self.genre.id,
            "genre_id": self.genre.id
        }
        response = self.client.post(self.movie_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.last().title, "Test Movie")

    def test_read_movie(self):
        movie = Movie.objects.create(title="Movie1", description="Desc", genre=self.genre, year=2000)
        response = self.client.get(self.movie_url)
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_update_movie(self):
        movie = Movie.objects.create(title="Old Title", description="Desc", genre=self.genre, year=2000)
        data = {"title": "New Title", "description": "Desc", "genre_id": self.genre.id, "year":2000, "genre": self.genre.id}
        url = reverse('movie-detail', args=[movie.id])
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie.refresh_from_db()
        self.assertEqual(movie.title, "New Title")

    def test_delete_movie(self):
        movie = Movie.objects.create(title="Delete Me", description="Desc", genre=self.genre, year=2000)
        url = reverse('movie-detail', args=[movie.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)
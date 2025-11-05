from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kino jarni")

    def __str__(self) -> str:
        return self.name
    

class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Kino nomi")
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField()
    genre = models.ForeignKey(Genre, related_name="movies", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    movie = models.ForeignKey(Movie, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.movie.title}"
    
class Like(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.movie.title}"
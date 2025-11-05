from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Genre, Movie, Comment, Like
from .serializers import GenreSerializer, MovieSerializer, CommentSerializer, LikeSerializer

class DefaultPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'user', None) == request.user

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'year']
    search_fields = ['title', 'description']
    ordering_fields = ['year', 'created_at']

    def perform_create(self, serializer):
        movie = serializer.save()
        users = User.objects.all()
        emails = [u.email for u in users if u.email]
        send_mail(
            subject="Yangi film qo'shildi!",
            message=f"Salom! Yangi film: {movie.title}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=True,
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
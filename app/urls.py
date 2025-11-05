from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, LikeViewSet, MovieViewSet, CommentViewSet

router = DefaultRouter()

router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls

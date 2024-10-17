from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import ShortenedURLViewSet, PublicShortenedURLViewSet
from .views.users import AuthViewSet

router = DefaultRouter()
router.register(r'my-urls', ShortenedURLViewSet, basename='shortenedurl')
router.register(r'public-urls', PublicShortenedURLViewSet, basename='public-shortenedurl')
router.register(r'auth', AuthViewSet, basename='authentication')

urlpatterns = [
    path('', include(router.urls)),
]

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from vhsapi.views import register_user, login_user, GenreView, MovieView, RareUserView, RentalView, ReviewView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genre', GenreView, 'genre')
router.register(r'movie', MovieView, 'movie')
router.register(r'user', RareUserView, 'user')
router.register(r'rental', RentalView, 'rental')
router.register(r'review', ReviewView, 'review')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
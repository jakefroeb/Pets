from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from petsapi.views import register_user, login_user, PetView, AnimalTypeView
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'pets', PetView, 'pet')
router.register(r'animaltypes', AnimalTypeView, 'animaltype')
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

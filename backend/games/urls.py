
from django.urls import path, include
from rest_framework import routers


import games.views as views

router = routers.DefaultRouter()
router.register(r'characters', views.CharacterViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('initialize_game/', views.initialize_game),
]
import django_eventstream.urls
from django.urls import path, include
from rest_framework import routers



import games.views as views

router = routers.DefaultRouter()
router.register(r'characters', views.CharacterViewSet)


urlpatterns = [
    path('api/', include(router.urls)),

     # event stream
    path('stream/<game_id>/', include(django_eventstream.urls), 
         {'format-channels': ['game-{game_id}']}),


    path('initialize_game/', views.initialize_game),
    path('legal_bids/', views.legal_bids),
    path('end_round/', views.end_round),
    
    path('get_move/', views.get_move),
    path('get_chat_messages/', views.get_chat_messages),
]
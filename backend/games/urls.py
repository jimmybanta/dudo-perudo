
from django.urls import path, include

import games.views as views


urlpatterns = [
    path('initialize_game/', views.initialize_game),

]
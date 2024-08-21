from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt # Allow request without csrf_token set
from rest_framework.decorators import api_view

from rest_framework import viewsets

import random

from games.models import Game, Character
from games.serializers import CharacterSerializer
from perudo.round import run_round




## Viewsets

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()    
    serializer_class = CharacterSerializer



@api_view(['POST'])
def initialize_game(request):
    '''Initializes a new game.'''

    ### Set up Game

    player = request.data['player']
    table = request.data['table']
    dice_per_player = request.data['dice_per_player']

    # check if the human player has been added as the first player in table
    if player != table[0]:
        table.insert(0, player)

    # create a new game
    game = Game.objects.create()

    game.player = player
    game.table = table
    game.dice_per_player = dice_per_player

    game.save()

    ### Determine who goes first
    starting_player = random.choice(table)

    # run the first round, up to the human
    run_round(game, starting_player)



    return HttpResponse(starting_player)








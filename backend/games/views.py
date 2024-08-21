from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt # Allow request without csrf_token set
from rest_framework.decorators import api_view

import random

from games.models import Game, Character
from perudo.round import run_round


# Create your views here.

@api_view(['POST'])
def initialize_game(request):
    '''Initializes a new game.'''

    ### Set up Game
    # request.data['players'] will be a list of the players, that the human has chosen
    #request.data['players'] = 

    player_name = request.data['player_name']
    players = request.data['players']

    # check if the human player has been added as the first player in players
    if player_name != players[0]:
        players.insert(0, player_name)

    # create a new game
    game = Game.objects.create()

    game.player_name = player_name
    game.players = players

    game.save()

    ### Determine who goes first
    starting_player = random.choice(players)

    # run the first round, up to the human
    run_round(game, starting_player)



    return HttpResponse(starting_player)








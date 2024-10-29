from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt # Allow request without csrf_token set
from rest_framework.decorators import api_view

from django_eventstream import send_event

from rest_framework import viewsets

import config
import random
import time
import json
import logging

from games.models import Game, Character
from games.serializers import CharacterSerializer
from perudo.round import run_round
import perudo.logic as logic

from perudo.characters.characters import CHARACTERS

from prompting import prompt

logger = logging.getLogger(__name__)


## Viewsets

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()    
    serializer_class = CharacterSerializer

@csrf_exempt
@api_view(['GET'])
def get_current_version(request):
    '''
    Returns the current version of the game.
    '''

    return JsonResponse({'version': config.game_version})


@api_view(['POST'])
def initialize_game(request):
    '''Initializes a new game.'''

    ### Set up Game

    player = request.data['player']
    table = request.data['table']
    dice_per_player = request.data['dice_per_player']
    sides_per_die = request.data['sides_per_die']

    # check if the human player has been added as the first player in table
    if player != table[0]:
        table.insert(0, player)

    # create a new game
    game = Game.objects.create()

    game.player = player
    game.table = table
    game.dice_per_player = dice_per_player
    game.sides_per_die = sides_per_die

    game.save()

    ### Determine who goes first
    current_player = random.choice(table)

    data_to_return = {
        'game_id': game.id,
        'starting_player': current_player
    }

    return JsonResponse(data_to_return)


@api_view(['POST'])
def legal_bids(request):
    '''Given the state of the table, returns all the legal bids.'''

    table_dict = request.data['table_dict']
    sides_per_die = request.data['sides_per_die']
    palifico = request.data['palifico']
    round_history = request.data['round_history']
    current_player = request.data['current_player']

    # get total num of dice
    try:
        total_dice = sum([int(table_dict[player]['dice']) for player in table_dict])
    except:
        print('problem')
        print(table_dict)
    
    # if there's no round history, then we're at the beginning of the round
    # we want to get the starting bids for the player
    if not round_history:

        bids = logic.legal_bids.legal_starting_bids(total_dice, 
                                    sides_per_die=sides_per_die, palifico=palifico)
    
    # if there is round history, then we're in the middle of the round
    # we want to get the legal bids for the player
    else:
        _, previous_bid = round_history[-1]

        bids = logic.legal_bids.legal_bids(previous_bid, total_dice, 
                                    sides_per_die=sides_per_die, palifico=palifico,
                                    ex_palifico=table_dict[current_player]['ex-palifico'])

    
    return JsonResponse({'legal_bids': bids})

@api_view(['POST'])
def get_move(request):
    ''' Given an AI player, gets their move given the current state of the round/game. '''

    current_player = request.data['current_player']
    round_history = request.data['round_history']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']

    logger.info(f'Getting move for {current_player}')

    # note - could be used later, if we want to incorporate game history into AI moves
    game_history = request.data['game_history']

    total_dice = sum([table_dict[player]['dice'] for player in table_dict])

    current_player_obj = CHARACTERS[current_player.split('-')[0].lower()]()

    # get the move from the AI player
    ## case 1 - round is underway
    if round_history:
        move = current_player_obj.move(round_history, game_history, total_dice, palifico=palifico)
    ## case 2 - round is starting
    else:
        move = current_player_obj.starting_bid(total_dice, palifico=palifico)

    ## to do - add pausing/thinking time logic
    # time in milliseconds
    pause = 5000
    
    return JsonResponse({'move': move, 'pause': pause})
    
@api_view(['POST'])
def end_round(request):
    '''Run at the end of a round.'''

    round_history = request.data['round_history']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']
    loser = request.data['loser']
    total = request.data['total']

    game_id = request.data['game_id']

    """ # first, score the bid 

    last_bid = round_history[-2][1]

    hands = [table_dict[key]['hand'] for key in table_dict.keys()]
    all_dice = [die for hand in hands for die in hand]
    
    score = logic.score.score(last_bid, all_dice, palifico=palifico)

    correct = score[0]
    total = score[1]

    # determine who loses a die
    loser = round_history[-1][0] if correct else round_history[-2][0] """

    # create the round_dict
    # this is a dictionary with all info about the round - hands, moves, loser
    round_dict = {
        'table_dict': table_dict,
        'round_history': round_history,
        'palifico': palifico,
        'loser': loser,
        'total': total,
    }

    # then, update the game state
    game = Game.objects.get(id=game_id)
    if game.history:
        game.history.append(round_dict)
    else:
        game.history = [round_dict]
    game.save()
    
    """ # then, return the loser and the total to the frontend
    data_to_return = {
        'loser': loser,
        'total': total,
    } """

    return JsonResponse({'success': True})

@api_view(['POST'])
def get_chat_messages(request):
    '''Generates chat messages for a game.'''

    game_id = request.data['game_id']
    player = request.data['player']
    table = request.data['table']
    round_history = request.data['round_history']
    message_history = request.data['message_history']
    starting_player = request.data['current_player'] 
    user_message = request.data['user_message']

    # context
    ## either: 
    ##      initialize_game - at the beginning of a game
    ##      move - during a round
    ##      user_message - when the user sends a message
    context = request.data['context']

    if context == 'intialize_game':
        pass
    
    # streaming responses
    current_message = ''
    sent_messages = 0
    total_delay = 0
    
    for chunk in prompt(
                    context=context,
                    message_history=message_history,
                    round_history=round_history,
                    user_message=user_message,
                    table=table,
                    player=player,
                    stream=True,
                    starting_player=starting_player
                ):
        
        # remove any newlines
        chunk = chunk.replace('\n', '')
        
        current_message += chunk

        # if we've reached the end of a message, send it
        if '{' in current_message and '}' in current_message:

            # get the message
            start_point = current_message.index('{')
            break_point = current_message.index('}') + 1
            message_dict = json.loads(current_message[start_point:break_point])

            # if it doesn't have a delay, then set it to 0
            try:
                message_delay = message_dict['delay']
            except:
                message_delay = 0

            # if it's the first message, then send with no delay
            if sent_messages == 0:
                message_dict['delay'] = 0
            # otherwise, add the total delay on
            else:
                message_dict['delay'] = message_delay + total_delay
                
            send_event(f'game-{game_id}', 'message', message_dict)
        
            current_message = current_message[break_point:]

            # add the delay
            total_delay += message_delay

            sent_messages += 1

    
        



    return JsonResponse({'success': True})

    
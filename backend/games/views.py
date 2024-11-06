import json
import logging
import random

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  # Allow request without csrf_token set
from rest_framework import viewsets
from rest_framework.decorators import api_view

from django_eventstream import send_event

import config
from games.models import Game, Character
from games.serializers import CharacterSerializer
from games.prompting import prompt
import perudo.logic as logic
from perudo.logic.calculate_probs import calculate_prob
from perudo.characters.characters import CHARACTERS

logger = logging.getLogger(__name__)


# Viewsets
class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()    
    serializer_class = CharacterSerializer

# Views
@csrf_exempt
@api_view(['GET'])
def get_current_version(request):
    '''
    Returns the current version of the game.
    '''

    return JsonResponse({'version': config.game_version})

@api_view(['POST'])
def initialize_game(request):
    '''Initializes a new game.
    
    API Parameters
    --------------
    player : str
        The name of the human user.
    table : list
        A list of players at the table.
    dice_per_player : int
        The number of dice each player starts with.
    sides_per_die : int
        The number of sides on each die.
    '''

    ### Set up Game

    player = request.data['player']
    table = request.data['table']
    dice_per_player = request.data['dice_per_player']
    sides_per_die = request.data['sides_per_die']

    # check if the human player has been added as the first player in table
    if player != table[0]:
        table.insert(0, player)

    # create a new game
    try:
        game = Game.objects.create(
            player=player,
            table=table,
            dice_per_player=dice_per_player,
            sides_per_die=sides_per_die
        )
    except:
        logger.exception('Error creating game')
        return HttpResponse('Error creating game. Please try again.', status=255)


    ### Determine who goes first
    current_player = random.choice(table)

    # return the game id and the starting player to the frontend
    data_to_return = {
        'game_id': game.id,
        'starting_player': current_player
    }

    return JsonResponse(data_to_return)

@api_view(['POST'])
def legal_bids(request):
    '''Given the state of the table, returns all the legal bids.
    
    API Parameters
    --------------
    table_dict : dict
        A dictionary of players and their attributes.
    sides_per_die : int
        The number of sides on each die.
    palifico : bool
        Whether it is a palifico round.
    round_history : list
        A list of previous moves.
    current_player : str
        The current player.
    '''

    table_dict = request.data['table_dict']
    sides_per_die = request.data['sides_per_die']
    palifico = request.data['palifico']
    round_history = request.data['round_history']
    current_player = request.data['current_player']

    try:
        # get total num of dice
        total_dice = sum([int(table_dict[player]['dice']) for player in table_dict])
        
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
    except:
        logger.exception('Error getting legal bids')
        return HttpResponse('Server error. Please try again.', status=255)

    return JsonResponse({'legal_bids': bids})

@api_view(['POST'])
def get_move(request):
    ''' Given an AI player, gets their move given the current state of the round/game. 
    
    API Parameters
    --------------
    current_player : str
        The current player.
    round_history : list
        A list of previous moves.
    table_dict : dict
        A dictionary of players and their attributes.
    palifico : bool
        Whether it is a palifico round.
    game_history : list
        A list of previous rounds.
    '''

    current_player = request.data['current_player']
    round_history = request.data['round_history']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']

    logger.info(f'Getting move for {current_player}')

    hand = table_dict[current_player]['hand']

    # note - could be used later, if we want to incorporate game history into AI moves
    game_history = request.data['game_history']

    try:
        total_dice = sum([table_dict[player]['dice'] for player in table_dict])

        current_player_obj = CHARACTERS[current_player.split('-')[0].lower()]()

        # get the move from the AI player
        ## case 1 - round is underway
        if round_history:
            move, pause = current_player_obj.move(hand, round_history, game_history, total_dice, palifico=palifico)
        ## case 2 - round is starting
        else:
            move, pause = current_player_obj.starting_bid(hand, total_dice, palifico=palifico)
    except: 
        logger.exception(f'Error getting move for {current_player}')
        return HttpResponse('Server error. Please try again.', status=255)
    
    return JsonResponse({'move': move, 'pause': pause})
    
@api_view(['POST'])
def end_round(request):
    '''Run at the end of a round.
    
    API Parameters
    --------------
    round_history : list
        A list of previous moves.
    table_dict : dict
        A dictionary of players and their attributes.
    palifico : bool
        Whether it is a palifico round.
    loser : str
        The player who lost the round.
    total : int
        The total number of dice on the table.
    game_id : int
        The game id.
    '''

    round_history = request.data['round_history']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']
    loser = request.data['loser']
    total = request.data['total']

    game_id = request.data['game_id']

    # create the round_dict
    # this is a dictionary with all info about the round - hands, moves, loser
    round_dict = {
        'table_dict': table_dict,
        'round_history': round_history,
        'palifico': palifico,
        'loser': loser,
        'total': total,
    }

    try:
        # then, update the game state
        game = Game.objects.get(id=game_id)
        if game.history:
            game.history.append(round_dict)
        else:
            game.history = [round_dict]
        game.save()
    except:
        logger.exception('Error saving game history')
        return HttpResponse('Server error. Please try again.', status=255)

    return JsonResponse({'success': True})

@api_view(['POST'])
def get_chat_messages(request):
    '''Generates chat messages for a game.

    API Parameters
    --------------
    game_id : int
        The game id.
    message_history : list
        A list of previous messages.
    player : str
        The current player.
    table : list
        A list of players at the table.
    round_history : list
        A list of previous moves.
    palifico : bool | None
        Whether it is a palifico round.
    table_dict : dict | None
        A dictionary of players and their attributes.
    total_dice : int | None
        The total number of dice on the table.
    sides_per_die : int | None
        The number of sides on each die.
    starting_player : str | None
        The starting player.
    round_total : int | None
        The total number of dice in the round.
    round_loser : str | None
        The player who lost the round.
    user_message : str | None
        The message from the user.
    player_out : str | None
        The player who is out of the game.
    context : str
        The context of the chat message.
    '''

    # these inputs will always be present
    game_id = request.data['game_id']
    player = request.data['player']
    table = request.data['table']
    round_history = request.data['round_history']
    message_history = request.data['message_history']

    # these inputs may not be present
    try:
        palifico = request.data['palifico']
    except:
        palifico = False

    try: 
        table_dict = request.data['table_dict']
        total_dice = sum([int(table_dict[x]['dice']) for x in table_dict.keys()])
        sides_per_die = request.data['sides_per_die']
    except:
        total_dice = None
        sides_per_die = None

    try:
        starting_player = request.data['starting_player'] 
    except:
        starting_player = None

    try:
        round_total = request.data['round_total']
        round_loser = request.data['round_loser']
    except:
        round_total = None
        round_loser = None

    try:
        user_message = request.data['user_message']
    except:
        user_message = None

    try:
        player_out = request.data['player_out']
    except:
        player_out = None

    # context
    ## either: 
    ##      initialize_game - at the beginning of a game
    ##      move - during a round
    ##      end_round - the end of a round, when someone loses a die
    ##      player_out - when a player is out of the game
    ##      user_message - when the user sends a message
    context = request.data['context']

    prob = None
    # if we're in the middle of a round, then we want to calculate the probability of the bid
    if context == 'move':

        move = round_history[-1][1]

        if move != 'call':
            prob = calculate_prob(move, total_dice, palifico=palifico, sides_per_die=sides_per_die)

            # if prob is within some range, we don't want any responses
            # no need for responses to these reasonable bids - just clogs up the chat
            if prob > 0.25 and prob < 0.75:
                return JsonResponse({'success': True})                
    
    # streaming responses
    current_message = ''
    sent_messages = 0
    total_delay = 0
    
    # get the response stream
    for chunk in prompt(
                    context=context,
                    message_history=message_history,
                    round_history=round_history,
                    user_message=user_message,
                    table=table,
                    player=player,
                    stream=True,
                    starting_player=starting_player,
                    palifico=palifico,
                    player_out=player_out,
                    round_total=round_total,
                    round_loser=round_loser,
                    bid_probability=prob,
                    total_dice=total_dice,
                    sides_per_die=sides_per_die,
                ):
        
        # remove any newlines
        chunk = chunk.replace('\n', '')
        
        # add the chunk to the current message
        current_message += chunk

        # if we've reached the end of a message, send it
        if '{' in current_message and '}' in current_message:

            # get the message
            start_point = current_message.index('{')
            break_point = current_message.index('}') + 1
            message_dict = json.loads(current_message[start_point:break_point])

            # don't let it return messages by the player
            try:
                if message_dict['writer'] == player:
                    break
            except:
                break

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

            # if there's no text, then break
            if 'text' not in message_dict:
                logger.info(f'No text in message: {message_dict}')
                break
                
            # send it to the frontend
            send_event(f'game-{game_id}', 'message', message_dict)
        
            # reset the current message
            current_message = current_message[break_point:]

            # add the delay
            total_delay += message_delay

            sent_messages += 1


    return JsonResponse({'success': True})

    
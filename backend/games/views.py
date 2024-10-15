from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt # Allow request without csrf_token set
from rest_framework.decorators import api_view

from rest_framework import viewsets

import random

from games.models import Game, Character
from games.serializers import CharacterSerializer
from perudo.round import run_round
import perudo.logic as logic

from perudo.characters.characters import CHARACTERS




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
    #current_player = random.choice(table)

    # temp - for now, the human player will always go first
    current_player = player

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

    print('round history:', round_history)
    print('palifico:', palifico)
    print(table_dict)

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



""" @api_view(['POST'])
def score_bid(request):
    '''Given the state of the table, scores the bid.'''

    round_history = request.data['round_history']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']

    last_bid = round_history[-2][1]

    #all_dice = [die for key in table_dict.keys() for hand in table_dict[key]['hand'] for die in hand]

    hands = [table_dict[key]['hand'] for key in table_dict.keys()]
    all_dice = [die for hand in hands for die in hand]
    
    score = logic.score.score(last_bid, all_dice, palifico=palifico)

    correct = score[0]
    total = score[1]

    return JsonResponse({
        'correct': correct,
        'total': total
    }) """


@api_view(['POST'])
def get_move(request):
    ''' Given an AI player, gets their move given the current state of the round/game. '''

    current_player = request.data['current_player']
    round_history = request.data['round_history']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']

    print('current player:', current_player)

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
    pause = 500
    
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
def run_round(request):
    '''
    Runs a round of the game.

    A round begins in one of two ways:
        1. the starting player is the human - in which case, the human will make a bid in the frontend, and it will 
            be sent here, then play will continue from there
        2. the starting player is an AI - in which case, the AI will make a bid, and the play will continue from there

    A round ends in one of two ways:
        1. an AI calls someone, so the outcome of the round needs to be evaluated
        2. play gets sent back to the human, in which case the human, in the frontend, needs to make a move
            - in this case, if the human bids, then another round is run
            - if the human lifts, it is dealt with in the frontend
    
    '''

    ### Get data from request
    game_id = request.data['game_id']
    player = request.data['player']
    starting_player = request.data['starting_player']
    table_dict = request.data['table_dict']

    
    # beginning case 1
    if player == starting_player:
        # we should have a bid from the human
        bid = request.data['bid']
    
    # beginning case 2
    else:
        pass
        


@api_view(['POST'])
def make_bid(request):
    '''For either a human player or an AI to make a bid.'''

    player = request.data['player']
    current_player = request.data['current_player']
    bid = request.data['bid']
    round_history = request.data['round_history']
    table = request.data['table']
    table_dict = request.data['table_dict']
    palifico = request.data['palifico']
    

    total_dice = sum([table_dict[player]['dice'] for player in table_dict])

    # moves is the list that will be returned
    # of moves that need to be reported by the frontend
    moves = []

    # current_bid and current_player go together in a somewhat unintuitive way
    # current_bid is the last bid made, and current_player is the player who now needs to make a new bid, based off that bid
    
    # case 1 - the human player is the current player, and they just made a bid
    if current_player == player:
        current_bid = bid
        next_player_name = table[(table.index(player) + 1) % len(table)]
    # case 2 - an AI player is the current player, and we need them to bid
    else:
        current_bid = None
        next_player_name = current_player


    # run through all the other players
    # stop when a player calls or when it gets back to the human player
    while current_bid != 'call' and next_player_name != player:

        next_player_obj = CHARACTERS[next_player_name.split('-')[0].lower()]
        next_player = next_player_obj()

        # get the move from the AI player
        ## case 1 - round is underway
        if current_bid:
            current_bid = next_player.move(current_bid, round_history, total_dice, palifico=palifico)
        ## case 2 - round is starting
        else:
            current_bid = next_player.starting_bid(total_dice, palifico=palifico)
            
        # add player bid to round history
        round_history.append((next_player_name, current_bid))
        # add player bid to move
        moves.append((next_player_name, current_bid))

        # get the next player
        next_player_name = table[(table.index(next_player_name) + 1) % len(table)]
    

    data_to_return = {
        'round_history': round_history,
        'moves': moves
    }
        

    return JsonResponse(data_to_return)



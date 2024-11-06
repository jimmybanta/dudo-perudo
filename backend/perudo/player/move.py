''' Contains functions that AI players use to make moves in a game of Perudo. '''

import random
from perudo.logic.calculate_probs import calculate_prob
from perudo.logic.hand import Hand




def choose_bid(hand, options, total_dice, min_probability, palifico=False, blur=0):
    ''' Uses binary search to identify the bid that is closest to a probability threshold. 
    
    Parameters
    ----------
    hand : Hand
        The player's hand.
    options : list
        The possible bids.
    total_dice : int
        The total number of dice in the game.
    min_probability : float
        The minimum probability threshold.
    palifico : bool | False
        Whether the game is in palifico.
    blur : float | 0
        The probability blur - how much to randomly skew the probability - to simulate uncertainty.
    '''

    # get the total dice outside of the player's hand
    total_dice_exclusive = total_dice - len(hand)

    # binary search
    current_min = 0
    current_max = len(options) - 1
    last_index = None

    while True:

        # go between the current min and current max
        current_index = (current_min + current_max) // 2

        # if we've reached the same index as last time, break
        if current_index == last_index:
            break

        option = options[current_index]

        # identify how many dice the player has that match the bid's value
        to_remove = hand.count(option[1])
        if not palifico and option[1] != 1:
            to_remove += hand.count(1)

        # calculate the probability of the bid
        # taking into account the player's hand


        prob = calculate_prob((option[0] - to_remove, option[1]), total_dice_exclusive, palifico=False, sides_per_die=6)

        # add the blur to the probability
        prob += blur
        
        if prob > 1:
            prob = 1
        elif prob < 0:
            prob = 0

        if prob > min_probability:
            current_min = current_index
        elif prob < min_probability:
            current_max = current_index
        
        last_index = current_index

    return option

def decide_call(hand, bid, total_dice, min_probability, palifico=False, blur=0):
    ''' 
    Decides whether to call or to bid. 

    Parameters
    ----------
    hand : Hand
        The player's hand.
    bid : tuple
        The current bid.
    total_dice : int
        The total number of dice in the game.
    min_probability : float
        The minimum probability threshold.
    palifico : bool | False
        Whether the game is in palifico.
    blur : float | 0
        The probability blur - how much to randomly skew the probability - to simulate uncertainty.
    '''

    # get the total dice outside of the player's hand
    total_dice_exclusive = total_dice - len(hand)

    to_remove = hand.count(bid[1])
    if not palifico and bid[1] != 1:
        to_remove += hand.count(1)

    # calculate the probability of the bid
    # taking into account the player's hand
    prob = calculate_prob((bid[0] - to_remove, bid[1]), total_dice_exclusive, palifico=False, sides_per_die=6)

    # add the blur to the probability
    prob += blur
    if prob > 1:
        prob = 1
    elif prob < 0:
        prob = 0

    return True if prob < min_probability else False

def create_bluff_hand(hand, bluff_value, bluffing_intensity=0.5, sides_per_die=6):
    '''
    Creates a bluff hand by changing the values of the dice.

    Parameters
    ----------
    hand : Hand
        The player's hand.
    bluff_value : int
        The value to bluff about.
    bluffing_intensity : float | 0.5
        The intensity of the bluff.
    sides_per_die : int | 6 
        The number of sides on each die.
    '''

    # we need to create a dummy hand that incorporates a bluff
            
    # determine how many dice they'll bluff about
    bluff_quantity = int(bluffing_intensity * len(hand))

    # create the dummy hand
    dummy_hand = [bluff_value for _ in range(bluff_quantity)]

    for _ in range(len(hand) - bluff_quantity):

        # get a random value that isn't the bluff value
        value = None
        while value == None or value == bluff_value:
            value = random.randint(1, sides_per_die)
        
        # add it to the hand
        dummy_hand.append(value)
        
        
    return Hand(size=len(dummy_hand), sides_per_die=sides_per_die, values=sorted(dummy_hand))


def choose_bluff_value(round_history, palifico=False, sides_per_die=6):
    '''
    Chooses a bluff value based on the previous bids.

    Parameters
    ----------
    round_history : list
        The history of the round.
    palifico : bool | False
        Whether the game is in palifico.
    sides_per_die : int | 6
        The number of sides on each die.
    '''

    # if there's no history, just choose randomly
    if not round_history:
        
        if palifico:
            return random.randint(1, sides_per_die)
        else:
            return random.randint(2, sides_per_die)

    # otherwise, get the previous values that have been bidded
    previous_bid_values = [x[1][1] for x in round_history]

    # get the most common value(s)
    counts = {x: previous_bid_values.count(x) for x in set(previous_bid_values)}
    max_count = max(counts.values())

    # if there's a tie, choose randomly
    max_values = [x for x in counts.keys() if counts[x] == max_count]
    bluff_value = random.choice(max_values)

    return bluff_value
    


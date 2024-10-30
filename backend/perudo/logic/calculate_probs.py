''' Holds functions for calculating probabilities. '''

from math import comb
import itertools as it



def calculate_prob(bid, total_dice, 
                   palifico=False,
                   sides_per_die=6):
    '''
    Calculates the probability of a bid being correct.

    Parameters
    ----------
    bid : tuple
        The bid in the form (quantity, value).
    total_dice : int
        The total number of dice in the game.
    palifico : bool | False
        Whether the game is in palifico.
    sides_per_die : int | 6
        The number of sides on each die.
    '''

    # unpack the bid
    quantity, value = bid

    # straight is when we don't double count wilds
    # this is when palifico, or when the value is 1
    straight = True if (value == 1 or palifico) else False

    # calculate the total combinations
    total_combinations = sides_per_die ** total_dice

    running_combinations = 0

    # set the combinations for each quantity
    for k in range(quantity, total_dice + 1):

        # k represents a given quantity of dice
        # we're calculating the total combinations in which there are k of a certain value,
        # given total_dice dice
        
        # don't want to count wilds
        if straight:
            running_combinations += comb(total_dice, k) * ((sides_per_die - 1) ** (total_dice - k))
        # there are wilds
        # and we need to take that into account
        else:
            running_combinations += comb(total_dice, k) * ((sides_per_die - 2) ** (total_dice - k)) * (2 ** k)

    
    return running_combinations / total_combinations

    


# for validating out the combinatorics method
def calculate_prob_brute(bid, total_dice):

    iter = it.product([1, 2, 3, 4, 5, 6], repeat=total_dice)

    total_comb = 6 ** total_dice

    running_comb = 0

    for combo in iter:
        
        if combo.count(bid[1]) + combo.count(1) >= bid[0]:
            running_comb += 1
    
    return running_comb / total_comb

''' Functions for determining legal bids. '''

import math


def legal_bids(current, total_dice, 
               sides_per_die=6, palifico=False, ex_palifico=False):
    '''
    Returns a list of all legal bids, given a situation.

    Parameters
    ----------
    current : tuple/list
        The current bid.
    total_dice : int
        The total number of dice in the game.
    sides_per_die : int || default: 6
        The number of sides on each die.
    palifico : bool || default: False
        Whether the current round is a palifico round or not.
    ex_palifico : bool || default: False
        Whether the current player is ex-palifico.
    '''

    legal_bids = []
    
    # get the current bid quantity and value
    current_quantity, current_value = current[0], current[1]

    # palifico logic
    if palifico:

        # if they're ex-palifico they can bid like normal
        if ex_palifico:
            # add the same quantity bids
            legal_bids += same_quantity_bids(current_quantity, current_value,
                                            sides_per_die=sides_per_die)
            
            # add the higher quantity bids
            legal_bids += higher_quantity_bids(current_quantity, total_dice,
                                                value_range=(1, sides_per_die))
                
        # if they're not ex-palifico they can only bid the same value with higher quantity
        else:
            legal_bids += higher_quantity_bids(current_quantity, total_dice,
                                                value_range=(current_value, current_value))
            
    # standard play logic
    else:
        
        # if the current bid is on jessies
        if current_value == 1:

            # add possible normie bids
            ## quantity must be double plus 1
            ### just double it, then the higher_quantity_bids function will add 1
            necessary_quantity = (current_quantity * 2)
            legal_bids += higher_quantity_bids(necessary_quantity, total_dice,
                                                value_range=(2, sides_per_die))
            
            # add possible jessie bids
            legal_bids += higher_quantity_bids(current_quantity, total_dice,
                                                value_range=(1, 1))
            

        # if the current bid is on normies
        else:

            # add the same quantity bids
            legal_bids += same_quantity_bids(current_quantity, current_value,
                                            sides_per_die=sides_per_die)
            
            # add the higher quantity bids
            legal_bids += higher_quantity_bids(current_quantity, total_dice,
                                                value_range=(2, sides_per_die))
            
            # add the jessie bids
            ## need to subtract 1 from the necessary quantity because the
            ## higher_quantity_bids function will add 1
            necessary_quantity = math.ceil(current_quantity / 2) - 1
            legal_bids += higher_quantity_bids(necessary_quantity, total_dice, 
                                                value_range=(1, 1))
            
    ## check for duplicates
    legal_bids = sorted(list(set(legal_bids)))
    ## remove any bids that have a quantity of 0
    legal_bids = [bid for bid in legal_bids if bid[0] != 0]


    return legal_bids
        
def legal_starting_bids(total_dice, 
                        sides_per_die=6,
                        palifico=False):
    '''
    Returns a list of all legal starting bids.
    A player must bid a quantity of at least 1.

    Parameters
    ----------
    total_dice : int
        The total number of dice in the game.
    sides_per_die : int || default: 6
        The number of sides on each die.
    palifico : bool || default: False
        Whether the current round is a palifico round or not.
    '''

    legal_starting_bids = []

    # palifico logic
    if palifico:
        # can start with any value
        legal_starting_bids += higher_quantity_bids(0, total_dice,
                                                value_range=(1, sides_per_die))
            
    # standard play logic
    else:
        # you can't start with jessies - must start with a value of 2 or higher
        legal_starting_bids += higher_quantity_bids(0, total_dice,
                                                value_range=(2, sides_per_die))
    
    return legal_starting_bids





def same_quantity_bids(quantity, value, 
                    sides_per_die=6):
    '''
    Returns a generator of all possible bids with the same quantity as the given bid.

    Parameters
    ----------
    quantity : int
        The given bid quantity.
    value : int
        The given bid value.
    sides_per_die : int || default: 6
        The number of sides on each die.
    '''

    for i in range(value + 1, sides_per_die + 1):
        yield (quantity, i)

def higher_quantity_bids(quantity, total_dice,
                    value_range=(1, 6)):
    '''
    Returns a generator of all possible bids with a higher quantity than the given bid.

    Parameters
    ----------
    quantity : int
        The given bid quantity.
    total_dice : int
        The total number of dice in the game.
    value_range : tuple || default: (2, 6)
        The range of values that can be called.
    '''

    # go through all possible quantities higher than the current quantity, 
    # less than or equal to the total number of dice
    for i in range(quantity + 1, total_dice + 1):
        # go through all possible values in the given range
        for j in range(value_range[0], value_range[1] + 1):
            yield (i, j)

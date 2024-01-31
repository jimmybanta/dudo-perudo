''' Holds functions for determining legal bids. '''

import math


def legal_bids(current, total_dice, 
               sides_per_die=6, palifico=False, ex_palifico=False):
    '''
    Returns a list of all legal bids.

    Parameters
    ----------
    current : tuple
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

    return legal_bids
        




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


    

if __name__ == '__main__':

    current = (4, 2)
    current_quantity, current_value = current[0], current[1]
    total_dice = 10
    sides_per_die = 6
    palifico = False
    ex_palifico = False

    value_range = (1, 1)

    bids = higher_quantity_bids(current_quantity, total_dice,
                    value_range=value_range)
    
    def print_list_with_newlines(lst, items_per_line=7):
        for i, item in enumerate(lst, start=1):
            print(item, end=', ')
            if i % items_per_line == 0:
                print()  # Move to a new line after every 7 items
        
        print()  # Move to a new line after the last item

    print_list_with_newlines(bids)
    

    







''' For scoring a bid in Perudo.'''



def score(bid, all_dice, palifico=False):
    '''Score a bid in Perudo.
    Returns True if the bid was true, False otherwise.
    
    Parameters
    ----------
    bid : tuple
        The bid to be scored.
    all_dice : list
        A list of all the dice in the game.
    palifico : bool || default: False
        Whether the current round is a palifico round or not.'''
    
    # get the bid quantity and value
    quantity, value = bid[0], bid[1]

    # get the number of dice with the given value
    num = all_dice.count(value)

    if palifico:
        total = (num, value)
        return (True, total) if num >= quantity else (False, total)
    
    # if in a standard round and the value wasn't jessies
    # then add the number of jessies to the total
    if value > 1:
        num += all_dice.count(1)

    total = (num, value)
    return (True, total) if num >= quantity else (False, total)
    



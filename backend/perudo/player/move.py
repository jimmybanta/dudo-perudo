''' Contains functions that AI players use to make moves in a game of Perudo. '''

from perudo.logic.calculate_probs import calculate_prob



def choose_bid(hand, options, total_dice, min_probability, palifico=False):
    ''' Uses binary search to identify the bid that is closest to a probability threshold. '''

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

        if prob > min_probability:
            current_min = current_index
        elif prob < min_probability:
            current_max = current_index
        
        last_index = current_index

    return option

def decide_call(hand, bid, total_dice, min_probability, palifico=False):
    ''' Decides whether to call or to bid. '''

    # get the total dice outside of the player's hand
    total_dice_exclusive = total_dice - len(hand)

    to_remove = hand.count(bid[1])
    if not palifico and bid[1] != 1:
        to_remove += hand.count(1)


    # calculate the probability of the bid
    # taking into account the player's hand
    prob = calculate_prob((bid[0] - to_remove, bid[1]), total_dice_exclusive, palifico=False, sides_per_die=6)
    
    return True if prob < min_probability else False
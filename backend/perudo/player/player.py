''' Contains the Player class and its subclasses. '''

import random

from perudo.logic.hand import Hand
from perudo.logic.legal_bids import legal_bids, legal_starting_bids
from perudo.local_game.utils import input_int
from perudo.player.move import choose_bid, decide_call, create_bluff_hand, choose_bluff_value

class Player:
    '''A player in a game of Perudo.
    Can be either a human player or an AI player.'''

    def __init__(self, 
                 name=None, 
                 num_dice=5, 
                 sides_per_die=6, 
                 ai=False):
        self.name = name
        self.num_dice = num_dice
        self.sides_per_die = sides_per_die
        self.ai = ai

        self.ex_palifico = False

        self.hand = None
    
    def roll(self, values=None):
        '''Roll the dice.
        If values is not None, then the dice are rolled with the given values.
        
        Parameters
        ----------
        values : list | None
            The values to roll the dice with. If None, then the dice are rolled randomly.
        '''

        self.hand = Hand(size=self.num_dice, sides_per_die=self.sides_per_die, values=values)
    
    def lose_die(self):
        '''Lose a die.'''
        self.num_dice -= 1
    
    def __str__(self):
        return self.name if self.name else super().__str__()

    @property
    def one_left(self):
        '''Returns True if the player has only one die left, False otherwise.'''
        return True if self.num_dice == 1 else False
    


class HumanPlayer(Player):
    '''A human player in a game of Perudo.'''

    def __init__(self, 
                 name=None, 
                 num_dice=5, 
                 sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die, ai=False)
    
    def starting_bid(self, total_dice, palifico=False):
        '''
        Inputs the player for the starting bid.

        Parameters
        ----------
        total_dice : int
            The total number of dice in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        allowed_bids = legal_starting_bids(total_dice=total_dice, 
                                           sides_per_die=self.sides_per_die,
                                           palifico=palifico)

        quantity = input_int('What quantity do you choose? ')
        value = input_int('what value do you choose? ')

        while (quantity, value) not in allowed_bids:
            print('Illegal bid!')
            quantity = input_int('What quantity do you choose? ')
            value = input_int('What value do you choose? ')

        return (quantity, value)

    def starting_direction(self, players, palifico=False):
        '''
        Inputs the player for the direction the player wants to go in.

        Note: I only used this in the local game. In the online game, the play always moves clockwise.

        Parameters
        ----------
        players : list
            The list of players in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        direction = input('Up or down? ')
        while direction.lower() not in ['up', 'down']:
            direction = input('Up or down? ')

        return direction.lower()
    
    def move(self, bid, history, total_dice, palifico=False):
        '''
        Allows the player to input a move - either a call or a higher bid.

        Parameters
        ----------
        bid : tuple
            The current bid in the form (quantity, value).
        history : list
            The history of the round.
        total_dice : int
            The total number of dice in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        call = input('Do you wish to call? Type y to call, anything else to bid. ')
        if call.lower() == 'y':
            return False

        allowed_bids = legal_bids(bid, total_dice, 
                                  sides_per_die=self.sides_per_die,
                                  palifico=palifico,
                                  ex_palifico=self.ex_palifico)
        
        print(f'    Allowed bids: {allowed_bids}')
        
        if not allowed_bids:
            return False

        quantity = input_int('What quantity do you choose? ')
        value = input_int('What value do you choose? ')

        while (quantity, value) not in allowed_bids:
            print('Illegal bid!')
            quantity = input_int('What quantity do you choose? ')
            value = input_int('What value do you choose? ')
        
        return (quantity, value)


class AIPlayer(Player):
    '''An AI player in a game of Perudo.'''

    def __init__(self, 
                 name=None, 
                 num_dice=5, 
                 sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die, ai=True)


class AIRandomPlayer(AIPlayer):
    '''An AI player that plays completely randomly.'''

    def starting_bid(self, hand, total_dice, palifico=False):
        '''
        Randomly selects a bid from all possible allowed starting bids.

        Parameters
        ----------
        hand : Hand
            The player's hand.
        total_dice : int
            The total number of dice in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        allowed_bids = legal_starting_bids(total_dice=total_dice, 
                                           sides_per_die=self.sides_per_die,
                                           palifico=palifico)

        return random.choice(allowed_bids), 1000

    
    def move(self, hand, round_history, game_history, total_dice, palifico=False):
        '''
        Randomly chooses to call (with a given probability) or to bid. 
        If bidding, randomly selects a bid from all allowed bids.

        Parameters
        ----------
        hand : Hand
            The player's hand.
        round_history : list
            The history of the current round.
        game_history : list
            The history of the game.
        total_dice : int
            The total number of dice in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        # 25% chance of calling
        if random.random() < 0.25:
            return 'call', 5000

        # 75% chance of bidding
        allowed_bids = legal_bids(round_history[-1][1], total_dice, 
                                  sides_per_die=self.sides_per_die,
                                  palifico=palifico,
                                  ex_palifico=self.ex_palifico)
        
        # if there are no legal bids to make, then call
        if not allowed_bids:
            return 'call', 5000

        # otherwise, randomly select a bid
        return random.choice(allowed_bids), 5000


class AISmartPlayer(AIPlayer):
    ''' An AI Player designed to play intelligently.'''

    def __init__(self, 
                 name=None, 
                 num_dice=5, 
                 sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # the probability that a bid needs to clear to be eligible to play
        ## the lower this is, the bolder the player
        self.betting_prob = .5

        # the probability that an incoming bid has to clear for you to raise the bet
        ## the lower this is, the more likely the player is to raise the bet 
        ## in other words, the more aggressive the player
        self.calling_prob = .5

        # the probability that a bid needs to clear to start a normal round
        self.starting_prob = .75
        # the probability that a bid needs to clear to start a palifico round
        self.starting_palifico_prob = .9

        # how much to blur the probability
        ## aka how much uncertainty to add to the player's probability calculations
        ## to simulate human-like play when unable to calculate exact probabilities
        self.probability_blur = 0.2

        # the probability that the player will bluff about their bid
        self.bluffing_prob = 0.25
        # the intensity of their bluffing
        ## the higher, the more of their dice they'll bluf about, essentially
        self.bluffing_intensity = 0.6

        # a range of time to take before making a move
        self.starting_pause = [500, 1500]



    def starting_bid(self, hand, total_dice, palifico=False):
        '''
        Selects a bid from all possible allowed starting bids.

        Parameters
        ----------
        hand : Hand
            The player's hand.
        total_dice : int
            The total number of dice in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        allowed_bids = legal_starting_bids(total_dice=total_dice, 
                                           sides_per_die=self.sides_per_die,
                                           palifico=palifico)
                
        starting_prob = self.starting_prob if not palifico else self.starting_palifico_prob

        # calculate the probability blur
        ## aka how much uncertainty to add to the player's probability calculations
        ## it will be a random value, uniformly picked from the range [-probability_blur, probability_blur]
        blur = random.uniform(-self.probability_blur, self.probability_blur)

        # determine if they'll be bluffing
        if random.random() < self.bluffing_prob:

            # randomly choose the value they'll bluff about
            # (as this is the starting bid, so there's no information to go off of)
            if palifico:
                bluff_value = random.randint(1, self.sides_per_die)
            else:
                bluff_value = random.randint(2, self.sides_per_die)

            hand = create_bluff_hand(hand, bluff_value, bluffing_intensity=self.bluffing_intensity, sides_per_die=self.sides_per_die)
            

        # choose the bid
        bid = choose_bid(hand, allowed_bids, total_dice, starting_prob, palifico=palifico, 
                         blur=blur)

        return bid, random.randint(*self.starting_pause)
        
    def move(self, hand, round_history, game_history, total_dice, palifico=False):
        ''' 
        Chooses a move based on the current state of the game.

        Parameters
        ----------
        hand : Hand
            The player's hand.
        round_history : list
            The history of the current round.
        game_history : list
            The history of the game. (Note: currently unused)
        total_dice : int
            The total number of dice in the game.
        palifico : bool | False
            Whether the game is in palifico.
        '''

        last_bid = round_history[-1][1]

        # calculate the probability blur
        blur = random.uniform(-self.probability_blur, self.probability_blur)

        # decide if they'll call
        if decide_call(hand, last_bid, total_dice, self.calling_prob, palifico=palifico, blur=blur):
            return 'call', random.randint(*self.starting_pause)
        
        # determine the allowed bids
        allowed_bids = legal_bids(round_history[-1][1], total_dice, 
                                  sides_per_die=self.sides_per_die,
                                  palifico=palifico,
                                  ex_palifico=self.ex_palifico)
        
        # determine if they'll be bluffing
        if random.random() < self.bluffing_prob:

            # choose the bluff value based on the round history
            bluff_value = choose_bluff_value(round_history, palifico=palifico, sides_per_die=self.sides_per_die)

            hand = create_bluff_hand(hand, bluff_value, bluffing_intensity=self.bluffing_intensity, sides_per_die=self.sides_per_die)
        
        # choose the bid
        bid = choose_bid(hand, allowed_bids, total_dice, self.betting_prob, palifico=palifico, 
                         blur=blur)

        return bid, random.randint(*self.starting_pause)
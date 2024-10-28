
import random

from perudo.hand import Hand
from perudo.logic.legal_bids import legal_bids, legal_starting_bids
from perudo.local_game.utils import input_int

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
        If values is not None, then the dice are rolled with the given values.'''

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
        '''Inputs the player for the starting bid.'''

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
        '''Inputs the player for the direction the player wants to go in.'''

        direction = input('Up or down? ')
        while direction.lower() not in ['up', 'down']:
            direction = input('Up or down? ')

        return direction.lower()
    
    def move(self, bid, history, total_dice, palifico=False):
        '''Allows the player to input a move - either a call or a higher bid.'''

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

    def starting_bid(self, total_dice, palifico=False):
        '''Randomly selects a bid from all possible allowed starting bids.'''

        allowed_bids = legal_starting_bids(total_dice=total_dice, 
                                           sides_per_die=self.sides_per_die,
                                           palifico=palifico)

        return random.choice(allowed_bids)

    def starting_direction(self, players, palifico=False):
        '''Randomly selects a direction.'''

        return random.choice(['up', 'down'])

    
    def move(self, round_history, game_history, total_dice, palifico=False):
        '''Randomly chooses to call (prob .25) or to bid (prob .75). 
        If bidding, randomly selects a bid from all allowed bids.'''

        n = random.random()

        # 25% chance of calling
        if n < 0.25:
            return 'call'

        # 75% chance of bidding
        allowed_bids = legal_bids(round_history[-1][1], total_dice, 
                                  sides_per_die=self.sides_per_die,
                                  palifico=palifico,
                                  ex_palifico=self.ex_palifico)
        
        # if there are no legal bids to make, then call
        if not allowed_bids:
            return 'call'

        # otherwise, randomly select a bid
        return random.choice(allowed_bids)

if __name__ == '__main__':

    num_dice = 5
    sides_per_die = 6

    player = Player(name='test', num_dice=num_dice, ai=False, sides_per_die=sides_per_die)

    print(player)
    print(player.num_dice)
    print(player.hand)
    player.roll()
    print(player.hand)
    print(player.hand.count(1))
    player.lose_die()
    print(player.num_dice)
    player.roll()
    print(player.hand)
    player.lose_die()
    player.roll()
    print(player.hand)
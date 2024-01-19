
from perudo.hand import Hand

class Player:
    '''A player in the game.
    Can be either a human player or an AI player.'''

    def __init__(self, name=None, num_dice=5, ai=False):
        self.name = name
        self.num_dice = num_dice
        self.ai = ai
    
    def roll(self, values=None):
        '''Roll the dice.
        If values is not None, then the dice are rolled with the given values.'''

        if values:
            self.hand = Hand(values=values, size=self.num_dice)
        else:
            self.hand = Hand(size=self.num_dice)
    
    def lose_die(self):
        '''Lose a die.'''
        self.num_dice -= 1
    
    def __str__(self):
        return self.name

    @property
    def one_left(self):
        '''Returns True if the player has only one die left, False otherwise.'''
        return True if self.num_dice == 1 else False
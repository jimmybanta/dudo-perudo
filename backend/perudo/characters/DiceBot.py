

from perudo.player.player import AISmartPlayer

class DiceBot(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # plays completely by the numbers - trying to play mathematically perfectly
        self.betting_prob = .5
        self.calling_prob = .5

        self.starting_prob = .75
        self.starting_palifico_prob = .75

        self.probability_blur = 0.0

        # bluffs a decent amount
        self.bluffing_prob = 0.5
        self.bluffing_intensity = 0.6

        # plays very quickly
        self.starting_pause = [400, 500]


from perudo.player.player import AISmartPlayer

class Cosbo(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # bold
        self.betting_prob = .25
        self.calling_prob = .25

        self.starting_prob = .4
        self.starting_palifico_prob = .7

        self.probability_blur = 0.2

        # bluffs a decent amount
        self.bluffing_prob = 0.4
        self.bluffing_intensity = 0.8

        # a range of time to take before making a move
        self.starting_pause = [500, 2500]
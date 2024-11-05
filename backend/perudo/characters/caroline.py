

from perudo.player.player import AISmartPlayer

class Caroline(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # somewhat bold
        self.betting_prob = .3
        self.calling_prob = .3

        self.starting_prob = .5
        self.starting_palifico_prob = .6

        self.probability_blur = 0.1

        # bluffs a decent amount
        self.bluffing_prob = 0.35
        self.bluffing_intensity = 0.6

        # a range of time to take before making a move
        self.starting_pause = [1500, 2500]
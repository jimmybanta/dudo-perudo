

from perudo.player.player import AISmartPlayer

class Sabina(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # sabina is cautius
        self.betting_prob = .6
        self.calling_prob = .6

        self.starting_prob = .7
        self.starting_palifico_prob = .8

        # she doesn't pay much attention to the probability
        self.probability_blur = 0.3

        # she doesn't bluff
        self.bluffing_prob = 0
        self.bluffing_intensity = 0

        # a range of time to take before making a move
        self.starting_pause = [750, 1500]
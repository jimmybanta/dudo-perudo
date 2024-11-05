

from perudo.player.player import AISmartPlayer

class Theo(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # theo
        self.betting_prob = .4
        self.calling_prob = .4

        self.starting_prob = .5
        self.starting_palifico_prob = .6

        # theo is fairly reckless/doesn't pay much attention to the probability
        self.probability_blur = 0.3

        # theo bluffs quite a bit
        self.bluffing_prob = 0.75
        self.bluffing_intensity = 0.6

        # a range of time to take before making a move
        self.starting_pause = [1000, 1500]
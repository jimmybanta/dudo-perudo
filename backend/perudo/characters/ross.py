

from perudo.player.player import AISmartPlayer

class Ross(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        self.betting_prob = .4
        self.calling_prob = .5

        self.starting_prob = .4
        self.starting_palifico_prob = .7

        self.probability_blur = 0.075

        # ross bluffs quite a bit
        self.bluffing_prob = 0.6
        self.bluffing_intensity = 0.6

        # ross plays quickly
        self.starting_pause = [250, 750]
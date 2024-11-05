

from perudo.player.player import AISmartPlayer

class Jimmy(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        self.betting_prob = .4
        self.calling_prob = .4

        self.starting_prob = .5
        self.starting_palifico_prob = .75

        self.probability_blur = 0.15

        # jimmy bluffs a bit
        self.bluffing_prob = 0.4
        self.bluffing_intensity = 0.5

        # jimmy thinks for a while before making a move
        self.starting_pause = [2500, 5000]
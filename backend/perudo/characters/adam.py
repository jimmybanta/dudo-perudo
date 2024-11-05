

from perudo.player.player import AISmartPlayer

class Adam(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # adam is bold
        self.betting_prob = .2
        self.calling_prob = .1

        self.starting_prob = .4
        self.starting_palifico_prob = .7

        self.probability_blur = 0.25

        # adam doesn't bluff much
        self.bluffing_prob = 0.15
        self.bluffing_intensity = 0.6

        # a range of time to take before making a move
        self.starting_pause = [750, 1500]
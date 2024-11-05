

from perudo.player.player import AISmartPlayer

class Riyaaz(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # riyaaz plays by the numbers when he can
        self.betting_prob = .5
        self.calling_prob = .5

        self.starting_prob = .6
        self.starting_palifico_prob = .75

        # he knows his math well - has a good idea of what the probability is
        self.probability_blur = 0.03

        # riyaaz bluffs a little
        self.bluffing_prob = 0.3
        self.bluffing_intensity = 0.6

        self.starting_pause = [1500, 2000]

    
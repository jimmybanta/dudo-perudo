

from perudo.player.player import AISmartPlayer

class Ignatius(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

        # ignatius is unnecessarily bold
        self.betting_prob = .1
        self.calling_prob = .1

        self.starting_prob = .6
        self.starting_palifico_prob = .6

        self.probability_blur = 0.35

        # ignatius always bluffs
        self.bluffing_prob = 1
        self.bluffing_intensity = 1

        # ignatius has a big range
        self.starting_pause = [250, 5000]
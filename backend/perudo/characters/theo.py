

from perudo.player.player import AISmartPlayer

class Theo(AISmartPlayer):

    def __init__(self, name=None, num_dice=5, sides_per_die=6):
        super().__init__(name=name, num_dice=num_dice, sides_per_die=sides_per_die)

    
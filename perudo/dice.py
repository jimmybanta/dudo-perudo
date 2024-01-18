import random

class Die:
    def __init__(self, sides, value=None):
        self.sides = sides if isinstance(sides, int) else False

        self.value = value if value and self.sides else random.randint(1, sides)

    def __eq__(self, other):
        return True if self.value == other.value else False

    def __lt__(self, other):
        return True if self.value < other.value else False
    
    def __le__(self, other):
        return True if self < other or self == other else False
    
    def __gt__(self, other):
        return True if self.value > other.value else False
    
    def __ge__(self, other):
        return True if self > other or self == other else False

class D6(Die):
    def __init__(self, value=None):
        super().__init__(6, value)

from perudo.dice import Die


class Hand(list):
    '''A "hand" of dice.
    Extends the list class.'''

    def __init__(self, size=5, values=None, sides_per_die=6):
        if values:
            if len(values) != size:
                raise ValueError(f'Need to pass in {size} values!')
            else:
                for value in values:
                    self.append(Die(sides=sides_per_die, value=value))
        else:
            for _ in range(size):
                self.append(Die(sides=sides_per_die))
        self.sort()

    def __str__(self):
        return f'{[die.value for die in self]}'
    
    def count(self, value, palifico=False):
        '''Count the number of dice with the given value.
        If palifico is True, only count the number of dice with the given value and not jessies.'''

        num = [die.value for die in self].count(value)

        # If someone is palifico, then don't count jessies
        if palifico:
            return num
        # If the value is 1, then just return the number of 1s
        if value == 1:
            return num
        # Otherwise, return the number of dice with the given value and the number of jessies
        jessies = [die.value for die in self].count(1)
        return num + jessies
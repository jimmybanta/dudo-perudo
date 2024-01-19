
from dice import D6


class Hand(list):
    def __init__(self, *args, size=5):
        if args:
            if len(args) != size:
                raise ValueError('Need to pass in {} values!'.format(size))
            else:
                for arg in args:
                    self.append(D6(value=arg))
        else:
            for _ in range(size):
                self.append(D6())
        self.sort()


        l = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']

        for i, attr in enumerate(l):
            setattr(self, attr, self.count(i + 1))


    def __str__(self):
        return '{}'.format([die.value for die in self])
    
    def count(self, num):
        d = [die.value for die in self]
        return d.count(num)
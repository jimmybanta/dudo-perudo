
import random
import math

class Game:
    def __init__(self):
        self.players = []
        self.order = []
        self.winner = None
        self.winner_dice = 0
        
    def end_round(self, player):
        player.num_dice -= 1

    def check_end(self):
        remaining_players = [player for player in self.players if player.num_dice != 0]
        return False if len(remaining_players) >= 2 else True
        
    def update_order(self):
        self.order = [player for player in self.players if player.num_dice > 0]
    
    def check_winner(self):
        # returns the winner 
        for player in self.players:
            if self.players[player] != 0:
                return player



class HumanGame(Game):
    def __init__(self, num_players):
        super().__init__(num_players)

        for player in AIPLAYERS:
            self.players[player] = NO_DICE
            self.order.append(player)

        name = input('What is your name? ')
        human_player = Player(name, dice=NO_DICE)
        self.players[human_player] = NO_DICE
        self.order.append(human_player)

        random.shuffle(self.order)

        self.total_dice = sum(self.players.values())

    def play(self):
        input('Welcome to perudo! You know the rules...')
        round_num = 0

        while not self.check_end():
            round_num += 1
            input('start of round... ')

            for player in self.players:
                print('Player: {}'.format(str(player)))
                print('Dice: {}'.format(self.players[player]))
            print('')
            print('order: {}'.format([str(player) for player in self.order]))
            print('')
            if round_num == 1:
                round = Round(self.players, self.order)
            print('Dice: {}'.format(round.all_dice))
            round.run()
            print('Loser: {}'.format(round.final_loser))
            self.end_round(round.final_loser)
            self.update_order()
            print('')
        print('Game Over!')
        self.check_winner()
        print('Winner: {} with {} dice'.format(self.winner, self.winner_dice))


class Round:
    def __init__(self, players, order):
        self.players = players
        self.order = order
        for player in self.order:
            player.roll()

        self.total_dice = sum(self.players.values())

        self.all_dice = []
        for player in self.order:
            for die in player.hand:
                self.all_dice.append(die.value)

        self.all_dice.sort()

        self.final_loser = None

        # keep track of bets - to be used later
        self.bets = []


    def start(self, straight=False):
        first = self.order[0]

        if first.ai:
            return first.starting_bet(self.total_dice, straight=straight)
        else:
            return self.input_start()
    
    def input_start(self):
        quantity = int(input('What quantity do you choose? '))
        value = int(input('what value do you choose? '))
        return (quantity, value)
    
    def input_later(self, bet):
        quantity = input('What quantity do you choose? (Or type call to call) ')
        if quantity.lower() == 'call':
            return False
        value = int(input('what value do you choose? '))
        new_bet = (int(quantity), value)
        while not self.legal_move(bet, new_bet):
            quantity = int(input('What quantity do you choose? '))
            value = int(input('what value do you choose? '))
            bet = (quantity, value)
        return bet


    def run(self):
        betting_player = self.order[0]
        first_bet = self.start()
        print("First bet: {} {}'s".format(first_bet[0], first_bet[1]))
        print(str(betting_player))
        print('')
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        if not calling_player.ai:
            bet = self.input_later(first_bet)
        else:
            bet = calling_player.bet(first_bet)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            print("Current bet: {} {}'s".format(bet[0], bet[1]))
            print(str(betting_player))
            print('')
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            if not calling_player.ai:
                bet = self.input_later(bet)
            else:
                bet = calling_player.bet(bet)
            

        print('Call! ')
        print('')
        bet = self.bets[-1]
        print('Betting player: {}'.format(str(betting_player)))
        print('Calling player: {}'.format(str(calling_player)))

        print('Bet is {}'.format(self.score(bet)))

        self.final_loser = self.loser(bet, calling_player, betting_player)
        
        print('Loser: {}'.format(self.final_loser))


    def score(self, bet, straight=False):
        # returns if a bet is true
        quantity, value = bet[0], bet[1]

        ones = self.all_dice.count(1)
        others = self.all_dice.count(value)

        if straight:
            return True if others >= quantity else False
        else:
            return True if ones + others >= quantity else False
    
    
    def legal_move(self, current, next):
        # returns whether a move is legal or not
        current_quantity, current_value = current[0], current[1]
        next_quantity, next_value = next[0], next[1]

        if current_value == 1:
            if next_value > 1:
                return True if next_quantity >= ((current_quantity * 2) + 1) else False
            elif next_value == 1:
                return True if next_quantity >= (current_quantity + 1) else False
            
        elif current_value > 1:
            if next_value == 1:
                return True if next_quantity >= (math.ceil(current_quantity / 2)) else False
            elif next_value > 1:
                if next_value > current_value:
                    return True if next_quantity >= current_quantity else False
                elif next_value <= current_value:
                    return True if next_quantity > current_quantity else False

    def straight_legal_move(self, current, next, player):
        player_straight = False
        if player.dice == 1:
            player_straight = True

        current_quantity, current_value = current[0], current[1]
        next_quantity, next_value = next[0], next[1]

        if player_straight:
            if next_value > current_value:
                return True if next_quantity >= current_quantity else False
            elif next_value <= current_value:
                return True if next_quantity > current_quantity else False
        else:
            if next_value != current_value:
                return False
            else:
                return True if next_quantity > current_quantity else False

    def test_moves(self, move1=False, move2=False):
        if move1 and move2:
            current_move = (move1[0], move1[1])
            next_move = (move2[0], move2[1])
        else:
            current_move = (random.randint(1,6), random.randint(1,6))
            next_move = (random.randint(1,6), random.randint(1,6))

        print("Current move: {} {}'s".format(current_move[0], current_move[1]))
        print("Next move: {} {}'s".format(next_move[0], next_move[1]))

        truth = True if self.legal_move(current_move, next_move) else False

        print('Legal!') if truth else print('ILLEGAL')
        print('')

    def loser(self, bet, calling_player, betting_player, straight=False):
        return calling_player if self.score(bet, straight=straight) else betting_player
        

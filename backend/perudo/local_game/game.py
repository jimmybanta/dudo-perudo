''' For playing a local game,
for testing out game logic.'''

import random
import math

from perudo.player.player import AIPlayer, HumanPlayer, AIRandomPlayer

from perudo.logic.score import score


class LocalGame:
    '''A game of Perudo, run locally in the console.
    For testing putposes.'''

    def __init__(self, human=True, ai_players=None, can_choose_direction=False,
                 dice_per_player=5, sides_per_die=6):
        
        self.human = human
        self.sides_per_die = sides_per_die
        self.dice_per_player = dice_per_player
        self.can_choose_direction = can_choose_direction
        
        self.players = []

        print('Welcome to Perudo!')

        if self.human:

            name = input('  What is your name?\n')
            self.players.append(HumanPlayer(name=name, 
                                            num_dice=self.dice_per_player,
                                            sides_per_die=self.sides_per_die))
            
        # add the ai players
        self.players += ai_players
            
        self.total_dice = sum([player.num_dice for player in self.players])
        print(f'There are {self.total_dice} dice in play.')
        
        print(f'The players are: {[str(player) for player in self.players]}')
        
    def update_players(self, loser, palifico):

        # if the round was palifico and the loser still has one die, then they're ex-palifico
        if palifico and loser.num_dice == 1:
            loser.ex_palifico = True
        
        self.players = [player for player in self.players if player.num_dice > 0]
    
    def check_winner(self):
        # returns the winner 
        self.winner = self.players[0]



    def play(self):
        input("Let's play some perudo!\n")

        round_num = 1
        palifico = False

        # get the starting player
        ## if a human is playing, they'll start
        if self.human:
            starting_player = [player for player in self.players if player.ai == False][0]
        ## otherwise, choose a random AI player to start
        else:
            starting_player = random.choice(self.players)
            # reorient the order so that the starting player is first
            while self.players[0] != starting_player:
                self.players.append(self.players.pop(0))
        
        print(f'{starting_player} starts!')


        # check if there is only one player left aka the game is over
        # otherwise keep the game goin!
        while len(self.players) > 1:

            print(f'\nRound {round_num}!')

            for player in self.players:
                print(f' Player: {str(player)} -- {player.num_dice} dice')

            # start the round
            round = Round(self.players, starting_player, 
                          palifico=palifico, can_choose_direction=self.can_choose_direction)

            # run the round
            round.run()

            ## GO THROUGH AND TEST THAT EVERYTHING IS WORKING HERE

            # get the loser and update game state after the round
            loser = round.loser
            loser.lose_die()

            # update the players
            ## 1) update direction/order of the players (as this may have flipped in the round)
            self.players = round.players

            ## 2) update the starting player to ex_palifico, if necessary
            if palifico:
                starting_player.ex_palifico = True

            ## 3) get the new starting player
            ### if the loser is out of dice, then the player after them is the new starting player
            if loser.num_dice == 0:
                # get the player after the loser
                starting_player = self.players[self.players.index(loser) + 1]
            else:
                starting_player = loser
                
            ## 4) update the players list
            self.update_players(loser, palifico)

            ## 5) set palifico
            ### palifico only applies if there are more than 2 players
            if len(self.players) > 2:
                palifico = True if loser.num_dice == 1 else False
            else:
                palifico = False

            
            round_num += 1

        print('Game Over!')
        print(f'Winner: {self.players[0]} with {self.players[0].num_dice} dice')



class Round:
    '''Runs a single round of Perudo.
    You need to give it the players and the starting player, and it will run the round,
    and return information about the round.'''

    def __init__(self, players, starting_player, palifico=False, can_choose_direction=False):
        self.players = players
        self.starting_player = starting_player
        self.palifico = palifico
        self.can_choose_direction = can_choose_direction

        # roll the dice and get them all together
        self.all_dice = []
        for player in self.players:
            player.roll()
            if not player.ai:
                print(f'    Your Hand: {player.hand}')
            for die in player.hand:
                self.all_dice.append(die.value)
        self.all_dice.sort()

        self.total_dice = len(self.all_dice)

        # keep track of the bids
        self.history = []

        self.loser = None


    def start(self, palifico=False):
        '''Gets the first bid and direction from the starting player,
        and reorganizes the players based on the direction.'''

        # get the bid from the player
        bid = self.starting_player.starting_bid(self.total_dice, palifico=palifico)

        if self.can_choose_direction:
            # get the direction from the player
            if len(self.players) > 2:
                direction = self.starting_player.starting_direction(self.players, palifico=palifico)
            # if there are only two players, direction doesn't matter
            else:
                direction = 'down'
        else:
            direction = 'down'

        # reorganize the players based on the direction
        # after the reorganization, the starting player should be first
        # with the correct order ascending
        if direction.lower() == 'up':
            self.players = self.players[::-1]
            # move the starting player to the front
            self.players.insert(0, self.players.pop())
        
        return bid


    def run(self):

        if self.palifico:
            print('Palifico!')

        # get the starting bid
        move = self.start(palifico=self.palifico)
        print(f'order: {[str(player) for player in self.players]}')

        # set starting player to calling player - as they will then be switched to bidding player in the while loop
        calling_player = self.starting_player
        turn = 1

        # when move is false, that means someone is calling
        while move != 'call':

            current_bid = move
            # add the bid to the history
            self.history.append(current_bid)
            # update the last calling player to the current bidding player
            bidding_player = calling_player
            # get the next player as the calling player
            calling_player = self.players[turn % len(self.players)]

            input(f'{bidding_player} bids {current_bid[0]} {current_bid[1]}s')
            print(f'calling player: {calling_player}')

            move = calling_player.move(current_bid, self.history, self.total_dice, palifico=self.palifico)
            print(f'move: {move}')

            turn += 1

        print(f'{calling_player} calls!')
        final_bid = self.history[-1]
        print(f'Bidding player: {bidding_player}')
        print(f'Calling player: {calling_player}')

        correct, total = score(final_bid, self.all_dice, palifico=self.palifico)

        print(f'Final bid: {final_bid[0]} {final_bid[1]}s is {"correct!" if correct else "incorrect."}')
        print(f'{self.all_dice}')
        print(f'There were actually {total[0]} {total[1]}s.')

        self.history.append((correct, total))

        print(f'history: {self.history}')

        self.loser = calling_player if correct else bidding_player
        
        print(f'Loser: {self.loser}')

        # reorganize the players so the loser is first
        self.players = self.players[self.players.index(self.loser):] + self.players[:self.players.index(self.loser)]

    




    
    
        

if __name__ == '__main__':

    human = True

    dice_per_player = 2
    sides_per_die = 6

    # ai players
    ai_players = [AIRandomPlayer('Barty', num_dice=dice_per_player, sides_per_die=sides_per_die), 
                    AIRandomPlayer('Cindy', num_dice=dice_per_player, sides_per_die=sides_per_die),
                    AIRandomPlayer('Maurice', num_dice=dice_per_player, sides_per_die=sides_per_die),
                    AIRandomPlayer('Evelyn', num_dice=dice_per_player, sides_per_die=sides_per_die),
                    ]
    

    game = LocalGame(human=human, ai_players=ai_players,
                        dice_per_player=dice_per_player, sides_per_die=sides_per_die,
                        can_choose_direction=False)
    
    game.play()
    

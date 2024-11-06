''' This file contains the models for the games app. '''

from django.db import models

# Create your models here.

class Game(models.Model):

    # the user who created the game
    player = models.CharField(max_length=200, null=True)

    # number of dice each player gets
    dice_per_player = models.IntegerField(null=True)
    # number of sides on each die
    sides_per_die = models.IntegerField(null=True)

    # table is a list of all the players
    # starting with the human player (name given by player)
    # then all the AI players after, in the order they should sit at the table, clockwise
    table = models.JSONField(null=True)

    # history contains a history of the rounds of the game
    ## from a history, you should be able to reconstruct an entire game
    history = models.JSONField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    
class Character(models.Model):

    # the name of the character
    name = models.CharField(max_length=200)

    # the description of the character
    description = models.CharField(max_length=1000, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
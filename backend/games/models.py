from django.db import models

# Create your models here.

class Game(models.Model):

    player = models.CharField(max_length=200, null=True)

    dice_per_player = models.IntegerField(null=True)

    # table is a list of all the players
    # starting with the human player (name given by player)
    # then all the AI players after, in the order they should sit at the table, clockwise
    table = models.JSONField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    
class Character(models.Model):

    name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
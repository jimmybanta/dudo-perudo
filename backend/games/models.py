from django.db import models

# Create your models here.

class Game(models.Model):

    player_name = models.CharField(max_length=200, null=True)

    # players is going to be a list of all the players
    # starting with the human player (name given by player_name)
    # then all the AI players after, in the order they should sit at the table, clockwise
    players = models.JSONField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    
class Character(models.Model):

    name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
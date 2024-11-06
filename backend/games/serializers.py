''' This file contains the serializers for the models in the games app. '''

from rest_framework import serializers

import games.models as models

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = '__all__'
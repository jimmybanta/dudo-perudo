# Generated by Django 5.1 on 2024-08-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_game_sides_per_die'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='history',
            field=models.JSONField(null=True),
        ),
    ]

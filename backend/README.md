# Dudo Perudo Backend

The Dudo Perudo backend is a Django application, that communicates to the frontend via a REST API as well as with Server Sent Events (SSEs).
It is a mix of a game backend, that implements the game logic for Perudo, and an LLM application, that use Google Gemini's family of models to simulate a live multi-user chat experience that integrates with the game of Perudo in real-time.


## Games App
The games app contains the views and functionality for communicating with the frontend as well as with the LLM api.

### Modules

#### admin.py
Contains the admin configuration for the game models.

#### apps.py
This module contains the configuration for the games app.

#### models.py
Contains the models for the game.

#### prompting.py
Contains functions for calling the LLM.

#### serializers.py
Contains serializers for the game models.

#### urls.py
Contains the urls for the game app.

#### utils.py
Contains utility functions for the game.

#### views.py
Contains the views for the game app.
Includes views for playing the game, as well as for calling the LLM.

## Perudo module
The Perudo module contains the game logic for Perudo.

### submodules
#### characters
Contains the character classes for the game.

#### local_game
Contains the game logic for a local game of Perudo.

#### logic
Contains functions that implement game logic for Perudo.

#### player
Contains the player classes for the game.


## Other files and folders
#### assets
Contains text files for prompting and random setup of a game.
#### backend
Contains the settings for the Django application.
#### config.py
Contains the configuration for the game - runs on startup to pull values from s3 parameter store.
#### current_version.json
Contains the current version of the game.
#### manage.py
The Django management script.
#### version_log.txt
Contains the version history of the game.
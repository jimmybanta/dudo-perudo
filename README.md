# Dudo Perudo
Perudo (also called Dudo or Liar's Dice) is the national game of Peru - a highly-social dice game involving bluffing and deception.

Dudo Perudo is an attempt to replicate the Perudo experience online - by implementing the main game, as well as an AI-generated chat, where the different players will banter and quibble, commenting on the game and everything else, as they would around the table in real life.

It can be played at [dudoperudo.com](https://dudoperudo.com/).

The user starts off by inputting their name, then crafting their table - choosing the characters they want to play Perudo with, with each one given a brief description.

Once the user has created their table, they're playing Perudo - players go around the table, making and raising bids, lifting, losing dice, calling out bluffs.
While the game goes on, game info is fed to the LLM, which generates a chat log from the different players - one that the user can interact with at any time by sending their own messages.


## Design
### Backend
The backend (/backend) is built using Django.
It uses Server Sent Events to stream the LLM messages to the frontend.

### LLM
The backend uses Google Gemini's family of models (flash in particular) to generate the interactive chat.

### Frontend
The frontend (/frontend) is built using React.

### Deployment
The application is deployed on AWS, using an ec2 instance to host the backend, and s3 + cloudfront to host the frontend.
The database is hosted on RDS, and the application is served using nginx and daphne.
Upon startup, the application pulls configuration from SSM parameter store.
Route 53 is used to manage the domain and subdomains.
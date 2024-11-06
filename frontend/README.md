# Dudo Perudo - Frontend

The Crash frontend is written in HTML, CSS, and Javascript, 
with React as the framework.
It uses axios to make calls to the backend.

It implements an AI-powered chat feature that uses Server Sent Events (SSEs) to stream messages from the backend.
Upon first render, a game will initiate a stream that is unique to that game ID.
It will continue to listen for messages from the backend until the page is exited.

## Main Pages
### Home
The landing page that a user sees when they first visit. Contains buttons that take you to the Play and About pages.

### Play
A page where a player can play a game.
It renders the Setup page. Then, when the setup configuration has been received from the Setup page, it passes the info to and renders the Game page, where the game will be played.

#### Setup
A page where a player can choose a configuration for their game.
This includes choosing a theme, timeframe, and details.
Or, if they're so inclined, they can click 'setup for me', which will make a call to the backend to return a random configuration
(randomly selected from lists I've come up with).
Then, once they're happy with the configuration, they can click 'Let's Play!' to start the game.
This passes the configuration back to the NewGame page.

#### Game
A page where a player can load a game they've saved. They're prompted for their game save key, then they can hit 'Load Game'. 
It will make a call to the backend to check that the key is valid, and if it is, it will load the game info.
This game info will be passed to the Game page, where the game will be played.


### About
A page that gives a little bit of information about the game.
Displays the current version, which is retrieved from the backend.





## Components
### Chat
A chat component that displays the messages between the player and the AIs. It implements all the chat functionality - creating the event stream, sending, receiving, and displaying AI messages from the backend.

### Header
A header that appears at the top of the Game page that displays 'Dudo Perudo'.

### HelpPopup
A popup that provides some useful rules and information while setting up and playing the game.

### PlayerBid 
A component that allows a player to make a bid, by inputting a quantity and value, or by choosing to lift.

### ValueDropDown
A component within PlayerBid, that displays the possible dice values a player can bid.


## utils/other files
### api.js
Contains the fuction used to make calls to the backend. Uses axios.

### BaseUrl.js
Contains the base URL for the backend. This is used in api.js to make calls to the backend.
Changes depending on the environment (development, staging, production).

### utils.js
Contains some utility functions that are used in multiple components.
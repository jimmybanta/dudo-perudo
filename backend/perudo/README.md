# Perudo

This holds all the game logic for Perudo.


## Glossary
Game - a full game of perudo, from start to finish - from everyone having all their dice to last person standing
Round - A single turn around the circle, starting with an initial call and ending with someone losing a die
Move - a single action taken by a player in a round, either a dudo or a bid
    Quantity - a number of dice ex. 3 dice
    Value - the face value of a die ex. 4's
    Bid - a call of a quantity and a value by a player, increasing the bid
    Dudo - a call of "Dudo" by a player, challenging the previous bid
    
Jessie - during normal play, a 1 is called a 'jessie', and counts as a wild aka it counts as any number
Normie - during normal play, any value other than 1 is called a 'normie' and counts as itself

Standard play - a round of perudo that isn't palifico
    - 1's are jessies
    - most rounds are standard
Palifico - a special round where 1's are not wild
    - Ex-palifico player - a player who has previously been palifico, aka they have one die
    - in addition, all non-ex-palifico players must keep the same value, but can change the quantity
    - ex-palifico players can change the quantity and face value 




## Formatting

Bid - a bid is a tuple of (quantity, value), where quantity is the number of dice of value that the player is claiming are on the table

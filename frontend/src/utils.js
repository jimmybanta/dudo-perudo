
//// utility functions


// rolls a die with the specified number of sides
const rollDie = (numSides) => {

    return Math.floor(Math.random() * numSides) + 1;

};

// rolls a number of dice with the specified number of sides
export const rollDice = (numDice, numSides) => {

    const rolls = [];

    for (let i = 0; i < numDice; i++) {
        rolls.push(rollDie(numSides));
    }

    // Sort the rolls
    rolls.sort((a, b) => a - b);

    return rolls;

};

// waits for a specified number of milliseconds
export const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};




const rollDie = (numSides) => {

    return Math.floor(Math.random() * numSides) + 1;

};

export const rollDice = (numDice, numSides) => {

    const rolls = [];

    for (let i = 0; i < numDice; i++) {
        rolls.push(rollDie(numSides));
    }

    // Sort the rolls
    rolls.sort((a, b) => a - b);

    return rolls;

};


export const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};
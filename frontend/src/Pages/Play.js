import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Input, Button } from 'reactstrap';
import { BASE_URL } from '../interceptors';

import Setup from './GamePages/Setup';
import PlayerBid from './GamePages/Components/PlayerBid';

import { rollDice, sleep } from '../utils'; 

axios.defaults.baseURL = BASE_URL;

const defaultDicePerPlayer = 5;
const defaultSidesPerDie = 6;

const Play = () => {

    // temp setup
    /* 
    const [player, setPlayer] = useState('crespin');
    const [table, setTable] = useState(['crespin', 'riyaaz', 'jimmy', 'adam', 'adam-2', 'theo']);
    const [dicePerPlayer, setDicePerPlayer] = useState(defaultDicePerPlayer);
    const [sidesPerDie, setSidesPerDie] = useState(defaultSidesPerDie);
    const [setupComplete, setSetupComplete] = useState(true);

    const [game, setGame] = useState(59);
    
    const [lastPlayer, setLastPlayer] = useState(null);
    const [lastBid, setLastBid] = useState(null);

    const [currentPlayer, setCurrentPlayer] = useState('crespin');
    const [currentBid, setCurrentBid] = useState(null);

    // display variables -- to be displayed
    const [displayLastPlayer, setDisplayLastPlayer] = useState(null);
    const [displayLastBid, setDisplayLastBid] = useState(null);
    const [displayCurrentPlayer, setDisplayCurrentPlayer] = useState('crespin');
    const [displayCurrentBid, setDisplayCurrentBid] = useState(null);

    const [roundHistory, setRoundHistory] = useState([]);
    const roundHistoryRef = useRef(roundHistory);

    const [showEndRound, setShowEndRound] = useState(false);
    const [roundLoser, setRoundLoser] = useState(null);
    const roundLoserRef = useRef(roundLoser);
    const [roundTotal, setRoundTotal] = useState(null);

    const [tableDict, setTableDict] = useState({
        'crespin': {'dice': 5, 'hand': rollDice(5, 6), 'ex-palifico': false},
        'riyaaz': {'dice': 5, 'hand': rollDice(5, 6), 'ex-palifico': false},
        'jimmy': {'dice': 5, 'hand': rollDice(5, 6), 'ex-palifico': false},
        'adam': {'dice': 5, 'hand': rollDice(5, 6), 'ex-palifico': false},
        'adam-2': {'dice': 5, 'hand': rollDice(5, 6), 'ex-palifico': false},
        'theo': {'dice': 5, 'hand': rollDice(5, 6), 'ex-palifico': false},
    });
    const [palifico, setPalifico] = useState(false); 
    */


    //// Setup variables

    // player is the human player's name
    const [player, setPlayer] = useState(null);
    // table is the list of players at the table - it will be the player, plus AI's
    const [table, setTable] = useState([]);
    // dicePerPlayer is the number of dice each player starts with
    const [dicePerPlayer, setDicePerPlayer] = useState(defaultDicePerPlayer);
    // sidesPerDie is the number of sides on each die
    const [sidesPerDie, setSidesPerDie] = useState(defaultSidesPerDie);
    // setupComplete is a boolean to determine if the game setup is complete
    const [setupComplete, setSetupComplete] = useState(false);


    //////// Game variables

    //// game state
    // gameID is the ID of the game in the backend
    const [gameID, setGameID] = useState({});
    // tableDict is the dictionary of players with how many dice they have left, their hands, and whether they're ex=palifico
    const [tableDict, setTableDict] = useState({});
    const tableDictRef = useRef(tableDict);
     

    //// round variables - specific to a round
    // roundHistory is the history of the round
    const [roundHistory, setRoundHistory] = useState([]);
    const roundHistoryRef = useRef(roundHistory);
    // palifico is a boolean to determine if the round is palifico
    const [palifico, setPalifico] = useState(false);
    // lastPlayer is the player who made the last bid
    const [lastPlayer, setLastPlayer] = useState(null);
    // lastBid is the last bid made 
    const [lastBid, setLastBid] = useState(null);
    // currentPlayer is the player whose turn it is
    const [currentPlayer, setCurrentPlayer] = useState(null);
    // currentBid is the current bid
    const [currentBid, setCurrentBid] = useState(null);   
    // roundLoser is the player who lost the round
    const [roundLoser, setRoundLoser] = useState(null);
    const roundLoserRef = useRef(roundLoser);
    // roundTotal is the total of the specific value that was lifted on
    const [roundTotal, setRoundTotal] = useState(null);

    //// display variables - variables governing what is displayed
    // displayLastPlayer is the player who made the last bid to be displayed
    const [displayLastPlayer, setDisplayLastPlayer] = useState(null);
    // displayLastBid is the last bid to be displayed
    const [displayLastBid, setDisplayLastBid] = useState(null);
    // displayCurrentPlayer is the player whose turn it is to be displayed
    const [displayCurrentPlayer, setDisplayCurrentPlayer] = useState(null);
    // displayCurrentBid is the current bid to be displayed
    const [displayCurrentBid, setDisplayCurrentBid] = useState(null);
    // showEndRound is a boolean to determine if the end round display should be shown
    const [showEndRound, setShowEndRound] = useState(false);
    


    /* To Setup the game in the backend */
    const handleSetup = async (player, dicePerPlayer, sidesPerDie, table) => {

        dicePerPlayer = parseInt(dicePerPlayer);
        sidesPerDie = parseInt(sidesPerDie);

        try {
            let response = await axios({
                method: 'post',
                url: '/games/initialize_game/',
                data: {
                    player: player,
                    dice_per_player: dicePerPlayer,
                    sides_per_die: sidesPerDie,
                    table: table
                }
            });

            let tempTableDict = {};

            table.forEach(player => {
                tempTableDict[player] = {
                    'dice': dicePerPlayer,
                    'hand': [],
                    'ex-palifico': false
                }
            }
            );

            setTableDict(tempTableDict);
            tableDictRef.current = tempTableDict;

            let startingPlayer = response.data.starting_player;

            setGameID(response.data.game_id);
            setCurrentPlayer(startingPlayer);
            console.log('starting player:', startingPlayer);

            // start the first round
            await handleStartRound(startingPlayer);
            setSetupComplete(true);
        } catch (error) {
            console.log('Error:', error);
            alert('Please refresh and try again.');
        }

    };

    // to handle AI bids returning from the backend
    const handleAIBids = async (response) => {

        // update the round history
        setRoundHistory(response.data.round_history);
        roundHistoryRef.current = response.data.round_history;

        console.log('roundHistory:', roundHistoryRef.current);

        // get the moves to display
        const moves = response.data.moves;

        // display all the AI moves
        await handleMoveDisplay(moves);
        console.log('moves displayed');

        // if the last move was a call, then end the round
        // wait for the display to finish
        if (moves[moves.length - 1][1] === 'call') {
            await handleEndRound();
            console.log('round ended');

            // then, show the end round display
            await handleEndRoundDisplay();
            console.log('end round displayed');

            handleRoundTransition();
            console.log('round transition');
        }
    };

    
    

    // To handle the human player's move 
    const handlePlayerMove = async (bid) => {

        // add the move to the round history
        setRoundHistory([...roundHistory, [player, bid]]);
        roundHistoryRef.current = [...roundHistory, [player, bid]];

        console.log('roundHistory:', roundHistoryRef.current);
        console.log('moved added to roundHistory:', [player, bid]);

        // if the player is calling, then end the round
        if (bid === 'call') {
            

            await handleMoveDisplay([[player, 'call']]);
            console.log('move displayed');

            await handleEndRound();
            console.log('round ended');
            console.log('roundLoser:', roundLoserRef.current);

            // then, show the end round display
            await handleEndRoundDisplay();
            console.log('end round displayed');
            console.log('roundLoser2: ', roundLoserRef.current);

            handleRoundTransition();
            console.log('round transition');

        } 
        // if they're bidding, send it to the backend
        else {
            try {
                let response = await axios({
                    method: 'post',
                    url: '/games/make_bid/',
                    data: {
                        player: player,
                        current_player: currentPlayer,
                        bid: bid,
                        round_history: roundHistoryRef.current,
                        table: table,
                        table_dict: tableDictRef.current,
                        palifico: palifico
                    }
                });

                handleAIBids(response);

                


            } catch (error) {
                alert('Error:', error);
                alert('Please refresh and try again.');
            }
    };
};

    /* to handle AI moves - for when they start a round */
    const handleAIMove = async (aiPlayer) => {

        try {
            let response = await axios({
                method: 'post',
                url: '/games/make_bid/',
                data: {
                    player: player,
                    current_player: aiPlayer,
                    bid: null,
                    round_history: roundHistoryRef.current,
                    table: table,
                    table_dict: tableDictRef.current,
                    palifico: palifico
                }
            });

            handleAIBids(response);

        } catch (error) {
            alert('Error:', error);
            alert('Please refresh and try again.');
        }




    };

    const handleMoveDisplay = async (moves) => {

        // iterate through moves, and display them

        for (const move of moves) {
            setDisplayCurrentPlayer(move[0]);

            setDisplayCurrentBid(move[1]);

            await sleep(1000);

            setDisplayLastPlayer(move[0]);

            setDisplayLastBid(move[1]);
        }

        // if the last move was not a call, then pass it back to the player
        if (moves[moves.length - 1][1] !== 'call') {
            setCurrentPlayer(player);
            setDisplayCurrentPlayer(player);
        }

        };
    
    const handleEndRoundDisplay = async () => {

        setDisplayCurrentPlayer(null);
        setShowEndRound(true);
        await sleep(3000);
        setShowEndRound(false);

    };

    // for displaying hands when someone calls
    const handleHandDisplay = async () => {


    }


    /* to handle starting a round */
    const handleStartRound = async (startingPlayer) => {

        console.log(player);

        // need to roll hands for everyone
        let tempTableDict = {...tableDictRef.current};
        for (const player in tempTableDict) {
            tempTableDict[player]['hand'] = rollDice(tempTableDict[player]['dice'], sidesPerDie);
        }
        setTableDict(tempTableDict);
        tableDictRef.current = tempTableDict;

        // setup the players
        setLastPlayer(null);
        setLastBid(null);

        setCurrentPlayer(startingPlayer);
        setCurrentBid(null);

        setDisplayCurrentPlayer(startingPlayer);
        setDisplayCurrentBid(null);
        setDisplayLastPlayer(null);
        setDisplayLastBid(null);

        // setup the round history
        setRoundHistory([]);
        roundHistoryRef.current = [];

        // setup the end round 
        setShowEndRound(false);
        setRoundLoser(null);
        setRoundTotal(null);

        // set palifico
        setPalifico(tableDictRef.current[startingPlayer]['dice'] === 1);

        console.log(startingPlayer);
        console.log(player);
        // if the starting player is an AI, then we need to get moves from the backend
        if (startingPlayer !== player) {
            handleAIMove(startingPlayer);
        }

    };

    /* to handle transitioning between rounds */
    const handleRoundTransition = () => {

        // TEST OUT THIS END GAME BEHAVIOR - MAKE SURE IT WORKS
        // see if the game is over
        if (Object.keys(tableDictRef.current).length === 1) {
            alert('Game over! The winner is:', Object.keys(tableDictRef.current)[0]);
        }
        else {
            // figure out who's starting the next round
            // if the loser is still in the game, then they start the next round
            // otherwise, the next player (still in the game) starts the next round

            let loser = roundLoserRef.current;

            while (!(loser in tableDictRef.current)) {
                let index = table.indexOf(loser);
                loser = table[(index + 1) % table.length];
            }
            // start the next round
            handleStartRound(loser);
        }


    };

    /* to handle ending a round */
    const handleEndRound = async () => {

        // first, send data to the backend to handle ending the round
        try {
            let response = await axios({
                method: 'post',
                url: '/games/end_round/',
                data: {
                    round_history: roundHistoryRef.current,
                    table_dict: tableDictRef.current,
                    palifico: palifico,
                    game_id: gameID
                }
            });

            const loser = response.data.loser;

            console.log('loser returned from backend', loser);

            setRoundLoser(loser);
            roundLoserRef.current = loser;
            setRoundTotal(response.data.total);

            // update the tableDict
            // remove 1 die from the loser
            let tempTableDict = {...tableDictRef.current};
            tempTableDict[loser]['dice'] -= 1;

            // if the loser has one die left, then set ex-palifico to true
            if (tempTableDict[loser]['dice'] === 1) {
                tempTableDict[loser]['ex-palifico'] = true;
            }

            // if the loser has no dice left, then remove them from the table
            if (tempTableDict[loser]['dice'] === 0) {
                delete tempTableDict[loser];
            }

            setTableDict(tempTableDict);
            tableDictRef.current = tempTableDict;


        } catch (error) {
            alert('Error:', error);
            alert('Please refresh and try again.');
        }


    };



    const test = () => {
        // display all the variables
        console.log('player:', player);
        console.log('table:', table);
        console.log('dicePerPlayer:', dicePerPlayer);
        console.log('sidesPerDie:', sidesPerDie);
        console.log('setupComplete:', setupComplete);
        console.log('gameID:', gameID);
        console.log('tableDict:', tableDictRef.current);
        console.log('currentPlayer:', currentPlayer);
        console.log('lastPlayer:', lastPlayer);
        console.log('lastBid:', lastBid);
        console.log('currentBid:', currentBid);
        console.log('displayLastPlayer:', displayLastPlayer);
        console.log('displayLastBid:', displayLastBid);
        console.log('displayCurrentPlayer:', displayCurrentPlayer);
        console.log('displayCurrentBid:', displayCurrentBid);
        console.log('roundHistory:', roundHistory);
        console.log('showEndRound:', showEndRound);
        console.log('roundLoser:', roundLoser);
        console.log('roundTotal:', roundTotal);
        console.log('palifico:', palifico);
    }

    return (
        <div>
            <h1>Play</h1>

            {/* First, setup the game */}
            {setupComplete === false && (
                <Setup
                    player={player}
                    dicePerPlayer={dicePerPlayer}
                    sidesPerDie={defaultSidesPerDie}
                    table={table}
                    onSave={(player, dicePerPlayer, sidesPerDie, table) => {
                        setPlayer(player);
                        setTable(table);
                        setDicePerPlayer(dicePerPlayer);
                        setSidesPerDie(sidesPerDie);
                        handleSetup(player, dicePerPlayer, sidesPerDie, table);
                    }
                    }
                />
            )}

            {/* Then, play the game */}
            {setupComplete === true && (
            <div>
                {table.map((tablePlayer) => {

                    {if (tablePlayer === displayCurrentPlayer) {
                        if (tablePlayer === player) {
                            return (
                                <div>
                                    <h3>(current) {tablePlayer}: </h3>
                                    <h3>Your hand: {tableDictRef.current[tablePlayer]['hand']}</h3>
                                    <PlayerBid 
                                    tableDict={tableDictRef.current}
                                    sidesPerDie={sidesPerDie}
                                    palifico={palifico}
                                    roundHistory={roundHistory}
                                    currentPlayer={tablePlayer}
                                    onSave={(move) => {
                                        handlePlayerMove(move);
                                    }}
                                    />
                                </div>
                            )
                        } else if (displayCurrentBid) {
                            if (displayCurrentBid === 'call') {
                                return (
                                    <div>
                                        <h3>(current) {tablePlayer}: {displayCurrentBid} </h3>
                                    </div>
                                )
                            }
                            else {
                                return (
                                    <div>
                                        <h3>(current) {tablePlayer}: ({displayCurrentBid[0]}, {displayCurrentBid[1]}) </h3>
                                    </div>
                                )
                            }
                            
                        }
                        else {
                            return (
                                <div>
                                    <h3>(current) {tablePlayer}: </h3>
                                </div>
                            )
                
                        }
                        
                     // if tablePlayer is before currentPlayer, then also display their move
                    } else if (tablePlayer === displayLastPlayer) {
                        return (
                            <div>
                                <h3>{tablePlayer}: ({displayLastBid[0]}, {displayLastBid[1]}) </h3>
                            </div>
                        )

                    }
                    else {
                        return (
                            <div>
                                <h3>{tablePlayer}: </h3>
                            </div>
                        )
                        
                    }
                    }
                }
                )}

                {showEndRound && (
                    <div>
                        <h3>Round over!</h3>
                        <h3>{roundLoserRef.current} lost the round. There were {roundTotal[0]} {roundTotal[1]}'s.</h3>
                    </div>
                )}  

                <Button onClick={() => test()}>test</Button>

            </div>
            )}
            


        </div>
    )};

export default Play;

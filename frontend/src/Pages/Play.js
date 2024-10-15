import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { BASE_URL } from '../interceptors';

import Setup from './GamePages/Setup';
import Game from './GamePages/Game';

import { apiCall } from '../api';


axios.defaults.baseURL = BASE_URL;



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

    const [player, setPlayer] = useState(null); // the player's name
    const [table, setTable] = useState([]); // the table of players
    const [dicePerPlayer, setDicePerPlayer] = useState(null); // the number of dice per player
    const [sidesPerDie, setSidesPerDie] = useState(null); // the number of sides per die

    const [setupComplete, setSetupComplete] = useState(false); // whether the game setup is complete


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

        // backend call to initialize the game
        const [initializeSuccess, initializeResp] = await apiCall({
            method: 'post',
            url: '/games/initialize_game/',
            data: {
                player: player,
                dice_per_player: dicePerPlayer,
                sides_per_die: sidesPerDie,
                table: table
            }
        });

        if (!initializeSuccess) {
            alert(initializeResp.data);
            return;
        }


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

        let startingPlayer = initializeResp.data.starting_player;

        setGameID(initializeResp.data.game_id);
        setCurrentPlayer(startingPlayer);
        console.log('starting player:', startingPlayer);

        setSetupComplete(true);

    };

    

    return (
        <div>
            <h1>Play</h1>

            {/* First, setup the game */}
            {!setupComplete && (
                <Setup
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
            {setupComplete && (
                <Game 
                player={player}
                table={table}
                sidesPerDie={sidesPerDie}
                />
            
            )}
            


        </div>
    )};

export default Play;

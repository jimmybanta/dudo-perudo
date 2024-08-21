import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Input, Button } from 'reactstrap';
import { BASE_URL } from '../interceptors';

import Setup from './GamePages/Setup';

axios.defaults.baseURL = BASE_URL;

const defaultDicePerPlayer = 5;

const Play = () => {

    /* Setup variables */
    /* player is the human player's name */
    const [player, setPlayer] = useState(null);
    /* table is the list of players at the table - it will be the player, plus AI's */
    const [table, setTable] = useState([]);
    const [dicePerPlayer, setDicePerPlayer] = useState(defaultDicePerPlayer);

    const [setupComplete, setSetupComplete] = useState(false);

    /* Game variables */
    const [tableDict, setTableDict] = useState({});
    const [startingPlayer, setStartingPlayer] = useState(null);

    /* To Setup the game in the backend */
    const handleSetup = async (player, dicePerPlayer, table) => {

        try {
            let response = await axios({
                method: 'post',
                url: '/games/initialize_game/',
                data: {
                    player: player,
                    dice_per_player: dicePerPlayer,
                    table: table
                }
            });
            /* if it sets up correctly, then set the tableDict and setSetupComplete to true */

            let tempTableDict = {};

            table.forEach(player => {
                tempTableDict[player] = dicePerPlayer;
            }
            );

            setTableDict(tempTableDict);

            setSetupComplete(true);
        } catch (error) {
            alert('Error:', error);
            alert('Please refresh and try again.');
        }




    };

    return (
        <div>
            <h1>Play</h1>

            {/* First, setup the game */}
            {setupComplete === false && (
                <Setup
                    player={player}
                    dicePerPlayer={dicePerPlayer}
                    table={table}
                    onSave={(player, dicePerPlayer, table) => {
                        setPlayer(player);
                        setTable(table);
                        setDicePerPlayer(dicePerPlayer);
                        handleSetup(player, dicePerPlayer, table);
                    }
                    }
                />
            )}

            {/* Then, play the game */}
            {setupComplete === true && (
                <div>
                    <h2>Game is set up!</h2>
                    <h3>Player: {player}</h3>
                    <h3>Table: {table}</h3>
                    <h3>Dice per player: {dicePerPlayer}</h3>
                </div>
            )}


        </div>
    )};

export default Play;

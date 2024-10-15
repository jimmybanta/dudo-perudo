import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Input, Button } from 'reactstrap';
import { BASE_URL } from '../../interceptors';

import { apiCall } from '../../api';

axios.defaults.baseURL = BASE_URL;

const defaultDicePerPlayer = 5;
const defaultSidesPerDie = 6;




const Setup = ({ onSave }) => {
    // component that sets up the game


    const [player, setPlayer] = useState(null); // the player's name
    const [dicePerPlayer, setDicePerPlayer] = useState(defaultDicePerPlayer); // the number of dice per player
    const [sidesPerDie, setSidesPerDie] = useState(defaultSidesPerDie); // the number of sides per die
    const [table, setTable] = useState([]); // the table of players

    const [characters, setCharacters] = useState([]); // the characters to choose from


    // get the characters
    useEffect(() => {

        const fetchCharacters = async () => {

            const [charactersSuccess, charactersResp] = await apiCall({
                method: 'get',
                url: '/games/api/characters/',
            });

            if (!charactersSuccess) {
                alert(charactersResp.data);
                return;
            }

            setCharacters(charactersResp);
        };

        // load in the characters
        fetchCharacters();
    }, []);

    const handleSetTablePlayers = (name) => {

        let newTable = [...table];

        let playerDict = {};

        /* first, check that the human is the first player */
        if (newTable[0] !== player) {
            /* remove the human from the list */
            newTable = newTable.filter(member => member !== player);
            console.log(newTable);
            /* add the human back to the front of the list */
            newTable.unshift(player);
        }

        /* then, check to see how many of that player are already on the table */
        newTable.forEach(player => {

            let baseName = player.split('-')[0];

            if (baseName in playerDict) {
                playerDict[baseName] += 1;
            } else {
                playerDict[baseName] = 1;
            }
        }
        );

        /* update the new player's name, if they're already on the table */
        if (name in playerDict) {
            name = name + '-' + (playerDict[name] + 1);
        }
        
        /* then, add the new player to the list */
        newTable = [...newTable, name];

        setTable(newTable);
    };

    return (
        <div>
            {/* First, get the player's name */}
            {player === null && (
                <div>
                    <Input
                        type='text'
                        placeholder='enter your name'
                        onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                                setPlayer(e.target.value);
                                setTable([e.target.value]);
                            }
                        }}
                    />
                </div>
            )}

            {/* Then, welcome the player and set up the table */}
            {player !== null && (
                <div>
                    <h2>Welcome, {player}!</h2>
                    <div className='container'>
                        <h3>Dice per player:</h3>
                        <Input
                            type='number'
                            value={dicePerPlayer}
                            onChange={(e) => {
                                setDicePerPlayer(e.target.value);
                            }}
                        />
                        
                    </div>
                    <div className='container'>
                        <h3>Sides per die:</h3>
                        <Input
                            type='number'
                            value={sidesPerDie}
                            onChange={(e) => {
                                setSidesPerDie(e.target.value);
                            }}
                        />
                    </div>
                    <h2>Craft your table</h2>
                    <div className='container'>
                        <div className='row'>
                            {characters.map((character) => (
                                <div className='col-4' key={character.id}>
                                    <Button
                                        onClick={() => {
                                            handleSetTablePlayers(character.name);
                                        }}
                                    >
                                        {character.name}
                                    </Button>
                                </div>
                            ))}
                        </div>
                        <div className='row'>
                            <h2>Table:</h2>
                                {table.map((player, i) => (
                                    <div className='col-4' key={i}>
                                        <div>
                                            <p>{i + 1}: {player}</p>
                                        </div>
                                    </div>
                                ))}
                        </div>
                        <div className='row'>
                                <Button
                                    onClick={() => onSave(player, dicePerPlayer, sidesPerDie, table)}
                                >
                                    Let's play some fuckin perudo!
                                </Button>
                        </div>
                    </div>
                </div>
        )}
        </div>
    )};

export default Setup;

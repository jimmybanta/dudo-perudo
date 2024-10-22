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

    const [stage, setStage] = useState('player'); // the stage of the setup


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

            console.log(charactersResp);

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
        <div
        className='container flex-column'
        style={{
            width: '100%',
            height: '100%',
        }}>
            {/* First, get the player's name */}
            {stage === 'player' && (
                <div className='container flex-column' style={{ width: '75%', margin: '3%' }}>
                    <h1 className='text setup-input-header'>what's your name?</h1>
                    <input
                        className='setup-input'
                        type='text'
                        placeholder=''
                        value={player}
                        onChange={(e) => setPlayer(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                setTable([player]);
                                setStage('table');
                            }}}
                    />
                </div>
            )}

            {/* Then, welcome the player and set up the table */}
            {stage === 'table' && (
                <div
                className='container flex-column'
                style={{
                    width: '80%',
                }}>
                    <h1 className='text setup-input-header'>craft your table, {player}</h1>

                    <div className='container flex-row'
                    style={{
                        width: '100%',
                        height: '300px',
                    }}
                    >

                        <div className='container flex-column setup-char-table' style={{ 
                            
                            border: '1px solid white'
                             }}>
                                <div className='setup-header'>Characters</div>
                                {characters.map((character) => (
                                <div key={character.id}>
                                    <div className='container flex-row setup-char' 
                                    onClick={() => handleSetTablePlayers(character.name)}>
                                        <div
                                        className='setup-char-name'
                                        >{character.name}</div>
                                        <div
                                        className='setup-char-description'
                                        >{character.description}</div>
                                    </div>
                                </div>
                            ))}

                        </div>

                        <div className='container flex-column setup-char-table' 
                        style={{ 
                             }}>
                                <div className='setup-header'>Table</div>
                                {table.map((player, i) => (
                                    <div className='col-4' key={i}>
                                        <div>
                                            <p>{i + 1}: {player}</p>
                                        </div>
                                    </div>
                                ))}

                        </div>

                    </div>

                    <div className='container flex-row'
                    style={{
                        width: '100%',

                    }}
                    >

                        <div className='container flex-column' style={{ 
                            width: '50%',
                             }}>
                                <h3>Dice per player:</h3>
                        <Input
                            type='number'
                            value={dicePerPlayer}
                            onChange={(e) => {
                                setDicePerPlayer(e.target.value);
                            }}
                        />

                        </div>

                        <div className='container flex-column' style={{ 
                            width: '50%' }}>
                                <h3>Sides per die:</h3>
                        <Input
                            type='number'
                            value={sidesPerDie}
                            onChange={(e) => {
                                setSidesPerDie(e.target.value);
                            }}
                        />

                        </div>

                    </div>
                    
                    <div className='container'>
                        <Button
                            onClick={() => onSave(player, dicePerPlayer, sidesPerDie, table)}
                        >
                            Let's play some fuckin perudo!
                        </Button>
                    </div>
                </div>
        )}
        </div>
    )};

export default Setup;

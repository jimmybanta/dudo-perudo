import React, { useState, useEffect, useRef } from 'react';
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

    const handleRemoveTablePlayer = (name) => {


        // can't delete the human
        if (name === player) {
            return;
        };

        // first, remove the player from the table
        let newTable = [...table];
        newTable = newTable.filter(player => player !== name);


        let finalTable = [];

        // then go through and add the players, keeping numbers correct
        newTable.forEach(player => {

            let baseName = player.split('-')[0];

            let newName = baseName;

            let i = 2;

            while (finalTable.includes(newName)) {
                newName = baseName + '-' + i;

                i += 1;
            }

            finalTable.push(newName);
        });


        setTable(finalTable);
    };

    const handleSave = () => {
        onSave(player, dicePerPlayer, sidesPerDie, table);
    }


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
                    height: '100%',
                    //border: '1px solid blue',
                }}>
                    <div 
                    className='text setup-input-header'
                    style={{
                        marginBottom: '40px',
                    }}
                    >craft your table, {player}</div>

                    <div className='container flex-row setup-char-table-container'
                    style={{
                        //border: '1px solid red'
                    }}
                    >


                        <div 
                        className='setup-char-table' 
                        style={{ 
                            //border: '1px solid white',
                            width: '60%',
                            
                             }}>
                                <div className='setup-header'>Characters</div>

                                {characters.map((character) => (

                                    <div 
                                    key={character.id}
                                    className='container flex-row setup-char character-press' 
                                    style={{
                                        width: '100%',
                                        //border: '1px solid white',
                                        margin: 'auto'
                                    }}
                                    onClick={() => handleSetTablePlayers(character.name)}>

                                        <div
                                        className='setup-char-name'
                                        style={{width: '25%',
                                            textAlign: 'left',
                                        }}
                                        >{character.name}</div>

                                        <div
                                        style={{width: '75%',
                                            textAlign: 'left',
                                        }}
                                        className='setup-char-description'
                                        >{character.description}</div>

                                    </div>
                            ))}
                            

                        </div>

                        <div className='setup-char-table' 
                        style={{ 
                            //border: '1px solid white',
                            alignItems: 'flex-start',
                            width: '40%',
                             }}>

                                <div className='setup-header'>Table</div>

                                {table.map((player, i) => (

                                    <div 
                                    key={i}
                                    className='container flex-row setup-char table-press'  
                                    style={{
                                        width: '100%',
                                        //border: '1px solid white',
                                    }}
                                    onClick={() => handleRemoveTablePlayer(player)}
                                    >

                                        <div
                                        className='setup-char-name'
                                        style={{width: '10%',
                                            textAlign: 'left',
                                        }}
                                        >{i + 1}</div>

                                        <div
                                        style={{width: '90%',
                                            textAlign: 'left',
                                        }}
                                        className='setup-char-description'
                                        >{player}</div>

                                    </div>

                                ))}

                        </div>

                    </div>

                    <div 
                    className='button home-button text lets-play-button' 
                    style={{
                        marginTop: '50px',
                    }}
                    onClick={() => handleSave()}
                    >
                        let's play
                    </div>

                    {/* <div className='container flex-row'
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

                    </div> */}
                    
                    {/* <div className='container'>
                        <Button
                            onClick={() => onSave(player, dicePerPlayer, sidesPerDie, table)}
                        >
                            Let's play some fuckin perudo!
                        </Button>
                    </div> */}
                </div>
        )}
        </div>
    )};

export default Setup;

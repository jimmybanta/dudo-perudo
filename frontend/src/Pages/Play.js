import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { BASE_URL } from '../interceptors';

import Setup from './GamePages/Setup';
import Game from './GamePages/Game';
import HelpPopup from './GamePages/Components/HelpPopup';

import { apiCall } from '../api';

import { rollDice } from '../utils';


axios.defaults.baseURL = BASE_URL;

const cupOptions = [1, 2, 3, 4, 5, 6]; // the ids of cup images that are currently available



const Play = ({ onSetCurrentPage }) => {

    /* 
    // temp setup
    const [dicePerPlayer, setDicePerPlayer] = useState(5);
    const [player, setPlayer] = useState('crespin');
    const [gameID, setGameID] = useState(59);
    const [table, setTable] = useState(['crespin', 'riyaaz', 'jimmy',
        'adam', 'adam-2', 'theo',
        ]);
    const [tableDict, setTableDict] = useState({
        'crespin': {'dice': dicePerPlayer, 'hand': rollDice(dicePerPlayer, 6), 'ex-palifico': false},
        'riyaaz': {'dice': dicePerPlayer, 'hand': rollDice(dicePerPlayer, 6), 'ex-palifico': false},
        'jimmy': {'dice': dicePerPlayer, 'hand': rollDice(dicePerPlayer, 6), 'ex-palifico': false},
        'adam': {'dice': dicePerPlayer, 'hand': rollDice(dicePerPlayer, 6), 'ex-palifico': false},
        'adam-2': {'dice': dicePerPlayer, 'hand': rollDice(dicePerPlayer, 6), 'ex-palifico': false},
        'theo': {'dice': dicePerPlayer, 'hand': rollDice(dicePerPlayer, 6), 'ex-palifico': false},
    });
    const [currentPlayer, setCurrentPlayer] = useState('crespin');
    const [sidesPerDie, setSidesPerDie] = useState(6);
    const [cups, setCups] = useState({
        'crespin': 1,
        'riyaaz': 2,
        'jimmy': 3,
        'adam': 4,
        'adam-2': 5,
        'theo': 6,
    });
    const [showDice, setShowDice] = useState({
        'crespin': false,
        'riyaaz': false,
        'jimmy': false,
        'adam': false,
        'adam-2': false,
        'theo': false,
    });
    const [setupComplete, setSetupComplete] = useState(true); 
    */


    //// Setup variables

    const [player, setPlayer] = useState(null); // the player's name
    const [table, setTable] = useState([]); // the table of players
    const [dicePerPlayer, setDicePerPlayer] = useState(null); // the number of dice per player
    const [sidesPerDie, setSidesPerDie] = useState(null); // the number of sides per die
    const [cups, setCups] = useState({}); // a dictionary mapping each player to their cup number (for image rendering)
    const [showDice, setShowDice] = useState({}); // a dictionary mapping each player to whether their dice should be shown

    const [setupComplete, setSetupComplete] = useState(false); // whether the game setup is complete


    //////// Game variables

    //// game state
    // gameID is the ID of the game in the backend
    const [gameID, setGameID] = useState({});
    // tableDict is the dictionary of players with how many dice they have left, their hands, and whether they're ex-palifico
    const [tableDict, setTableDict] = useState({});

    // currentPlayer is the player whose turn it is
    const [currentPlayer, setCurrentPlayer] = useState(null);

    //// help popup
    const [helpPopup, setHelpPopup] = useState(false); // if the help popup is open
    const [helpPopupFadeClass, setHelpPopupFadeClass] = useState('help-popup-in'); // class for fading the help popup
    


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
            alert(initializeResp);
            return;
        }


        let tempTableDict = {};

        table.forEach(player => {
            tempTableDict[player] = {
                'dice': dicePerPlayer,
                'hand': rollDice(dicePerPlayer, sidesPerDie),
                'ex-palifico': false
            }
        }
        );

        setTableDict(tempTableDict);

        let startingPlayer = initializeResp.starting_player;

        setGameID(initializeResp.game_id);
        setCurrentPlayer(startingPlayer);

        // set the cups
        let tempCups = [...cupOptions];
        // shuffle tempcups
        tempCups.sort(() => Math.random() - 0.5);
        let tempCupsDict = {};

        table.forEach(player => {

            // if we've run out of cups, then start over
            if (tempCups.length === 0) {
                tempCups = [...cupOptions];
                // shuffle tempcups
                tempCups.sort(() => Math.random() - 0.5);
            }

            tempCupsDict[player] = tempCups.pop();
        }
        )
        setCups(tempCupsDict);

        // set the showDice dict
        let tempShowDice = {};

        table.forEach(player => {
            tempShowDice[player] = false;
        });
        setShowDice(tempShowDice);


        setSetupComplete(true);

    };

    // handle clicking on the help button
    const handleHelpClick = (e) => {
        // params:
        // e: the event

        // prevent the event from bubbling up
        e.stopPropagation();

        // if it's oopen, then fade it out
        if (helpPopup) {
            setHelpPopupFadeClass('help-popup-out');
            // wait for the popup to fade out
            setTimeout(() => {
                setHelpPopup(false);
            }, 500);
        }
        // if it's closed, then fade it in
        else {
            setHelpPopupFadeClass('help-popup-in');
            setHelpPopup(true);
        }


    };

    

    return (
        <div
        className='container flex-column'
        style={{
            width: '100%',
            height: '100%',
        }}>

            {/* First, setup the game */}
            {!setupComplete && (
                <div
                className='container flex-column'
                style={{
                    width: '100%',
                    height: '100%',
                }}>
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
                <div 
                className='button home-button text back-button' 
                style={{
                    marginTop: '50px',
                }}
                onClick={() => onSetCurrentPage('Home')}>
                    back
                </div>
                </div>
            )}

            {/* Then, play the game */}
            {setupComplete && (
                <Game 
                    player={player}
                    gameID={gameID}
                    table={table}
                    playTableDict={tableDict}
                    playCurrentPlayer={currentPlayer}
                    sidesPerDie={sidesPerDie}
                    cups={cups}
                    playShowDice={showDice}
                />
            
            )}

            {/* render the help button */}
            <div 
                className='help-button text help'
                onClick={(e) => handleHelpClick(e)}
            >
                ?
            </div>

            {/* render the help popup */}
            {helpPopup && 
                <HelpPopup
                fadeClass={helpPopupFadeClass}
                page={ setupComplete ? 'game' : 'setup' } />
            }

            
            


        </div>
    )};

export default Play;

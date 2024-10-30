
import React, { useState, useRef, useEffect, } from 'react';
import axios from 'axios';

import PlayerBid from './Components/PlayerBid';
import Chat from './Components/Chat';
import Header from './Components/Header';

import { apiCall } from '../../api';
import { rollDice, sleep } from '../../utils'; 


const Game = ({ player, gameID, table, playTableDict, playCurrentPlayer, sidesPerDie, cups, playShowDice }) => {

    // game state
    const [tableDict, setTableDict] = useState(playTableDict); // dictionary of players with dice, hands, ex-palifico
    
    const [currentPlayer, setCurrentPlayer] = useState(playCurrentPlayer); // the current player

    const [gameHistory, setGameHistory] = useState([]); // the history of the game
    const [roundHistory, setRoundHistory] = useState([]); // the history of the round

    const [palifico, setPalifico] = useState(false); // whether the round is palifico
    
    // end round state
    const [roundEnd, setRoundEnd] = useState(false); // whether we're at the end of a round
    const [roundLoser, setRoundLoser] = useState(null); // the loser of the round
    const [roundTotal, setRoundTotal] = useState(null); // the total of the specific value that was lifted on

    const [showDice, setShowDice] = useState(playShowDice); // a dictionary to decide 

    const [playerOut, setPlayerOut] = useState(null); // the latest player out of the game

    // refs
    const tableDictRef = useRef(tableDict);
    useEffect(() => { tableDictRef.current = tableDict; }, [tableDict]);

    // whenever currentPlayer changes
    useEffect(() => {

        const handleAIMove = async () => {

            const [moveSuccess, moveResp] = await apiCall({
                method: 'post',
                url: '/games/get_move/',
                data: {
                    current_player: currentPlayer,
                    round_history: roundHistory,
                    game_history: gameHistory,
                    table_dict: tableDict,
                    palifico: palifico
                }
            });

            if (!moveSuccess) {
                alert(moveResp);
                return;
            }

            const move = moveResp.move;
            const pause = moveResp.pause;

            // wait the pause time
            // before making the move
            setTimeout(() => {

                if (move == 'call') {
                    
                    handleCall();

                }
                else {
                    // add the move to the round history
                    setRoundHistory([...roundHistory, [currentPlayer, move]]);

                    // advance to the next player
                    advancePlayer();
                }

            }
            , pause);
        };

        if (currentPlayer === null || currentPlayer === 'nobody') {
            return;
        }

        if (currentPlayer !== player) {
            handleAIMove();
        }


    }, [currentPlayer]);


    // given a bid, determines if it's correct (true) or incorrect (false)
    const scoreBid = (bid) => {

        let [quantity, value] = bid;

        let total = 0;

        const allDice = Object.values(tableDict).map(player => player['hand']).flat();

        if (palifico) {
            total += allDice.filter(die => die === value).length;
        }
        else if (value === 1) {
            total += allDice.filter(die => die === value).length;
        }
        else {
            total += allDice.filter(die => die === value).length;
            total += allDice.filter(die => die === 1).length;

        }

        // return whether the bid was correct, and the total number of dice of the bid value
        return [quantity <= total, [total, value]];


        /* for (const player in tableDict) {



            total += tableDict[player]['hand'].filter(die => die === value).length;

            // if this isn't palifico, then add the 1's
            if (!palifico) {
                total += tableDict[player]['hand'].filter(die => die === 1).length;
            }
        } */

        //return count <= total

    };

    // uses the round history to get the last player and their bid
    const getLastPlayerBid = () => {

        if (roundHistory.length === 0) {
            return [null, null];
        }
        if (roundHistory[roundHistory.length - 1][1] === 'call') {
            return roundHistory[roundHistory.length - 2];
        }

        return roundHistory[roundHistory.length - 1];

    };

    // advances to the next player who is still in the game
    const advancePlayer = () => {

        let index = table.indexOf(currentPlayer);

        let nextPlayer = table[(index + 1) % table.length];

        while (tableDict[nextPlayer]['dice'] === 0) {
            index = table.indexOf(nextPlayer);
            nextPlayer = table[(index + 1) % table.length];
        }

        setCurrentPlayer(nextPlayer);

    };

    // checks if the game is over
    const checkEndGame = () => {

        // see how many players with dice are left
        let playersLeft = 0;

        for (const player in tableDict) {
            if (tableDict[player]['dice'] > 0) {
                playersLeft += 1;
            }
        }

        return playersLeft === 1;
    };
        
    // To handle the player's move 
    const handlePlayerMove = async (bid) => {

        // if the player is calling, then end the round
        if (bid === 'call') {

            handleCall();

        } 
        // if they're bidding, then add the move to the round history and advance to the next player
        else {


            // add the move to the round history
            setRoundHistory([...roundHistory, [currentPlayer, bid]]);

            // advance to the next player
            advancePlayer();

    };
    };

    // handles a player (user or AI) calling
    // thus ending a round
    const handleCall = async () => {

        // starting at the current player, go around the table and show all the dice
        const callingPlayer = currentPlayer;
 
        // reorganize the table so that the current player is first
        let tempTable = [...table];
        tempTable = tempTable.slice(table.indexOf(callingPlayer)).concat(tempTable.slice(0, table.indexOf(callingPlayer)));

        let shown = [];

        // get the last player and their bid
        const [lastPlayer, lastBid] = getLastPlayerBid();

        // add the call to the round history
        const newRoundHistory = [...roundHistory, [callingPlayer, 'call']];
        setRoundHistory(newRoundHistory);

        setRoundEnd(true);

        // update the total of the relevant number
        let runningTotal = 0;

        const showDice = async () => {

            // one by one show the dice
            for (let index = 0; index < tempTable.length; index++) {

                // wait a bit extra for the second person
                if (index === 1) {
                    await sleep(500);
                }

                let player = tempTable[index];

                // if the player is out of the game, skip them
                if (tableDict[player]['dice'] === 0) {
                    continue;
                }

                let tempShowDice = {...showDice};
                tempShowDice[player] = true;

                shown.forEach(shownPlayer => {
                    tempShowDice[shownPlayer] = true;
                });
                setShowDice(tempShowDice);

                let hand = tableDict[player]['hand'];

                if (palifico) {
                    runningTotal += hand.filter(die => die === lastBid[1]).length;
                }
                else if (lastBid[1] === 1) {
                    runningTotal += hand.filter(die => die === lastBid[1]).length;
                }
                else {
                    runningTotal += hand.filter(die => die === lastBid[1]).length;
                    runningTotal += hand.filter(die => die === 1).length;
                }

                setRoundTotal(runningTotal);

                shown.push(player);

                // wait a random amount of time between .75 and 1.5 seconds
                let waitTime = Math.random() * 750 + 500;
                await sleep(waitTime);
        }};

        
        await showDice();

        setCurrentPlayer(null);

        // score the bid
        const [correct, total] = scoreBid(lastBid);

        // determine the loser
        const loser = correct ? currentPlayer : lastPlayer;

        // determine if the loser is out
        if (tableDict[loser]['dice'] === 1) {
            setPlayerOut(loser);
        }

        // clear the shown dice
        let tempShowDice = {...showDice};
        for (const player in tempShowDice) {
            tempShowDice[player] = false;
        }
        setShowDice(tempShowDice);

        setRoundLoser(loser);

        // update the round in the backend 
        //// currently not doing this - no need to store game histories in the database for now, I don't think
        /* apiCall({
            method: 'post',
            url: '/games/end_round/',
            data: {
                round_history: newRoundHistory,
                table_dict: tableDict,
                palifico: palifico,
                loser: loser,
                total: total,
                game_id: gameID
            }
        }); */

        // wait a bit before transitioning to the next round
        await sleep(2000);

        // end the round and transition to the next one (if there is one)
        handleRoundTransition(loser, total, newRoundHistory);

    };

    // to handle transitioning between rounds
    const handleRoundTransition = async (loser, total, newRoundHistory) => {

        setRoundEnd(false);

        // reset palifico
        setPalifico(false);

        // get a dict of all the round info and add it to the game history
        let roundDict = {
            tableDict: tableDict,
            roundHistory: newRoundHistory,
            palifico: palifico,
            roundLoser: loser,
            roundTotal: total
        }
        setGameHistory([...gameHistory, roundDict]);

        // update the tableDict
        // remove 1 die from the loser
        let tempTableDict = {...tableDict};
        tempTableDict[loser]['dice'] -= 1;

        // if the loser has one die left, then set ex-palifico to true
        // and set palifico to true
        if (tempTableDict[loser]['dice'] === 1) {

            // but check - if there are only 2 people left, we don't do palifico
            let playersLeft = 0;
            for (const player in tempTableDict) {
                if (tempTableDict[player]['dice'] > 0) {
                    playersLeft += 1;
                }
            }

            if (playersLeft > 2) {
                tempTableDict[loser]['ex-palifico'] = true;
                setPalifico(true);
            }
        }

        // then, check if the game is over
        if (checkEndGame()) {
            alert('Game over!');
            return;
        };

        // if it's not, then continue onto next round

        // need to roll hands for everyone
        for (const player in tempTableDict) {
            tempTableDict[player]['hand'] = rollDice(tempTableDict[player]['dice'], sidesPerDie);
        }
        setTableDict(tempTableDict);

        // then, reset the round state
        setRoundHistory([]);
        setRoundLoser(null);
        setRoundTotal(null);

        // then, determine the starting player for the next round
        let startingPlayer = loser;
            
        // if the loser is no longer in the game, we need to advance to the next player in the game
        while (tempTableDict[startingPlayer]['dice'] === 0) {
            let index = table.indexOf(startingPlayer);
            startingPlayer = table[(index + 1) % table.length];
        }

        // this will trigger the start of a new round
        setCurrentPlayer(startingPlayer);

    };

    // formats a move to be displayed
    const formatMove = (move) => {

        if (move === 'call') {
            return 'lift!';
        }

        const [quantity, value] = move;

        let singular = false;

        if (parseInt(quantity) === 1) {
            singular = true;
        }

        const valueDict = {
            1: singular ? (palifico ? 'one' : 'jessie') : (palifico ? 'ones' : 'jessies'),
            2: singular ? 'two' : 'twos',
            3: singular ? 'three' : 'threes',
            4: singular ? 'four' : 'fours',
            5: singular ? 'five' : 'fives',
            6: singular ? 'six' : 'sixes',
        }

        return `${quantity} ${valueDict[value]}`;
    };
    

    // renders the table
    const renderTable = () => {


        let vw = document.documentElement.clientWidth;
        let vh = document.documentElement.clientHeight;

        const centerX = (vw < 768) ? (vw / 2) : ((vw / 10) * 3);
        const centerY = (vw < 768) ? ((vh / 10) * 3) : (vh / 2);


        const radius = (vw < 768) ? ((vw / 2)) : Math.min(vh / 2, 300);

        let innerRadius = 0;
        let middleRadius = 0;
        let outerRadius = 0;

        if (vw < 768) {
            innerRadius = radius * 0.4;
            middleRadius = radius * 0.65;
            outerRadius = radius * 0.92;
        }
        else {
            innerRadius = radius * 0.5;
            middleRadius = radius * 0.9;
            outerRadius = radius * 1.2;
        }


        // inner will hold the cups/hands
        // middle will hold the player names
        // outer will hold the player moves/thinking
        
        const angleStep = (2 * Math.PI) / table.length;
        

        return (
            table.map((tablePlayer, index) => {

                let angle = angleStep * index + (Math.PI / 2);

                const innerX = centerX + (innerRadius * Math.cos(angle));
                const innerY = centerY + (innerRadius * Math.sin(angle));

                const middleX = centerX + (middleRadius * Math.cos(angle));
                const middleY = centerY + (middleRadius * Math.sin(angle));

                const outerX = centerX + (outerRadius * Math.cos(angle));
                const outerY = centerY + (outerRadius * Math.sin(angle));

                // rendering the current player
                {if (tablePlayer === currentPlayer) {
                    // if the current Player is the user
                    if (tablePlayer === player) {
                        return (
                            <div>
                                <div
                                className='table-text table-character'
                                style={{
                                    top: innerY,
                                    left: innerX,
                                }}>
                                    { renderCupDice(tablePlayer) }
                                </div>
                                <div 
                                className={`table-text table-character color-${cups[tablePlayer]}`}
                                style={{
                                    top: middleY,
                                    left: middleX,
                                    opacity: tableDict[tablePlayer]['dice'] === 0 ? 0.5 : 1,
                                }}>
                                    <h3>{tablePlayer} </h3>
                                </div>
                                <div
                                className='table-text table-move player-move'
                                style={{
                                    top: outerY,
                                    left: outerX,
                                    position: 'absolute',
                                }}>

                                    {roundEnd ? 
                                    'lift!'
                                    :
                                    <PlayerBid 
                                    tableDict={tableDict}
                                    sidesPerDie={sidesPerDie}
                                    palifico={palifico}
                                    roundHistory={roundHistory}
                                    currentPlayer={tablePlayer}
                                    onSave={(move) => {
                                        handlePlayerMove(move);
                                    }}
                                    />
                                }
                                </div>
                            </div>
                        )
                    }
                    // if the current player is an AI
                    else {
                        return (
                            <div>
                                <div
                                className='table-text table-character'
                                style={{
                                    top: innerY,
                                    left: innerX,
                                }}>
                                    { renderCupDice(tablePlayer) }
                                </div>
                                <div 
                                className={`table-text table-character color-${cups[tablePlayer]}`}
                                style={{
                                    top: middleY,
                                    left: middleX,
                                    opacity: tableDict[tablePlayer]['dice'] === 0 ? 0.5 : 1,
                                }}>
                                    <h3>{tablePlayer} </h3>
                                </div>
                                <div
                                className='table-text table-move'
                                style={{
                                    top: outerY,
                                    left: outerX,
                                }}>
                                    {roundEnd ? 'lift!': renderThinking() }
                                </div>
                            </div>
                        )
                    }



                }
                // if tablePlayer is right before currentPlayer, then also display their move
                else if (tablePlayer === getLastPlayerBid()[0]) {
                    return (
                        <div>
                            <div
                                className='table-text table-character'
                                style={{
                                    top: innerY,
                                    left: innerX,
                                }}>
                                    { renderCupDice(tablePlayer) }
                            </div>
                            <div 
                            className={`table-text table-character color-${cups[tablePlayer]}`}
                            style={{
                                top: middleY,
                                left: middleX,
                                opacity: tableDict[tablePlayer]['dice'] === 0 ? 0.5 : 1,
                            }}>
                                <h3>{tablePlayer}</h3>
                            </div>
                            <div
                            className='table-text table-move'
                            style={{
                                top: outerY,
                                left: outerX,
                            }}>
                                <div>{formatMove(getLastPlayerBid()[1])}</div>
                            </div>
                        </div>
                    )

                }
                else {
                    return (
                        <div
                        style={{
                        }}>
                            <div
                            className='table-text table-character'
                            style={{
                                top: innerY,
                                left: innerX,
                            }}>
                                { renderCupDice(tablePlayer) }
                            </div>
                            <div 
                            className={`table-text table-character color-${cups[tablePlayer]}`}
                            style={{
                                top: middleY,
                                left: middleX,
                                opacity: tableDict[tablePlayer]['dice'] === 0 ? 0.5 : 1,
                                //border: '1px solid white',
                            }}>
                                <h3>{tablePlayer} </h3>
                            </div>
                            
                        </div>
                    )
                    
                }
                }
            }
            )
        )
    };
    // renders at the end of a round - to display the loser and the total
    const renderEndRound = () => {

        let name = palifico ? 'table-end-round-palifico': 'table-end-round-normal';

        let total = roundTotal ? roundTotal : 0;

        if (!roundLoser) {

            let move = [total, getLastPlayerBid()[1][1]];

            return (
                    <div 
                    className={`${name} text`}
                    style={{
                        fontStyle: 'italic'
                    }}>
                        {`${formatMove(move)}!`}
                    </div>
            )
        }
        else {
            return (
                <div 
                className={`${name} text`}
                style={{
                    fontStyle: 'italic'
                }}>
                    {`${roundLoser} loses a die`}
                </div>
            )
        }

    };
    // renders the palifico signal/alert
    const renderPalifico = () => {

        return (
            <div className='table-palifico'>
                <div>palifico!</div>
            </div>
        )
    };
    // renders the thinking animation
    const renderThinking = () => {

        return (
            <div className='text'
            style={{
                fontStyle: 'italic'
            }}>
                thinking 
                <div>
                    <span className="dot">.</span>
                    <span className="dot">.</span>
                    <span className="dot">.</span>
                </div>
            </div>
        )
    };
    // renders either a cup or dice
    const renderCupDice = (tablePlayer) => {

        if (tableDict[tablePlayer]['dice'] === 0) {
            return;
        }

        if (tablePlayer === player) {

            if (!showDice[tablePlayer]) {
                return (
                    <img
                        className='table-cup player-cup'
                        src={`assets/cups/cup-${cups[tablePlayer]}.png`}
                        onClick={() => {
                            let tempShowDice = {...showDice};
                            tempShowDice[tablePlayer] = true;
                            setShowDice(tempShowDice);
                        }}
                        />
                )
            }
            else {
                return (
                    <div
                    className='player-dice'
                    onClick={() => {
                        let tempShowDice = {...showDice};
                        tempShowDice[tablePlayer] = false;
                        setShowDice(tempShowDice);
                    }}
                    >{ renderDice(tableDict[tablePlayer]['hand']) }</div>
                )
            }
        }
        else {

            if (!showDice[tablePlayer]) {
                return (
                    <img 
                        className='table-cup'
                        src={`assets/cups/cup-${cups[tablePlayer]}.png`}
                        />
                )
            }
            else {
                return (
                    <div>{ renderDice(tableDict[tablePlayer]['hand']) }</div>
                )
            }
        }

        

    };
    // renders a hand of dice
    const renderDice = (diceValues) => {

        // determines the layout of the dice images
        const diceLayoutDict = {
            5: [2, 1, 2],
            4: [2, 2],
            3: [2, 1], 
            2: [2],
            1: [1]
        }

        const diceLayout = diceLayoutDict[diceValues.length];

        // sort the dice in reverse order
        diceValues.sort((a, b) => b - a);

        let currentDieIndex = -1;

        return (

            diceLayout.map((numDice, index) => {
                
                return (
                    <div 
                    className='dice-row'
                    style={{
                        display: 'flex',
                        flexDirection: 'row',
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}>
                        {Array(numDice).fill().map((_, index) => {
                            currentDieIndex += 1;
                            return (
                                <img 
                                className='die-image'
                                src={`assets/dice/die-${diceValues[currentDieIndex]}.png`}
                                />
                            )
                        })}
                    </div>
                )
            })
        )
    };


    return (
        <div
        className='game-container'
        style={{
            //border: '1px solid white',
        }}>

                <Header />

                
                <div 
                className='table-container'
                style={{
                    //border: '1px solid white',
                }}>
                    {/* table image */} 
                    <img 
                    className='game-table'
                    src='assets/table.png' alt='table'/>
                    {/* render palifico alert */}
                    { palifico && renderPalifico() }
                    {/* render the end round display */}
                    { roundEnd && renderEndRound() }
                    {/* render the table */}
                    { renderTable() }
                </div>


                <div 
                className='chat-container'

                >
                    <Chat 
                    gameID={gameID}
                    player={player}
                    table={table}
                    tableDict={tableDict}
                    currentPlayer={currentPlayer}
                    roundHistory={roundHistory}
                    palifico={palifico}
                    roundLoser={roundLoser}
                    roundTotal={roundTotal}
                    playerOut={playerOut}
                    cups={cups}
                    />

                </div>
                

            </div>
    )

};


export default Game;
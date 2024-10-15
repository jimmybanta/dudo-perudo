
import React, { useState, useRef, useEffect, } from 'react';
import axios from 'axios';
import { Button } from 'reactstrap';

import PlayerBid from '../GamePages/Components/PlayerBid';

import { apiCall } from '../../api';
import { rollDice, sleep } from '../../utils'; 


const Game = ({ player, gameID, table, playTableDict, playCurrentPlayer, sidesPerDie }) => {

    // game state
    const [tableDict, setTableDict] = useState(playTableDict); // dictionary of players with dice, hands, ex-palifico
    
    const [currentPlayer, setCurrentPlayer] = useState(playCurrentPlayer); // the current player
    const [currentBid, setCurrentBid] = useState(null); // the current bid

    const [gameHistory, setGameHistory] = useState([]); // the history of the game
    const [roundHistory, setRoundHistory] = useState([]); // the history of the round

    const [palifico, setPalifico] = useState(false); // whether the round is palifico
    
    // end round state
    const [roundEnd, setRoundEnd] = useState(false); // whether we're at the end of a round
    const [roundLoser, setRoundLoser] = useState(null); // the loser of the round
    const [roundTotal, setRoundTotal] = useState(null); // the total of the specific value that was lifted on


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

        if (currentPlayer === null) {
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
            let index = table.indexOf(currentPlayer);
            setCurrentPlayer(table[(index + 1) % table.length]);

    };
    };

    // handles a player (user or AI) calling
    // thus ending a round
    const handleCall = () => {

        // get the last player and their bid
        const [lastPlayer, lastBid] = getLastPlayerBid();

        // score the bid
        const [correct, total] = scoreBid(lastBid);

        // determine the loser
        const loser = correct ? currentPlayer : lastPlayer;

        setRoundLoser(loser);
        setRoundTotal(total);

        // add the call to the round history
        const newRoundHistory = [...roundHistory, [currentPlayer, 'call']];
        setRoundHistory(newRoundHistory);

        // update the round in the backend 
        apiCall({
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
        });

        // end the round and transition to the next one (if there is one)
        handleRoundTransition(loser, total, newRoundHistory);

    };

    // to handle transitioning between rounds
    const handleRoundTransition = async (loser, total, newRoundHistory) => {

        // first - show the end round display
        setCurrentPlayer(null);

        setRoundEnd(true);
        await sleep(3000);
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
            tempTableDict[loser]['ex-palifico'] = true;
            setPalifico(true);
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
        setCurrentPlayer(null);
        setCurrentBid(null);
        setRoundLoser(null);
        setRoundTotal(null);

        // then, determine the starting player for the next round
        // this will trigger the start of a new round
        let startingPlayer = loser;
            
        // if the loser is no longer in the game, we need to advance to the next player in the game
        while (tempTableDict[startingPlayer]['dice'] === 0) {
            let index = table.indexOf(startingPlayer);
            startingPlayer = table[(index + 1) % table.length];
        }

        // this will trigger the start of a new round
        setCurrentPlayer(startingPlayer);

    };

    
    
    // renders the table
    const renderTable = () => {

        return (
            table.map((tablePlayer) => {

                {if (tablePlayer === currentPlayer) {
                    if (tablePlayer === player) {
                        return (
                            <div>
                                <h3>(current) {tablePlayer}: </h3>
                                <h3>Your hand: {tableDict[tablePlayer]['hand']}</h3>
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
                            </div>
                        )
                    } else if (currentBid) {
                        if (currentBid === 'call') {
                            return (
                                <div>
                                    <h3>(current) {tablePlayer}: {currentBid} </h3>
                                </div>
                            )
                        }
                        else {
                            return (
                                <div>
                                    <h3>(current) {tablePlayer}: ({currentBid[0]}, {currentBid[1]}) </h3>
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
                } else if (tablePlayer === getLastPlayerBid()[0]) {
                    return (
                        <div>
                            <h3>{tablePlayer}: &nbsp;
                                {getLastPlayerBid()[1][0]},
                                {getLastPlayerBid()[1][1]} </h3>
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
            )
        )
        


    };

    // renders at the end of a round - to display the loser and the total
    const renderEndRound = () => {

        return (
            <div>
                <h3>Round over!</h3>
                <h3>{roundLoser} lost the round. There were {roundTotal[0]} {roundTotal[1]}'s.</h3>
            </div>
        )

    };





    const test = () => {


    };

    const renderHands = () => {

        return (
            table.map((tablePlayer) => {

                return (
                    <div>
                        <h3>{tablePlayer}: {tableDict[tablePlayer]['hand']}</h3>
                    </div>
                )

            })
        )
    }


    return (
        <div>
                
                { renderTable() }

                {roundEnd && (
                    renderEndRound()
                )}
                    

                <Button onClick={() => test()}>test</Button>

                <div>
                    <h3>palifico: {palifico ? 'true' : 'false'}</h3>
                </div>

                { renderHands() }

            </div>
    )

};


export default Game;
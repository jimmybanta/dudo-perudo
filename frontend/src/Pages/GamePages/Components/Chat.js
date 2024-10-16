import React, { useEffect, useState, useReducer } from 'react';

import { BASE_URL } from '../../../BaseURL';

import { apiCall } from '../../../api';


// set our chat state with a reducer
const initialState = {
    queue: [],
    history: [],
};

const reducer = (state, action) => {
    switch (action.type) {
        case 'updateQueue':
            return { ...state, queue: [...state.queue, action.payload] };
        case 'popQueue':
            let newQueue = [...state.queue];
            newQueue.shift();
            return { ...state, queue: newQueue };
        case 'updateHistory':
            return { ...state, history: [...state.history, action.payload] };
    }
};

const Chat = ({ gameID, player, table, roundHistory }) => {
    // a component for the chat

    // chat state
    const [state, dispatch] = useReducer(reducer, initialState);

    const [userMessage, setUserMessage] = useState('');




    // event stream 
    useEffect(() => {

        if (!gameID) {
            return;
        }

        const loadInitialChat = async () => {

            const [chatSuccess, chatResp] = await apiCall({
                method: 'post',
                url: `/games/get_chat_messages/`,
                data: {
                    game_id: gameID,
                    player: player,
                    table: table,
                    context: 'initialize_game',
                    round_history: roundHistory,
                    message_history: state.history,
                }
            });

            if (!chatSuccess) {
                alert(chatResp);
                return;
            }

        };

        // Initialize EventSource
        const eventSource = new EventSource(`${BASE_URL}games/stream/${gameID}/`);

        // then, load initial chat
        loadInitialChat();

        // Handle incoming messages
        eventSource.onmessage = (event) => {

            const chunk = JSON.parse(event.data);

            dispatch({ type: 'updateQueue', payload: chunk });

            /* // turn off the loading dots
            setLoading(false);
            const chunk = JSON.parse(event.data);

            // if we're loading the game, then chunks are dictionaries
            if (gameContextRef.current === 'loadGame') {

                if (chunk.item) {
                    // set the current stream to the text
                    //dispatch({ type: 'setCurrentStream', payload: chunk.item.text });
                    // add the chunk to history
                    dispatch({ type: 'appendHistory', payload: {
                        writer: chunk.item.writer,
                        text: chunk.item.text,
                        turn: chunk.item.turn,
                    
                    } });
                }

            }
            // otherwise, chunks are just text
            else {
                if (chunk.text) {
                    // add chunk to the current stream
                    dispatch({ type: 'appendCurrentStream', payload: chunk.text });

                    // wordsDict gives the number of words to scroll by
                    // scroll depends on game context
                    // i.e. it will scroll for the entire intro
                    // but only 150 words for a main response - so it doesn't go out of view
                    // just want to make it easier on the user
                    const wordsDict = {
                        'newGame': 0,
                        'loadGame': 0,
                        'gameLoaded': 0,
                        'gameIntro': 1000,
                        'gamePlay': 100,
                    }
                    // scroll
                    if ((currentStreamRef.current.split(' ').length > scrollWordRef.current) && 
                        (scrollWordRef.current < wordsDict[gameContextRef.current])) {
                        window.scrollBy({ top: 500, behavior: 'smooth' });
                        dispatch({ type: 'incrementScrollWord' });
                    }
                }
            } */

        };

        // Handle connection open
        eventSource.onopen = () => {
            console.log('Connection to server opened.');
        };

        // Cleanup on component unmount
        return () => {
            eventSource.close();
        };
    }, [gameID]);


    // for when the roundHistory changes
    // so a new move has been made, and we want to get comments on it
    useEffect(() => {

        if (roundHistory.length > 0) {

            const loadMoveComments = async () => {

                const [commentsSuccess, commentsResp] = await apiCall({
                    method: 'post',
                    url: `/games/get_chat_messages/`,
                    data: {
                        game_id: gameID,
                        player: player,
                        table: table,
                        context: 'move',
                        round_history: roundHistory,
                        message_history: state.history,
                    }
                });

                if (!commentsSuccess) {
                    alert(commentsResp);
                    return;
                }

            };

            //loadMoveComments();
            console.log(roundHistory);

        }

    }, [roundHistory]);


    // for when the chat queue changes
    useEffect(() => {

        if (state.queue.length > 0) {
                
            const chunk = state.queue[0];

            dispatch({ type: 'popQueue' });

            setTimeout(() => {
                
                dispatch({ type: 'updateHistory', payload: {
                    writer: chunk.writer,
                    text: chunk.text,
                } });

            }, chunk.delay);
        }

    }, [state.queue]);

    // for when the chat history changes
    useEffect(() => {

        //console.log(state.history[state.history.length - 1]);

    }, [state.history]);

    const renderHistory = () => {
        return state.history.map((message, index) => {
            return (
                <div key={index}>
                    <p>{message.writer}: {message.text}</p>
                </div>
            );
        });
    };


    return (
        <div
        style={{
            height: '200px',
            overflow: 'auto',
        }}>
            {renderHistory()}
            <input
                type="text"
                value={userMessage}
                onChange={(e) => {
                    setUserMessage(e.target.value);
                }}
            />

        </div>
    )
};

export default Chat;
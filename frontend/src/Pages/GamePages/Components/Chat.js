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

const Chat = ({ gameID, table }) => {
    // a component for the chat

    // chat state
    const [state, dispatch] = useReducer(reducer, initialState);




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
                    table: table
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


    // for when the chat queue changes
    useEffect(() => {

        if (state.queue.length > 0) {
                
            const chunk = state.queue[0];

            setTimeout(() => {
                dispatch({ type: 'popQueue' });

                dispatch({ type: 'updateHistory', payload: chunk });
            }, chunk.delay);
        }

    }, [state.queue]);

    // for when the chat history changes
    useEffect(() => {

        if (state.history.length > 0) {
            console.log('chat history:', state.history);
        }

    }, [state.history]);



    /* // for when the game is initialized
    useEffect(() => {

        const loadInitialChat = async () => {

            const [chatSuccess, chatResp] = await apiCall({
                method: 'post',
                url: `/games/get_chat_messages/`,
                data: {
                    game_id: gameID,
                    table: table
                }
            });

            if (!chatSuccess) {
                alert(chatResp);
                return;
            }

        };

        loadInitialChat();

    },[gameID]);
 */
};

export default Chat;
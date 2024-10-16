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

const Chat = ({ gameID, player, table, currentPlayer, roundHistory }) => {
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
                    current_player: currentPlayer,
                    round_history: roundHistory,
                    message_history: state.history,
                    user_message: null,
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
                        user_message: null,
                        round_history: roundHistory,
                        message_history: state.history,

                        current_player: null,
                    }
                });

                if (!commentsSuccess) {
                    alert(commentsResp);
                    return;
                }

            };

            loadMoveComments();
            //console.log(roundHistory);

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

    const handleUserSubmit = async (e) => {

        if (e.key === 'Enter') {

            // add the user's message to the history
            dispatch({ type: 'updateHistory', payload: {
                writer: player,
                text: userMessage,
            } });

            const [chatSuccess, chatResp] = await apiCall({
                method: 'post',
                url: `/games/get_chat_messages/`,
                data: {
                    game_id: gameID,
                    player: player,
                    table: table,
                    writer: player,
                    user_message: userMessage,
                    context: 'user_message',
                    round_history: roundHistory,
                    message_history: state.history,
                    current_player: currentPlayer,
                }
            });

            if (!chatSuccess) {
                alert(chatResp);
                return;
            }

            setUserMessage('');
        }


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
                onChange={(e) => setUserMessage(e.target.value)}
                onKeyDown={(e) => handleUserSubmit(e)}
            />

        </div>
    )
};

export default Chat;
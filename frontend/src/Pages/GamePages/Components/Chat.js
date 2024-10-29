import React, { useEffect, useState, useReducer, useRef } from 'react';

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

const Chat = ({ gameID, player, table, currentPlayer, roundHistory, cups }) => {
    // a component for the chat

    // chat state
    const [state, dispatch] = useReducer(reducer, initialState);

    const [userMessage, setUserMessage] = useState('');

    const containerRef = useRef(null);
    const inputRef = useRef(null);




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

        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }

    }, [state.history]);

    const renderHistory = () => {

        return state.history.map((message, index) => {

            return (
                <div 
                className={`chat-message color-${cups[message.writer]}`}
                key={index}>
                    <span
                    style={{
                        fontWeight: 'bold',
                    }}>[{message.writer}]:&nbsp;
                    </span>
                    <span>
                        {message.text}
                    </span>
                </div>
            );
        });
    };

    const handleUserSubmit = async (e) => {

        if (e.key === 'Enter') {

            let message = userMessage.trim();

            setUserMessage('');

            // add the user's message to the history
            dispatch({ type: 'updateHistory', payload: {
                writer: player,
                text: message,
            } });

            const [chatSuccess, chatResp] = await apiCall({
                method: 'post',
                url: `/games/get_chat_messages/`,
                data: {
                    game_id: gameID,
                    player: player,
                    table: table,
                    writer: player,
                    user_message: message,
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

            
        }


    };


    return (
        <div
        className='main-chat-container'
        style={{
        }}
        onClick={() => inputRef.current && inputRef.current.focus()}>
            <div
            className='chat-header'>
                <div 
                className='text'>
                    Chat
                </div>
            </div>

            <div 
            className='chat-history'
            ref={containerRef}
            >
                { renderHistory() }
            </div>

            <div
            className='chat-input-container'
            >
                <input
                ref={inputRef}
                className='chat-input'
                type="text"
                placeholder="..."
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                onKeyDown={(e) => handleUserSubmit(e)}
                />

            </div>

            
            

        </div>
    )
};

export default Chat;
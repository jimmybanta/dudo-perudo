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
        default:
            return state;
    }
};

const Chat = ({
    gameID, player, table, tableDict, currentPlayer, roundHistory,
    palifico, roundLoser, roundTotal, cups, playerOut, sidesPerDie
}) => {
    // the chat box

    const [state, dispatch] = useReducer(reducer, initialState); // the chat state
    const [userMessage, setUserMessage] = useState(''); // the user's message
    const [playersOut, setPlayersOut] = useState([]); // keeps track of players who are out of the game
    const containerRef = useRef(null); // ref for scrolling to the bottom of the chat box
    const inputRef = useRef(null); // ref for focusing on the input box

    // event stream 
    useEffect(() => {
        // if we don't have a gameID, don't do anything
        if (!gameID) {
            return;
        }

        const loadInitialChat = async () => {
            // load the initial chat messages
            const [chatSuccess, chatResp] = await apiCall({
                method: 'post',
                url: `/games/get_chat_messages/`,
                data: {
                    game_id: gameID,
                    player: player,
                    table: table,
                    context: 'initialize_game',
                    starting_player: currentPlayer,
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
            // Parse the incoming data
            const chunk = JSON.parse(event.data);
            // Update the chat queue
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
                        table_dict: tableDict,
                        context: 'move',
                        round_history: roundHistory,
                        message_history: state.history,
                        palifico: palifico,
                        sides_per_die: sidesPerDie,
                    }
                });

                if (!commentsSuccess) {
                    alert(commentsResp);
                    return;
                }
            };

            loadMoveComments();
        }
    }, [roundHistory]);

    // for the end of a round
    useEffect(() => {

        // if these are true, we're at the end of a round
        if (roundLoser && roundTotal) {

            const loadEndRoundComments = async () => {
                const [commentsSuccess, commentsResp] = await apiCall({
                    method: 'post',
                    url: `/games/get_chat_messages/`,
                    data: {
                        game_id: gameID,
                        player: player,
                        table: table,
                        context: 'end_round',
                        round_history: roundHistory,
                        message_history: state.history,
                        palifico: palifico,
                        round_loser: roundLoser,
                        round_total: roundTotal,
                    }
                });

                if (!commentsSuccess) {
                    alert(commentsResp);
                    return;
                }
            };

            loadEndRoundComments();
            
        }
    }, [roundLoser, roundTotal]);

    // for when a new player is out
    useEffect(() => {
        if (playerOut) {
            const loadPlayerOutComments = async () => {
                const [commentsSuccess, commentsResp] = await apiCall({
                    method: 'post',
                    url: `/games/get_chat_messages/`,
                    data: {
                        game_id: gameID,
                        player: player,
                        table: table,
                        context: 'player_out',
                        round_history: roundHistory,
                        message_history: state.history,
                        player_out: playerOut,
                    }
                });

                if (!commentsSuccess) {
                    alert(commentsResp);
                    return;
                }
            };

            loadPlayerOutComments();
        }
    }, [playerOut]);

    // for when the chat queue changes
    useEffect(() => {
        if (state.queue.length > 0) {
            const chunk = state.queue[0];
            dispatch({ type: 'popQueue' });

            // add the chunk to the history
            // after the given delay
            setTimeout(() => {
                dispatch({
                    type: 'updateHistory', payload: {
                        writer: chunk.writer,
                        text: chunk.text,
                    }
                });
            }, chunk.delay);
        }
    }, [state.queue]);

    // for when the chat history changes
    useEffect(() => {
        // scroll to the bottom
        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [state.history]);

    // handle the user submitting a message
    const handleUserSubmit = async (e) => {
        if (e.key === 'Enter') {
            // get the user's message
            let message = userMessage.trim();
            setUserMessage('');

            // add the user's message to the history
            dispatch({
                type: 'updateHistory', payload: {
                    writer: player,
                    text: message,
                }
            });

            // send the message to the backend, get responses
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
                    starting_player: currentPlayer,
                    palifico: palifico,
                }
            });

            if (!chatSuccess) {
                alert(chatResp);
                return;
            }
        }
    };

    // render the chat history
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

    return (
        <div
            className='chat-box'
            style={{}}
            onClick={() => inputRef.current && inputRef.current.focus()}>
            <div className='chat-header'>
                <div className='text'>
                    Chat
                </div>
            </div>

            <div
                className='chat-history'
                ref={containerRef}>
                { renderHistory() }
            </div>

            <div className='chat-input-container'>
                <input
                    ref={inputRef}
                    className='chat-input'
                    type="text"
                    placeholder="type here..."
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                    onKeyDown={(e) => handleUserSubmit(e)}
                />
            </div>
        </div>
    );
};

export default Chat;

import { React, useState } from 'react';



const Play = () => {

    const [players, setPlayers] = useState([]);

    const tempPlayers = ['Human', 'AI-1', 'AI-2', 'AI-3', 'AI-4', 'AI-5'];
    setPlayers(tempPlayers);

    return (
        <div>
        <h1>Play</h1>
        <p>Game here</p>
        </div>
    )
    }


export default Play;
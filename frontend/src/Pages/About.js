import React, { useState, useEffect } from 'react';

import { apiCall } from '../api';

const About = ({ onSetCurrentPage }) => {
    // The about page

    // The current game version
    const [gameVersion, setGameVersion] = useState(null);

    useEffect(() => {
        const getGameVersion = async () => {
            // Make a call to the backend to get the current version of the game
            const [success, resp] = await apiCall({
                method: 'get',
                url: '/games/get_current_version/',
            });

            if (!success) {
                return;
            }

            setGameVersion(resp.version);
        };

        getGameVersion();
    }, []);

    return (
        <div
            className='container flex-column'
            style={{
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
                width: '100%',
                paddingLeft: '5%',
                paddingRight: '5%',
                //border: '1px solid white',
            }}
        >
            <div
                className='container flex-column'
                style={{
                    width: '100%',
                    marginBottom: '10%',
                    //border: '1px solid white',
                }}
            >
                <div className='text about-header all-caps'>About</div>
            </div>

            <div className='container flex-column' style={{ width: '100%', height: '66%' }}>
                <div className='text about-paragraphs'>
                    Perudo (also called Dudo or Liar's Dice) is the national game of Peru - best played 
                    in real life, with a group of good friends, around an old wooden table,
                    drinking bourbon or tea or whatever you like.
                </div>

                <div className='text about-paragraphs'>
                    Dudo Perudo (this game) is meant to simulate the banter and fun of the real game - 
                    but it will never be as good as the real thing.
                </div>

                <div className='text about-paragraphs'>
                    After playing here, do yourself a favor and get some dice, cups, and friends, 
                    and play the real game.
                </div>

                <div
                style={{
                    height: '50px',
                }} 
                />

                <div className='text about-paragraphs'>
                    Dudo Perudo was designed by Jimmy Banta. You can see more of his work {' '}
                    <a className='about-link'
                    href='https://jimmybanta.com' target='_blank' rel='noreferrer'>
                        here
                    </a>
                    .
                </div>

                <div className='text about-paragraphs'>
                    Or you can check out the code for Dudo Perudo{' '}
                    <a className='about-link'
                    href='https://github.com/jimmybanta/crash-the-game/' target='_blank' rel='noreferrer'>
                        here
                    </a>
                    .
                </div>

                {gameVersion && (
                    <div className='text about-paragraphs'>Current version: {gameVersion}</div>
                )}

                <div className='button home-button text' onClick={() => onSetCurrentPage('Home')}>
                    back
                </div>
            </div>
        </div>
    );
};

export default About;

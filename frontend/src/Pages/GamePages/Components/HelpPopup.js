
import React, { useState } from 'react';



const HelpPopup = ({ fadeClass, page }) => {


    const renderParagraphs = () => {

        let paragraphs = [];


        if (page === 'setup') {

             paragraphs = [
                'Click on characters on the left to add them to the table.',
                'Click their names on the right to remove them from the table.',
                "The table supports a max of 12 players.",
                "Once you're satisfied, click 'onward!' to start the game."
            ];
        }

        if (page === 'game') {

            paragraphs = [
                "Click on your cup to see your dice.",
                "When it's your turn, you can make a bid by inputting a quantity and value of dice.",
                "If you're not starting the round, you can also lift - calling the previous player's bid.",
                "Whoever is wrong loses a die.",
                "Ones (called jessies) are wild - they count as any value.",
                "When you're down to one die, the round is 'palifico' - jessies are no longer wild for that one round.",
                "When you're out of dice, you're out of the game.",
            ]
        }


        return (
            <div
            className='container flex-column'
            style={{
                gap: '10px',
            }}>
            { paragraphs.map((paragraph, index) => {
                return (
                    <div key={index} className='text help-paragraph'>
                        {paragraph}
                    </div>
                )
            }
        )
    }
        </div>
    )
    };


    return (
        <div 
            className={ `help-popup ${fadeClass}` }
            onClick={(e) => e.stopPropagation()}
        >
            <div 
                className='container flex-column text help-popup-text'
                style={{ gap: '10px' }}
            >
                <div style={{ fontStyle: 'italic' }}>Help</div>
                { renderParagraphs() }
            </div>
        </div>
    )


};


export default HelpPopup;
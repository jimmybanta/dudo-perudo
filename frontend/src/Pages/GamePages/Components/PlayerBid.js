/* component where a player can make a bid */
import { React, useEffect, useState } from 'react';
import { Button, Input } from 'reactstrap';
import axios from 'axios';


import { apiCall } from '../../../api';




const PlayerBid = (props) => {

    const { tableDict, sidesPerDie, palifico, roundHistory, currentPlayer, onSave } = props;

    const [legalBids, setLegalBids] = useState([]);
    const [currentQuantity, setCurrentQuantity] = useState(null);
    const [currentValue, setCurrentValue] = useState(null);

    const [roundStart, setRoundStart] = useState(true ? roundHistory.length === 0 : false);


    useEffect(() => {

        const loadLegalBids = async () => {

            const [bidsSuccess, bidsResp] = await apiCall({
                method: 'post',
                url: '/games/legal_bids/',
                data: {
                    table_dict: tableDict,
                    sides_per_die: sidesPerDie,
                    palifico: palifico,
                    round_history: roundHistory,
                    current_player: currentPlayer
                }
            });

            if (!bidsSuccess) {
                alert(bidsResp);
                return;
            }

            setLegalBids(bidsResp.legal_bids.map(bid => {
                return [parseInt(bid[0]), parseInt(bid[1])];
            }
            ));
        };

        loadLegalBids();

    }
    , [tableDict, currentPlayer]);

    const handleBid = (quantity, value) => {

        const bid = [parseInt(quantity), parseInt(value)];
        let legal = false;

        /* check if the bid is legal */
        legalBids.forEach(legalBid => {
            if (bid[0] === legalBid[0] && bid[1] === legalBid[1]) {
                legal = true;
                onSave(bid);
            } 
        }
        );
        if (!legal) {
            alert('Illegal bid. Please try again.');
        }

    };

    const handleCall = () => {

        onSave('call');

    };



    return (
        <div>
            <h1>Bid</h1>
            <Input
                        type="text"
                        placeholder="Quantity"
                        onChange={(e) => {
                            setCurrentQuantity(e.target.value);
                        }}
            />
            <Input 
                        type="text"
                        placeholder="Value"
                        onChange={(e) => {
                                setCurrentValue(e.target.value);
                            
                        }}
            />
            <Button
            onClick={() => handleBid(currentQuantity, currentValue)}
            >
                Bid
            </Button>
            {!roundStart && (
                <div>
                    <p>or</p>
                    <Button
                    onClick={() => handleCall()}
                    >
                        Call
                    </Button>
                </div>
            )}
            
        </div>
    );
};


export default PlayerBid;
/* component where a player can make a bid */
import { React, useEffect, useState } from 'react';
import ValueDropDown from './ValueDropDown';
import { apiCall } from '../../../api';

const PlayerBid = ({ tableDict, sidesPerDie, palifico, roundHistory, currentPlayer, onSave }) => {
    // component where a player can make a bid

    const [legalBids, setLegalBids] = useState([]); // all the legal bids for the current player
    const [currentQuantity, setCurrentQuantity] = useState(null); // the current quantity of the bid
    const [currentValue, setCurrentValue] = useState(null); // the current value of the bid
    const [availableValues, setAvailableValues] = useState([]); // the available values, given the current quantity
    const [roundStart, setRoundStart] = useState(roundHistory.length === 0); // whether the current round has just started
    const [legal, setLegal] = useState(false); // whether the current bid is legal

    // when the current player changes, load the legal bids
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
            }));
        };

        loadLegalBids();
    }, [tableDict, currentPlayer]);

    // updates available values when the current quantity changes
    useEffect(() => {
        if (!currentQuantity) {
            return;
        }

        let singular = false;
        if (parseInt(currentQuantity) === 1) {
            singular = true;
        }

        let newAvailableValues = [];
        const valueDict = {
            1: singular ? (palifico ? 'one' : 'jessie') : (palifico ? 'ones' : 'jessies'),
            2: singular ? 'two' : 'twos',
            3: singular ? 'three' : 'threes',
            4: singular ? 'four' : 'fours',
            5: singular ? 'five' : 'fives',
            6: singular ? 'six' : 'sixes',
        };

        let quantityBids = legalBids.filter(bid => bid[0] === parseInt(currentQuantity));
        quantityBids.forEach(bid => {
            newAvailableValues.push(valueDict[bid[1]]);
        });

        // remove duplicates
        newAvailableValues = [...new Set(newAvailableValues)];
        setAvailableValues(newAvailableValues);
    }, [currentQuantity]);

    // updates whether the current bid is legal
    useEffect(() => {
        if (!currentQuantity || !currentValue) {
            setLegal(false);
            return;
        }

        setLegal(checkLegal(currentQuantity, currentValue));
    }, [currentQuantity, currentValue]);

    // check if a bid is legal
    const checkLegal = (quantity, value) => {
        let currentBid = [parseInt(quantity), parseInt(value)];
        const isLegal = legalBids.some((legalBid) => {
            let bid = [parseInt(legalBid[0]), parseInt(legalBid[1])];
            return currentBid[0] === bid[0] && currentBid[1] === bid[1];
        });
        return isLegal;
    };

    // handle a bid
    const handleBid = (quantity, value) => {
        const bid = [parseInt(quantity), parseInt(value)];
        let legal = false;

        // check if the bid is legal
        legalBids.forEach(legalBid => {
            if (bid[0] === legalBid[0] && bid[1] === legalBid[1]) {
                legal = true;
                onSave(bid);
            }
        });

        if (!legal) {
            alert('Illegal bid. Please try again.');
        }
    };

    // handle a lift (call)
    const handleCall = () => {
        onSave('call');
    };

    // handle the value changing
    const handleValueChange = (value) => {
        const valueToInt = {
            'one': 1, 'ones': 1,
            'jessie': 1, 'jessies': 1,
            'two': 2, 'twos': 2,
            'three': 3, 'threes': 3,
            'four': 4, 'fours': 4,
            'five': 5, 'fives': 5,
            'six': 6, 'sixes': 6,
        };
        setCurrentValue(valueToInt[value]);
    };

    return (
        <div
            className='container flex-row player-bid-row'
            style={{ position: 'relative' }}>
            <input
                className='bid-quantity text player-bid'
                type="text"
                placeholder="quantity"
                onChange={(e) => setCurrentQuantity(e.target.value)}
            />
            <ValueDropDown
                availableValues={availableValues}
                palifico={palifico}
                singular={parseInt(currentQuantity) === 1}
                onValueChange={(value) => handleValueChange(value)}
            />
            <div
                className='bid-button text player-bid'
                disabled={!currentQuantity || !currentValue}
                onClick={() => handleBid(currentQuantity, currentValue)}
                style={{
                    pointerEvents: legal ? 'auto' : 'none',
                    opacity: legal ? 1 : 0.5
                }}>
                bid
            </div>
            {!roundStart && (
                <>
                    <div className='player-bid-or'>or</div>
                    <div
                        className='bid-button text player-bid'
                        onClick={() => handleCall()}>
                        lift
                    </div>
                </>
            )}
        </div>
    );
};

export default PlayerBid;

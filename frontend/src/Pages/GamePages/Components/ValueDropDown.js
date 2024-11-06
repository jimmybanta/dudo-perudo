import React, { useState, useEffect } from "react";

const ValueDropDown = ({ availableValues, palifico, singular, onValueChange }) => {
    // A dropdown for selecting a value

    const allValues = [
        singular ? (palifico ? 'one' : 'jessie') : (palifico ? 'ones' : 'jessies'),
        singular ? 'two' : 'twos',
        singular ? 'three' : 'threes',
        singular ? 'four' : 'fours',
        singular ? 'five' : 'fives',
        singular ? 'six' : 'sixes',
    ]; // all possible values

    const [selectedValue, setSelectedValue] = useState(null); // the selected value
    const [dropdownOpen, setDropdownOpen] = useState(false); // whether the dropdown is open

    // if singular changes, update the selected value
    useEffect(() => {
        const singularToPlural = {
            'one': 'ones',
            'jessie': 'jessies',
            'two': 'twos',
            'three': 'threes',
            'four': 'fours',
            'five': 'fives',
            'six': 'sixes',
        };

        const pluralToSingular = {
            'ones': 'one',
            'jessies': 'jessie',
            'twos': 'two',
            'threes': 'three',
            'fours': 'four',
            'fives': 'five',
            'sixes': 'six',
        };

        if (selectedValue in singularToPlural) {
            setSelectedValue(singularToPlural[selectedValue]);
        }

        if (selectedValue in pluralToSingular) {
            setSelectedValue(pluralToSingular[selectedValue]);
        }
    }, [singular]);

    // toggle the dropdown
    const toggle = (e) => {
        setDropdownOpen(!dropdownOpen);
    };

    // handle a value change
    const handleValueChange = (value) => {
        onValueChange(value);
        setSelectedValue(value);
        toggle();
    };

    return (
        <div className='value-dropdown'>
            <button
                className="value-dropdown-button text player-bid"
                onClick={() => toggle()}
            >
                {selectedValue ? selectedValue : 'value'}
            </button>

            <div
                className="value-dropdown-content text player-bid"
                style={{
                    display: dropdownOpen ? 'block' : 'none',
                }}
            >
                {allValues.map((value) => (
                    <span
                        className="value-dropdown-item"
                        onClick={() => handleValueChange(value)}
                        style={{
                            opacity: availableValues.includes(value) ? 1 : 0.5,
                            pointerEvents: availableValues.includes(value) ? 'auto' : 'none',
                        }}
                    >
                        {value}
                    </span>
                ))}
            </div>
        </div>
    );
}

export default ValueDropDown;

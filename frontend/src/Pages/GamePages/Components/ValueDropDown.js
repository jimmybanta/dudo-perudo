import React, { useState, useEffect } from "react";
import { Dropdown, 
    DropdownToggle, 
    DropdownMenu, 
    DropdownItem, 
    FormGroup, 
    Label, 
    Input,
    UncontrolledDropdown,
    Col,
    Button } from "reactstrap";


const ValueDropDown = ({ availableValues, palifico, singular, onValueChange }) => {

    const allValues = [
        singular ? (palifico ? 'one': 'jessie') : (palifico ? 'ones': 'jessies'),
        singular ? 'two' : 'twos',
        singular ? 'three' : 'threes',
        singular ? 'four' : 'fours',
        singular ? 'five' : 'fives',
        singular ? 'six' : 'sixes',
    ]

    const [selectedValue, setSelectedValue] = useState(null);
    
    const [dropdownOpen, setDropdownOpen] = useState(false);

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


    
      
    const toggle = (e) => {
        setDropdownOpen(!dropdownOpen);
    };

    const handleValueChange = (value) => {

        onValueChange(value);

        setSelectedValue(value);

        toggle();

    };


      
    
    
      return (
        <div 
        className='value-dropdown'
        >
            <button 
            className="value-dropdown-button text player-bid"
            onClick={() => toggle()}
            >
                {selectedValue ? selectedValue : 'value'}
            </button>

            <div className="value-dropdown-content text player-bid"
            style={{
                display: dropdownOpen ? 'block' : 'none',
            }}>

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
    
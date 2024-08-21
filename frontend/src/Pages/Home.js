import { React, useState } from 'react';

import { Button } from 'reactstrap';



const Home = ({onSetCurrentPage}) => {

    return (
        <div>
        <h1>Dudo Perudo</h1>
         <div className='container'>
        <Button
        onClick={() => onSetCurrentPage('Play')}>
          Play
        </Button>
        </div>
        <div className='container'>
        <Button
         onClick={() => onSetCurrentPage('Instructions')}>
          Instructions
        </Button>
      </div>
      <div className='container'>
        <Button
        onClick={() => onSetCurrentPage('Settings')}>
          Settings
        </Button>
      </div>
    </div>
    )
    }



export default Home;
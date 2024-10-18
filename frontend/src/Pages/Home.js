import { React, useState } from 'react';

import { Button } from 'reactstrap';



const Home = ({ onSetCurrentPage }) => {

    return (
        <div
        className='container flex-column'
        style={{
          gap: '30px',
        }}>
          <div 
          className='text main-title gradient-text all-caps'
          style={{marginBottom: '20%'}}
          >
            Dudo Perudo
          </div>
          <div 
          className='text button home-button home-play-button'
          onClick={() => onSetCurrentPage('Play')}
          >
            <span className='gradient-text home-play'>let's play!</span>
          </div>
          <div 
          className='text button home-button home-about-button'
          onClick={() => onSetCurrentPage('About')}
          >
            <span className='gradient-text home-about'>about</span>
          </div>




{/*           <div className='container'>
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
        </div> */}
    </div>
    )
    }



export default Home;
import { React, useState } from 'react';

import { Button } from 'reactstrap';



const Home = ({ onSetCurrentPage }) => {

    return (
      <div
      className='container flex-column'
      style={{
        position: 'relative',
        gap: '30px',
        width: '100%',
        height: '100%',
      }}>

        <div 
          className='text main-title all-caps'
          style={{
          }}
          >
          Dudo Perudo
        </div>

        <div className='container flex-column'
        style={{
          position: 'relative',
        }} >

          <img 
          className='home-table'
          src='assets/table.png' 
          alt='table' 
          />

          <div 
          className='text button home-button home-play-button'
          onClick={() => onSetCurrentPage('Play')}
          >
          <span className=''>let's play!</span>
          </div>

          <div 
          className='text button home-button home-about-button'
          onClick={() => onSetCurrentPage('About')}
          >
          <span className=''>about</span>
          </div>



        </div>
        
        
        
    </div>
    )
    }



export default Home;
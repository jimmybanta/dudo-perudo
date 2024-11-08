import './App.css';
import { React, useState } from 'react';

import Home from './Pages/Home';
import Play from './Pages/Play';
import About from './Pages/About';

function App() {

  const [currentPage, setCurrentPage] = useState('Home');


  return (
    <div className="App">
      <div
        className='container flex-column main-app-container'
        style={{
          height: '100vh',
          width: '100vw',
          overflow: 'auto',
          //border: '1px solid white'
        }}
      >

        {currentPage === 'Home' && 
        <Home
        onSetCurrentPage={(page) => setCurrentPage(page)}
        />}
        {currentPage === 'Play' &&
          <Play 
          onSetCurrentPage={(page) => setCurrentPage(page)}/>}
        {currentPage === 'About' && 
          <About 
          onSetCurrentPage={(page) => setCurrentPage(page)}
          />}

      </div>        
      
    </div>

      
     
);
}

export default App;

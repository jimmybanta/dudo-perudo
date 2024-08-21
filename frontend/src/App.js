import './App.css';
import { React, useState } from 'react';

import Instructions from './Pages/Instructions';
import Home from './Pages/Home';
import Play from './Pages/Play';
import Settings from './Pages/Settings';

function App() {

  const [currentPage, setCurrentPage] = useState('Home');


  return (
    <div className="App">

    {currentPage === 'Home' && 
    <Home
    onSetCurrentPage={(page) => setCurrentPage(page)}
     />}
    {currentPage === 'Play' &&
      <Play />}
    {currentPage === 'Instructions' && 
      <Instructions />}
    {currentPage === 'Settings' &&
      <Settings />}
      
    </div>

      
     
);
}

export default App;

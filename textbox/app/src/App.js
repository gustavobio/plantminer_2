import React from 'react';
import logo from './logo.svg';
import './App.css';
import HideableText from './HideableText';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      </header>
      <div className="App-content">
        <HideableText text="Gustavo" />
      </div>
    </div>
  );
}

export default App;

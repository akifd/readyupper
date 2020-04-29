import React from 'react';

import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';

import './App.css';
import Frontpage from './components/Frontpage'


function App() {
  return (
    <div className="app">
      <Container className="App" maxWidth="md">
        <Typography variant="h1" component="h1" gutterBottom align="center">
          Readyupper
        </Typography>

        <Frontpage />
      </Container>
    </div>
  );
}

export default App;

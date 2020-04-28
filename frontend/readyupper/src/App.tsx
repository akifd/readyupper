import React from 'react';
import Button from '@material-ui/core/Button';
import './App.css';
import TextField from '@material-ui/core/TextField';
import Container from '@material-ui/core/Container';


function App() {
  return (
    <div className="App">
      <Container className="App" maxWidth="sm">
        <TextField label="Calendar name" />
        <Button variant="contained" color="primary">
          Create calendar
        </Button>
      </Container>
    </div>
  );
}

export default App;

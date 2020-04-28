import React from 'react';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Grid from '@material-ui/core/Grid';

import './App.css';


function App() {
  return (
    <div className="app">
      <Container className="App" maxWidth="md">
        <Typography variant="h1" component="h1" gutterBottom align="center">
          Readyupper
        </Typography>

        <Grid container spacing={3}>
          <Grid item sm={12} md={6}>
            <Card>
              <CardContent>
                <Typography component="h2" variant="h4" gutterBottom>
                  Create new calendar
                </Typography>
                <TextField label="Calendar name" variant="filled" fullWidth />
              </CardContent>
              <CardActions>
                <Button variant="contained" color="primary" fullWidth>
                  Create calendar
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item sm={12} md={6}>
            <Card>
              <CardContent>
                <Typography component="h2" variant="h4" gutterBottom>
                  Open existing calendar
                </Typography>
                <TextField label="Calendar hash" variant="filled" fullWidth />
              </CardContent>
              <CardActions>
                <Button variant="contained" fullWidth>
                  Open calendar
                </Button>
              </CardActions>
            </Card>
          </Grid>
        </Grid>

      </Container>
    </div>
  );
}

export default App;

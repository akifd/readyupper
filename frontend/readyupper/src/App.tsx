import React from 'react'

import { BrowserRouter as Router, Switch, Route } from "react-router-dom"

import Container from '@material-ui/core/Container'
import Typography from '@material-ui/core/Typography'

import './App.css'
import Frontpage from './components/Frontpage'
import CalendarDetail from './components/CalendarDetail'


function App() {
  return (
    <Router>
      <div className="app">
        <Container className="App" maxWidth="md">
          <Typography variant="h1" component="h1" gutterBottom align="center">
            Readyupper
          </Typography>

          <Switch>
            <Route path="/:urlHash">
              <CalendarDetail />
            </Route>
            <Route path="/">
              <Frontpage />
            </Route>
          </Switch>
        </Container>
      </div>
    </Router>
  )
}

export default App

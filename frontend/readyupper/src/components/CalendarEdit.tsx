import React, { useState, useEffect } from 'react'

import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import ButtonGroup from '@material-ui/core/ButtonGroup'
import TextField from '@material-ui/core/TextField'
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';

import { Link } from 'react-router-dom'
import { AxiosResponse, AxiosError } from 'axios'
import { Redirect } from 'react-router-dom'

import { Calendar } from '../interfaces'
import { deleteCalendar, createEntry, fetchEntries, createParticipant, fetchParticipants } from '../utils'
import ErrorMessage from './ErrorMessage'


function CalendarEdit(props: {calendar: Calendar}) {
  let [deleted, setDeleted] = useState(false)
  let [error, setError] = useState("")
  let [participants, setParticipants] = useState([])
  let [entries, setEntries] = useState([])

  // Participant fetching.
  useEffect(() => {
    function success(response: AxiosResponse) {
      setParticipants(response.data)
    }

    function failure(response: AxiosError) {
      setError("Participant fetching failed.")
    }

    fetchParticipants(props.calendar.id).then(success).catch(failure)
  }, [props.calendar.id])

  // Entry fetching.
  useEffect(() => {
    function success(response: AxiosResponse) {
      setEntries(response.data)
    }

    function failure(response: AxiosError) {
      setError("Entry fetching failed.")
    }

    fetchEntries(props.calendar.id).then(success).catch(failure)
  }, [props.calendar.id])

  if (error)
    return <ErrorMessage message={error} />

  if (deleted)
    return <Redirect to="/" />

  function onCreateParticipant(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    let input = (document.getElementById('participant-input') as HTMLInputElement)
    let name: string = input.value
    input.value = ''

    function success(response: AxiosResponse) {
      setParticipants([...participants, response.data])
    }

    function failure(response: AxiosError) {
      setError("Participant creation failed.")
    }

    createParticipant(props.calendar.id, name).then(success).catch(failure)
  }

  function onCreateEntry(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    let input = (document.getElementById('entry-input') as HTMLInputElement)
    let timestamp: string = input.value
    input.value = ''

    function success(response: AxiosResponse) {
      setEntries([...entries, response.data])
    }

    function failure(response: AxiosError) {
      setError("Entry creation failed.")
    }

    createEntry(props.calendar.id, timestamp).then(success).catch(failure)
  }

  function saveCalendar() {
     // TODO
  }

  return (
    <Grid container spacing={6}>
      <Grid item xs={12} md={6}>
        <form method="post" onSubmit={onCreateParticipant}>
          <TextField id="participant-input" label="Participant name" helperText="Press enter to add." fullWidth />
        </form>

        <List>
          {participants.map((participant, index) =>
            <ListItem key={index}>
              <ListItemText primary={participant.name} />
              <ListItemSecondaryAction>
                <IconButton edge="end" aria-label="delete">
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          )}
        </List>
      </Grid>

      <Grid item xs={12} md={6}>
        <form method="post" onSubmit={onCreateEntry}>
          <TextField id="entry-input" label="Entry" helperText="Press enter to add." fullWidth />
        </form>

        <List>
          {entries.map((entry, index) =>
            <ListItem key={index}>
              <ListItemText primary={entry.timestamp} />
              <ListItemSecondaryAction>
                <IconButton edge="end" aria-label="delete">
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          )}
        </List>
      </Grid>

      <Grid container item justify="space-between" xs={12}>
        <Grid item>
          <ButtonGroup>
            <Button variant="contained" color="primary" onClick={saveCalendar}>
              Save Calendar
            </Button>
            <Button variant="contained" component={Link} to={`/${props.calendar.id}/`}>
              Cancel
            </Button>
          </ButtonGroup>
        </Grid>
        <Grid item>
          <Button variant="contained" color="secondary" onClick={() => deleteCalendar(props.calendar.id, setDeleted)}>
            Delete Calendar
          </Button>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default CalendarEdit

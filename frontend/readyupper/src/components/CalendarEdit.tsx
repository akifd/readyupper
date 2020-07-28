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
import { deleteCalendar, createEntry, fetchEntries } from '../utils'
import ErrorMessage from './ErrorMessage'


function CalendarEdit(props: { calendar: Calendar }) {
  let [deleted, setDeleted] = useState(false)
  let [participants, setParticipants] = useState([])
  let [entries, setEntries] = useState([])
  let [error, setError] = useState("")

  useEffect(() => fetchEntries(props.calendar.id, setEntries, setError), [props.calendar.id])

  if (error)
    return <ErrorMessage message={error} />

  if (deleted)
    return <Redirect to="/" />

  function createParticipant(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    let input = (document.getElementById('participant-input') as HTMLInputElement)
    setParticipants([...participants, input.value])
    input.value = ''
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
      // TODO
    }

    createEntry(props.calendar.id, timestamp).then(success).catch(failure)
  }

  function saveCalendar() {
     // TODO
  }

  console.log("Rendering!")
  console.log(entries)

  return (
    <Grid container spacing={6}>

      <Grid item xs={12} md={6}>
        <form method="post" onSubmit={createParticipant}>
          <TextField id="participant-input" label="Participant name" helperText="Press enter to add." fullWidth />
        </form>
      </Grid>

      <Grid item xs={12} md={6}>
        <form method="post" onSubmit={onCreateEntry}>
          <TextField id="entry-input" label="Entry" helperText="Press enter to add." fullWidth />
        </form>

        <List>
          {entries.map((value, index) =>
            <ListItem>
              <ListItemText primary={value.timestamp} />
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

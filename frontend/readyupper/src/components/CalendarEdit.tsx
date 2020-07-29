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
import { Redirect } from 'react-router-dom'

import { Calendar } from '../interfaces'
import { deleteCalendar, createEntry, fetchEntries, createParticipant, fetchParticipants, convertEntry } from '../utils'
import ErrorMessage from './ErrorMessage'


function CalendarEdit(props: {calendar: Calendar}) {
  let [deleted, setDeleted] = useState(false)
  let [error, setError] = useState("")
  let [participants, setParticipants] = useState([])
  let [entries, setEntries] = useState([])

  // Participant fetching.
  useEffect(() => {
    async function fetchData() {
      try {
        let response = await fetchParticipants(props.calendar.id)

        if (response.status === 200)
          setParticipants(response.data)
      }
      catch (error) {
        setError("Participant fetching failed.")
      }
    }
    fetchData()
  }, [props.calendar.id])

  // Entry fetching.
  useEffect(() => {
    async function fetchData() {
      try {
        let response = await fetchEntries(props.calendar.id)

        if (response.status === 200)
          setEntries(response.data.map(convertEntry))
      }
      catch(error) {
        setError("Entry fetching failed.")
      }
    }
    fetchData()
  }, [props.calendar.id])

  if (error)
    return <ErrorMessage message={error} />

  if (deleted)
    return <Redirect to="/" />

  async function onCreateParticipant(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    let input = (document.getElementById('participant-input') as HTMLInputElement)
    let name: string = input.value
    input.value = ''

    try {
      let response = await createParticipant(props.calendar.id, name)

      if (response.status === 200)
        setParticipants([...participants, response.data])
    }
    catch (error) {
      setError("Participant creation failed.")
    }
  }

  async function onCreateEntry(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    let input = (document.getElementById('entry-input') as HTMLInputElement)
    let timestamp: string = input.value
    input.value = ''

    try {
      let response = await createEntry(props.calendar.id, timestamp)

      if (response.status === 200)
        setEntries([...entries, convertEntry(response.data)])
    }
    catch (error) {
      setError("Entry creation failed.")
    }
  }

  function onSaveCalendar() {
     // TODO
  }

  async function onDeleteCalendar() {
    try {
      let response = await deleteCalendar(props.calendar.id)

      if (response.status === 200)
        setDeleted(true)
    }
    catch (error) {
      setError("Calendar deletion failed.")
    }
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
          {entries.map((entry) =>
            <ListItem key={entry.id}>
              <ListItemText primary={entry.timestamp.toLocaleString()} />
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
            <Button variant="contained" color="primary" onClick={onSaveCalendar}>
              Save Calendar
            </Button>
            <Button variant="contained" component={Link} to={`/${props.calendar.id}/`}>
              Cancel
            </Button>
          </ButtonGroup>
        </Grid>
        <Grid item>
          <Button variant="contained" color="secondary" onClick={onDeleteCalendar}>
            Delete Calendar
          </Button>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default CalendarEdit

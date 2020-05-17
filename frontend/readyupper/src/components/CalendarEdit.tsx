import React, { useState } from 'react'

import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import ButtonGroup from '@material-ui/core/ButtonGroup'
import IconButton from '@material-ui/core/IconButton'
import Input from '@material-ui/core/Input'
import InputLabel from '@material-ui/core/InputLabel'
import InputAdornment from '@material-ui/core/InputAdornment'
import FormControl from '@material-ui/core/FormControl'
import AddCircleOutlinedIcon from '@material-ui/icons/AddCircleOutlined';

import { Link } from 'react-router-dom'
import axios, { AxiosResponse, AxiosError } from 'axios'
import { Redirect } from 'react-router-dom'

import { Calendar } from '../interfaces'
import { backendUrl } from '../utils'


function CalendarEdit(props: { calendar: Calendar }) {
  let [deleted, setDeleted] = useState(false)

  if (deleted)
    return <Redirect to="/" />

  function deleteCalendar() {
    let promise = axios.delete(backendUrl("/calendars/" + props.calendar.id + "/"))

    promise.then((response: AxiosResponse) => {
      setDeleted(true)
    })

    promise.catch((error: AxiosError) => {
      // TODO
    })
  }

  function saveCalendar() {
     // TODO
  }

  return (
    <Grid container spacing={6}>
      <Grid item xs={12} md={6}>
        <FormControl fullWidth>
          <InputLabel htmlFor="add-participant">Participant name</InputLabel>
          <Input id="add-participant" endAdornment={
            <InputAdornment position="end">
              <IconButton>
                <AddCircleOutlinedIcon color="primary" />
              </IconButton>
            </InputAdornment>
          }/>
        </FormControl>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormControl fullWidth>
          <InputLabel htmlFor="add-entry">Datetime</InputLabel>
          <Input id="add-entry" endAdornment={
            <InputAdornment position="end">
              <IconButton>
                <AddCircleOutlinedIcon color="primary" />
              </IconButton>
            </InputAdornment>
          }/>
        </FormControl>
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
          <Button variant="contained" color="secondary" onClick={deleteCalendar}>
            Delete Calendar
          </Button>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default CalendarEdit

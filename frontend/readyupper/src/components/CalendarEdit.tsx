import React, { useState } from 'react'

import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import ButtonGroup from '@material-ui/core/ButtonGroup'

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
    <div>
      <Grid justify="space-between" container spacing={2}>
        <Grid item>
          <ButtonGroup>
            <Button variant="contained" color="primary" onClick={saveCalendar}>
              Save
            </Button>
            <Button variant="contained" component={Link} to={`/${props.calendar.id}/`}>
              Cancel
            </Button>
          </ButtonGroup>
        </Grid>
        <Grid item>
          <Button variant="contained" color="secondary" onClick={deleteCalendar}>
            Delete
          </Button>
        </Grid>
      </Grid>
    </div>
  )
}

export default CalendarEdit

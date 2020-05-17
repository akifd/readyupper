import React, { useState } from 'react'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import { Link } from 'react-router-dom'
import axios, { AxiosResponse, AxiosError } from 'axios'
import { Redirect } from 'react-router-dom'

import { Calendar } from '../interfaces'


function CalendarEdit(props: { calendar: Calendar }) {
  let [deleted, setDeleted] = useState(false)

  if (deleted)
    return <Redirect to="/" />

  function deleteCalendar() {
    let promise = axios.delete("http://localhost:8000/calendars/" + props.calendar.id + "/")

    promise.then((response: AxiosResponse) => {
      setDeleted(true)
    })

    promise.catch((error: AxiosError) => {
      // TODO
    })
  }

  return (
    <div>
      <Button variant="contained" color="secondary" onClick={deleteCalendar}>
        Delete calendar
      </Button>

      <Typography component="p">
        Back to <Link to={`/${props.calendar.id}/`}>calendar</Link>
      </Typography>
    </div>
  )
}

export default CalendarEdit

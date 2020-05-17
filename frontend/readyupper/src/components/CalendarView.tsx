import React, { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'

import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'

import { fetchCalendar, setTitle } from '../utils'
import Loading from './Loading'
import ErrorMessage from './ErrorMessage'


function CalendarView(props: { Child: Function }) {
  let { calendarId } = useParams()
  let [calendar, setCalendar] = useState()
  let [error, setError] = useState("")

  useEffect(() => fetchCalendar(calendarId, setCalendar, setError), [calendarId])
  useEffect(() => setTitle(calendar), [calendar])

  if (error)
    return <ErrorMessage message={error} />

  if (!calendar)
    return <Loading />

  return (
    <Grid container spacing={4}>
      <Grid item xs={12}>
        <Typography variant="h2" component="h2" align="center">
          { calendar.name }
        </Typography>
      </Grid>

      <Grid item xs={12}>
        <props.Child calendar={calendar} />
      </Grid>

      <Grid item xs={12}>
        <Typography component="p" gutterBottom>
          Back to <Link to="/">frontpage</Link>
        </Typography>
      </Grid>
    </Grid>
  )
}

export default CalendarView

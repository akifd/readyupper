import React, { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
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
    <div>
      <Typography variant="h2" component="h2" gutterBottom align="center">
        { calendar.name }
      </Typography>

      <props.Child calendar={calendar} />

      <Typography component="p" gutterBottom align="center">
        Back to <Link to="/">frontpage</Link>.
      </Typography>
    </div>
  )
}

export default CalendarView

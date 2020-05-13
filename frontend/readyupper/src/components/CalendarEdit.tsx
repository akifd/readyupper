import React from 'react'
import Typography from '@material-ui/core/Typography'
import { Link } from 'react-router-dom'

import { Calendar } from '../interfaces'


function CalendarEdit(props: { calendar: Calendar }) {
  return (
    <div>
      <Typography component="p" gutterBottom align="center">
        Here you can edit the calendar.
      </Typography>

      <Typography component="p" align="center">
        Back to <Link to={`/${props.calendar.id}/`}>calendar</Link>
      </Typography>
    </div>
  )
}

export default CalendarEdit

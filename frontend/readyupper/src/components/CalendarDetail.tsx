import React from 'react'
import Typography from '@material-ui/core/Typography'
import { Link } from 'react-router-dom'

import { Calendar } from '../interfaces'


function CalendarDetail(props: { calendar: Calendar }) {
  return (
    <div>
      <Typography component="p" gutterBottom>
        Copy the link to this page and share it to the participants.
      </Typography>

      <Typography component="p">
        Edit <Link to={`/${props.calendar.id}/edit/`}>calendar</Link>
      </Typography>
    </div>
  )
}

export default CalendarDetail

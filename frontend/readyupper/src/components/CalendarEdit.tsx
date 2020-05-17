import React from 'react'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import { Link } from 'react-router-dom'

import { Calendar } from '../interfaces'


function CalendarEdit(props: { calendar: Calendar }) {
  return (
    <div>
      <Typography component="p">
        Back to <Link to={`/${props.calendar.id}/`}>calendar</Link>
      </Typography>
    </div>
  )
}

export default CalendarEdit

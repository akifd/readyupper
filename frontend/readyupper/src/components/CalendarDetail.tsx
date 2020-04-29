import React, { useState } from 'react'

import Typography from '@material-ui/core/Typography'

import { useParams } from 'react-router-dom'

import axios, { AxiosResponse, AxiosError } from 'axios'


function CalendarDetail() {
  let { urlHash } = useParams()
  let [calendar, setCalendar] = useState()
  let [error, setError] = useState()

  if (!calendar) {
    let promise = axios.get("http://localhost:8000/calendar/" + urlHash)

    promise.then((response: AxiosResponse) => {
      setCalendar(response.data)
    })

    promise.catch((error: AxiosError) => {
      setError("An error occurred. Try loading the page again soon.")
    })

    return <Typography variant="h2" component="h2" gutterBottom align="center">
      { "Loading..." }
    </Typography>
  }

  if (calendar.hasOwnProperty("error"))
    return (
      <div>
        <Typography variant="h2" component="h2" gutterBottom align="center">
          Error!
        </Typography>
        <Typography component="p" align="center">
          { error }
        </Typography>
      </div>
    )

  return (
    <div>
      <Typography variant="h2" component="h2" gutterBottom align="center">
        { calendar.name }
      </Typography>
      <Typography component="p" gutterBottom align="center">
        { urlHash }
      </Typography>
      <Typography component="p" gutterBottom align="center">
        Copy the link to this page and share it to the participants. <br />
      </Typography>
    </div>
  )
}

export default CalendarDetail

import React, { useState, useEffect } from 'react'
import Immutable from 'immutable'
import Typography from '@material-ui/core/Typography'
import { Link, useParams } from 'react-router-dom'
import axios, { AxiosResponse, AxiosError } from 'axios'

import { Calendar } from '../interfaces'


function setTitle(calendar: Calendar): () => void {
  if (calendar)
    document.title = "Readyupper - " + calendar.name

  return function cleanup() {
    document.title = "Readyupper"
  }
}


function fetchData(urlHash: string, data: Immutable.Map<string, Calendar>, setData: Function, setError: Function) {
  let promise = axios.get("http://localhost:8000/calendar/" + urlHash)

  promise.then((response: AxiosResponse) => {
    setData(data.set(urlHash, response.data))
    setTitle(response.data)
  })

  promise.catch((error: AxiosError) => {
    setError("An error occurred. Try loading the page again soon.")
  })
}


function CalendarDetail() {
  let { urlHash } = useParams()
  let [data, setData] = useState(Immutable.Map<string, Calendar>())
  let [error, setError] = useState()
  let calendar: Calendar = data.get(urlHash)

  useEffect(() => {
    return setTitle(calendar)
  })

  if (error) {
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
  }

  if (!calendar) {
    fetchData(urlHash, data, setData, setError)

    return <Typography variant="h2" component="h2" gutterBottom align="center">
      { "Loading..." }
    </Typography>
  }

  return (
    <div>
      <Typography variant="h2" component="h2" gutterBottom align="center">
        { calendar.name }
      </Typography>
      <Typography component="p" gutterBottom align="center">
        { urlHash }
      </Typography>
      <Typography component="p" gutterBottom align="center">
        Copy the link to this page and share it to the participants.
      </Typography>
      <Typography component="p" gutterBottom align="center">
        Back to <Link to="/">frontpage</Link>.
      </Typography>
    </div>
  )
}

export default CalendarDetail

import axios, { AxiosResponse, AxiosError } from 'axios'

import { Calendar } from './interfaces'


export function setTitle(calendar: Calendar): () => void {
  if (calendar)
    document.title = "Readyupper - " + calendar.name

  return function cleanup() {
    document.title = "Readyupper"
  }
}


export function fetchCalendar(calendarId: string, setCalendar: Function, setError: Function) {
  setCalendar(null)

  let promise = axios.get("http://localhost:8000/calendar/" + calendarId + "/")

  promise.then((response: AxiosResponse) => {
    setCalendar(response.data)
  })

  promise.catch((error: AxiosError) => {
    setError("An error occurred. Try loading the page again soon.")
  })
}

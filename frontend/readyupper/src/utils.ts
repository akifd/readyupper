import axios, { AxiosResponse, AxiosError } from 'axios'

import config from './config'
import { Calendar } from './interfaces'


export function backendUrl(path: string) {
    return config.BACKEND_URL + path
}

export function setTitle(calendar: Calendar): () => void {
  if (calendar)
    document.title = "Readyupper - " + calendar.name

  return function cleanup() {
    document.title = "Readyupper"
  }
}


export function fetchCalendar(calendarId: string, setCalendar: Function, setError: Function) {
  setCalendar(null)

  let promise = axios.get(backendUrl("/calendars/" + calendarId + "/"))

  promise.then((response: AxiosResponse) => {
    setCalendar(response.data)
  })

  promise.catch((error: AxiosError) => {
    setError("An error occurred. Try loading the page again soon.")
  })
}


export function deleteCalendar(calendarId: string, setDeleted: Function) {
  var promise = axios.delete(backendUrl("/calendars/" + calendarId + "/"))

  promise.then((response: AxiosResponse) => {
    setDeleted(true)
  })

  promise.catch((error: AxiosError) => {
    // TODO
  })
}


export function createEntry(calendarId: string, timestamp: string) {
  return axios.post(backendUrl('/entries/'), {'calendar_id': calendarId, 'timestamp': timestamp})
}


export function fetchEntries(calendarId: string) {
  return axios.get(backendUrl("/entries/?calendar_id=" + calendarId))
}


export function createParticipant(calendarId: string, name: string) {
  return axios.post(backendUrl('/participants/'), {'calendar_id': calendarId, 'name': name})
}


export function fetchParticipants(calendarId: string) {
  return axios.get(backendUrl("/participants/?calendar_id=" + calendarId))
}

import React, { useState, useEffect } from 'react'
import Typography from '@material-ui/core/Typography'
import { Link } from 'react-router-dom'
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import { Calendar, Participant, Entry } from '../interfaces'
import { fetchEntries, fetchParticipants } from '../utils'
import ErrorMessage from './ErrorMessage'
import ParticipationCheckbox from './ParticipationCheckbox.js'


function CalendarDetail(props: { calendar: Calendar }) {
  let [error, setError] = useState("")
  let [participants, setParticipants] = useState([])
  let [entries, setEntries] = useState([])

  // Participant fetching.
  useEffect(() => {
    async function fetchData() {
      try {
        let response = await fetchParticipants(props.calendar.id)

        if (response.status === 200)
          setParticipants(response.data)
      }
      catch (error) {
        setError("Participant fetching failed.")
      }
    }
    fetchData()
  }, [props.calendar.id])

  // Entry fetching.
  useEffect(() => {
    async function fetchData() {
      try {
        let response = await fetchEntries(props.calendar.id)

        if (response.status === 200) {
          let entries = response.data.map((entry: Entry) => {
            entry.timestamp = new Date(entry.timestamp)
            return entry
          })
          setEntries(entries)
        }
      }
      catch(error) {
        setError("Entry fetching failed.")
      }
    }
    fetchData()
  }, [props.calendar.id])

  if (error)
    return <ErrorMessage message={error} />

  return (
    <div>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              {entries.map((entry: Entry) => (
                <TableCell align="center" key={entry.id}>
                  {entry.timestamp.toLocaleDateString()}<br/>
                  {entry.timestamp.toLocaleTimeString()}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {participants.map((participant: Participant) => (
              <TableRow key={participant.id}>
                <TableCell component="th" scope="row">
                  {participant.name}
                </TableCell>
                {entries.map((entry: Entry) => (
                  <TableCell align="center" key={`${participant.id}-${entry.id}`}>
                    <ParticipationCheckbox calendar={props.calendar} participant={participant} entry={entry} />
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <br />

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

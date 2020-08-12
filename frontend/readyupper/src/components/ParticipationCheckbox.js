import React from 'react'
import Checkbox from '@material-ui/core/Checkbox';

import {fetchParticipation, createParticipation, deleteParticipation} from '../utils'


class ParticipationCheckbox extends React.Component {
  constructor(props) {
    super(props)
    this.state = {participation: null}
  }

  async componentDidMount() {
    // Fetch participation.
    try {
      let response = await fetchParticipation(this.props.calendar.id, this.props.participant.id, this.props.entry.id)

      if (response.status === 200) {
        if (response.data.length > 0)
          this.setState({participation: response.data[0]})
      }
      else if (response.status === 404)
        this.setState({participation: null})
      else
        throw new Error('Response status was not 200, but: ' + response.status)
    }
    catch (error) {
      console.error('Fetching participation failed: ' + error.message)
    }
  }

  async toggleParticipation(event) {
    // Create participation.
    if (this.state.participation === null) {
      try {
        let response = await createParticipation(this.props.calendar.id, this.props.participant.id, this.props.entry.id)

        if (response.status === 200)
          this.setState({participation: response.data})
        else
          throw new Error('Response status was not 200, but: ' + response.status)
      }
      catch (error) {
        console.error('Creating participation failed: ' + error.message)
      }
    }

    // Delete participation.
    else {
      try {
        let response = await deleteParticipation(this.state.participation.id)

        if (response.status === 200)
          this.setState({participation: null})
        else
          throw new Error('Response status was not 200, but: ' + response.status)
      }
      catch (error) {
        console.error('Creating participation failed: ' + error.message)
      }
    }
  }

  render() {
    return <Checkbox onChange={this.toggleParticipation.bind(this)} checked={(this.state.participation) ? true : false} />
  }
}

export default ParticipationCheckbox

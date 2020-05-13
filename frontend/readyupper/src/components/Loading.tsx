import React from 'react'
import { Link } from 'react-router-dom'
import Typography from '@material-ui/core/Typography'


function Loading() {
  return <div>
    <Typography variant="h2" component="h2" gutterBottom align="center">
      { "Loading..." }
    </Typography>
    <Typography component="p" gutterBottom align="center">
      Back to <Link to="/">frontpage</Link>.
    </Typography>
  </div>
}


export default Loading

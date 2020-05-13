import React from 'react'
import { Link } from 'react-router-dom'
import Typography from '@material-ui/core/Typography'


function ErrorMessage(props: { message: string }) {
  return <div>
    <Typography variant="h2" component="h2" gutterBottom align="center">
      Error!
    </Typography>
    <Typography component="p" align="center">
      { props.message }
    </Typography>
    <Typography component="p" gutterBottom align="center">
      Back to <Link to="/">frontpage</Link>.
    </Typography>
  </div>
}


export default ErrorMessage

import React from 'react'
import Typography from '@material-ui/core/Typography'


function ErrorMessage(props: { message: string }) {
  return <div>
    <Typography variant="h2" component="h2" gutterBottom align="center">
      Error!
    </Typography>
    <Typography component="p" align="center">
      { props.message }
    </Typography>
  </div>
}


export default ErrorMessage

import React from 'react';

import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Grid from '@material-ui/core/Grid';


export default function Frontpage() {
  return <Grid container spacing={3}>
    <Grid item sm={12} md={6}>
      <Card>
        <CardContent>
          <Typography component="h2" variant="h4" gutterBottom>
            About
          </Typography>
          <Typography component="p" gutterBottom>
            With Readyupper you can quickly schedule events/meetings by creating a calendar
            and adding datetimes and participants. Share the link and everyone can choose the
            datetimes that are available for them.
          </Typography>
          <ul>
            <li>Free and fast to use</li>
            <li>No registration</li>
            <li>Anyone can edit calendars</li>
          </ul>
          <Typography component="p" gutterBottom>
            Calendars are automatically deleted after 3 months.
          </Typography>
        </CardContent>
      </Card>
    </Grid>
    <Grid item sm={12} md={6}>
      <Card>
        <CardContent>
          <Typography component="h2" variant="h4" gutterBottom>
            Create new calendar
          </Typography>
          <TextField label="Calendar name" variant="filled" fullWidth />
        </CardContent>
        <CardActions>
          <Button variant="contained" color="primary" fullWidth>
            Create calendar
          </Button>
        </CardActions>
      </Card>
    </Grid>
  </Grid>
}

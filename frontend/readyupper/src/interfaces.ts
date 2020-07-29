export interface Calendar {
  id: string,
  name: string,
  created: Date,
}

export interface Participant {
  id: string,
  calendar_id: string,
  name: string,
  created: Date
}

export interface Entry {
  id: string,
  calendar_id: string,
  timestamp: Date,
  created: Date
}

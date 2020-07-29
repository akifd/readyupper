export interface Calendar {
  id: string,
  name: string,
  created: string,
}

export interface Participant {
  id: string,
  calendar_id: string,
  name: string,
  created: string
}

export interface Entry {
  id: string,
  calendar_id: string,
  timestamp: string,
  created: string
}

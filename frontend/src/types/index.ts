export interface Face {
  id: number
  image: string
  skin_color: 'Black' | 'White'
}

export interface UserScore {
  image: number
  numeric: number
  sentiment: string | null
}

export interface Sentiments {
  count: number
  positive: string[]
  negative: string[]
}

export interface SessionCache {
  country: string
  date_of_birth: string
  race: 'Black' | 'White'
  sexe: 'Woman' | 'Man'
}

export type Action = 'get.face' |
  'get.emotions' |
  'get.session_id' |
  'set.session_id' |
  'random.face' |
  'save.score' |
  'scoring.finished' |
  'update.index' |
  'next.level'

export interface WebsocketData {
  action: Action
  data?: Face | Sentiments | Record<string, string | number> | string
  token?: string
  level?: number
  index?: number
}

export interface SendMessageData {
  action: Action
  data?: Face | Record<string, string | number> | string
  face_id?: number
  score?: string | number
  session_id?: string | null
}

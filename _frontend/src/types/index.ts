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

export interface Emotions {
    count: number
    positive: string[]
    negative: string[]
}

export interface WSResponse {
    type: string
}

export interface WSFaceResponse extends WSResponse {
    results: Face[]
    session_id: string
}

export interface WSEmotionsResponse extends WSResponse { }

export interface SessionCache {
    country: string
    date_of_birth: string
    race: 'Black' | 'White'
    sexe: 'Woman' | 'Man'
}

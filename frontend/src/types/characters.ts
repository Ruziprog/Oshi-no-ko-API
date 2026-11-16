
export interface CharacterProfile {
    biography: string
    personality: string
    abilities: string
    relationships: string
    trivia: string
    analysis: string
}

export interface Character {
    id: string
    name: string
    age: number
    description: string | null
    role: string | null
    image_url: string | null
    profile: CharacterProfile | null
}

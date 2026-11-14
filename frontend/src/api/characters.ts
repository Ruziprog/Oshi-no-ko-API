import api from './client'
import type { Character } from '../types/characters'

export async function getCharacters(): Promise<Character[]> {
    const response = await api.get<Character[]>('/characters')

    return response.data
}

export async function getCharacterById(id: string): Promise<Character> {
    const response = await api.get<Character>(`/characters/${id}`)
    return response.data
}
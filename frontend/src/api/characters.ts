import api from './client'
import type { Character } from '../types/characters'

export async function getCharacters(): Promise<Character[]> {
    const response = await api.get<Character[]>('/characters')

    return response.data
}
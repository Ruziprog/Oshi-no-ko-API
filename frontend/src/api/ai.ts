import api from './client'

export interface AIProfileResponse {
    profile: string
}

export async function generateCharacterProfile(
    characterId: string
): Promise<AIProfileResponse> {
    const response = await api.post<AIProfileResponse>(
        `/ai/characters/${characterId}`
    )

    return response.data
}
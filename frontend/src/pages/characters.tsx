
import { useEffect, useState } from 'react'
import { getCharacters } from '../api/characters'
import type { Character } from '../types/characters'
import '../styles/characters.scss'

function Characters() {
    const [characters, setCharacters] = useState<Character[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function fetchCharacters() {
            try {
                const data = await getCharacters()
                setCharacters(data)
            } catch (error) {
                console.error('Failed to fetch characters:', error)
                setError('Failed to load characters.')
            } finally {
                setLoading(false)
            }
        }

        fetchCharacters()
    }, [])

    if (loading) {
        return <main><p>Loading characters...</p></main>
    }

    if (error) {
        return <main><p>{error}</p></main>
    }

    return (
    <main className="characters-page">
        <header className="characters-header">
            <h1>Characters</h1>
            <p>Meet the stars of Oshi no Ko.</p>
        </header>

        {characters.length === 0 ? (
            <p className="empty-message">No characters found.</p>
        ) : (
            <div className="characters-grid">
                {characters.map((character) => (
                    <article className="character-card" key={character.id}>
                        <div className="character-image">
                            {character.image_url ? (
                                <img
                                    src={character.image_url}
                                    alt={character.name}
                                    onError={(event) => {
                                        event.currentTarget.style.display = 'none'
                                    }} 
                                />
                            ) : (
                                <div className="image-placeholder">
                                    No image available
                                </div>
                            )}
                        </div>

                        <div className="character-info">
                            <h2>{character.name}</h2>
                            <span className="character-role">
                                {character.role ?? 'Unknown'}
                            </span>
                            <p className="character-age">
                                Age: {character.age}
                            </p>
                            <p className="character-description">
                                {character.description ?? 'No description.'}
                            </p>
                        </div>
                    </article>
                ))}
            </div>
        )}
    </main>
)
}

export default Characters

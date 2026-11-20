
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getCharacters } from '../api/characters'
import type { Character } from '../types/characters'
import '../styles/characters.scss'


function getCharacterAccentClass(name: string): string {
    const normalized = name.toLowerCase()

    if (normalized.includes('ruby')) return 'character-card--ruby'
    if (normalized.includes('kana')) return 'character-card--kana'
    if (normalized.includes('akane')) return 'character-card--akane'
    if (normalized.includes('aqua')) return 'character-card--aqua'
    if (normalized.includes('memcho')) return 'character-card--memcho'
    if (normalized.includes('ai')) return 'character-card--ai'

    return 'character-card--default'
}


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
        return (
            <main className="characters-page">
                <p className="characters-status">Loading characters...</p>
            </main>
        )
    }

    if (error) {
        return (
            <main className="characters-page">
                <p className="characters-status">{error}</p>
            </main>
        )
    }

    return (
        <main className="characters-page">
            <header className="characters-header">
                <span className="characters-eyebrow">
                    OSHI NO KO DATABASE
                </span>

                <h1>Characters</h1>

                <p>Meet the stars of Oshi no Ko.</p>
            </header>

            {characters.length === 0 ? (
                <p className="empty-message">
                    No characters found.
                </p>
            ) : (
                <div className="characters-grid">
                    {characters.map((character) => (
                        <Link
                            to={`/characters/${character.id}`}
                            className={`character-card ${getCharacterAccentClass(character.name)}`}
                            key={character.id}
                        >
                            <div className="character-image">
                                {character.image_url ? (
                                    <img
                                        src={character.image_url}
                                        alt={character.name}
                                        loading="lazy"
                                        onError={(event) => {
                                            event.currentTarget.style.display = 'none'
                                            event.currentTarget.parentElement?.classList.add('image-failed')
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
                        </Link>
                    ))}
                </div>
            )}
        </main>
    )
}

export default Characters

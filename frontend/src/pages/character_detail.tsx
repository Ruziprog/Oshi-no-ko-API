
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getCharacterById } from '../api/characters'
import type { Character } from '../types/characters'
import '../styles/character_detail.scss'

function CharacterDetail() {
    const { id } = useParams<{ id: string }>()

    const [character, setCharacter] = useState<Character | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function fetchCharacter() {
            if (!id) return

            try {
                const data = await getCharacterById(id)
                setCharacter(data)
            } catch (error) {
                console.error('Failed to fetch character:', error)
                setError('Character not found.')
            } finally {
                setLoading(false)
            }
        }

        fetchCharacter()
    }, [id])

    if (loading) {
        return <main><p>Loading character...</p></main>
    }

    if (error || !character) {
        return <main><p>{error ?? 'Character not found.'}</p></main>
    }

    const profileSections = [
        {
            title: 'Biography',
            content: character.profile?.biography,
        },
        {
            title: 'Personality',
            content: character.profile?.personality,
        },
        {
            title: 'Abilities & Skills',
            content: character.profile?.abilities,
        },
        {
            title: 'Relationships',
            content: character.profile?.relationships,
        },
        {
            title: 'Trivia',
            content: character.profile?.trivia,
        },
        {
            title: 'Character Analysis',
            content: character.profile?.analysis,
        },
    ]

    return (
        <main className="character-detail">
            <section className="character-detail-header">
                <div className="character-detail-image">
                    {character.image_url && (
                        <img
                            src={character.image_url}
                            alt={character.name}
                        />
                    )}
                </div>

                <div className="character-detail-info">
                    <h1>{character.name}</h1>

                    <span className="character-detail-role">
                        {character.role ?? 'Unknown'}
                    </span>

                    <p>Age: {character.age}</p>

                    <p>
                        {character.description ?? 'No description.'}
                    </p>
                </div>
            </section>

            {character.profile && (
                <section className="character-profile">
                    {profileSections.map((section) => (
                        <article
                            className="character-profile-section"
                            key={section.title}
                        >
                            <h2>{section.title}</h2>
                            <p>
                                {section.content ?? 'No information available.'}
                            </p>
                        </article>
                    ))}
                </section>
            )}
        </main>
    )
}

export default CharacterDetail

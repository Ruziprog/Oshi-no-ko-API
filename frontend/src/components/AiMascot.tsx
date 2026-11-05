
import { useEffect, useRef } from 'react'
import './AiMascot.scss'

function AiMascot() {
    const mascotRef = useRef<HTMLDivElement>(null)
    const pupilRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        function handlePointerMove(event: PointerEvent) {
            if (event.pointerType !== 'mouse') return

            const mascot = mascotRef.current
            const pupil = pupilRef.current

            if (!mascot || !pupil) return

            const rect = mascot.getBoundingClientRect()

            // Координаты открытого глаза на изображении
            const eyeX = rect.left + rect.width * 0.413
            const eyeY = rect.top + rect.height * 0.104

            const dx = event.clientX - eyeX
            const dy = event.clientY - eyeY

            const maxMovement = 5

            const x = Math.max(
                -maxMovement,
                Math.min(maxMovement, dx / 35)
            )

            const y = Math.max(
                -maxMovement,
                Math.min(maxMovement, dy / 35)
            )

            pupil.style.setProperty('--pupil-x', `${x}px`)
            pupil.style.setProperty('--pupil-y', `${y}px`)
        }

        window.addEventListener('pointermove', handlePointerMove)

        return () => {
            window.removeEventListener('pointermove', handlePointerMove)
        }
    }, [])

    return (
        <div className="ai-mascot" ref={mascotRef}>
            <img
                src="/hoshino-ai.png"
                alt="Hoshino Ai"
                className="ai-mascot__image"
            />
        </div>
    )
}

export default AiMascot

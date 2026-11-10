
import { useRef, useState } from 'react'
import { useAuth } from '../context/useAuth'
import {
    uploadAvatar,
    deleteAvatar,
    getCurrentUser
} from '../api/auth'
import '../styles/avatar-upload.scss'

function AvatarUpload() {
    const { user, updateUser } = useAuth()

    const inputRef = useRef<HTMLInputElement>(null)

    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [preview, setPreview] = useState<string | null>(null)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')

    if (!user) return null

    function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0]

        if (!file) return

        if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
            setError('Only JPG, PNG and WEBP are allowed.')
            return
        }

        if (file.size > 5 * 1024 * 1024) {
            setError('Maximum file size is 5 MB.')
            return
        }

        setError('')
        setSelectedFile(file)

        if (preview) URL.revokeObjectURL(preview)

        setPreview(URL.createObjectURL(file))
    }

    async function handleSave() {
        if (!selectedFile) return

        try {
            setSaving(true)
            setError('')

            await uploadAvatar(selectedFile)

            const updatedUser = await getCurrentUser()
            updateUser(updatedUser)

            setSelectedFile(null)
            setPreview(null)

            if (inputRef.current) {
                inputRef.current.value = ''
            }
        } catch {
            setError('Failed to upload avatar.')
        } finally {
            setSaving(false)
        }
    }

    async function handleDelete() {
        try {
            setSaving(true)
            setError('')

            await deleteAvatar()

            const updatedUser = await getCurrentUser()
            updateUser(updatedUser)

            setPreview(null)
            setSelectedFile(null)
        } catch {
            setError('Failed to delete avatar.')
        } finally {
            setSaving(false)
        }
    }

    const avatarUrl = user.avatar_url
        ? `http://localhost:8001${user.avatar_url}`
        : null

    return (
        <div className="avatar-upload">
            <input
                ref={inputRef}
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={handleFileChange}
                hidden
            />

            <button
                type="button"
                className="avatar-preview"
                onClick={() => inputRef.current?.click()}
                disabled={saving}
            >
                {preview || avatarUrl ? (
                    <img
                        src={preview || avatarUrl || ''}
                        alt="Avatar"
                    />
                ) : (
                    <span>{user.username.charAt(0).toUpperCase()}</span>
                )}

                <span className="avatar-edit">Edit</span>
            </button>

            {selectedFile && (
                <div className="avatar-actions">
                    <button
                        type="button"
                        onClick={handleSave}
                        disabled={saving}
                    >
                        {saving ? 'Saving...' : 'Save'}
                    </button>

                    <button
                        type="button"
                        onClick={() => {
                            setSelectedFile(null)
                            setPreview(null)
                            setError('')
                            if (inputRef.current) {
                                inputRef.current.value = ''
                            }
                        }}
                        disabled={saving}
                    >
                        Cancel
                    </button>
                </div>
            )}

            {user.avatar_url && !selectedFile && (
                <button
                    type="button"
                    className="avatar-delete"
                    onClick={handleDelete}
                    disabled={saving}
                >
                    Remove avatar
                </button>
            )}

            {error && <p className="avatar-error">{error}</p>}
        </div>
    )
}

export default AvatarUpload

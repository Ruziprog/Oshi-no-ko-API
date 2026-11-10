import { createContext } from 'react'
import type { UserResponse } from '../types/auth'

interface AuthContextType {
    user: UserResponse | null
    loading: boolean
    login: (token: string) => Promise<void>
    logout: () => void
    updateUser: (user: UserResponse) => void
}

export const AuthContext = createContext<AuthContextType | null>(null)
import { createContext } from 'react'
import type { UserResponse } from '../types/auth'

export interface AuthContextType {
  user: UserResponse | null
  loading: boolean
  login: (token: string) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)
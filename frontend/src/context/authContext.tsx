import {
  useEffect,
  useState,
  type ReactNode,
} from 'react'

import type { UserResponse } from '../types/auth'
import { AuthContext } from './auth-Context'
import { getCurrentUser, saveToken } from '../api/auth'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function checkAuth() {
      const token = localStorage.getItem('access_token')

      if (token) {
        try {
          const currentUser = await getCurrentUser()
          setUser(currentUser)
        } catch {
          localStorage.removeItem('access_token')
        }
      }

      setLoading(false)
    }

    checkAuth()
  }, [])

  async function login(token: string) {
    saveToken(token)

    try {
      const currentUser = await getCurrentUser()
      setUser(currentUser)
    } catch (error) {
      localStorage.removeItem('access_token')
      throw error
    }
  }

  function logout() {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
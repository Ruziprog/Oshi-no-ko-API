
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { registerUser } from '../api/auth'

function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    setError('')
    setSuccess('')
    setLoading(true)

    try {
      await registerUser({
        username,
        email,
        password,
      })

      setSuccess('Account created successfully!')
      setUsername('')
      setEmail('')
      setPassword('')
    } catch (err: unknown) {
      if (
        typeof err === 'object' &&
        err !== null &&
        'response' in err
      ) {
        const response = err.response as {
          data?: { detail?: string }
        }

        setError(response.data?.detail ?? 'Registration failed')
      } else {
        setError('Unable to connect to the server')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <main>
      <h1>Create account</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          minLength={3}
          maxLength={50}
          required
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          minLength={5}
          maxLength={72}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Creating account...' : 'Register'}
        </button>
      </form>

      {error && <p>{error}</p>}
      {success && <p>{success}</p>}

      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </main>
  )
}

export default Register


import { useState, type FormEvent } from 'react'
import { loginUser } from '../api/auth'
import { useAuth } from '../context/useAuth'
import '../styles/Login.scss'

function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)

    const { login } = useAuth()

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()

        try {
            const token = await loginUser({
                username,
                password,
            })

            await login(token.access_token)

            alert('Вы вошли в аккаунт!')
        } catch {
            alert('Неверный username или password')
        }
    }

    return (
        <main className="login-page">

            <div className="login-glow login-glow--pink" />
            <div className="login-glow login-glow--purple" />

            <section className="login-card">

                <div className="login-logo">
                    <span>OSHI</span>
                    <span className="logo-no">NO</span>
                    <span className="logo-ko">KO</span>
                </div>

                <h1>Welcome Back</h1>

                <p className="login-subtitle">
                    Your story continues here.
                </p>

                <form onSubmit={handleSubmit}>

                    <div className="login-field">
                        <label htmlFor="username">Username</label>

                        <input
                            id="username"
                            type="text"
                            placeholder="Enter your username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>

                    <div className="login-field">
                        <label htmlFor="password">Password</label>

                        <div className="password-wrapper">
                            <input
                                id="password"
                                type={showPassword ? 'text' : 'password'}
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />

                            <button
                                type="button"
                                className="password-toggle"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? 'Hide' : 'Show'}
                            </button>
                        </div>
                    </div>

                    <button className="login-button" type="submit">
                        LOGIN
                    </button>

                </form>

                <p className="login-footer">
                    OSHI NO KO API
                    <span> • </span>
                    2026
                </p>

            </section>
        </main>
    )
}

export default Login

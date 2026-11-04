import { useState, type FormEvent } from 'react'
import { loginUser, saveToken } from '../api/auth'


function Login() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    try {
    const token = await loginUser({
        username,
        password,
})

saveToken(token.access_token)


        alert('Вы вошли в аккаунт!')
    } catch {
        alert('Неверный username или password')
    }
}

    return (
    <main>
        <h1>Login</h1>

    <form onSubmit={handleSubmit}>
        <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        />

        <div>
    <input
    type={showPassword ? 'text' : 'password'}
    placeholder="Password"
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    required
/>

    <button
    type="button"
    onClick={() => setShowPassword(!showPassword)}
>
    {showPassword ? 'Hide password' : 'Show password'}
    </button>
</div>

        <button type="submit">
        Login
        </button>
    </form>
    </main>
)
}

export default Login
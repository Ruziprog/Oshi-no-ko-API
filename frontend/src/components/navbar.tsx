
import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/useAuth'
import '../styles/navbar.scss'

function Navbar() {
    const { user, loading, logout } = useAuth()

    return (
    <nav className="navbar">
        <NavLink to="/" className="logo">
            <span className="logo-oshi">OSHI</span>{' '}
            <span className="logo-no">NO</span>{' '}
            <span className="logo-ko">KO</span>
        </NavLink>

    <div className="nav-links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/characters">Characters</NavLink>
    </div>

    {!loading && (
        <div className="user-section">
            {user ? (
            <>
            <span>Welcome, {user.username}</span>

            <button onClick={logout}>
                Logout
            </button>
            </>
        ) : (
        <>
            <NavLink to="/register">Register</NavLink>
            <NavLink to="/login">Login</NavLink>
        </>
    )}
        </div>
    )}
    </nav>
)
}

export default Navbar

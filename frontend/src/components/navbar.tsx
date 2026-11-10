import AvatarUpload from './avatarUpload'
import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/useAuth'
import '../styles/navbar.scss'

function Navbar() {
    const { user, loading, logout } = useAuth()

    return (
        <nav className="navbar">

            <NavLink to="/" className="navbar-logo">
                <span className="logo-oshi">OSHI</span>
                <span className="logo-no">NO</span>
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
                            <div className="user-profile">
                                <AvatarUpload />

                                <div className="user-info">
                                    <span className="user-label">
                                        SIGNED IN AS
                                    </span>

                                    <span className="user-name">
                                        {user.username}
                                    </span>
                                </div>

                                <span className="online-indicator" />
                            </div>

                            <button
                                className="logout-button"
                                onClick={logout}
                            >
                                <span>Logout</span>
                                <span className="logout-icon">↗</span>
                            </button>
                        </>
                    ) : (
                        <div className="auth-links">
                            <NavLink to="/register">Register</NavLink>
                            <NavLink to="/login" className="login-nav-button">
                                Login
                            </NavLink>
                        </div>
                    )}

                </div>
            )}

        </nav>
    )
}

export default Navbar

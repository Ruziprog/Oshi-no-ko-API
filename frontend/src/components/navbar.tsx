import {NavLink} from "react-router-dom";

function Navbar() {
    return (
        <nav>
            <NavLink to="/">Home</NavLink>
            <NavLink to="/characters">Characters</NavLink>
            <NavLink to="/register">Register</NavLink>
        </nav>
    )
}

export default Navbar
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/home'
import Characters from './pages/characters'
import Navbar from './components/navbar'
import Register from './pages/register'
import Login from './pages/login'
import { AuthProvider } from './context/authContext'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/characters" element={<Characters />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
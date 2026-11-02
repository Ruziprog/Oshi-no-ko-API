import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/home'
import Characters from './pages/characters'
import Navbar from './components/navbar'
import Register from './pages/register'

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/characters" element={<Characters />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
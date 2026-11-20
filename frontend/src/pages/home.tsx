
import { Link } from 'react-router-dom'
import '../styles/home.scss'

function Home() {
    return (
        <main className="home-page">
            <section className="home-hero">
                <div className="home-content">
                    <span className="home-eyebrow">
                        THE WORLD OF IDOLS
                    </span>

                    <h1>
                        OSHI NO <span>KO</span>
                    </h1>

                    <h2>Behind every star lies a story.</h2>

                    <p>
                        Explore the characters, discover their stories
                        and dive into the world of Oshi no Ko.
                    </p>

                    <Link to="/characters" className="home-button">
                        Explore Characters
                    </Link>
                </div>

                <div className="home-artwork">
                    <img src="/images/ai.webp" alt="Hoshino Ai" />
                </div>
            </section>
        </main>
    )
}

export default Home

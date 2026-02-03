import { useState, useEffect } from 'react';
import { checkHealth } from '../services/api';
import './Resume.css';

interface HealthStatus {
  ollama: boolean;
  vectorstore: boolean;
  documents: number;
}

export default function Resume() {
  const [health, setHealth] = useState<HealthStatus | null>(null);

  useEffect(() => {
    checkHealthStatus();
  }, []);

  const checkHealthStatus = async () => {
    try {
      const response = await checkHealth();
      setHealth({
        ollama: response.ollama_connected,
        vectorstore: response.vectorstore_ready,
        documents: response.documents_loaded,
      });
    } catch (error) {
      console.error('Health check failed:', error);
    }
  };

  return (
    <div className="resume-container">
      <header className="resume-header">
        <div className="header-content">
          <h1>Parker Chen</h1>
          <p className="tagline">Software RD Engineer | AI Application Engineer</p>
          <div className="contact-info">
            <span>airparkchen@gmail.com</span>
            <span>|</span>
            <span>Contact: +886 976342908</span>
          </div>
        </div>
        <div className="system-status">
          <h4>System Status</h4>
          <div className="status-items">
            <div className={`status-item ${health?.ollama ? 'online' : 'offline'}`}>
              <span className="status-dot"></span>
              LLM (Ollama)
            </div>
            <div className={`status-item ${health?.vectorstore ? 'online' : 'offline'}`}>
              <span className="status-dot"></span>
              Vector Store
            </div>
            <div className={`status-item ${health?.documents ? 'online' : 'offline'}`}>
              <span className="status-dot"></span>
              Documents: {health?.documents || 0}
            </div>
          </div>
        </div>
      </header>

      <main className="resume-content">
        <section className="section">
          <h2>About This Project</h2>
          <div className="project-info">
            <p>
              This is a demonstration of a <strong>Local LLM RAG System</strong> for resume Q&A.
              The chatbot in the bottom-right corner can answer questions about my resume using:
            </p>
            <ul>
              <li><strong>Ollama</strong> - Local LLM deployment (qwen3:1.7b)</li>
              <li><strong>LangChain</strong> - RAG framework for document retrieval</li>
              <li><strong>ChromaDB</strong> - Vector database for semantic search</li>
              <li><strong>FastAPI</strong> - Backend API server</li>
              <li><strong>React</strong> - Frontend UI</li>
            </ul>
            <p className="highlight">
              Click the chat button to ask questions about my experience, skills, or education!
            </p>
          </div>
        </section>

        <section className="section">
          <h2>Professional Experience</h2>
          <div className="experience-item">
            <div className="exp-header">
              <h3>Software Engineer</h3>
              <span className="date">2022 - Present</span>
            </div>
            <p className="company">Tech Company Inc.</p>
            <ul>
              <li>Developed and maintained full-stack applications using Python and React</li>
              <li>Implemented machine learning pipelines and AI-powered features</li>
              <li>Collaborated with cross-functional teams to deliver high-quality products</li>
            </ul>
          </div>
          <div className="experience-item">
            <div className="exp-header">
              <h3>Junior Developer</h3>
              <span className="date">2020 - 2022</span>
            </div>
            <p className="company">Startup Ltd.</p>
            <ul>
              <li>Built RESTful APIs and microservices architecture</li>
              <li>Participated in code reviews and agile development practices</li>
            </ul>
          </div>
        </section>

        <section className="section">
          <h2>Technical Skills</h2>
          <div className="skills-grid">
            <div className="skill-category">
              <h4>Languages</h4>
              <div className="skill-tags">
                <span className="tag">Python</span>
                <span className="tag">TypeScript</span>
                <span className="tag">JavaScript</span>
                <span className="tag">SQL</span>
              </div>
            </div>
            <div className="skill-category">
              <h4>AI/ML</h4>
              <div className="skill-tags">
                <span className="tag">LangChain</span>
                <span className="tag">Ollama</span>
                <span className="tag">RAG</span>
                <span className="tag">LLM</span>
              </div>
            </div>
            <div className="skill-category">
              <h4>Frameworks</h4>
              <div className="skill-tags">
                <span className="tag">React</span>
                <span className="tag">FastAPI</span>
                <span className="tag">Node.js</span>
              </div>
            </div>
            <div className="skill-category">
              <h4>Tools</h4>
              <div className="skill-tags">
                <span className="tag">Git</span>
                <span className="tag">Docker</span>
                <span className="tag">Linux</span>
              </div>
            </div>
          </div>
        </section>

        <section className="section">
          <h2>Education</h2>
          <div className="education-item">
            <div className="exp-header">
              <h3>Bachelor's Degree in Computer Science</h3>
              <span className="date">2016 - 2020</span>
            </div>
            <p className="company">University Name</p>
          </div>
        </section>
      </main>

      <footer className="resume-footer">
        <p>
          This resume is powered by a local LLM. Try the chatbot to learn more!
        </p>
      </footer>
    </div>
  );
}

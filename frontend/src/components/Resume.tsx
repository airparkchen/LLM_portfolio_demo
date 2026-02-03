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
        <div className="header-left">
          <div className="name-block">
            <h1 className="name">Parker Chen</h1>
            <div className="name-sub">陳重瑜 · Taipei, Neihu</div>
          </div>

          <p className="tagline">
            AI Application R&amp;D Engineer · Algorithm / System Integration
          </p>

          <div className="contact-info">
            <span>airparkchen@gmail.com</span>
            <span className="sep">|</span>
            <span>+886 976-342-908</span>
            <span className="sep">|</span>
            <span>TOEIC 830</span>
          </div>

          <div className="headline">
            Currently at Pegatron (Core Technology R&amp;D Center). Focus: product-oriented AI
            algorithm research, cross-domain system integration (AI + Android/AOSP + DSP/BSP collaboration).
          </div>
        </div>

        <div className="header-right">
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
            <div className="status-hint">
              Ask the chatbot about projects, algorithms, Android/AOSP, or research.
            </div>
          </div>
        </div>
      </header>

      <main className="resume-content">
        {/* TOP GRID: Profile + Project / RAG Info */}
        <section className="grid-2">
          <section className="card section">
            <h2>Profile</h2>
            <p>
              AI Application R&amp;D Engineer with hands-on experience in product-oriented AI solutions and
              cross-functional system integration. Work covers experiment design, data collection/analysis,
              ML/DL algorithm planning &amp; implementation, and Android system-level development/testing.
            </p>
            <ul className="bullets">
              <li>
                Headphone-related AI: physiological-signal-driven music recommendation &amp; dynamic EQ adjustment.
              </li>
              <li>
                Android system: AOSP/Framework debugging, XTS workflows (CTS/VTS), system integration with BSP/DSP.
              </li>
              <li>
                Research background: Robust interactive hand pose estimation (2.5D) with Vision Transformer enhancements.
              </li>
            </ul>
          </section>

          <section className="card section">
            <h2>About This Site (Local LLM Resume Q&amp;A)</h2>
            <p>
              This website demonstrates a <strong>local LLM + RAG</strong> workflow for resume Q&amp;A.
              The chatbot retrieves chunks from my resume docs and answers with citations.
            </p>
            <div className="tech-stack">
              <div className="pill">Ollama (local)</div>
              <div className="pill">LangChain (RAG)</div>
              <div className="pill">ChromaDB (vector store)</div>
              <div className="pill">FastAPI (backend)</div>
              <div className="pill">React (frontend)</div>
            </div>
            <p className="highlight">
              Tip: ask “Tell me about the EQ direction learning approach” or “What did you do in AOSP/XTS testing?”
            </p>
          </section>
        </section>

        {/* KEY PROJECTS */}
        <section className="section">
          <h2>Key Projects</h2>

          <div className="card project">
            <div className="row">
              <h3>Physiological-Signal-Driven Music Recommendation &amp; EQ Adjustment (Headphone Product)</h3>
              <span className="meta">Product-oriented research · Pegatron</span>
            </div>
            <ul className="bullets">
              <li>Designed experiment flow (baseline / stimulus / washout) and data structure for sustainable retraining.</li>
              <li>Recommendation approaches: SVD latent factor, user clustering with effect mapping.</li>
              <li>Dynamic EQ: direction / ranking style learning framework (ongoing experiments).</li>
              <li>Music feature analysis + statistical validation (ANOVA, t-test, frequency analysis) to verify hypotheses.</li>
              <li>Collaboration with BSP/DSP teams for device-side integration and data pipeline readiness.</li>
            </ul>
          </div>

          <div className="card project">
            <div className="row">
              <h3>Android System Development &amp; Compatibility Testing</h3>
              <span className="meta">AOSP/Framework · XTS (CTS/VTS)</span>
            </div>
            <ul className="bullets">
              <li>Owned XTS workflow execution (CTS/VTS) and issue triage for Android compatibility compliance.</li>
              <li>Framework-level modifications and system-level debugging/performance optimization.</li>
            </ul>
          </div>

          <div className="card project">
            <div className="row">
              <h3>Robot Reinforcement Learning (Quadruped)</h3>
              <span className="meta">Isaac Gym · paper reproduction</span>
            </div>
            <ul className="bullets">
              <li>Reproduced RL papers and trained/evaluated policies using Isaac Gym.</li>
              <li>Focused on training workflow, validation, and experiment iteration.</li>
            </ul>
          </div>

          <div className="card project">
            <div className="row">
              <h3>Cross-Platform App Productization</h3>
              <span className="meta">Flutter · API integration · firmware collaboration</span>
            </div>
            <ul className="bullets">
              <li>Built product-level cross-platform app (Android/iOS) using Flutter.</li>
              <li>Implemented API integrations and supported firmware-level debugging for end-to-end stability.</li>
            </ul>
          </div>
        </section>

        {/* EXPERIENCE */}
        <section className="section">
          <h2>Experience</h2>

          <div className="experience-item card">
            <div className="exp-header">
              <div>
                <h3>AI Application R&amp;D Engineer (Algorithm Engineer)</h3>
                <p className="company">Pegatron Corporation · Core Technology R&amp;D Center</p>
              </div>
              <span className="date">2025/01 – Present</span>
            </div>
            <ul className="bullets">
              <li>Product-driven AI/DL/ML research &amp; implementation: from problem framing to model delivery.</li>
              <li>Experiment planning, data collection/analysis, algorithm design, and cross-team integration.</li>
              <li>Worked closely with BSP team on DSP/device-side integration and system troubleshooting.</li>
            </ul>
          </div>

          <div className="experience-item card">
            <div className="exp-header">
              <div>
                <h3>Graduate Research Assistant / Teaching Assistant</h3>
                <p className="company">National Taiwan Ocean University · Institute of Intelligent Living Technology</p>
              </div>
              <span className="date">2022/09 – 2024/08</span>
            </div>
            <ul className="bullets">
              <li>Research topic: Robust Interactive Hand Pose Estimation (2.5D), handling occlusion &amp; ambiguity.</li>
              <li>Vision Transformer enhancement (specialized token), algorithm integration, occlusion-aware augmentation.</li>
              <li>Maintained Linux server/NAS and supported lab projects and junior mentoring.</li>
            </ul>
          </div>

          <div className="experience-item card">
            <div className="exp-header">
              <div>
                <h3>Software Engineer (Quant Trading System Ops &amp; Optimization)</h3>
                <p className="company">Changyu International Co., Ltd.</p>
              </div>
              <span className="date">2021/11 – 2022/01</span>
            </div>
            <ul className="bullets">
              <li>Maintained and optimized a quant trading system for crypto platform operations.</li>
              <li>Refactored code for efficiency; built monitoring (web/Telegram) for operational visibility.</li>
            </ul>
          </div>
        </section>

        {/* EDUCATION */}
        <section className="section">
          <h2>Education</h2>

          <div className="education-item card">
            <div className="exp-header">
              <div>
                <h3>M.S., Electrical Engineering</h3>
                <p className="company">National Taiwan Ocean University</p>
              </div>
              <span className="date">2022/09 – 2024/09</span>
            </div>
            <p className="note">
              Focus: Intelligent Living Technology · 2.5D hand pose estimation · Vision Transformer improvements.
            </p>
          </div>

          <div className="education-item card">
            <div className="exp-header">
              <div>
                <h3>B.S., Electrical Engineering</h3>
                <p className="company">National Taiwan Ocean University</p>
              </div>
              <span className="date">2017/09 – 2022/09</span>
            </div>
          </div>
        </section>

        {/* SKILLS */}
        <section className="section">
          <h2>Technical Skills</h2>

          <section className="grid-2">
            <div className="card skill-category">
              <h4>AI / ML</h4>
              <div className="skill-tags">
                <span className="tag">Machine Learning</span>
                <span className="tag">Deep Learning</span>
                <span className="tag">Recommendation (SVD)</span>
                <span className="tag">Clustering</span>
                <span className="tag">Ranking / Direction Learning</span>
                <span className="tag">Reinforcement Learning</span>
                <span className="tag">Isaac Gym</span>
                <span className="tag">Statistical Analysis (ANOVA / t-test)</span>
              </div>
            </div>

            <div className="card skill-category">
              <h4>System / App</h4>
              <div className="skill-tags">
                <span className="tag">Android AOSP</span>
                <span className="tag">Android Framework</span>
                <span className="tag">XTS (CTS/VTS)</span>
                <span className="tag">Flutter</span>
                <span className="tag">API Integration</span>
                <span className="tag">Firmware Debugging</span>
                <span className="tag">System Integration</span>
              </div>
            </div>

            <div className="card skill-category">
              <h4>Programming</h4>
              <div className="skill-tags">
                <span className="tag">Python</span>
                <span className="tag">C/C++</span>
                <span className="tag">Java</span>
                <span className="tag">TypeScript</span>
                <span className="tag">Linux</span>
                <span className="tag">Git / GitHub</span>
              </div>
            </div>

            <div className="card skill-category">
              <h4>Data / Signal</h4>
              <div className="skill-tags">
                <span className="tag">Feature Engineering</span>
                <span className="tag">Data Analysis</span>
                <span className="tag">PPG / HRV</span>
                <span className="tag">Experiment Design</span>
              </div>
            </div>
          </section>
        </section>

        {/* CERTS & LINKS */}
        <section className="section">
          <h2>Certifications &amp; Links</h2>
          <div className="card">
            <ul className="bullets">
              <li>Generative AI capability certification (as listed in resume attachments).</li>
              <li>
                GitHub: personal projects and scripts (computer vision projects, automation scripts).
              </li>
            </ul>
            <p className="note">
              If you want, I can add a “Selected Works” section once you provide the portfolio/project PDF (作品集) content.
            </p>
          </div>
        </section>
      </main>

      <footer className="resume-footer">
        <p>
          Local LLM-powered resume Q&amp;A. Use the chatbot to explore experience and project details.
        </p>
      </footer>
    </div>
  );
}

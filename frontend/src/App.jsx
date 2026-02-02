import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import {
  ChevronRight, Check, Globe, Briefcase, MapPin, GraduationCap,
  ArrowLeft, Download, RefreshCw, DollarSign, TrendingUp, ShieldCheck
} from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5000/api";

// --- ANIMATION VARIANTS ---
const pageVariants = {
  initial: { opacity: 0, x: 20 },
  in: { opacity: 1, x: 0 },
  out: { opacity: 0, x: -20 }
};

const pageTransition = { type: 'tween', ease: 'anticipate', duration: 0.5 };

// --- 1. ONBOARDING SCREEN ---
const Onboarding = ({ onNext }) => (
  <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="page-container">
    <nav className="navbar">
      <h1 className="logo">Global Pathways AI</h1>
      <div className="nav-links">
        <button>About</button>
        <button>Features</button>
        <button className="btn-secondary">Login</button>
        <button className="btn-black" onClick={onNext}>Get Started</button>
      </div>
    </nav>

    <div className="hero-section">
      <div className="hero-content">
        <h1>Plan your education and career with data, not guesswork.</h1>
        <p>An AI-assisted decision support system helping you navigate education and career choices between India and abroad.</p>
        <div className="hero-actions">
          <button className="btn-black-lg" onClick={onNext}>Get Started <ChevronRight size={20} /></button>
          <button className="btn-outline-lg">How it Works <ChevronRight size={20} /></button>
        </div>
      </div>

      <div className="hero-visual">
        <div className="glass-card">
          <div className="card-header">Preferences</div>
          <div className="row"><span>Budget</span> <strong>20-30L</strong></div>
          <div className="row"><span>Field</span> <strong>Science</strong></div>
          <div className="divider"></div>
          <div className="card-header">Comparison</div>
          <div className="row">🇨🇦 Canada <span className="tag-green">High ROI</span></div>
          <div className="row">🇩🇪 Germany <span className="tag-yellow">Med ROI</span></div>
        </div>
      </div>
    </div>

    <div className="steps-section">
      <h3>How it works</h3>
      <div className="steps-grid">
        <div className="step-pill">Answer Questions</div>
        <div className="step-pill">AI Evaluation</div>
        <div className="step-pill">Get Recommendations</div>
      </div>
    </div>
  </motion.div>
);

// --- 2. GOAL SELECTION ---
const GoalSelection = ({ onNext, setGoal }) => {
  const [selected, setSelected] = useState(null);

  const handleSelect = (id) => {
    setSelected(id);
    setGoal(id);
  };

  const Option = ({ id, icon: Icon, title, desc }) => (
    <div
      className={`goal-card ${selected === id ? 'selected' : ''}`}
      onClick={() => handleSelect(id)}
    >
      <div className="icon-box"><Icon size={24} /></div>
      <div className="goal-text">
        <h4>{title}</h4>
        <p>{desc}</p>
      </div>
      {selected === id && <div className="check-badge"><Check size={14} color="white" /></div>}
    </div>
  );

  return (
    <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
      <div className="question-container">
        <h2>What is your Primary Goal?</h2>
        <p className="subtext">Choose one option to personalize your pathway</p>

        <div className="goals-grid">
          <Option id="study_abroad" icon={Globe} title="Study Abroad" desc="Explore global universities & programs" />
          <Option id="work_abroad" icon={Briefcase} title="Work Abroad" desc="Find international jobs & visa paths" />
          <Option id="study_local" icon={GraduationCap} title="Study Local" desc="Top universities near you" />
          <Option id="work_local" icon={MapPin} title="Work Local" desc="Career options in your region" />
        </div>

        <div className="footer-action">
          <button className="btn-black wide" disabled={!selected} onClick={onNext}>Continue <ChevronRight size={18} /></button>
        </div>
      </div>
    </motion.div>
  );
};

// --- 3. USER INPUTS (ADAPTIVE) ---
const UserInputs = ({ onNext, goal, updateData, onEvaluate, loading }) => {
  const [form, setForm] = useState({
    goal: goal,
    stream: 'Science',
    marks: 85,
    budget: '20-30L',
    interest: 'Technology',
    risk: 'Medium',
    experience: '2',
    skills: 'Software Engineering',
    industry: 'Technology'
  });

  const Toggle = ({ label, value, group }) => (
    <button
      className={`toggle-btn ${form[group] === value ? 'active' : ''}`}
      onClick={() => setForm({ ...form, [group]: value })}
    >
      {label}
    </button>
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    updateData(form);
    onEvaluate(form);
  };
  const renderFormFields = () => {
    if (goal === 'study_abroad' || goal === 'study_local') {
      return (
        <>
          <div className="input-group">
            <label>Academic Stream</label>
            <div className="toggles">
              {['Science', 'Commerce', 'Arts'].map(s => <Toggle key={s} label={s} value={s} group="stream" />)}
            </div>
          </div>
          <div className="input-group">
            <label>12th Percentage: {form.marks}%</label>
            <input type="range" min="40" max="100" className="w-full accent-black" value={form.marks} onChange={(e) => setForm({ ...form, marks: parseInt(e.target.value) })} />
          </div>
          <div className="input-group">
            <label>Budget Range</label>
            <div className="toggles">
              {['5-10L', '10-20L', '20-30L', '30-50L', '50L+'].map(b => <Toggle key={b} label={b} value={b} group="budget" />)}
            </div>
          </div>
        </>
      );
    } else {
      return (
        <>
          <div className="input-group">
            <label>Industry</label>
            <div className="toggles">
              {['Technology', 'Medicine', 'Business', 'Finance', 'Engineering'].map(i => <Toggle key={i} label={i} value={i} group="industry" />)}
            </div>
          </div>
          <div className="input-group">
            <label>Current Skills</label>
            <input className="text-input" placeholder="e.g. Java, Management, Nursing" value={form.skills} onChange={(e) => setForm({ ...form, skills: e.target.value })} />
          </div>
          <div className="input-group">
            <label>Years of Experience: {form.experience}yr</label>
            <input type="range" min="0" max="20" className="w-full accent-black" value={form.experience} onChange={(e) => setForm({ ...form, experience: e.target.value })} />
          </div>
        </>
      );
    }
  };

  return (
    <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
      <div className="form-card">
        <h2>{goal.replace('_', ' ').toUpperCase()} Path</h2>
        <p className="subtext">Tell us your current profile for AI analysis.</p>

        {renderFormFields()}

        <div className="input-group">
          <label>Risk Appetite</label>
          <div className="toggles">
            {['Low', 'Medium', 'High'].map(r => <Toggle key={r} label={r} value={r} group="risk" />)}
          </div>
        </div>

        <button className="btn-black wide" onClick={handleSubmit} disabled={loading}>
          {loading ? "Analyzing Pathway..." : "Evaluate Pathway"}
        </button>
      </div>
    </motion.div>
  );
};

// --- 4. COMPARISON TABLE ---
const ComparisonTable = ({ onNext, staticData, results }) => (
  <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
    <div className="wide-card">
      <div className="card-header-row">
        <h2>Perspective Comparison</h2>
        <div className="badges">
          <span className="badge">Pathway: {results?.goal?.replace('_', ' ')}</span>
          <span className="badge">Risk: {results?.risk || 'Medium'}</span>
        </div>
      </div>

      <table className="modern-table">
        <thead>
          <tr>
            <th>Metric / Factor</th>
            <th>Domestic Focus (India)</th>
            <th>Global Focus (Abroad)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Entry Difficulty</td>
            <td>High (Competitive Exams)</td>
            <td>Medium (Assessment Based)</td>
          </tr>
          <tr>
            <td>Academic Focus</td>
            <td>Theory & Marks</td>
            <td>Application & Research</td>
          </tr>
          <tr>
            <td>Exp. Investment</td>
            <td>{results?.goal?.includes('study') ? '5L - 15L' : 'Minimal'}</td>
            <td>{results?.recommendation?.roi?.cost?.toLocaleString() || '25L+'}</td>
          </tr>
          <tr className="highlight-row">
            <td><strong>AI Verdict</strong></td>
            <td colSpan="2" className="text-center">
              <div style={{
                background: '#2563EB',
                color: 'white',
                padding: '12px',
                borderRadius: '12px',
                display: 'inline-block',
                boxShadow: '0 4px 12px rgba(37,99,235,0.2)'
              }}>
                <strong style={{ fontSize: '18px' }}>
                  {results?.decision === 'Stay in India' ? 'Domestic Tier-1 Path' : results?.decision}
                </strong>
              </div>
              <div style={{ fontSize: '12px', color: '#666', marginTop: '10px', fontWeight: '500' }}>
                Analysis Confidence: {results?.confidence}% • Data-Driven Comparison
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div className="right-align">
        <button className="btn-black" onClick={onNext}>View My Personalized Plan <ChevronRight size={16} /></button>
      </div>
    </div>
  </motion.div>
);

// --- 5. PATHWAY DETAILS ---
const PathwayDetails = ({ onNext, results }) => (
  <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
    <div className="wide-card">
      <h2>Pathway Verdict</h2>

      <div className="recommendation-hero">
        <div className="match-badge"><Check size={14} /> Best match ★</div>
        <div className="rec-content">
          <h3>{results?.recommendation?.country}</h3>
          <p>{results?.university_comparison}</p>
        </div>
        <div className="rec-stats">
          <div className="stat"><span>Est. Budget</span><strong>{results?.recommendation?.roi?.cost}</strong></div>
          <div className="stat"><span>Avg Salary</span><strong>{results?.recommendation?.roi?.salary}</strong></div>
          <div className="stat"><span>AI Confidence</span><strong>{results?.confidence}%</strong></div>
          <div className="stat"><span>ROI</span><strong className="text-green">{results?.recommendation?.roi?.label}</strong></div>
        </div>
      </div>

      <div className="reasons-list">
        <h4>Key Insights</h4>
        <div className="reason-pill shadow-sm">✔ Visa/Compliance: {results?.visa_summary}</div>
        <div className="reason-pill shadow-sm">✔ Required Exams: {results?.exams?.abroad || "Certifications"}</div>
        <div className="reason-pill shadow-sm">✔ Market Growth: {results?.insights?.growth}</div>
      </div>

      <div className="action-row-center">
        <button className="btn-black" onClick={onNext}>Generate Final Report</button>
        <button className="btn-outline" onClick={() => window.location.reload()}>Start Over</button>
      </div>
    </div>
  </motion.div>
);

// --- 6. DETAILED REPORT ---
const DetailedReport = ({ onReset, results }) => (
  <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
    <div className="wide-card">
      <button className="back-btn" onClick={onReset}><ArrowLeft size={16} /> Back to dashboard</button>

      <div className="report-header">
        <div className="header-left">
          <h1>{results?.recommendation?.country} Analysis</h1>
          <p>{results?.decision}</p>
        </div>
        <div className="match-badge-black">Verified Analysis</div>
      </div>

      <div className="metrics-grid">
        <div className="metric-box"><DollarSign size={20} /><h3>{results?.recommendation?.roi?.score}x</h3><p>ROI Score</p></div>
        <div className="metric-box"><Briefcase size={20} /><h3>{results?.insights?.growth}</h3><p>Career Growth</p></div>
        <div className="metric-box"><ShieldCheck size={20} /><h3>{results?.confidence}%</h3><p>AI Stability</p></div>
        <div className="metric-box"><TrendingUp size={20} /><h3>{results?.insights?.salary_range}</h3><p>Salary Outlook</p></div>
      </div>

      <div className="breakdown-container">
        <div className="cost-breakdown">
          <h4>Profile Summary</h4>
          <div className="receipt">
            <div className="line"><span>Criteria</span><span>{results?.cutoff_criteria}</span></div>
            <div className="line"><span>Visa Policy</span><span>{results?.visa_summary}</span></div>
          </div>
        </div>
        <div className="report-reasons">
          <h4>Why this works for you</h4>
          <div className="reason-pill">✔ Alignment with {results?.goal?.replace('_', ' ')} goals</div>
          <div className="reason-pill">✔ {results?.insights?.scholarship_chance !== "N/A" ? "Scholarship Available" : "Direct Placement Route"}</div>
        </div>
      </div>

      <div className="final-actions">
        <button className="btn-black" onClick={() => window.print()}>Save PDF Report</button>
        <button className="btn-gray" onClick={onReset}><RefreshCw size={16} /> New Analysis</button>
      </div>
    </div>
  </motion.div>
);

// --- MAIN APP COMPONENT ---
function App() {
  const [step, setStep] = useState(0);
  const [data, setData] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [staticData, setStaticData] = useState(null);

  const next = () => setStep(s => s + 1);
  const reset = () => {
    setStep(0);
    setResults(null);
  };

  useEffect(() => {
    axios.get(`${API_BASE}/static-data`).then(res => setStaticData(res.data)).catch(console.error);
  }, []);

  const handleEvaluate = async (formData) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/evaluate`, { ...formData, goal: data.goal });
      setResults({ ...res.data, goal: data.goal });
      setLoading(false);
      next();
    } catch (err) {
      console.error(err);
      setLoading(false);
      alert("Evaluation failed. Make sure the backend is active.");
    }
  };

  return (
    <div className="app-wrapper">
      <AnimatePresence mode='wait'>
        {step === 0 && <Onboarding onNext={next} />}
        {step === 1 && <GoalSelection onNext={next} setGoal={(g) => setData({ ...data, goal: g })} />}
        {step === 2 && <UserInputs onNext={next} goal={data.goal} updateData={(d) => setData({ ...data, ...d })} onEvaluate={handleEvaluate} loading={loading} />}
        {step === 3 && <ComparisonTable onNext={next} staticData={staticData} results={results} />}
        {step === 4 && <PathwayDetails onNext={next} results={results} />}
        {step === 5 && <DetailedReport onReset={reset} results={results} />}
      </AnimatePresence>
    </div>
  );
}

export default App;

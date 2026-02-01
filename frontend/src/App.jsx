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

// --- 3. USER INPUTS (ADAPTED FOR ML) ---
const UserInputs = ({ onNext, updateData, onEvaluate, loading }) => {
  const [form, setForm] = useState({
    stream: 'Science',
    marks: 85,
    budget: '20-30L',
    interest: 'Technology',
    risk: 'Medium'
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

  return (
    <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
      <div className="form-card">
        <h2>Plan Your Future Path</h2>
        <p className="subtext">Tell us your academic and financial preferences for the AI to analyze.</p>

        <div className="input-group">
          <label>Academic Stream</label>
          <div className="toggles">
            {['Science', 'Commerce', 'Arts'].map(s => <Toggle key={s} label={s} value={s} group="stream" />)}
          </div>
        </div>

        <div className="input-group">
          <label>12th Percentage: {form.marks}%</label>
          <input
            type="range" min="40" max="100"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-black"
            value={form.marks}
            onChange={(e) => setForm({ ...form, marks: parseInt(e.target.value) })}
          />
        </div>

        <div className="input-group">
          <label>Total Budget Range</label>
          <div className="toggles">
            {['5-10L', '10-20L', '20-30L', '30-50L', '50L+'].map(b => <Toggle key={b} label={b} value={b} group="budget" />)}
          </div>
        </div>

        <div className="input-group">
          <label>Primary Interest</label>
          <div className="toggles">
            {['Technology', 'Business', 'Medicine', 'Arts', 'Research'].map(i => <Toggle key={i} label={i} value={i} group="interest" />)}
          </div>
        </div>

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
        <h2>Compare Global Entrance Benchmarks</h2>
        <div className="badges">
          <span className="badge">Budget: {results?.budget || 'N/A'}</span>
          <span className="badge">Field: {results?.stream || 'N/A'}</span>
        </div>
      </div>

      <table className="modern-table">
        <thead>
          <tr>
            <th>Stream/Field</th>
            <th>India Focus</th>
            <th>Global Focus</th>
          </tr>
        </thead>
        <tbody>
          {staticData?.exams?.map((row, i) => (
            <tr key={i}>
              <td>{row.field}</td>
              <td>{row.india}</td>
              <td>{row.abroad}</td>
            </tr>
          ))}
          <tr className="highlight-row">
            <td><strong>AI Suggestion</strong></td>
            <td colSpan="2"><strong>{results?.decision || "Evaluating..."} ({results?.confidence}%)</strong></td>
          </tr>
        </tbody>
      </table>

      <div className="right-align">
        <button className="btn-black" onClick={onNext}>View My Best Match</button>
      </div>
    </div>
  </motion.div>
);

// --- 5. PATHWAY DETAILS ---
const PathwayDetails = ({ onNext, results }) => (
  <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
    <div className="wide-card">
      <h2>Your Recommended Pathway</h2>
      <p className="subtext">Based on your Budget, Career Interests, and Academic Profile</p>

      {results?.recommendation ? (
        <div className="recommendation-hero">
          <div className="match-badge"><Check size={14} /> Best match ★</div>
          <div className="rec-content">
            <h3>{results.recommendation.country}</h3>
            <p>Target Tier-1 Universities in {results.recommendation.country}</p>
          </div>
          <div className="rec-stats">
            <div className="stat"><span>Est. Cost</span><strong>₹{results.recommendation.roi.cost.toLocaleString()}</strong></div>
            <div className="stat"><span>Exp Salary</span><strong>₹{results.recommendation.roi.salary.toLocaleString()}</strong></div>
            <div className="stat"><span>AI Confidence</span><strong>{results.confidence}%</strong></div>
            <div className="stat"><span>ROI</span><strong className="text-green">{results.recommendation.roi.label}</strong></div>
          </div>
        </div>
      ) : (
        <div className="recommendation-hero pink-bg" style={{ color: '#831843' }}>
          <div className="rec-content">
            <h3>Stay in India</h3>
            <p>The models suggest that high-tier Indian universities offer better immediate ROI for your profile.</p>
          </div>
          <div className="rec-stats">
            <div className="stat"><span>AI Confidence</span><strong>{results?.confidence}%</strong></div>
          </div>
        </div>
      )}

      <div className="reasons-list">
        <h4>Analysis & Next Steps</h4>
        <div className="reason-pill">✔ {results?.visa_summary}</div>
        <div className="reason-pill">✔ Recommended Exams (India): {results?.exams.india}</div>
        <div className="reason-pill">✔ Recommended Exams (Abroad): {results?.exams.abroad}</div>
      </div>

      <div className="secondary-options">
        <h4>University Comparison</h4>
        <div className="secondary-card pink-bg">
          {results?.university_comparison}
        </div>
      </div>

      <div className="action-row-center">
        <button className="btn-black" onClick={onNext}>View Detailed Plan</button>
        <button className="btn-outline" onClick={() => window.location.reload()}>Evaluate Again</button>
      </div>
    </div>
  </motion.div>
);

// --- 6. DETAILED REPORT ---
const DetailedReport = ({ onReset, results }) => (
  <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} className="centered-layout">
    <div className="wide-card">
      <button className="back-btn" onClick={() => onReset()}><ArrowLeft size={16} /> Back to beginning</button>

      <div className="report-header">
        <div className="header-left">
          <h1>{results?.recommendation?.country || "Indian Pathway"}</h1>
          <p>Detailed AI Analysis Report</p>
        </div>
        <div className="match-badge-black">Final Verdict ★</div>
      </div>

      <div className="metrics-grid">
        <div className="metric-box"><DollarSign size={20} /><h3>{results?.recommendation?.roi.score || "N/A"}x</h3><p>5-Year ROI Factor</p></div>
        <div className="metric-box"><Briefcase size={20} /><h3>{results?.insights.growth}</h3><p>Career Growth</p></div>
        <div className="metric-box"><ShieldCheck size={20} /><h3>{results?.confidence}%</h3><p>Model Confidence</p></div>
        <div className="metric-box"><TrendingUp size={20} /><h3>{results?.insights.scholarship_chance}</h3><p>Scholarship Chance</p></div>
      </div>

      <div className="breakdown-container">
        <div className="cost-breakdown">
          <h4>Entrance Criteria</h4>
          <div className="receipt">
            <div className="line"><span>Benchmarks</span></div>
            <div className="text-sm text-text-sub mt-2 leading-relaxed" style={{ fontSize: '12px', color: '#666' }}>
              {results?.cutoff_criteria}
            </div>
          </div>
        </div>

        <div className="report-reasons">
          <h4>Why this is recommended</h4>
          <div className="reason-pill">✔ Career Salary: {results?.insights.salary_range}</div>
          <div className="reason-pill">✔ {results?.recommendation?.roi.label || "Optimized for India Selection"}</div>
          <div className="reason-pill">✔ Neutral AI Decision Verification Complete</div>
        </div>
      </div>

      <div className="final-actions">
        <button className="btn-black" onClick={() => window.print()}>Download Report</button>
        <button className="btn-gray" onClick={onReset}><RefreshCw size={16} /> New Comparison</button>
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
    setStep(1); // Jump to goal selection
    setResults(null);
  };

  useEffect(() => {
    axios.get(`${API_BASE}/static-data`).then(res => setStaticData(res.data)).catch(console.error);
  }, []);

  const handleEvaluate = async (formData) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/evaluate`, formData);
      setResults({ ...res.data, ...formData });
      setLoading(false);
      next();
    } catch (err) {
      console.error(err);
      setLoading(false);
      alert("Error calling the AI model. Ensure server.py is running on port 5000.");
    }
  };

  return (
    <div className="app-wrapper">
      <AnimatePresence mode='wait'>
        {step === 0 && <Onboarding onNext={next} />}
        {step === 1 && <GoalSelection onNext={next} setGoal={(g) => setData({ ...data, goal: g })} />}
        {step === 2 && <UserInputs onNext={next} updateData={(d) => setData({ ...data, ...d })} onEvaluate={handleEvaluate} loading={loading} />}
        {step === 3 && <ComparisonTable onNext={next} staticData={staticData} results={results} />}
        {step === 4 && <PathwayDetails onNext={next} results={results} />}
        {step === 5 && <DetailedReport onReset={reset} results={results} />}
      </AnimatePresence>
    </div>
  );
}

export default App;

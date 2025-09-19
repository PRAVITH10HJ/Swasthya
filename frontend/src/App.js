import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [symptoms, setSymptoms] = useState('');
  const [question, setQuestion] = useState('');
  const [triageResult, setTriageResult] = useState(null);
  const [qaAnswer, setQaAnswer] = useState(null);
  const [clinics, setClinics] = useState([]);
  const [loading, setLoading] = useState('');
  const [error, setError] = useState('');

  const handleTriage = async () => {
    if (!symptoms) return;
    setLoading('triage');
    setError('');
    setTriageResult(null);
    try {
      const symptomList = symptoms.split(',').map(s => s.trim());
      const response = await axios.post('http://127.0.0.1:5001/triage', {
        symptoms: symptomList,
      });
      setTriageResult(response.data);
    } catch (err) {
      setError('Triage service is not available. Please ensure it is running.');
    }
    setLoading('');
  };

  const handleAsk = async () => {
    if (!question) return;
    setLoading('qa');
    setError('');
    setQaAnswer(null);
    try {
      const response = await axios.post('http://127.0.0.1:5003/ask', {
        question: question,
      });
      setQaAnswer(response.data);
    } catch (err) {
      setError('Q&A service is not available. Please ensure it is running.');
    }
    setLoading('');
  };

  const handleFindClinics = () => {
    setLoading('clinics');
    setError('');
    setClinics([]);
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      setLoading('');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords;
          const response = await axios.get(
            `http://127.0.0.1:5002/clinics?lat=${latitude}&lon=${longitude}&radius=15`
          );
          setClinics(response.data.clinics);
        } catch (err) {
          setError('Clinic locator service is not available. Please ensure it is running.');
        }
        setLoading('');
      },
      () => {
        setError('Unable to retrieve your location.');
        setLoading('');
      }
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SWASTHYA 🤝</h1>
        <p>AI Health Assistant for Displaced Communities</p>
      </header>

      {error && <p className="error-message">{error}</p>}

      <div className="service-container">
        {/* Triage Service */}
        <div className="service-card">
          <h2>Symptom Triage</h2>
          <p>Enter symptoms separated by commas (e.g., fever, headache).</p>
          <input
            type="text"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="fever, cough, headache"
          />
          <button onClick={handleTriage} disabled={loading}>
            {loading === 'triage' ? 'Checking...' : 'Check Symptoms'}
          </button>
          {triageResult && (
            <div className="result">
              <h3>Triage Result: <span className={`level-${triageResult.triage_result}`}>{triageResult.triage_result}</span></h3>
              <p>{triageResult.recommendation}</p>
            </div>
          )}
        </div>

        {/* Q&A Service */}
        <div className="service-card">
          <h2>Medical Q&A</h2>
          <p>Ask a question based on our WHO knowledge base.</p>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="How to treat a minor burn?"
          />
          <button onClick={handleAsk} disabled={loading}>
            {loading === 'qa' ? 'Searching...' : 'Ask Question'}
          </button>
          {qaAnswer && (
            <div className="result">
              <h3>Answer:</h3>
              <p>{qaAnswer.answer}</p>
              <small>Source: {qaAnswer.source}</small>
            </div>
          )}
        </div>

        {/* Clinic Locator */}
        <div className="service-card">
          <h2>Find Nearby Clinics</h2>
          <p>Allow location access to find humanitarian health services near you.</p>
          <button onClick={handleFindClinics} disabled={loading}>
             {loading === 'clinics' ? 'Searching...' : 'Find Clinics'}
          </button>
          {clinics.length > 0 && (
            <div className="result clinics-list">
              <h3>Nearby Clinics:</h3>
              <ul>
                {clinics.map((clinic) => (
                  <li key={clinic.name}>
                    <strong>{clinic.name}</strong> ({clinic.distance_km} km away)
                    <br />
                    <small>{clinic.address}</small>
                    <br/>
                    <small>Services: {clinic.services}</small>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
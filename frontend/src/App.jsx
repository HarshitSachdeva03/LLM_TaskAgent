import { useState } from 'react';

function App() {
  const [command, setCommand] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setResponse('');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
      });

      const data = await res.json();
      setResponse(data.result || 'No result received.');
    } catch (err) {
      console.error('Fetch error:', err);
      setResponse('Error connecting to backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h2>LLM Workflow Agent</h2>
      <textarea
        rows="4"
        cols="60"
        placeholder="e.g., Send an email to Alice saying hello"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
      />
      <br />
      <button onClick={handleSubmit} disabled={loading} style={{ marginTop: '1rem' }}>
        {loading ? 'Processing...' : 'Send to Agent'}
      </button>

      <pre style={{ marginTop: '2rem', backgroundColor: '#000000', padding: '1rem' }}>
        {response}
      </pre>
    </div>
  );
}

export default App;

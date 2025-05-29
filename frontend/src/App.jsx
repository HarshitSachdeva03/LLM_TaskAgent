// frontend/src/App.jsx

import { useState } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! I can help you send emails or create calendar events. What would you like to do?' }
  ]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);

    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          history: newMessages.map(m => `${m.sender === 'user' ? 'User' : 'Assistant'}: ${m.text}\n`)
        })
      });

      const data = await res.json();
      setMessages([...newMessages, { sender: 'bot', text: data.reply }]);
    } catch (err) {
      setMessages([...newMessages, { sender: 'bot', text: '⚠️ Error connecting to server.' }]);
    } finally {
      setInput('');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
      <div style={{ width: '100%', maxWidth: '700px', fontFamily: 'Arial, sans-serif' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>LLM Chat Agent</h2>
        <div style={{ background: '#f4f4f8', padding: '1rem', height: '400px', overflowY: 'scroll', borderRadius: '8px', border: '1px solid #ccc', boxShadow: '0 0 10px rgba(0,0,0,0.05)' }}>
          {messages.map((msg, i) => (
            <div key={i} style={{
              display: 'flex',
              justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '0.5rem'
            }}>
              <span
                style={{
                  padding: '0.6rem 1rem',
                  borderRadius: '1rem',
                  background: msg.sender === 'user' ? '#007bff' : '#e0e0e0',
                  color: msg.sender === 'user' ? '#fff' : '#000',
                  maxWidth: '75%',
                  lineHeight: '1.4'
                }}
              >
                {msg.text}
              </span>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', marginTop: '1rem' }}>
          <input
            style={{ flex: 1, padding: '0.75rem', borderRadius: '6px 0 0 6px', border: '1px solid #ccc', fontSize: '1rem' }}
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button
            style={{ padding: '0.75rem 1.5rem', borderRadius: '0 6px 6px 0', border: 'none', backgroundColor: '#007bff', color: '#fff', fontSize: '1rem' }}
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

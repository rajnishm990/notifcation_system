import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const MOCK_USER = { email: 'sandbox@email.com', phone: 'sandbox_number' };

export default function App() {
  const [triggers, setTriggers] = useState([]);
  const [newTrigger, setNewTrigger] = useState('');

  const fetchTriggers = () => axios.get(`${API_BASE}/triggers/`).then(res => setTriggers(res.data));
  useEffect(() => { fetchTriggers(); }, []);

  const addTrigger = async () => {
    await axios.post(`${API_BASE}/triggers/`, { name: newTrigger });
    fetchTriggers();
  };

  const updateTemplate = async (id, content, isActive) => {
    await axios.patch(`${API_BASE}/templates/${id}/`, { content, is_active: isActive });
    fetchTriggers();
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>User Simulation</h2>
      {triggers.map(t => (
        <button key={`sim-${t.id}`} onClick={() => axios.post(`${API_BASE}/fire/`, { trigger_name: t.name, user_data: MOCK_USER })}>
          Simulate {t.name} Event
        </button>
      ))}

      <h2>Admin Panel</h2>
      <input value={newTrigger} onChange={e => setNewTrigger(e.target.value)} placeholder="New trigger..." />
      <button onClick={addTrigger}>Add Row</button>

      <table border="1" style={{ marginTop: '20px', width: '100%' }}>
        <thead><tr><th>Trigger</th><th>WhatsApp</th><th>Email</th><th>Web Push</th></tr></thead>
        <tbody>
          {triggers.map(trigger => (
            <tr key={trigger.id}>
              <td>{trigger.name}</td>
              {['wa', 'email', 'push'].map(ch => {
                const tmpl = trigger.templates.find(t => t.channel === ch);
                if (!tmpl) return <td key={ch}>-</td>;
                return (
                  <td key={tmpl.id}>
                    <textarea defaultValue={tmpl.content} onBlur={e => updateTemplate(tmpl.id, e.target.value, tmpl.is_active)} />
                    <div>
                      <input type="checkbox" checked={tmpl.is_active} onChange={e => updateTemplate(tmpl.id, tmpl.content, e.target.checked)} /> Active
                      <button onClick={() => axios.post(`${API_BASE}/test/${tmpl.id}/`, { user_data: MOCK_USER })}>Test</button>
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
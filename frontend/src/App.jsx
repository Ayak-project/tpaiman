import { useState } from 'react';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('signup');
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('');
  const [files, setFiles] = useState([]);
  const [users, setUsers] = useState([]);

  // Signup form
  const [signupData, setSignupData] = useState({ email: '', password: '', name: '' });

  // Login form
  const [loginData, setLoginData] = useState({ email: '', password: '' });

  // Upload form
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('private');
  const [uploadName, setUploadName] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(signupData),
      });
      const data = await res.json();
      if (data.success) {
        setUser(data.user);
        setMessage(`✅ ${data.message}`);
        setActiveTab('login');
      } else {
        setMessage(`❌ ${data.detail || 'Erreur'}`);
      }
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });
      const data = await res.json();
      if (data.success) {
        setUser(data.user);
        setMessage(`✅ ${data.message} - Bienvenue ${data.user.name}!`);
        setActiveTab('upload');
      } else {
        setMessage(`❌ ${data.detail || 'Erreur'}`);
      }
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!uploadFile || !user || !uploadName) {
      setMessage('❌ Veuillez remplir tous les champs (fichier et nom)');
      return;
    }

    setUploading(true);
    setMessage('📤 Upload en cours...');

    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('user_id', user.id);
    formData.append('name', uploadName);
    formData.append('status', uploadStatus);

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.success) {
        setMessage(`✅ ${data.message} - Fichier "${data.file.name}" uploadé avec succès!`);
        setUploadFile(null);
        setUploadName('');
        // Reset file input
        e.target.reset();
        loadUserFiles();
        setTimeout(() => setActiveTab('files'), 1500);
      } else {
        setMessage(`❌ ${data.detail || 'Erreur'}`);
      }
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const loadUserFiles = async () => {
    if (!user) return;
    try {
      const res = await fetch(`${API_URL}/files/${user.id}`);
      const data = await res.json();
      if (data.success) {
        setFiles(data.files);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadAllUsers = async () => {
    try {
      const res = await fetch(`${API_URL}/users`);
      const data = await res.json();
      if (data.success) {
        setUsers(data.users);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const deleteFile = async (fileId) => {
    try {
      const res = await fetch(`${API_URL}/files/${fileId}`, {
        method: 'DELETE',
      });
      const data = await res.json();
      if (data.success) {
        setMessage(`✅ ${data.message}`);
        loadUserFiles();
      }
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    }
  };

  const updateFileStatus = async (fileId, newStatus) => {
    try {
      const res = await fetch(`${API_URL}/files/${fileId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });
      const data = await res.json();
      if (data.success) {
        setMessage(`✅ ${data.message}`);
        loadUserFiles();
      }
    } catch (err) {
      setMessage(`❌ ${err.message}`);
    }
  };



  return (
    <div className="App">
      <header>
        <h1>☁️ Cloud Storage API Tester</h1>
        {user && (
          <div className="user-info">
            <span>👤 {user.name} ({user.email})</span>
            <button onClick={() => { setUser(null); setMessage(''); }}>Déconnexion</button>
          </div>
        )}
      </header>

      {message && <div className="message">{message}</div>}

      <div className="tabs">
        <button className={activeTab === 'signup' ? 'active' : ''} onClick={() => setActiveTab('signup')}>
          Inscription
        </button>
        <button className={activeTab === 'login' ? 'active' : ''} onClick={() => setActiveTab('login')}>
          Connexion
        </button>
        <button className={activeTab === 'upload' ? 'active' : ''} onClick={() => setActiveTab('upload')}>
          Upload
        </button>
        <button className={activeTab === 'files' ? 'active' : ''} onClick={() => { setActiveTab('files'); loadUserFiles(); }}>
          Mes Fichiers
        </button>
        <button className={activeTab === 'users' ? 'active' : ''} onClick={() => { setActiveTab('users'); loadAllUsers(); }}>
          Utilisateurs
        </button>
      </div>

      <div className="content">
        {activeTab === 'signup' && (
          <form onSubmit={handleSignup}>
            <h2>Créer un compte</h2>
            <input
              type="email"
              placeholder="Email"
              value={signupData.email}
              onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
              required
            />
            <input
              type="password"
              placeholder="Mot de passe"
              value={signupData.password}
              onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
              required
            />
            <input
              type="text"
              placeholder="Nom (optionnel)"
              value={signupData.name}
              onChange={(e) => setSignupData({ ...signupData, name: e.target.value })}
            />
            <button type="submit">S'inscrire</button>
          </form>
        )}

        {activeTab === 'login' && (
          <form onSubmit={handleLogin}>
            <h2>Se connecter</h2>
            <input
              type="email"
              placeholder="Email"
              value={loginData.email}
              onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
              required
            />
            <input
              type="password"
              placeholder="Mot de passe"
              value={loginData.password}
              onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
              required
            />
            <button type="submit">Se connecter</button>
          </form>
        )}

        {activeTab === 'upload' && (
          <div>
            <h2>Upload un fichier</h2>
            {!user ? (
              <p>Connectez-vous d'abord!</p>
            ) : (
              <form onSubmit={handleUpload}>
                <input
                  type="text"
                  placeholder="Nom du fichier (sans extension) *"
                  value={uploadName}
                  onChange={(e) => setUploadName(e.target.value)}
                  required
                />
                <p className="help-text">💡 L'extension (.pdf, .docx, etc.) sera ajoutée automatiquement</p>
                <input
                  type="file"
                  onChange={(e) => setUploadFile(e.target.files[0])}
                  required
                />
                <select value={uploadStatus} onChange={(e) => setUploadStatus(e.target.value)}>
                  <option value="private">Privé</option>
                  <option value="public">Public</option>
                </select>
                <button type="submit" disabled={uploading}>
                  {uploading ? '📤 Upload en cours...' : '📤 Upload'}
                </button>
              </form>
            )}
          </div>
        )}

        {activeTab === 'files' && (
          <div>
            <h2>Mes Fichiers ({files.length})</h2>
            {!user ? (
              <p>Connectez-vous d'abord!</p>
            ) : files.length === 0 ? (
              <p>Aucun fichier</p>
            ) : (
              <div className="files-list">
                {files.map((file) => (
                  <div key={file.id} className="file-card">
                    <div className="file-header">
                      <h3>📄 {file.name}</h3>
                    </div>
                    <a href={file.link} target="_blank" rel="noopener noreferrer" className="file-link">
                      🔗 Ouvrir le fichier
                    </a>
                    <div className="file-info">
                      <span className={`badge ${file.status}`}>{file.status}</span>
                      <span className="date">{new Date(file.created_at).toLocaleString()}</span>
                    </div>
                    <div className="file-actions">
                      <button onClick={() => updateFileStatus(file.id, file.status === 'private' ? 'public' : 'private')}>
                        {file.status === 'private' ? '🔓 Rendre public' : '🔒 Rendre privé'}
                      </button>
                      <button onClick={() => deleteFile(file.id)} className="delete">
                        🗑️ Supprimer
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'users' && (
          <div>
            <h2>Tous les utilisateurs ({users.length})</h2>
            <div className="users-list">
              {users.map((u) => (
                <div key={u.id} className="user-card">
                  <div>
                    <strong>{u.name}</strong>
                    <p>{u.email}</p>
                  </div>
                  <span className="date">{new Date(u.created_at).toLocaleString()}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

import { useState } from 'react';
import UploadZone from './components/UploadZone';
import ChatPanel from './components/ChatPanel';
import './index.css';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [activeFile, setActiveFile] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleUpload = async (file: File) => {
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
      if (!res.ok) throw new Error('upload failed');
      setActiveFile(file.name);
    } catch {
      alert('Upload failed. Is the backend running?');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="app-shell">
      <h1>Chat with your PDF</h1>
      <div className="app-body">
        <div className="panel">
          <UploadZone onUpload={handleUpload} activeFile={activeFile} isProcessing={isProcessing} />
        </div>
        <div className="panel">
          <ChatPanel apiBase={API_BASE} hasDocument={!!activeFile} />
        </div>
      </div>
    </div>
  );
}

export default App;

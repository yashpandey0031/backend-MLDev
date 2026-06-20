import { useRef, useState } from 'react';

interface UploadZoneProps {
  onUpload: (file: File) => void;
  activeFile: string | null;
  isProcessing: boolean;
}

function UploadZone({ onUpload, activeFile, isProcessing }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') onUpload(file);
  };

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onUpload(file);
  };

  return (
    <div
      className={`dropzone ${isDragging ? 'dropzone--active' : ''} ${activeFile ? 'dropzone--filled' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input ref={inputRef} type="file" accept="application/pdf" hidden onChange={handleSelect} />
      <div className="dropzone-icon">{isProcessing ? '…' : '↑'}</div>
      <p className="dropzone-label">
        {isProcessing ? 'Processing…' : activeFile ? activeFile : 'Drop a PDF here'}
      </p>
      <p className="dropzone-sub">{activeFile ? 'Drop a new file to replace it' : 'or click to browse'}</p>
    </div>
  );
}

export default UploadZone;

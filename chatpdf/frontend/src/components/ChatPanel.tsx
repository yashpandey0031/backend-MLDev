import { useEffect, useRef, useState } from 'react';

interface Message {
  role: 'user' | 'assistant' | 'error';
  text: string;
}

interface ChatPanelProps {
  apiBase: string;
  hasDocument: boolean;
}

function ChatPanel({ apiBase, hasDocument }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isThinking]);

  const sendMessage = async () => {
    const question = input.trim();
    if (!question || isThinking) return;

    setMessages((prev) => [...prev, { role: 'user', text: question }]);
    setInput('');
    setIsThinking(true);

    try {
      const res = await fetch(`${apiBase}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();

      if (data.error) {
        setMessages((prev) => [...prev, { role: 'error', text: data.error }]);
      } else {
        setMessages((prev) => [...prev, { role: 'assistant', text: data.answer }]);
      }
    } catch {
      setMessages((prev) => [...prev, { role: 'error', text: 'Could not reach the server.' }]);
    } finally {
      setIsThinking(false);
    }
  };

  if (!hasDocument) {
    return <div className="chat-panel"><p className="chat-empty">Upload a PDF to start chatting</p></div>;
  }

  return (
    <div className="chat-panel">
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`bubble bubble--${m.role}`}>{m.text}</div>
        ))}
        {isThinking && <div className="bubble bubble--assistant">Thinking…</div>}
        <div ref={bottomRef} />
      </div>
      <div className="chat-input-row">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
          placeholder="Ask a question about the PDF…"
          rows={1}
        />
        <button onClick={sendMessage} disabled={isThinking || !input.trim()}>Send</button>
      </div>
    </div>
  );
}

export default ChatPanel;

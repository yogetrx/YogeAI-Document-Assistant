
import { useRef, useState } from 'react'
import {
  FileText, Upload, Plus, Search, MessageSquare, Sparkles,
  Send, Bot, PanelLeft, Trash2, LoaderCircle, CheckCircle2,
  AlertCircle, X,
} from 'lucide-react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'

async function readResponse(response) {
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.detail || `Request failed (${response.status})`)
  }
  return data
}

export default function App() {
  const [documents, setDocuments] = useState([])
  const [question, setQuestion] = useState('')
  const [uploading, setUploading] = useState(false)
  const [asking, setAsking] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Hey! I’m YogeAI. Upload a document and ask me anything about its contents.',
    },
  ])

  async function uploadDocuments(event) {
    const files = Array.from(event.target.files || [])
    event.target.value = ''
    if (!files.length) return

    setError('')
    setUploading(true)

    for (const file of files) {
      if (!file.name.toLowerCase().endsWith('.pdf')) {
        setError(`${file.name}: only PDF files are supported.`)
        continue
      }

      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await fetch(`${API_BASE}/documents`, {
          method: 'POST',
          body: formData,
        })
        const result = await readResponse(response)

        setDocuments((previous) => [
          ...previous,
          {
            name: result.document_name || file.name,
            size: file.size,
            chunks: result.chunks_indexed,
            pages: result.pages_with_text,
            status: result.status || 'indexed',
          },
        ])

        setMessages((previous) => [
          ...previous,
          {
            role: 'assistant',
            text: `Successfully uploaded and indexed ${result.document_name || file.name}. ${result.pages_with_text ?? 'The'} pages with text; ${result.chunks_indexed ?? 'Document'} chunks indexed.`,
          },
        ])
      } catch (err) {
        setError(`Couldn't upload ${file.name}: ${err.message}. Check that FastAPI is running.`)
      }
    }

    setUploading(false)
  }

  async function sendMessage(event) {
    event.preventDefault()
    const text = question.trim()
    if (!text || asking) return

    setQuestion('')
    setError('')
    setMessages((previous) => [...previous, { role: 'user', text }])
    setAsking(true)

    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text, top_k: 4 }),
      })
      const result = await readResponse(response)

      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          text: result.answer || 'The API returned no answer.',
          sources: result.sources || [],
          retrievalCount: result.retrieval_count ?? 0,
        },
      ])
    } catch (err) {
      setError(`Couldn't get an answer: ${err.message}. Check that FastAPI is running.`)
      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          text: 'I couldn’t reach the backend for that question. Please check the error message and try again.',
        },
      ])
    } finally {
      setAsking(false)
    }
  }

  function startNewConversation() {
    setMessages([
      {
        role: 'assistant',
        text: 'New conversation started. Your indexed documents remain available. What would you like to know?',
      },
    ])
    setError('')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Sparkles size={21} /></div>
          <div><strong>YogeAI</strong><span>DOCUMENT INTELLIGENCE</span></div>
        </div>

        <button className="new-chat" onClick={startNewConversation}>
          <Plus size={17} /> New conversation
        </button>

        <div className="section-label">WORKSPACE</div>
        <div className="nav-item active"><MessageSquare size={17} /> AI Assistant</div>
        <div className="nav-item">
          <FileText size={17} /> My documents <span>{documents.length}</span>
        </div>

        <div className="section-label document-heading">
          YOUR DOCUMENTS
          <button
            type="button"
            className="icon-button"
            title="Upload PDF"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            <Plus size={17} />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            multiple
            onChange={uploadDocuments}
            hidden
          />
        </div>

        <div className="document-list">
          {documents.map((document, index) => (
            <div className="document-item" key={`${document.name}-${index}`}>
              <FileText size={17} />
              <span title={document.name}>{document.name}</span>
              <CheckCircle2 size={14} aria-label="Indexed" />
            </div>
          ))}
          {documents.length === 0 && (
            <p className="empty-documents">Upload a PDF to see it here.</p>
          )}
        </div>

        <div className="sidebar-footer">
          <div className="avatar">Y</div>
          <div><strong>YogeAI Workspace</strong><span>Personal workspace</span></div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div className="breadcrumb">
            <PanelLeft size={18} /><span>Workspace</span>
            <span className="muted">/</span><strong>AI Assistant</strong>
          </div>
          <div className="status"><span /> API connected when requests succeed</div>
        </header>

        <section className="chat-layout">
          <div className="chat-header">
            <div className="assistant-icon"><Bot size={25} /></div>
            <div>
              <h1>Document Assistant</h1>
              <p>Ask questions. Find answers in your documents.</p>
            </div>
            <div className="model-badge"><span /> YogeAI</div>
          </div>

          <div className="chat-messages">
            {messages.length === 1 && (
              <div className="welcome-card">
                <div className="welcome-sparkle"><Sparkles size={25} /></div>
                <h2>Your documents, understood.</h2>
                <p>Upload PDFs, ask natural-language questions, and get answers grounded in your content.</p>
                <label className="upload-card">
                  {uploading ? <LoaderCircle className="spin" size={21} /> : <Upload size={21} />}
                  <strong>{uploading ? 'Uploading and indexing…' : 'Upload your PDF documents'}</strong>
                  <span>Choose one or more PDF files from your computer</span>
                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    multiple
                    onChange={uploadDocuments}
                    hidden
                    disabled={uploading}
                  />
                </label>
                <div className="suggestions">
                  <span>TRY ASKING</span>
                  <button type="button" onClick={() => setQuestion('Summarize the key points')}>
                    Summarize key points
                  </button>
                  <button type="button" onClick={() => setQuestion('What are the important policies?')}>
                    Find important policies
                  </button>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div className={`message ${message.role}`} key={index}>
                <div className="message-avatar">
                  {message.role === 'assistant' ? <Sparkles size={16} /> : 'Y'}
                </div>
                <div className="message-content">
                  <span className="message-author">
                    {message.role === 'assistant' ? 'YogeAI' : 'You'}
                  </span>
                  <p className="answer-text">{message.text}</p>

                  {message.sources?.length > 0 && (
                    <div className="sources">
                      <strong>Sources ({message.sources.length})</strong>
                      {message.sources.map((source, sourceIndex) => (
                        <details className="source-card" key={`${source.chunk_id}-${sourceIndex}`}>
                          <summary>
                            <FileText size={15} />
                            {source.document_name} · Page {source.page}
                          </summary>
                          <p>{source.text}</p>
                          {source.score != null && (
                            <small>Retrieval score: {Number(source.score).toFixed(3)}</small>
                          )}
                        </details>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {asking && (
              <div className="message assistant">
                <div className="message-avatar"><Sparkles size={16} /></div>
                <div className="message-content">
                  <span className="message-author">YogeAI</span>
                  <p><LoaderCircle className="spin" size={16} /> Searching documents and generating an answer…</p>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="error-banner" role="alert">
              <AlertCircle size={17} />
              <span>{error}</span>
              <button type="button" onClick={() => setError('')} aria-label="Dismiss error">
                <X size={16} />
              </button>
            </div>
          )}

          {uploading && (
            <p className="upload-status"><LoaderCircle className="spin" size={15} /> Uploading and indexing PDF(s)…</p>
          )}

          <div className="composer-area">
            <form className="composer" onSubmit={sendMessage}>
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Ask a question about your documents..."
                rows={2}
                disabled={asking}
              />
              <div className="composer-bottom">
                <span><Search size={14} /> Answers are generated by your RAG backend</span>
                <button type="submit" disabled={!question.trim() || asking}>
                  {asking ? <LoaderCircle className="spin" size={16} /> : <Send size={16} />}
                  {asking ? 'Thinking…' : 'Send'}
                </button>
              </div>
            </form>
            <p className="disclaimer">YogeAI can make mistakes. Verify important information against your source documents.</p>
          </div>
        </section>
      </main>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import Chat from '../components/Chat'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const API_URL = 'http://127.0.0.1:8000'

function Conversation() {
  const { conversationId } = useParams()
  const location = useLocation()

  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [thinking, setThinking] = useState(false)

  const [artifact, setArtifact] = useState(
    location.state?.artifact ?? null
  )

  useEffect(() => {
    async function loadConversation() {
      try {
        setLoading(true)

        const response = await fetch(
          `${API_URL}/conversations/${conversationId}/messages`
        )

        if (!response.ok) {
          throw new Error('Failed to load conversation')
        }

        const data = await response.json()

        setMessages(data)

        const latestArtifact = [...data]
          .reverse()
          .find(
            (message) =>
              message.role === 'assistant' &&
              message.artifact
          )

        // Only replace the current artifact if the API
        // actually returned one.
        if (latestArtifact?.artifact) {
          setArtifact(latestArtifact.artifact)
        }
      } catch (error) {
        console.error(
          'Failed to load conversation:',
          error
        )
      } finally {
        setLoading(false)
      }
    }

    if (conversationId) {
      loadConversation()
    }
  }, [conversationId])

  function handleMessageSent(message) {
    setMessages((previousMessages) => [
      ...previousMessages,
      message,
    ])

    if (message.role === 'assistant' && message.artifact) {
      setArtifact(message.artifact)
    }
  }

  return (
    <div className="conversation-page">

      {artifact && (
        <div className="artifact-panel">

          <div className="artifact-header">
            <h2>{artifact.title}</h2>
            <span>{artifact.type}</span>
          </div>

          <div className="artifact-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {artifact.content}
            </ReactMarkdown>
          </div>

        </div>
      )}

      <div className="conversation-header">
        <h1>Lenny Growth Assistant</h1>
      </div>

      <div className="messages">

        {loading ? (
          <div className="message-loading">
            Loading conversation...
          </div>
        ) : messages.length === 0 ? (
          <div className="message-loading">
            No messages yet.
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id || message.message_id}
              className={`message ${message.role}`}
            >
              <div className="message-role">
                {message.role === 'user'
                  ? 'You'
                  : 'Lenny'}
              </div>

              <div className="message-content">
                {message.content}
              </div>

              {message.role === 'assistant' &&
                message.sources &&
                message.sources.length > 0 && (
                  <div className="message-sources">

                    <div className="sources-title">
                      Sources
                    </div>

                    {message.sources.map(
                      (source, index) => (
                        <div
                          className="source-item"
                          key={`${source.source}-${source.chunk}-${index}`}
                        >
                          <div className="source-title">
                            {source.title}
                          </div>

                          <div className="source-meta">
                            {source.source}
                            {' · '}
                            Chunk {source.chunk}
                          </div>
                        </div>
                      )
                    )}

                  </div>
                )}
            </div>
          ))
        )}

        {thinking && (
          <div className="message assistant thinking-message">

            <div className="message-role">
              Lenny
            </div>

            <div className="thinking-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>

          </div>
        )}

      </div>

      <div className="chat-input">
        <Chat
          conversationId={conversationId}
          onMessageSent={handleMessageSent}
          onLoadingChange={setThinking}
        />
      </div>

    </div>
  )
}

export default Conversation
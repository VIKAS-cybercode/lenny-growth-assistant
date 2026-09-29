import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useUser } from '../context/UserContext'

const API_URL = 'http://127.0.0.1:8000'

function Chat({
  conversationId = null,
  onMessageSent,
  onLoadingChange,
}) {
  const { userId } = useUser()
  const navigate = useNavigate()

  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    const text = message.trim()

    if (!text || !userId || loading) {
      return
    }

    setLoading(true)
    onLoadingChange?.(true)
    setMessage('')

    try {
      let currentConversationId = conversationId

      // 1. Create conversation if this is a new chat
      if (!currentConversationId) {
        const conversationResponse = await fetch(
          `${API_URL}/conversations`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: userId,
            }),
          }
        )

        if (!conversationResponse.ok) {
          throw new Error(
            'Failed to create conversation'
          )
        }

        const conversationData =
          await conversationResponse.json()

        currentConversationId =
          conversationData.conversation_id
      }

      // 2. Immediately show user's message
      const userMessage = {
        id: crypto.randomUUID(),
        conversation_id: currentConversationId,
        role: 'user',
        content: text,
        created_at: new Date().toISOString(),
      }

      if (onMessageSent) {
        onMessageSent(userMessage)
      }

      // 3. Send message to backend
      const messageResponse = await fetch(
        `${API_URL}/conversations/${currentConversationId}/messages`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            content: text,
          }),
        }
      )

      if (!messageResponse.ok) {
        const errorText =
          await messageResponse.text()

        throw new Error(
          `Failed to send message: ${errorText}`
        )
      }

      // 4. Get Lenny's response
      const assistantMessage =
        await messageResponse.json()

      console.log(
        'ASSISTANT MESSAGE FROM BACKEND:',
        assistantMessage
      )

      // 5. Show Lenny's response
      if (onMessageSent) {
        onMessageSent(assistantMessage)
      }

      // 6. Navigate to the conversation if this was new
      if (!conversationId) {
        navigate(
          `/c/${currentConversationId}`,
          {
            state: {
              artifact:
                assistantMessage.artifact ?? null,
            },
          }
        )
      }
    } catch (error) {
      console.error(
        'Message sending failed:',
        error
      )
    } finally {
      setLoading(false)
      onLoadingChange?.(false)
    }
  }

  return (
    <div className="chat-box">
      <form
        className="chat-form"
        onSubmit={handleSubmit}
      >
        <input
          className="chat-text-input"
          type="text"
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          placeholder="Message Lenny..."
          disabled={!userId || loading}
        />

        <button
          className="chat-send-button"
          type="submit"
          disabled={
            !userId ||
            !message.trim() ||
            loading
          }
        >
          {loading ? '...' : '↑'}
        </button>
      </form>
    </div>
  )
}

export default Chat
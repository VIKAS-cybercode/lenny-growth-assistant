import { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useUser } from '../context/UserContext'

const API_URL = 'http://127.0.0.1:8000'

function Sidebar() {
  const { userId } = useUser()
  const navigate = useNavigate()
  const location = useLocation()

  const [conversations, setConversations] = useState([])

  useEffect(() => {
    if (!userId) {
      return
    }

    async function loadConversations() {
      try {
        const response = await fetch(
          `${API_URL}/conversations/user/${userId}`
        )

        if (!response.ok) {
          throw new Error('Failed to load conversations')
        }

        const data = await response.json()

        setConversations(data)
      } catch (error) {
        console.error(
          'Failed to load conversations:',
          error
        )
      }
    }

    loadConversations()
  }, [userId, location.pathname])

  function handleNewChat() {
    navigate('/')
  }

  return (
    <aside className="sidebar">

      <div className="sidebar-header">

        <div className="sidebar-title">
          Lenny Growth
        </div>

        <button
          className="new-chat-button"
          onClick={handleNewChat}
        >
          + New Chat
        </button>

      </div>

      <div className="recent-section">

        <div className="recent-title">
          Recent chats
        </div>

        {conversations.length === 0 ? (
          <div className="recent-chat">
            No recent chats
          </div>
        ) : (
          conversations.map((conversation) => (
            <button
              key={conversation.conversation_id}
              className={`recent-chat ${
                location.pathname ===
                `/c/${conversation.conversation_id}`
                  ? 'active'
                  : ''
              }`}
              onClick={() =>
                navigate(
                  `/c/${conversation.conversation_id}`
                )
              }
            >
              {conversation.title ||
                'New conversation'}
            </button>
          ))
        )}

      </div>

    </aside>
  )
}

export default Sidebar
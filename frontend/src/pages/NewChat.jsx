import Chat from '../components/Chat'

function NewChat() {
  return (
    <div className="new-chat-page">

      <div className="new-chat-center">
        <h1>Lenny Growth Assistant</h1>
        <p>How can I help you?</p>
      </div>

      <div className="new-chat-input">
        <Chat />
      </div>

    </div>
  )
}

export default NewChat
import { Routes, Route } from 'react-router-dom'
import Layout from './Layout'
import NewChat from './pages/NewChat'
import Conversation from './pages/Conversation'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<NewChat />} />

        <Route
          path="/c/:conversationId"
          element={<Conversation />}
        />
      </Route>
    </Routes>
  )
}

export default App
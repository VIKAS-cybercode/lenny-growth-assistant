import { createContext, useContext, useEffect, useState } from 'react'

const API_URL = 'http://127.0.0.1:8000'

const UserContext = createContext(null)

let userInitializationPromise = null

function initializeUser() {
  const existingUserId = localStorage.getItem('user_id')

  if (existingUserId) {
    return Promise.resolve(existingUserId)
  }

  if (!userInitializationPromise) {
    userInitializationPromise = fetch(`${API_URL}/users/anonymous`, {
      method: 'POST',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to create anonymous user')
        }

        return response.json()
      })
      .then((data) => {
        localStorage.setItem('user_id', data.user_id)
        return data.user_id
      })
      .catch((error) => {
        userInitializationPromise = null
        throw error
      })
  }

  return userInitializationPromise
}

export function UserProvider({ children }) {
  const [userId, setUserId] = useState(null)

  useEffect(() => {
    initializeUser()
      .then((id) => {
        setUserId(id)
      })
      .catch((error) => {
        console.error('User initialization failed:', error)
      })
  }, [])

  return (
    <UserContext.Provider value={{ userId }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  return useContext(UserContext)
}
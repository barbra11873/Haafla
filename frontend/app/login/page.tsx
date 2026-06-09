"use client"

import { useState } from 'react'
import { api, getMe } from '../../lib/api'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const login = async () => {
    try {
      const res = await api.post('/auth/token/', { username, password })
      localStorage.setItem('access', res.data.access)
      localStorage.setItem('refresh', res.data.refresh)
      // fetch user info and redirect based on role
      const user = await getMe()
      if (user.role === 'vendor') {
        router.push('/vendor/dashboard')
      } else {
        router.push('/dashboard')
      }
    } catch (err) {
      console.error(err)
      alert('Login failed')
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Login</h1>
      <input placeholder="username" onChange={(e) => setUsername(e.target.value)} />
      <br />
      <input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
      <br />
      <button onClick={login}>Login</button>
    </div>
  )
}

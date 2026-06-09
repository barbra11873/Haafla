"use client"

import { useEffect, useState } from 'react'
import { getMe } from '../../lib/api'
import { useRouter } from 'next/navigation'

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const router = useRouter()

  useEffect(() => {
    async function fetchMe() {
      try {
        const data = await getMe()
        setUser(data)
        if (data.role === 'vendor') {
          router.replace('/vendor/dashboard')
        }
      } catch (err) {
        console.error(err)
        router.push('/login')
      }
    }
    fetchMe()
  }, [])

  if (!user) return <div>Loading...</div>

  return (
    <main style={{ padding: 24 }}>
      <h1>Dashboard</h1>
      <p>Welcome, {user.username} ({user.role})</p>
    </main>
  )
}

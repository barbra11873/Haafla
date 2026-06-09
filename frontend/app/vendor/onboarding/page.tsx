"use client"

import { useState } from 'react'
import { api } from '../../../lib/api'
import { useRouter } from 'next/navigation'

export default function VendorOnboarding() {
  const [businessName, setBusinessName] = useState('')
  const [description, setDescription] = useState('')
  const [location, setLocation] = useState('')
  const router = useRouter()

  const submit = async () => {
    try {
      const payload = {
        display_name: businessName,
        bio: description,
        location,
      }
      await api.post('/vendors/vendors/', payload)
      alert('Vendor profile created')
      router.push('/vendor/dashboard')
    } catch (err: any) {
      console.error(err)
      alert(err?.response?.data || 'Failed to create vendor')
    }
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>Vendor Onboarding</h1>
      <div>
        <label>Business name</label>
        <br />
        <input onChange={(e) => setBusinessName(e.target.value)} />
      </div>
      <div>
        <label>Description</label>
        <br />
        <textarea onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div>
        <label>Location</label>
        <br />
        <input onChange={(e) => setLocation(e.target.value)} />
      </div>
      <button onClick={submit}>Create profile</button>
    </main>
  )
}

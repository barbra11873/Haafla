"use client"

import { useState } from 'react'
import { api } from '../../../lib/api'
import { useRouter } from 'next/navigation'

export default function VendorOnboarding() {
  const [businessName, setBusinessName] = useState('')
  const [description, setDescription] = useState('')
  const [location, setLocation] = useState('')
  const router = useRouter()

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState<number | null>(null)

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl)
    }
  }, [previewUrl])

  const validate = () => {
    if (!businessName || businessName.trim().length < 3) {
      setError('Business name must be at least 3 characters')
      return false
    }
    return true
  }

  const handleFileChange = (f: File | null) => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
      setPreviewUrl(null)
    }
    setFile(f)
    if (f) setPreviewUrl(URL.createObjectURL(f))
  }

  const resizeImage = (file: File, maxWidth = 1600, maxHeight = 1600, quality = 0.8) => {
    return new Promise<Blob | null>((resolve) => {
      const img = new Image()
      img.onload = () => {
        let { width, height } = img
        const aspect = width / height
        if (width > maxWidth) {
          width = maxWidth
          height = Math.round(width / aspect)
        }
        if (height > maxHeight) {
          height = maxHeight
          width = Math.round(height * aspect)
        }
        const canvas = document.createElement('canvas')
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        if (!ctx) return resolve(null)
        ctx.drawImage(img, 0, 0, width, height)
        canvas.toBlob(
          (blob) => {
            resolve(blob)
          },
          'image/jpeg',
          quality,
        )
      }
      img.onerror = () => resolve(null)
      img.src = URL.createObjectURL(file)
    })
  }

  const submit = async () => {
    setError(null)
    if (!validate()) return
    setLoading(true)
    try {
      const payload = {
        display_name: businessName,
        bio: description,
        location,
      }
      await api.post('/vendors/vendors/', payload)

      if (file) {
        const resized = await resizeImage(file)
        if (resized) {
          const form = new FormData()
          form.append('file', resized, file.name)
          await api.post('/vendors/portfolio/', form, {
            headers: { 'Content-Type': 'multipart/form-data' },
            onUploadProgress: (progressEvent: any) => {
              if (progressEvent.total) {
                setUploadProgress(Math.round((progressEvent.loaded * 100) / progressEvent.total))
              }
            },
          })
        }
      }

      router.push('/vendor/dashboard')
    } catch (err: any) {
      console.error(err)
      setError(err?.response?.data || 'Failed to create vendor')
    } finally {
      setLoading(false)
      setUploadProgress(null)
    }
  }

  return (
    <main>
      <h1>Vendor Onboarding</h1>
      <div>
        <label>Business name</label>
        <br />
        <input value={businessName} onChange={(e) => setBusinessName(e.target.value)} />
      </div>
      <div>
        <label>Description</label>
        <br />
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div>
        <label>Location</label>
        <br />
        <input value={location} onChange={(e) => setLocation(e.target.value)} />
      </div>
      <div>
        <label>Portfolio (optional)</label>
        <br />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleFileChange(e.target.files ? e.target.files[0] : null)}
        />
        {previewUrl && (
          <div style={{ marginTop: 8 }}>
            <div>Preview:</div>
            <img src={previewUrl} alt="preview" style={{ maxWidth: 300, maxHeight: 200 }} />
          </div>
        )}
      </div>
      {uploadProgress !== null && <div>Upload progress: {uploadProgress}%</div>}
      {error && <div style={{ color: 'red' }}>{JSON.stringify(error)}</div>}
      <div>
        <button disabled={loading} onClick={submit}>
          {loading ? 'Creating...' : 'Create profile'}
        </button>
      </div>
    </main>
  )
}

"use client"

import { useEffect, useState } from 'react'
import { api } from '../../../lib/api'
import { useRouter } from 'next/navigation'

const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_IMAGE_SIZE = 5 * 1024 * 1024

export default function VendorOnboarding() {
  const [businessName, setBusinessName] = useState('')
  const [description, setDescription] = useState('')
  const [location, setLocation] = useState('')
  const [portfolioTitle, setPortfolioTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState<number | null>(null)
  const router = useRouter()

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

  const setPreviewFile = (nextFile: File | null) => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
      setPreviewUrl(null)
    }
    setError(null)
    setSuccess(null)
    setUploadProgress(null)

    if (!nextFile) {
      setFile(null)
      return
    }

    if (!ALLOWED_IMAGE_TYPES.includes(nextFile.type)) {
      setError('Only jpg, png, and webp images are allowed')
      setFile(null)
      return
    }

    if (nextFile.size > MAX_IMAGE_SIZE) {
      setError('Image must be 5MB or smaller')
      setFile(null)
      return
    }

    setFile(nextFile)
    setPreviewUrl(URL.createObjectURL(nextFile))
  }

  const resizeImage = (imageFile: File, maxWidth = 1600, maxHeight = 1600, quality = 0.8) => {
    return new Promise<Blob | null>((resolve) => {
      const image = new Image()
      image.onload = () => {
        let { width, height } = image
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
        const context = canvas.getContext('2d')
        if (!context) return resolve(null)
        context.drawImage(image, 0, 0, width, height)
        canvas.toBlob((blob) => resolve(blob), 'image/jpeg', quality)
      }
      image.onerror = () => resolve(null)
      image.src = URL.createObjectURL(imageFile)
    })
  }

  const submit = async () => {
    setError(null)
    setSuccess(null)
    if (!validate()) return

    setLoading(true)
    setUploadProgress(null)

    try {
      await api.post('/vendors/vendors/', {
        display_name: businessName,
        bio: description,
        location,
      })

      if (file) {
        const resized = await resizeImage(file)
        if (resized) {
          const form = new FormData()
          form.append('title', portfolioTitle || `${businessName} portfolio`)
          form.append('description', description)
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

      setSuccess('Vendor profile created successfully')
      router.push('/vendor/dashboard')
    } catch (err: any) {
      console.error(err)
      const responseData = err?.response?.data
      setError(typeof responseData === 'string' ? responseData : 'Failed to create vendor')
    } finally {
      setLoading(false)
      setUploadProgress(null)
    }
  }

  return (
    <main>
      <h1>Vendor Onboarding</h1>
      <div>
        <label htmlFor="businessName">Business name</label>
        <br />
        <input id="businessName" value={businessName} onChange={(e) => setBusinessName(e.target.value)} />
      </div>
      <div>
        <label htmlFor="description">Description</label>
        <br />
        <textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div>
        <label htmlFor="location">Location</label>
        <br />
        <input id="location" value={location} onChange={(e) => setLocation(e.target.value)} />
      </div>
      <div>
        <label htmlFor="portfolioTitle">Portfolio title</label>
        <br />
        <input
          id="portfolioTitle"
          value={portfolioTitle}
          onChange={(e) => setPortfolioTitle(e.target.value)}
          placeholder="Optional, defaults to your business name"
        />
      </div>
      <div>
        <label htmlFor="portfolioFile">Portfolio image</label>
        <br />
        <input
          id="portfolioFile"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={(e) => setPreviewFile(e.target.files ? e.target.files[0] : null)}
        />
        {previewUrl && (
          <div style={{ marginTop: 8 }}>
            <div>Preview:</div>
            <img src={previewUrl} alt="preview" style={{ maxWidth: 300, maxHeight: 200 }} />
          </div>
        )}
      </div>
      {uploadProgress !== null && <div>Upload progress: {uploadProgress}%</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>{success}</div>}
      <div>
        <button disabled={loading} onClick={submit}>
          {loading ? 'Creating...' : 'Create profile'}
        </button>
      </div>
    </main>
  )
}

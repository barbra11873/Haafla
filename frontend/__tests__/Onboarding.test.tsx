import React from 'react'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import VendorOnboarding from '../app/vendor/onboarding/page'

const mockApiPost = jest.fn()
const mockPush = jest.fn()

jest.mock('../lib/api', () => ({
  api: {
    post: (...args: any[]) => mockApiPost(...args),
  },
}))

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
}))

const mockCanvas = () => {
  const context = {
    drawImage: jest.fn(),
  }
  const canvas = {
    width: 0,
    height: 0,
    getContext: jest.fn(() => context),
    toBlob: jest.fn((callback: any) => callback(new Blob(['thumb'], { type: 'image/jpeg' }))),
  }

  const originalCreateElement = document.createElement.bind(document)
  jest.spyOn(document, 'createElement').mockImplementation((tagName: any) => {
    if (tagName === 'canvas') return canvas as any
    return originalCreateElement(tagName)
  })

  return canvas
}

const mockImageLoad = () => {
  class MockImage {
    onload: null | (() => void) = null
    onerror: null | (() => void) = null
    width = 800
    height = 600

    set src(_value: string) {
      setTimeout(() => {
        if (this.onload) this.onload()
      }, 0)
    }
  }

  ;(global as any).Image = MockImage
}

describe('VendorOnboarding upload flow', () => {
  beforeEach(() => {
    mockApiPost.mockReset()
    mockPush.mockReset()
    jest.restoreAllMocks()
    ;(window.URL.createObjectURL as any) = jest.fn(() => 'blob:preview')
    ;(window.URL.revokeObjectURL as any) = jest.fn()
    mockImageLoad()
  })

  it('shows validation errors for short business name and bad file type', async () => {
    render(<VendorOnboarding />)

    fireEvent.change(screen.getByLabelText(/Business name/i), { target: { value: 'AB' } })
    fireEvent.click(screen.getByRole('button', { name: /Create profile/i }))

    await waitFor(() =>
      expect(screen.getByText(/Business name must be at least 3 characters/i)).toBeInTheDocument(),
    )

    fireEvent.change(screen.getByLabelText(/Business name/i), { target: { value: 'Valid Biz' } })
    fireEvent.change(screen.getByLabelText(/Portfolio image/i), {
      target: { files: [new File(['plain text'], 'notes.txt', { type: 'text/plain' })] },
    })

    await waitFor(() => expect(screen.getByText(/Only jpg, png, and webp images are allowed/i)).toBeInTheDocument())
  })

  it('submits successfully, shows loading, and triggers API calls', async () => {
    let resolvePortfolio: (value: unknown) => void = () => undefined

    mockApiPost.mockImplementation((url: string) => {
      if (url === '/vendors/vendors/') {
        return Promise.resolve({ data: { id: 1 } })
      }
      if (url === '/vendors/portfolio/') {
        return new Promise((resolve) => {
          resolvePortfolio = resolve
        })
      }
      return Promise.resolve({ data: {} })
    })

    mockCanvas()
    render(<VendorOnboarding />)

    fireEvent.change(screen.getByLabelText(/Business name/i), { target: { value: 'Valid Biz' } })
    fireEvent.change(screen.getByLabelText(/Description/i), { target: { value: 'Great events' } })
    fireEvent.change(screen.getByLabelText(/Location/i), { target: { value: 'Lagos' } })
    fireEvent.change(screen.getByLabelText(/Portfolio title/i), { target: { value: 'Wedding Gallery' } })

    const image = new File(['fake-image-bytes'], 'portfolio.jpg', { type: 'image/jpeg' })
    fireEvent.change(screen.getByLabelText(/Portfolio image/i), { target: { files: [image] } })

    fireEvent.click(screen.getByRole('button', { name: /Create profile/i }))

    await waitFor(() => expect(screen.getByRole('button', { name: /Creating/i })).toBeDisabled())
    expect(mockApiPost).toHaveBeenCalledWith('/vendors/vendors/', {
      display_name: 'Valid Biz',
      bio: 'Great events',
      location: 'Lagos',
    })

    await waitFor(() => expect(mockApiPost).toHaveBeenCalledWith('/vendors/portfolio/', expect.any(FormData), expect.any(Object)))

    await act(async () => {
      resolvePortfolio({ data: { id: 99 } })
    })

    await waitFor(() => expect(screen.getByText(/Vendor profile created successfully/i)).toBeInTheDocument())
    expect(mockPush).toHaveBeenCalledWith('/vendor/dashboard')
  })
})

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import VendorOnboarding from '../app/vendor/onboarding/page'

jest.mock('../lib/api', () => ({
  api: {
    post: jest.fn(() => Promise.resolve({ data: {} })),
  },
}))

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn() }),
}))

describe('VendorOnboarding', () => {
  it('validates form and submits', async () => {
    render(<VendorOnboarding />)

    const nameInput = screen.getByLabelText(/Business name/i)
    const desc = screen.getByLabelText(/Description/i)
    const loc = screen.getByLabelText(/Location/i)
    const button = screen.getByRole('button', { name: /Create profile/i })

    fireEvent.change(nameInput, { target: { value: 'AB' } })
    fireEvent.change(desc, { target: { value: 'My desc' } })
    fireEvent.change(loc, { target: { value: 'Here' } })

    fireEvent.click(button)

    // short name should trigger validation error and not submit
    await waitFor(() => expect(screen.getByText(/Business name must be at least 3 characters/)).toBeInTheDocument())
  })
})

import Link from 'next/link'

export default function Home() {
  return (
    <main style={{padding: 24}}>
      <h1>EventChain AI</h1>
      <p>Welcome to the frontend scaffold.</p>
      <p><Link href="/planner">Open AI Planner</Link></p>
    </main>
  )
}

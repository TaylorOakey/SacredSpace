import { useState, useEffect, useRef } from 'react'

const API = 'http://localhost:8888'

export default function useSyncSocket(intervalMs = 10_000) {
  const [status, setStatus] = useState(null)   // { nodes, edges, uptime_seconds }
  const [error, setError]   = useState(null)
  const timerRef = useRef(null)

  async function poll() {
    try {
      const res = await fetch(`${API}/mobile/status`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      setStatus(await res.json())
      setError(null)
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => {
    poll()
    timerRef.current = setInterval(poll, intervalMs)
    return () => clearInterval(timerRef.current)
  }, [intervalMs])

  return { status, error }
}

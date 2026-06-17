import { useState, useEffect, useCallback } from 'react'
import { getHistory as fetchHistory, getProfile as fetchProfile } from '../api/sigil'

export interface HistoryEntry {
  id: number
  query: string
  dimension: string
  result_count: number
  source: string
  created_at: string
}

export interface CasterProfile {
  resonance: number
  xp: number
  insight: number
  level: number
  queries_cast: number
  spells_cast: number
}

export function useSigilHistory() {
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [profile, setProfile] = useState<CasterProfile | null>(null)
  const [loading, setLoading] = useState(false)

  const refresh = useCallback(async () => {
    setLoading(true)
    try {
      const [hRes, pRes] = await Promise.all([
        fetchHistory(50),
        fetchProfile(),
      ])
      setHistory(hRes.history || [])
      setProfile((pRes.profile || {}) as CasterProfile)
    } catch {
      // silent — backend may be offline
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { refresh() }, [refresh])

  return { history, profile, loading, refresh }
}

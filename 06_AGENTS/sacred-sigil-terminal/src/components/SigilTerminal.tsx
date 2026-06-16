import React, { useState, useEffect, useRef, useCallback } from 'react'
import { querySigil, getDimensions, getStatus, listSpells, executeSpell } from '../api/sigil'
import { useSigilHistory } from '../hooks/useSigilHistory'

// ── Types ──────────────────────────────────────────────────────────────

interface Dimension {
  id: string
  name: string
  description: string
  icon?: string
  color?: string
}

interface SigilResult {
  title: string
  path?: string
  preview: string
  dimension: string
  score?: number
  source?: string
}

interface SpellInfo {
  id: string
  name: string
  description: string
  effect?: string
  cost?: Record<string, number>
  reward?: Record<string, number>
}

const DIMENSION_COLORS: Record<string, string> = {
  vault: '#8B5A8F', grove: '#2D5016', forest: '#3A5C3A', codex: '#8B7355',
  memory: '#5A5A8F', agent: '#8F5A5A', social: '#5A8F8F', market: '#8F8F5A', path: '#5A8F5A',
}

const DIMENSION_ICONS: Record<string, string> = {
  vault: '📚', grove: '🌳', forest: '🌲', codex: '📖',
  memory: '💎', agent: '✨', social: '👥', market: '🛍️', path: '🎓',
}

type ViewState = 'home' | 'results' | 'spell-result' | 'history' | 'profile' | 'error'

// ── Component ──────────────────────────────────────────────────────────

export default function SigilTerminal() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SigilResult[]>([])
  const [dimensions, setDimensions] = useState<Dimension[]>([])
  const [spells, setSpells] = useState<SpellInfo[]>([])
  const [view, setView] = useState<ViewState>('home')
  const [loading, setLoading] = useState(false)
  const [statusText, setStatusText] = useState('⟡ Sacred Sigil Terminal v2.0 — Online')
  const [error, setError] = useState<string | null>(null)
  const [spellResult, setSpellResult] = useState<any>(null)
  const [selectedIndex, setSelectedIndex] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)
  const { history, profile, refresh: refreshHistory } = useSigilHistory()

  // ── Init ───────────────────────────────────────────────────────────

  useEffect(() => {
    getStatus().then(s => {
      setStatusText(`⟡ ${s.terminal} — ${s.dimensions} dimensions live`)
    }).catch(() => {
      setStatusText('⟡ Terminal — Backend offline (demo mode, install pnpm dev deps)')
    })
    getDimensions().then(d => setDimensions(d.dimensions || [])).catch(() => {})
    listSpells().then(s => setSpells(s.spells || [])).catch(() => {})
  }, [])

  // ── Keyboard shortcuts ─────────────────────────────────────────────

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        inputRef.current?.focus()
      }
      if (e.key === 'Escape' && view === 'home') {
        setQuery(''); setResults([]); inputRef.current?.blur()
      }
      if (e.key === 'h' && document.activeElement !== inputRef.current) {
        e.preventDefault(); refreshHistory(); setView('history')
      }
      if (e.key === 'p' && document.activeElement !== inputRef.current) {
        e.preventDefault(); refreshHistory(); setView('profile')
      }
      if (results.length > 0) {
        if (e.key === 'ArrowDown') {
          e.preventDefault(); setSelectedIndex(i => Math.min(i + 1, results.length - 1))
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault(); setSelectedIndex(i => Math.max(i - 1, 0))
        }
        if (e.key === 'Enter' && view === 'results') {
          e.preventDefault(); handleSelectResult(results[selectedIndex])
        }
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [results, selectedIndex, view])

  // ── Query handler ─────────────────────────────────────────────────

  const handleQuery = useCallback(async (q: string) => {
    const trimmed = q.trim()
    if (!trimmed) { setView('home'); setResults([]); return }
    setLoading(true); setView('results'); setError(null); setSelectedIndex(0)

    try {
      const res = await querySigil(trimmed)
      setResults(res.results || [])
      setStatusText(
        res.results?.length
          ? `${res.total} result${res.total !== 1 ? 's' : ''} for "${trimmed}"`
          : `No results for "${trimmed}"`
      )
    } catch (err: any) {
      setResults([])
      setError(err.message || 'Query failed')
      setStatusText('Query failed — backend unreachable')
    } finally {
      setLoading(false)
    }
  }, [])

  const handleSelectResult = useCallback((result: SigilResult) => {
    setStatusText(`Selected: ${result.title} [${result.dimension}]`)
    if (result.path) window.open(result.path, '_blank')
  }, [])

  const handleDimensionClick = useCallback((dimId: string) => {
    setQuery(dimId); handleQuery(dimId)
  }, [handleQuery])

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && query.trim()) handleQuery(query)
  }, [query, handleQuery])

  const handleCastSpell = useCallback(async (spellId: string) => {
    setLoading(true); setError(null)
    try {
      const result = await executeSpell(spellId)
      setSpellResult(result); setView('spell-result')
      setStatusText(`Spell cast: ${result.spell}`)
    } catch (err: any) {
      setError(err.message || 'Spell failed'); setView('error')
    } finally {
      setLoading(false)
    }
  }, [])

  // ── Render helpers ─────────────────────────────────────────────────

  const renderHome = () => (
    <>
      <div className="welcome">
        <h2>∆ Navigate the Nine Dimensions</h2>
        <p>Type a query, select a dimension, or cast a spell</p>
        <p className="canon">In lakesh alakin. ∆</p>
      </div>
      <div className="dim-grid">
        {dimensions.map(dim => (
          <button key={dim.id} className="dim-button" onClick={() => handleDimensionClick(dim.id)} title={dim.description}>
            <span className="dim-icon">{DIMENSION_ICONS[dim.id] || '◈'}</span>
            <span className="dim-name">{dim.name.replace(/[∞◊∆⊙≈♦⊗⊜Λ]\s*/, '')}</span>
          </button>
        ))}
      </div>
      {spells.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <div className="welcome"><h2>♦ Spells</h2></div>
          <div className="dim-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))' }}>
            {spells.map(sp => (
              <button key={sp.id} className="dim-button" style={{ borderColor: 'rgba(0,212,255,0.3)' }}
                onClick={() => handleCastSpell(sp.id)} title={sp.description}>
                <span className="dim-name" style={{ fontSize: 11, color: '#00d4ff' }}>{sp.name}</span>
                <span style={{ fontSize: 10, color: 'rgba(255,255,255,0.4)' }}>{sp.effect}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  )

  const renderResults = () => {
    if (loading) {
      return (
        <div className="loading-state">
          <div className="spinner">⟳</div>
          <p>Querying the Sacred Universe...</p>
        </div>
      )
    }
    if (error) return <div className="error-state">{error}</div>
    if (results.length === 0) {
      return (
        <div className="no-results">
          <p>No results found for "{query}"</p>
          <p className="hint">Try a dimension name, concept, or spell</p>
        </div>
      )
    }
    return results.map((r, i) => (
      <div key={`${r.dimension}-${r.title}-${i}`} className="result-card"
        style={{ borderLeftColor: DIMENSION_COLORS[r.dimension] || 'var(--sigil-primary)' }}
        onClick={() => handleSelectResult(r)}>
        <div className="result-header">
          <span className="result-badge">{r.dimension}</span>
          <span className="result-title">{r.title}</span>
        </div>
        <p className="result-preview">{r.preview}</p>
      </div>
    ))
  }

  const renderSpellResult = () => {
    if (!spellResult) return null
    return (
      <div className="spell-output">
        <h3>♦ {spellResult.spell}</h3>
        <div className="effect">
          {spellResult.effect && <p><strong>Effect:</strong> {spellResult.effect}</p>}
          {spellResult.output?.response && <p>{spellResult.output.response}</p>}
          {spellResult.output?.insight?.response && <p>{spellResult.output.insight.response}</p>}
          {spellResult.output?.connections?.response && <p>{spellResult.output.connections.response}</p>}
          {spellResult.output?.path && (
            <div>
              <p><strong>Path found:</strong> {spellResult.output.path.hops} hop(s)</p>
              {spellResult.output.path.path?.map((n: any, i: number) => (
                <p key={i} style={{ paddingLeft: 12 }}>{'→'.repeat(i + 1)} {n.label}</p>
              ))}
            </div>
          )}
          {spellResult.output?.stored?.stored && <p>✓ Stored to {spellResult.output.stored.path}</p>}
        </div>
        <div className="meta">
          {spellResult.cost && <span>Cost: {JSON.stringify(spellResult.cost)} · </span>}
          {spellResult.reward && <span>Reward: {JSON.stringify(spellResult.reward)}</span>}
        </div>
        <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
          onClick={() => setView('home')}>← Back</button>
      </div>
    )
  }

  // ── History View ──────────────────────────────────────────────────

  const renderHistory = () => (
    <div className="sigil-section">
      <h3 className="section-title">◈ Sigil History</h3>
      {history.length === 0 ? (
        <div className="no-results"><p>No queries yet. Cast your first sigil!</p></div>
      ) : (
        <div className="history-list">
          {history.map((entry) => (
            <div key={entry.id} className="history-entry" onClick={() => {
              setQuery(entry.query); setView('home')
            }}>
              <div className="history-query">"{entry.query}"</div>
              <div className="history-meta">
                <span className="history-dim">{entry.dimension}</span>
                <span>{entry.result_count} result{entry.result_count !== 1 ? 's' : ''}</span>
                <span className="history-time">{new Date(entry.created_at).toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
      <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
        onClick={() => setView('home')}>← Back</button>
    </div>
  )

  // ── Profile View ──────────────────────────────────────────────────

  const renderProfile = () => {
    const p = profile
    return (
      <div className="sigil-section">
        <h3 className="section-title">⟡ Caster Profile</h3>
        {!p ? (
          <div className="no-results"><p>Loading profile...</p></div>
        ) : (
          <div className="profile-display">
            <div className="profile-level">Level {p.level || 1}</div>
            <div className="profile-stats">
              <div className="profile-stat">
                <span className="stat-label">✦ Resonance</span>
                <span className="stat-value" style={{ color: '#8B5A8F' }}>{p.resonance ?? 50}</span>
              </div>
              <div className="profile-stat">
                <span className="stat-label">⚡ XP</span>
                <span className="stat-value" style={{ color: '#00d4ff' }}>{p.xp ?? 0}</span>
              </div>
              <div className="profile-stat">
                <span className="stat-label">⊙ Insight</span>
                <span className="stat-value" style={{ color: '#8B7355' }}>{p.insight ?? 0}</span>
              </div>
              <div className="profile-stat">
                <span className="stat-label">🔮 Queries</span>
                <span className="stat-value">{p.queries_cast ?? 0}</span>
              </div>
              <div className="profile-stat">
                <span className="stat-label">♦ Spells</span>
                <span className="stat-value">{p.spells_cast ?? 0}</span>
              </div>
            </div>
            <div className="xp-bar-container">
              <div className="xp-bar-label">Next level: {(p.level || 1) * 100} XP</div>
              <div className="xp-bar">
                <div className="xp-bar-fill" style={{ width: `${Math.min(100, ((p.xp ?? 0) / ((p.level || 1) * 100)) * 100)}%` }} />
              </div>
            </div>
          </div>
        )}
        <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
          onClick={() => setView('home')}>← Back</button>
      </div>
    )
  }

  // ── Main Render ────────────────────────────────────────────────────

  return (
    <div className="sigil-terminal">
      <div className="sigil-header">
        <span className="sigil-title">🔮 Sacred Sigil Terminal</span>
        <span className="sigil-subtitle">v2.0</span>
      </div>

      <div className="sigil-input-wrapper">
        <input ref={inputRef} type="text" className="sigil-input"
          placeholder="navigate the sacred universe... (⌘K)"
          value={query}
          onChange={e => {
            setQuery(e.target.value)
            if (e.target.value.length === 0) { setView('home'); setResults([]); setError(null) }
          }}
          onKeyDown={handleKeyDown}
          autoFocus
        />
        {!query && (
          <span className="sigil-hint">Try: <strong>vault</strong>, <strong>codex</strong>, <strong>AURORA.WEAVE()</strong></span>
        )}
      </div>

      <div className="sigil-output">
        {view === 'home' && renderHome()}
        {view === 'results' && renderResults()}
        {view === 'spell-result' && renderSpellResult()}
        {view === 'history' && renderHistory()}
        {view === 'profile' && renderProfile()}
        {view === 'error' && <div className="error-state">{error}</div>}
      </div>

      <div className="sigil-status">
        <span className={`sigil-status-dot ${loading ? 'loading' : ''}`} />
        {statusText}
        {profile && view === 'home' && (
          <span style={{ marginLeft: 12, opacity: 0.5, fontSize: 10 }}>
            Lv.{profile.level} | ⟡{profile.resonance}
          </span>
        )}
        <span style={{ marginLeft: 'auto', opacity: 0.3 }}>↑↓ Enter · h(history) p(profile) Esc</span>
      </div>
    </div>
  )
}

import React, { useState, useEffect, useRef, useCallback } from 'react'
import { querySigil, getDimensions, getStatus, listSpells, executeSpell,
  getStoryIndex, getStoryCharacters, getStoryEpisodes, getStoryNodes, getStoryArchetypes, getStorySchools,
  parseGrammar, lintGrammar, getGrammarLibrary, listMacros, createMacro, deleteMacro,
  ParseResponse, GrammarLibraryResponse, MacroListResponse } from '../api/sigil'
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
  lore: '#FF6B35',
}

const DIMENSION_ICONS: Record<string, string> = {
  vault: '📚', grove: '🌳', forest: '🌲', codex: '📖',
  memory: '💎', agent: '✨', social: '👥', market: '🛍️', path: '🎓', lore: '📜',
}

type ViewState = 'home' | 'results' | 'spell-result' | 'history' | 'profile' | 'story' | 'grammar' | 'library' | 'macros' | 'error'

type StoryCategory = 'overview' | 'characters' | 'episodes' | 'nodes' | 'archetypes' | 'schools'

interface StoryCharacter {
  id: string; name: string; archetype: string; archetype_name?: string
  episode?: number; episode_title?: string; node?: string; role?: string
  description?: string; glyph?: string; color?: string
  cipher_verse?: string; element?: string; soul_tone?: number
  is_meta?: boolean; is_transcendent?: boolean; title?: string; domain?: string
}

interface StoryEpisode {
  episode_number: number | string; title: string; npc: string
  archetype: string; node: string; spell_unlocked: string
  core_lesson: string; summary: string
}

interface StoryNode {
  id: string; name: string; number: number
  guardian_name?: string; element?: string; unlock?: string
  description?: string; color?: string
}

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
  const [storyCat, setStoryCat] = useState<StoryCategory>('overview')
  const [storyIndex, setStoryIndex] = useState<any>(null)
  const [storyCharacters, setStoryCharacters] = useState<StoryCharacter[]>([])
  const [storyEpisodes, setStoryEpisodes] = useState<StoryEpisode[]>([])
  const [storyNodes, setStoryNodes] = useState<StoryNode[]>([])
  const [storyArchetypes, setStoryArchetypes] = useState<any[]>([])
  const [storySchools, setStorySchools] = useState<any[]>([])
  const [storyDetail, setStoryDetail] = useState<any>(null)
  const [grammarInput, setGrammarInput] = useState('')
  const [grammarResult, setGrammarResult] = useState<ParseResponse | null>(null)
  const [libraryData, setLibraryData] = useState<GrammarLibraryResponse | null>(null)
  const [macros, setMacros] = useState<MacroListResponse['macros']>([])
  const [macroEditor, setMacroEditor] = useState({ name: '', composition: '', description: '', show: false })
  const [libTab, setLibTab] = useState('sigils')

  // ── Story loader ──────────────────────────────────────────────────

  const loadStory = useCallback(async () => {
    try {
      const [idx, chars, eps, nds, archs, schs] = await Promise.all([
        getStoryIndex(), getStoryCharacters(), getStoryEpisodes(),
        getStoryNodes(), getStoryArchetypes(), getStorySchools(),
      ])
      setStoryIndex(idx)
      setStoryCharacters(chars.characters || [])
      setStoryEpisodes(eps.episodes || [])
      setStoryNodes(nds.nodes || [])
      setStoryArchetypes(archs.archetypes || [])
      setStorySchools(schs.schools || [])
    } catch { /* story backend unavailable */ }
  }, [])

  const loadMacros = useCallback(async () => {
    try { const m = await listMacros(); setMacros(m.macros || []) } catch {}
  }, [])

  // ── Init ───────────────────────────────────────────────────────────

  useEffect(() => {
    getStatus().then(s => {
      setStatusText(`⟡ ${s.terminal} — ${s.dimensions} dimensions live`)
    }).catch(() => {
      setStatusText('⟡ Terminal — Backend offline (demo mode, install pnpm dev deps)')
    })
    getDimensions().then(d => setDimensions(d.dimensions || [])).catch(() => {})
    listSpells().then(s => setSpells(s.spells || [])).catch(() => {})
    getGrammarLibrary().then(d => setLibraryData(d)).catch(() => {})
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
      if (e.key === 's' && document.activeElement !== inputRef.current) {
        e.preventDefault(); loadStory(); setView('story'); setStoryCat('overview')
      }
      if (e.key === 'g' && document.activeElement !== inputRef.current) {
        e.preventDefault(); setGrammarInput(''); setGrammarResult(null); setView('grammar')
      }
      if (e.key === 'l' && document.activeElement !== inputRef.current) {
        e.preventDefault(); setLibTab('sigils'); setView('library')
      }
      if (e.key === 'm' && document.activeElement !== inputRef.current) {
        e.preventDefault(); loadMacros(); setView('macros')
        setMacroEditor({ name: '', composition: '', description: '', show: false })
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

  // ── Story View ────────────────────────────────────────────────────

  const renderStory = () => {
    const catMap: { key: StoryCategory; label: string }[] = [
      { key: 'overview', label: '📜 Overview' },
      { key: 'characters', label: `👥 Characters (${storyCharacters.length})` },
      { key: 'episodes', label: `🎬 Episodes (${storyEpisodes.length})` },
      { key: 'nodes', label: `🗺 Nodes (${storyNodes.length})` },
      { key: 'archetypes', label: `🃏 Archetypes (${storyArchetypes.length})` },
      { key: 'schools', label: `🏫 Schools (${storySchools.length})` },
    ]

    return (
      <div className="sigil-section">
        <div className="section-title">📜 Sacred Storyline — Jenga's Journey</div>
        <div className="story-tabs">
          {catMap.map(c => (
            <button key={c.key} className={`story-tab ${storyCat === c.key ? 'active' : ''}`}
              onClick={() => { setStoryCat(c.key); setStoryDetail(null) }}>
              {c.label}
            </button>
          ))}
        </div>
        <div className="story-content">
          {storyDetail ? renderStoryDetail() : (
            storyCat === 'overview' ? renderStoryOverview() :
            storyCat === 'characters' ? renderStoryCharList() :
            storyCat === 'episodes' ? renderStoryEpList() :
            storyCat === 'nodes' ? renderStoryNodeList() :
            storyCat === 'archetypes' ? renderStoryArchList() :
            renderStorySchoolList()
          )}
        </div>
        <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
          onClick={() => setView('home')}>← Back to Terminal</button>
      </div>
    )
  }

  const renderStoryOverview = () => {
    const idx = storyIndex
    if (!idx) return <div className="no-results"><p>Loading story...</p></div>
    return (
      <div className="story-overview">
        <div className="story-hero">
          <div style={{ fontSize: 24, fontWeight: 700 }}>{idx.title}</div>
          <div style={{ fontSize: 14, opacity: 0.7 }}>{idx.subtitle}</div>
          <div style={{ marginTop: 8, fontSize: 12, opacity: 0.5 }}>{idx.canon}</div>
        </div>
        <div className="story-stats">
          <div className="stat-card"><span className="stat-num">{idx.characters}</span>Characters</div>
          <div className="stat-card"><span className="stat-num">{idx.episodes}</span>Episodes</div>
          <div className="stat-card"><span className="stat-num">{idx.nodes}</span>Nodes</div>
          <div className="stat-card"><span className="stat-num">{idx.archetypes}</span>Archetypes</div>
          <div className="stat-card"><span className="stat-num">{idx.schools}</span>Schools</div>
          <div className="stat-card"><span className="stat-num">{idx.total_spells}</span>Spells</div>
        </div>
        <div className="story-entities">
          <div><strong>Protagonist:</strong> {idx.protagonist}</div>
          <div><strong>Antagonist:</strong> {idx.antagonist}</div>
          <div><strong>Overmind:</strong> {idx.overmind}</div>
        </div>
      </div>
    )
  }

  const renderStoryCharList = () => {
    if (storyCharacters.length === 0) return <div className="no-results"><p>No characters loaded</p></div>
    return (
      <div className="story-list">
        {storyCharacters.map(c => (
          <div key={c.id} className={`story-item ${c.is_meta ? 'meta' : c.is_transcendent ? 'transcendent' : ''}`}
            style={{ borderLeftColor: c.color || 'var(--sigil-primary)' }}
            onClick={() => setStoryDetail({ type: 'character', data: c })}>
            <div className="story-item-header">
              <span className="story-item-name">{c.glyph || '👤'} {c.name}</span>
              <span className="story-item-badge">{c.archetype || c.title || ''}</span>
            </div>
            <div className="story-item-sub">{c.role || c.domain || c.description?.slice(0, 80) || ''}</div>
          </div>
        ))}
      </div>
    )
  }

  const renderStoryEpList = () => {
    if (storyEpisodes.length === 0) return <div className="no-results"><p>No episodes loaded</p></div>
    return (
      <div className="story-list">
        {storyEpisodes.map(ep => (
          <div key={String(ep.episode_number)} className="story-item"
            onClick={() => setStoryDetail({ type: 'episode', data: ep })}>
            <div className="story-item-header">
              <span className="story-item-name">Ep {ep.episode_number}: {ep.title}</span>
              <span className="story-item-badge">{ep.npc}</span>
            </div>
            <div className="story-item-sub">{ep.core_lesson} · {ep.node}</div>
          </div>
        ))}
      </div>
    )
  }

  const renderStoryNodeList = () => {
    if (storyNodes.length === 0) return <div className="no-results"><p>No nodes loaded</p></div>
    return (
      <div className="story-list">
        {storyNodes.map(n => (
          <div key={n.id} className="story-item"
            style={{ borderLeftColor: n.color || 'var(--sigil-primary)' }}
            onClick={() => setStoryDetail({ type: 'node', data: n })}>
            <div className="story-item-header">
              <span className="story-item-name">Node {n.number}: {n.name}</span>
              <span className="story-item-badge">{n.guardian_name || ''}</span>
            </div>
            <div className="story-item-sub">{n.unlock || n.description?.slice(0, 80) || ''}</div>
          </div>
        ))}
      </div>
    )
  }

  const renderStoryArchList = () => {
    if (storyArchetypes.length === 0) return <div className="no-results"><p>No archetypes loaded</p></div>
    return (
      <div className="story-list">
        {storyArchetypes.map(a => (
          <div key={String(a.number)} className="story-item"
            onClick={() => setStoryDetail({ type: 'archetype', data: a })}>
            <div className="story-item-header">
              <span className="story-item-name">{a.number}. {a.name}</span>
              <span className="story-item-badge">Tone {a.soul_tone} · {a.element}</span>
            </div>
            <div className="story-item-sub">{a.npc ? `Embodied by ${a.npc}` : ''} {a.description?.slice(0, 60)}</div>
          </div>
        ))}
      </div>
    )
  }

  const renderStorySchoolList = () => {
    if (storySchools.length === 0) return <div className="no-results"><p>No schools loaded</p></div>
    return (
      <div className="story-list">
        {storySchools.map(s => (
          <div key={s.id} className="story-item"
            style={{ borderLeftColor: s.color || 'var(--sigil-primary)' }}
            onClick={() => setStoryDetail({ type: 'school', data: s })}>
            <div className="story-item-header">
              <span className="story-item-name">{s.name}</span>
              <span className="story-item-badge">{s.element} · {s.guardian}</span>
            </div>
            <div className="story-item-sub">{s.description?.slice(0, 80)}</div>
          </div>
        ))}
      </div>
    )
  }

  const renderStoryDetail = () => {
    if (!storyDetail) return null
    const { type, data } = storyDetail
    return (
      <div className="story-detail">
        <button className="dim-button" style={{ marginBottom: 8, width: 'auto', padding: '4px 12px', fontSize: 11 }}
          onClick={() => setStoryDetail(null)}>← Back to list</button>
        {type === 'character' && (
          <div>
            <h3>{data.glyph || '👤'} {data.name}</h3>
            <div className="story-detail-meta">
              <span>{data.archetype_name || data.archetype}</span>
              {data.element && <span>· {data.element}</span>}
              {data.soul_tone !== undefined && <span>· Tone {data.soul_tone}</span>}
            </div>
            {data.episode && <p><strong>Episode:</strong> {data.episode}: {data.episode_title}</p>}
            {data.node && <p><strong>Node:</strong> {data.node}</p>}
            <p><strong>Role:</strong> {data.role}</p>
            <p>{data.description}</p>
            {data.cipher_verse && <p className="cipher-verse">{data.cipher_verse}</p>}
            {data.title && <p><strong>Title:</strong> {data.title}</p>}
            {data.domain && <p><strong>Domain:</strong> {data.domain}</p>}
          </div>
        )}
        {type === 'episode' && (
          <div>
            <h3>Episode {data.episode_number}: {data.title}</h3>
            <div className="story-detail-meta">
              <span>{data.npc}</span><span>· {data.archetype}</span><span>· {data.node}</span>
            </div>
            <p><strong>Spell unlocked:</strong> {data.spell_unlocked}</p>
            <p><strong>Core lesson:</strong> {data.core_lesson}</p>
            <p>{data.summary}</p>
          </div>
        )}
        {type === 'node' && (
          <div>
            <h3>Node {data.number}: {data.name}</h3>
            <div className="story-detail-meta">
              <span>Guardian: {data.guardian_name}</span>
              {data.element && <span>· {data.element}</span>}
            </div>
            <p><strong>Unlock:</strong> {data.unlock}</p>
            <p>{data.description}</p>
          </div>
        )}
        {type === 'archetype' && (
          <div>
            <h3>{data.number}. {data.name}</h3>
            <div className="story-detail-meta">
              <span>Tarot: {data.tarot_card}</span>
              <span>· Tone {data.soul_tone}</span>
              <span>· {data.element}</span>
            </div>
            {data.npc && <p><strong>Embodied by:</strong> {data.npc}</p>}
            {data.episode && <p><strong>Episode:</strong> {data.episode}</p>}
            <p>{data.description}</p>
          </div>
        )}
        {type === 'school' && (
          <div>
            <h3>{data.name}</h3>
            <div className="story-detail-meta">
              <span>{data.element}</span><span>· {data.guardian}</span>
            </div>
            <p>{data.description}</p>
            <p><strong>Spells:</strong> {data.spells?.join(', ') || ''}</p>
            <p><strong>Episodes:</strong> {data.episodes?.join(', ') || ''}</p>
          </div>
        )}
      </div>
    )
  }

  // ── Grammar View ──────────────────────────────────────────────────

  const renderGrammar = () => (
    <div className="grammar-view">
      <div className="grammar-input-area">
        <input type="text" className="grammar-input" placeholder="Enter sigil string (e.g. ∆:⚒ or AURORA.WEAVE)"
          value={grammarInput} onChange={e => setGrammarInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter' && grammarInput.trim()) {
            parseGrammar(grammarInput.trim()).then(r => setGrammarResult(r)).catch(() => {})
          }}}
          autoFocus />
        <button className="dim-button" style={{ width: 'auto', padding: '8px 16px', whiteSpace: 'nowrap' }}
          onClick={() => { if (grammarInput.trim()) {
            parseGrammar(grammarInput.trim()).then(r => setGrammarResult(r)).catch(() => {})
          }}}>Parse</button>
        <button className="dim-button" style={{ width: 'auto', padding: '8px 16px', whiteSpace: 'nowrap' }}
          onClick={() => { if (grammarInput.trim()) {
            lintGrammar(grammarInput.trim()).then(r => setGrammarResult(r)).catch(() => {})
          }}}>Lint</button>
      </div>
      {grammarResult && (
        <div className="grammar-breakdown">
          <div className="grammar-display">{grammarResult.parsed.display || grammarResult.parsed.original}</div>

          {grammarResult.parsed.is_macro && (
            <div className="grammar-section">
              <div className="grammar-section-title">✦ Macro</div>
              <div className="grammar-item">{grammarResult.parsed.macro_name}()</div>
              <div className="grammar-item">Composition: {grammarResult.parsed.macro_composition}</div>
            </div>
          )}

          {grammarResult.parsed.dimensions?.length > 0 && (
            <div className="grammar-section">
              <div className="grammar-section-title">📍 Dimensions</div>
              {grammarResult.parsed.dimensions.map((d, i) => (
                <div key={i} className="grammar-item">
                  <span className="grammar-glyph">{libraryData?.dimensions.find(x => x.id === d)?.glyph || ''}</span>
                  {d.charAt(0).toUpperCase() + d.slice(1)}
                </div>
              ))}
            </div>
          )}

          {grammarResult.parsed.operations?.length > 0 && (
            <div className="grammar-section">
              <div className="grammar-section-title">⚡ Operations</div>
              {grammarResult.parsed.operations.map((o, i) => (
                <div key={i} className="grammar-item">
                  <span className="grammar-glyph">{libraryData?.root_sigils.find(x => x.id === o)?.glyph || ''}</span>
                  {o.charAt(0).toUpperCase() + o.slice(1)}
                  <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: 10, marginLeft: 6 }}>
                    ({libraryData?.root_sigils.find(x => x.id === o)?.shape_class || ''})
                  </span>
                </div>
              ))}
            </div>
          )}

          {Object.keys(grammarResult.parsed.affixes || {}).length > 0 && (
            <div className="grammar-section">
              <div className="grammar-section-title">🔧 Affixes</div>
              {Object.entries(grammarResult.parsed.affixes).map(([a, v], i) => v && (
                <div key={i} className="grammar-item">{a}</div>
              ))}
            </div>
          )}

          {grammarResult.cost && (
            <div className="grammar-cost">
              <div><span className="grammar-cost-label">Base</span><br/>{grammarResult.cost.base}</div>
              <span className="grammar-cost-sep">+</span>
              <div><span className="grammar-cost-label">Dims</span><br/>{grammarResult.cost.per_dimension}</div>
              <span className="grammar-cost-sep">+</span>
              <div><span className="grammar-cost-label">Affixes</span><br/>{grammarResult.cost.affixes}</div>
              <span className="grammar-cost-sep">=</span>
              <div style={{ fontSize: 28, color: '#00d4ff' }}><span className="grammar-cost-label">Total</span><br/>{grammarResult.cost.total}</div>
            </div>
          )}

          <div className="grammar-description">{grammarResult.description}</div>

          <div style={{ textAlign: 'center' }}>
            {grammarResult.parsed.valid
              ? <span className="grammar-valid">✓ Valid</span>
              : <span className="grammar-invalid">✗ Invalid</span>}
          </div>

          {grammarResult.parsed.errors?.length > 0 && (
            <div className="grammar-lint-output">
              <div className="grammar-invalid" style={{ marginBottom: 6 }}>Errors</div>
              {grammarResult.parsed.errors.map((e, i) => (
                <div key={i} className="grammar-item" style={{ color: '#ff6b6b' }}>• {e}</div>
              ))}
            </div>
          )}
        </div>
      )}
      <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
        onClick={() => setView('home')}>← Back</button>
    </div>
  )

  // ── Library View ──────────────────────────────────────────────────

  const renderLibrary = () => {
    const tabs = [
      { key: 'sigils', label: `Root Sigils (${libraryData?.root_sigils?.length || 0})` },
      { key: 'dims', label: `Dimensions (${libraryData?.dimensions?.length || 0})` },
      { key: 'macros', label: `Macros (${libraryData?.macros?.length || 0})` },
      { key: 'affixes', label: `Affixes (${libraryData?.affixes?.length || 0})` },
    ]
    return (
      <div className="library-view">
        <h3 className="section-title">◈ Grammar Reference</h3>
        <div className="library-tabs">
          {tabs.map(t => (
            <button key={t.key} className={'story-tab ' + (libTab === t.key ? 'active' : '')}
              onClick={() => setLibTab(t.key)}>{t.label}</button>
          ))}
        </div>
        {libTab === 'sigils' && (
          <div className="library-grid">
            {libraryData?.root_sigils?.map(s => (
              <div key={s.id} className="library-card">
                <span className="library-card-glyph">{s.glyph}</span>
                <span className="library-card-name">{s.name}</span>
                <span className="library-card-shape">{s.shape_class}</span>
              </div>
            ))}
          </div>
        )}
        {libTab === 'dims' && (
          <div className="library-grid">
            {libraryData?.dimensions?.map(d => (
              <div key={d.id} className="library-card">
                <span className="library-card-glyph">{d.glyph}</span>
                <span className="library-card-name">{d.name}</span>
              </div>
            ))}
          </div>
        )}
        {libTab === 'macros' && (
          <div className="library-list">
            {libraryData?.macros?.map(m => (
              <div key={m.id} className="library-macro-item">
                <div className="library-macro-header">
                  <span className="library-macro-name">{m.name}()</span>
                  <span className="library-macro-agent">{m.agent}</span>
                </div>
                <div className="library-macro-comp">{m.composition}</div>
                <div style={{ fontSize: 10, color: 'rgba(255,255,255,0.4)', marginTop: 2 }}>{m.description}</div>
                <div style={{ fontSize: 10, color: 'rgba(255,255,255,0.3)', marginTop: 2 }}>
                  Cost: {m.cost_resonance}⟡  Reward: {m.reward_insight}⊙ + {m.reward_xp}⚡
                </div>
              </div>
            ))}
          </div>
        )}
        {libTab === 'affixes' && (
          <div className="library-list">
            {libraryData?.affixes?.map(a => (
              <div key={a.glyph} className="library-macro-item" style={{ textAlign: 'center' }}>
                <span style={{ fontSize: 18 }}>{a.glyph}</span>
                <div style={{ fontSize: 12, marginTop: 4, textTransform: 'capitalize' }}>{a.name}</div>
              </div>
            ))}
          </div>
        )}
        <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
          onClick={() => setView('home')}>← Back</button>
      </div>
    )
  }

  // ── Macros View ───────────────────────────────────────────────────

  const renderMacros = () => (
    <div className="macro-view">
      <h3 className="section-title">♦ Custom Macros</h3>
      <button className="dim-button" style={{ width: 'auto', padding: '8px 16px', marginBottom: 12 }}
        onClick={() => setMacroEditor(prev => ({ ...prev, show: !prev.show }))}>
        {macroEditor.show ? '− Cancel' : '+ Create Macro'}
      </button>
      {macroEditor.show && (
        <div className="macro-editor">
          <h4>New Custom Macro</h4>
          <input type="text" className="macro-field" placeholder="Name (e.g. MY_CUSTOM.WEAVE)"
            value={macroEditor.name} onChange={e => setMacroEditor(p => ({ ...p, name: e.target.value }))} />
          <input type="text" className="macro-field" placeholder="Composition (e.g. ∆:✦+╻)"
            value={macroEditor.composition} onChange={e => setMacroEditor(p => ({ ...p, composition: e.target.value }))} />
          <textarea className="macro-textarea" placeholder="Description (optional)"
            value={macroEditor.description} onChange={e => setMacroEditor(p => ({ ...p, description: e.target.value }))} />
          <button className="dim-button" style={{ width: 'auto', padding: '8px 16px' }}
            onClick={async () => {
              if (!macroEditor.name.trim() || !macroEditor.composition.trim()) return
              try {
                await createMacro(macroEditor.name.trim(), macroEditor.composition.trim(), macroEditor.description.trim())
                setMacroEditor({ name: '', composition: '', description: '', show: false })
                loadMacros()
              } catch (err: any) { setError(err.message) }
            }}>Create</button>
        </div>
      )}
      {macros.length === 0 ? (
        <div className="macro-empty">No macros found. Create your first custom macro above!</div>
      ) : (
        <div className="library-list">
          {macros.map(m => (
            <div key={m.id} className={'macro-item ' + (m.custom_id ? 'custom' : '')}>
              <div className="macro-info">
                <div className="macro-name">{m.name}()</div>
                <div className="macro-comp">{m.composition}</div>
                <div style={{ fontSize: 10, color: 'rgba(255,255,255,0.4)' }}>{m.description} {m.agent && `— ${m.agent}`}</div>
              </div>
              {m.custom_id && (
                <button className="macro-delete" onClick={async () => {
                  try { await deleteMacro(m.custom_id!); loadMacros() }
                  catch (err: any) { setError(err.message) }
                }} title="Delete macro">×</button>
              )}
            </div>
          ))}
        </div>
      )}
      <button className="dim-button" style={{ marginTop: 12, width: 'auto', padding: '8px 16px' }}
        onClick={() => setView('home')}>← Back</button>
    </div>
  )

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
        {view === 'story' && renderStory()}
        {view === 'grammar' && renderGrammar()}
        {view === 'library' && renderLibrary()}
        {view === 'macros' && renderMacros()}
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
        <span style={{ marginLeft: 'auto', opacity: 0.3 }}>↑↓ Enter · h(hist) p(prof) s(story) g(grammar) l(lib) m(macro) Esc</span>
      </div>
    </div>
  )
}

const API_BASE = '/api/sigil'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export interface StatusResponse {
  status: string
  terminal: string
  dimensions: number
  dimension_list: string[]
  canon: string
}

export interface DimensionListResponse {
  dimensions: Array<{
    id: string
    name: string
    description: string
    icon?: string
    color?: string
  }>
  total: number
}

export interface QueryResponse {
  query: string
  results: Array<{
    title: string
    path?: string
    preview: string
    dimension: string
    score?: number
    source?: string
  }>
  total: number
  dimension?: string
}

export interface SpellsResponse {
  spells: Array<{
    id: string
    name: string
    description: string
    effect?: string
    cost?: Record<string, number>
    reward?: Record<string, number>
  }>
  total: number
}

export interface SpellResponse {
  spell: string
  success: boolean
  effect?: string
  dimensions_touched?: string[]
  cost?: Record<string, number>
  reward?: Record<string, number>
  output?: Record<string, any>
  profile?: Record<string, number>
  level_up?: string
}

export interface HistoryResponse {
  history: Array<{
    id: number
    query: string
    dimension: string
    result_count: number
    source: string
    created_at: string
  }>
  total: number
}

export interface ProfileResponse {
  profile: Record<string, number>
}

export async function getStatus(): Promise<StatusResponse> {
  return request<StatusResponse>('/status')
}

export async function getDimensions(): Promise<DimensionListResponse> {
  return request<DimensionListResponse>('/dimensions')
}

export async function querySigil(query: string, dimension?: string, limit = 10): Promise<QueryResponse> {
  return request<QueryResponse>('/query', {
    method: 'POST',
    body: JSON.stringify({ query, dimension, limit }),
  })
}

export async function listSpells(): Promise<SpellsResponse> {
  return request<SpellsResponse>('/spells')
}

export async function executeSpell(spellId: string, params?: Record<string, any>): Promise<SpellResponse> {
  return request<SpellResponse>('/execute-spell', {
    method: 'POST',
    body: JSON.stringify({ spell_id: spellId, params }),
  })
}

export async function getHistory(limit = 20): Promise<HistoryResponse> {
  return request<HistoryResponse>(`/history?limit=${limit}`)
}

export async function getProfile(): Promise<ProfileResponse> {
  return request<ProfileResponse>('/profile')
}

// ── Story API ─────────────────────────────────────────────────────────────

export interface StoryIndexResponse {
  title: string
  subtitle: string
  canon: string
  characters: number
  nodes: number
  episodes: number
  archetypes: number
  schools: number
  transcendent_entities: number
  weaver_spells: number
  school_spells: number
  total_spells: number
  protagonist: string
  antagonist: string
  overmind: string
}

export interface StoryCharactersResponse {
  characters: Array<{
    id: string
    name: string
    archetype: string
    archetype_name?: string
    episode?: number
    episode_title?: string
    node?: string
    role?: string
    description?: string
    glyph?: string
    color?: string
    cipher_verse?: string
    element?: string
    soul_tone?: number
    is_meta?: boolean
    is_transcendent?: boolean
    title?: string
    domain?: string
  }>
  total: number
}

export interface StoryNodesResponse {
  nodes: Array<{
    id: string
    name: string
    number: number
    guardian_name?: string
    element?: string
    unlock?: string
    description?: string
    color?: string
  }>
  total: number
}

export interface StoryEpisodesResponse {
  episodes: Array<{
    episode_number: number | string
    title: string
    npc: string
    archetype: string
    node: string
    spell_unlocked: string
    core_lesson: string
    summary: string
  }>
  total: number
}

export interface StoryArchetypesResponse {
  archetypes: Array<{
    number: number | string
    name: string
    tarot_card: string
    soul_tone: number
    element: string
    npc: string
    episode?: number | string
    description: string
  }>
  total: number
}

export interface StorySchoolsResponse {
  schools: Array<{
    id: string
    name: string
    element: string
    guardian: string
    description: string
    color: string
    spells: string[]
    episodes: number[]
  }>
  total: number
}

export async function getStoryIndex(): Promise<StoryIndexResponse> {
  return request<StoryIndexResponse>('/story')
}

export async function getStoryCharacters(search?: string): Promise<StoryCharactersResponse> {
  const params = search ? `?search=${encodeURIComponent(search)}` : ''
  return request<StoryCharactersResponse>(`/story/characters${params}`)
}

export async function getStoryCharacter(id: string): Promise<any> {
  return request<any>(`/story/characters/${id}`)
}

export async function getStoryNodes(search?: string): Promise<StoryNodesResponse> {
  const params = search ? `?search=${encodeURIComponent(search)}` : ''
  return request<StoryNodesResponse>(`/story/nodes${params}`)
}

export async function getStoryNode(id: string): Promise<any> {
  return request<any>(`/story/nodes/${id}`)
}

export async function getStoryEpisodes(search?: string): Promise<StoryEpisodesResponse> {
  const params = search ? `?search=${encodeURIComponent(search)}` : ''
  return request<StoryEpisodesResponse>(`/story/episodes${params}`)
}

export async function getStoryEpisode(num: number): Promise<any> {
  return request<any>(`/story/episodes/${num}`)
}

export async function getStoryArchetypes(search?: string): Promise<StoryArchetypesResponse> {
  const params = search ? `?search=${encodeURIComponent(search)}` : ''
  return request<StoryArchetypesResponse>(`/story/archetypes${params}`)
}

export async function getStorySchools(search?: string): Promise<StorySchoolsResponse> {
  const params = search ? `?search=${encodeURIComponent(search)}` : ''
  return request<StorySchoolsResponse>(`/story/schools${params}`)
}

// ── Grammar API ─────────────────────────────────────────────────────

export interface ParseResponse {
  parsed: {
    dimensions: string[]
    operations: string[]
    affixes: Record<string, boolean>
    limit: number | null
    original: string
    is_macro: boolean
    macro_name: string
    macro_composition: string
    errors: string[]
    valid: boolean
    display: string
  }
  cost: { base: number; per_dimension: number; affixes: number; total: number }
  description: string
}

export interface GrammarLibraryResponse {
  dimensions: Array<{ glyph: string; name: string; id: string }>
  root_sigils: Array<{ glyph: string; name: string; id: string; shape_class: string; canonical: string }>
  macros: Array<{ id: string; name: string; composition: string; description: string; agent: string; cost_resonance: number; reward_insight: number; reward_xp: number }>
  affixes: Array<{ glyph: string; name: string }>
  all_macros: Record<string, any>
  version: string
  canon: string
}

export interface MacroListResponse {
  macros: Array<{ id: string; name: string; composition: string; description: string; agent: string; custom_id?: number }>
  total: number
}

export async function parseGrammar(sigil: string): Promise<ParseResponse> {
  return request<ParseResponse>('/grammar/parse', {
    method: 'POST',
    body: JSON.stringify({ sigil }),
  })
}

export async function lintGrammar(sigil: string): Promise<any> {
  return request<any>('/grammar/lint', {
    method: 'POST',
    body: JSON.stringify({ sigil }),
  })
}

export async function getGrammarLibrary(): Promise<GrammarLibraryResponse> {
  return request<GrammarLibraryResponse>('/grammar/library')
}

export async function getSpellCost(spellId: string): Promise<any> {
  return request<any>(`/grammar/spell-cost/${spellId}`)
}

export async function listMacros(): Promise<MacroListResponse> {
  return request<MacroListResponse>('/macros')
}

export async function createMacro(name: string, composition: string, description?: string, agent?: string): Promise<any> {
  return request<any>('/macro', {
    method: 'POST',
    body: JSON.stringify({ name, composition, description: description || '', agent: agent || 'CUSTOM' }),
  })
}

export async function deleteMacro(macroId: number): Promise<any> {
  return request<any>(`/macro/${macroId}`, { method: 'DELETE' })
}

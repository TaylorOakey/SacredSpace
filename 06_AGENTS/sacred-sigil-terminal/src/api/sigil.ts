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

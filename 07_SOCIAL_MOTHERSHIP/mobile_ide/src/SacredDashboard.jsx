import { useState } from 'react'
import Editor from '@monaco-editor/react'
import useSyncSocket from './useSyncSocket'

const PILLARS = [
  { id: '01', label: 'Obsidian Vaults',    icon: '◈' },
  { id: '02', label: 'Council Grove',      icon: '⬡' },
  { id: '03', label: 'Neural Forest',      icon: '⟁' },
  { id: '04', label: 'Sacred Codex',       icon: '⌘' },
  { id: '05', label: 'Memory Engine',      icon: '◎' },
  { id: '06', label: 'Agent Layer',        icon: '⟳' },
  { id: '07', label: 'Social Mothership',  icon: '⬢' },
  { id: '08', label: 'Learning Path',      icon: '◉' },
  { id: '09', label: 'Sacred Market',      icon: '✦' },
]

const STARTER = `// SacredSpace OS — Mobile IDE
// Pillar 07 · Social Mothership

export const sacred = {
  version: '0.1.0',
  theme: 'dark-forest',
  pillars: 9,
}
`

const MONACO_THEME = {
  base: 'vs-dark',
  inherit: true,
  rules: [
    { token: 'comment',   foreground: '2d6a4f', fontStyle: 'italic' },
    { token: 'keyword',   foreground: '74c69d' },
    { token: 'string',    foreground: 'b7e4c7' },
    { token: 'number',    foreground: '95d5b2' },
    { token: 'type',      foreground: '52b788' },
    { token: 'variable',  foreground: 'd8f3dc' },
  ],
  colors: {
    'editor.background':          '#060d07',
    'editor.foreground':          '#d8f3dc',
    'editorLineNumber.foreground':'#2d6a4f',
    'editorLineNumber.activeForeground': '#74c69d',
    'editor.lineHighlightBackground': '#0a1a0c',
    'editorCursor.foreground':    '#74c69d',
    'editor.selectionBackground': '#1b3a1f',
    'editorIndentGuide.background1': '#112614',
    'editorIndentGuide.activeBackground1': '#2d6a4f',
    'scrollbarSlider.background': '#1b3a1f88',
    'scrollbarSlider.hoverBackground': '#2d6a4faa',
  },
}

function beforeMount(monaco) {
  monaco.editor.defineTheme('sacred-forest', MONACO_THEME)
}

export default function SacredDashboard() {
  const [activePillar, setActivePillar] = useState('07')
  const [code, setCode] = useState(STARTER)
  const [cursorInfo, setCursorInfo] = useState({ line: 1, col: 1 })
  const { status, error: syncError } = useSyncSocket(10_000)

  function handleEditorDidMount(editor, monaco) {
    editor.onDidChangeCursorPosition(e => {
      setCursorInfo({ line: e.position.lineNumber, col: e.position.column })
    })
  }

  const pillar = PILLARS.find(p => p.id === activePillar)

  return (
    <div className="flex flex-col h-full bg-forest-900 text-forest-50 font-mono">

      {/* Header */}
      <header className="flex items-center justify-between px-4 py-2 bg-forest-950 border-b border-forest-700 shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-forest-300 text-lg">✦</span>
          <span className="text-forest-50 font-sans font-medium tracking-widest text-sm uppercase">
            Sacred OS
          </span>
        </div>
        <div className="flex items-center gap-3 text-xs text-forest-400">
          {syncError ? (
            <span className="text-red-400">api offline</span>
          ) : status ? (
            <>
              <span className="w-2 h-2 rounded-full bg-forest-300 animate-pulse inline-block" />
              <span>{status.nodes}n · {status.edges}e</span>
              <span className="text-forest-600">↑{Math.floor(status.uptime_seconds / 60)}m</span>
            </>
          ) : (
            <span className="text-forest-600">connecting…</span>
          )}
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">

        {/* Sidebar */}
        <nav className="w-14 md:w-52 flex flex-col bg-forest-950 border-r border-forest-700 shrink-0 overflow-y-auto">
          <p className="hidden md:block px-3 pt-4 pb-2 text-forest-500 text-xs uppercase tracking-widest">
            Pillars
          </p>
          {PILLARS.map(p => (
            <button
              key={p.id}
              onClick={() => setActivePillar(p.id)}
              className={[
                'flex items-center gap-3 px-3 py-2 text-left transition-colors text-sm',
                activePillar === p.id
                  ? 'bg-forest-800 text-forest-100 border-l-2 border-forest-300'
                  : 'text-forest-400 hover:bg-forest-800 hover:text-forest-200 border-l-2 border-transparent',
              ].join(' ')}
            >
              <span className="text-base shrink-0">{p.icon}</span>
              <span className="hidden md:block truncate">{p.id} · {p.label}</span>
            </button>
          ))}
        </nav>

        {/* Editor pane */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Tab bar */}
          <div className="flex items-center gap-1 px-3 py-1 bg-forest-800 border-b border-forest-700 shrink-0">
            <span className="text-forest-300 text-xs">{pillar?.icon}</span>
            <span className="text-forest-200 text-xs ml-1">{pillar?.label}.js</span>
            <span className="ml-1 text-forest-600 text-xs">●</span>
          </div>

          <div className="flex-1 overflow-hidden">
            <Editor
              height="100%"
              defaultLanguage="javascript"
              value={code}
              onChange={v => setCode(v ?? '')}
              theme="sacred-forest"
              beforeMount={beforeMount}
              onMount={handleEditorDidMount}
              options={{
                fontSize: 14,
                fontFamily: "'Cascadia Code', 'Fira Code', ui-monospace, monospace",
                fontLigatures: true,
                lineNumbers: 'on',
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                wordWrap: 'on',
                renderLineHighlight: 'line',
                cursorBlinking: 'smooth',
                smoothScrolling: true,
                padding: { top: 16, bottom: 16 },
              }}
            />
          </div>
        </main>
      </div>

      {/* Status bar */}
      <footer className="flex items-center justify-between px-4 py-1 bg-forest-700 text-forest-200 text-xs shrink-0">
        <span>07_SOCIAL_MOTHERSHIP / mobile_ide / {pillar?.label}.js</span>
        <span>Ln {cursorInfo.line}, Col {cursorInfo.col}</span>
      </footer>

    </div>
  )
}

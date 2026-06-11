import React, { useState, useEffect, useRef } from 'react';
import './SacredSigilTerminal.css';

/**
 * ∆ SACRED SIGIL TERMINAL v2.0 ∆
 * 
 * Universal command palette for navigating the Nine Dimensions of SacredSpace.
 * 
 * Usage:
 * - Desktop: Press Cmd+K (Mac) or Ctrl+K (Windows/Linux)
 * - Mobile: Tap the terminal icon or swipe up from bottom
 * - Embedded: Use as React component or iframe
 * 
 * Commands follow natural language pattern:
 * [ACTION] [OBJECT] [FILTER/CONTEXT]
 */

// ∆ DIMENSION DEFINITIONS
const DIMENSIONS = {
  vault: {
    id: 'vault',
    name: '∞ VAULT',
    icon: '📚',
    description: 'Your Obsidian knowledge & memories',
    color: '#8B5A8F',
    commands: ['show vault', 'search vault', 'create note', 'my memories']
  },
  grove: {
    id: 'grove',
    name: '◊ GROVE',
    icon: '🌳',
    description: 'Council Grove - Agent routing',
    color: '#2D5016',
    commands: ['ask IRIS', 'ask AURORA', 'ask ELIAS', 'ask ASHER', 'invoke agent']
  },
  forest: {
    id: 'forest',
    name: '∆ FOREST',
    icon: '🌲',
    description: 'Neural Forest - Pattern discovery & lore',
    color: '#3A5C3A',
    commands: ['search lore', 'show patterns', 'find connections', 'browse forest']
  },
  codex: {
    id: 'codex',
    name: '⊙ CODEX',
    icon: '📖',
    description: 'Sacred Codex - Canonical rules & truth',
    color: '#8B7355',
    commands: ['what is canonical', 'show rules', 'browse canon', 'game rules']
  },
  memory: {
    id: 'memory',
    name: '≈ MEMORY',
    icon: '💎',
    description: 'Memory Engine - Your persistent state',
    color: '#5A5A8F',
    commands: ['my memories', 'show state', 'what changed', 'history']
  },
  agent: {
    id: 'agent',
    name: '♦ AGENT',
    icon: '✨',
    description: 'Agent Layer - Spells & invocations',
    color: '#8F5A5A',
    commands: ['cast spell', 'invoke AURORA', 'ELIAS.OPEN_PATH()', 'spell list']
  },
  social: {
    id: 'social',
    name: '⊗ SOCIAL',
    icon: '👥',
    description: 'Social Mothership - Community',
    color: '#5A8F8F',
    commands: ['who is online', 'recent activity', 'message player', 'community']
  },
  market: {
    id: 'market',
    name: '⊜ MARKET',
    icon: '🛍️',
    description: 'Sacred Market - Artifacts & exchange',
    color: '#8F8F5A',
    commands: ['browse artifacts', 'marketplace', 'pricing', 'my items']
  },
  path: {
    id: 'path',
    name: 'Λ PATH',
    icon: '🎓',
    description: 'Learning Path - Your growth & progress',
    color: '#5A8F5A',
    commands: ['my progress', 'next lesson', 'maestro check', 'learning path']
  }
};

// ∆ MOCK RESULTS (Replace with real API calls)
const MOCK_RESULTS = {
  vault: [
    { id: 1, title: 'Arcana Grid Definition', type: 'note', dimension: 'vault', preview: 'Metatron at center, 12 archetypes...' },
    { id: 2, title: 'My Memory: Aurora Spell', type: 'memory', dimension: 'vault', preview: 'When I first learned to weave...' },
    { id: 3, title: 'Vault Index', type: 'index', dimension: 'vault', preview: 'Complete knowledge structure...' }
  ],
  grove: [
    { id: 4, title: 'IRIS Agent', type: 'agent', dimension: 'grove', preview: 'The Connector. Knowledge distillation...' },
    { id: 5, title: 'AURORA Agent', type: 'agent', dimension: 'grove', preview: 'The Illuminator. Code generation...' },
    { id: 6, title: 'Council Grove Status', type: 'status', dimension: 'grove', preview: 'All agents online and responsive...' }
  ],
  forest: [
    { id: 7, title: 'Lore: The Well of Twilight', type: 'lore', dimension: 'forest', preview: 'A place balanced between life and mystery...' },
    { id: 8, title: 'Pattern: Growth Cycle', type: 'pattern', dimension: 'forest', preview: 'The seasonal dance of creation...' },
    { id: 9, title: 'Episode 2: The Weaver', type: 'narrative', dimension: 'forest', preview: 'Your hands learn to weave vines...' }
  ],
  codex: [
    { id: 10, title: 'Game Rules', type: 'rules', dimension: 'codex', preview: 'How the sacred game works...' },
    { id: 11, title: 'Magic System', type: 'rules', dimension: 'codex', preview: 'Sigil Levels 1-6 and spell structure...' },
    { id: 12, title: 'Sacred Nodes', type: 'definition', dimension: 'codex', preview: '5 nodes: Center, Jungle, City, Grove, Shadow...' }
  ],
  agent: [
    { id: 13, title: 'AURORA.WEAVE()', type: 'spell', dimension: 'agent', preview: 'Cost: 10 Resonance, Reward: +15...' },
    { id: 14, title: 'ELIAS.OPEN_PATH()', type: 'spell', dimension: 'agent', preview: 'Cost: 5 Resonance, Reward: +8...' },
    { id: 15, title: 'IRIS.THREAD()', type: 'spell', dimension: 'agent', preview: 'Cost: 12 Resonance, Reward: +25...' }
  ]
};

// ∆ QUERY PARSER (Ultra-lite NLP)
const parseQuery = (query) => {
  const lowerQuery = query.toLowerCase();
  
  // Detect dimension keywords
  for (const [key, dimension] of Object.entries(DIMENSIONS)) {
    for (const cmd of dimension.commands) {
      if (lowerQuery.includes(cmd)) {
        return {
          action: 'search',
          dimension: key,
          query: query,
          matched: true
        };
      }
    }
  }
  
  // Fallback: cross-dimension search
  return {
    action: 'cross-search',
    query: query,
    matched: false
  };
};

// ∆ MAIN TERMINAL COMPONENT
export default function SacredSigilTerminal({ embedded = false, onClose = null }) {
  const [isOpen, setIsOpen] = useState(embedded);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [recentQueries, setRecentQueries] = useState([]);
  const inputRef = useRef(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  // ∆ KEYBOARD SHORTCUTS
  useEffect(() => {
    const handleKeyPress = (e) => {
      // Cmd+K or Ctrl+K to open
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
        setTimeout(() => inputRef.current?.focus(), 100);
      }
      
      // Esc to close
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
      
      // Arrow keys to navigate
      if (isOpen && results.length > 0) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          setSelectedIndex((i) => (i + 1) % results.length);
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          setSelectedIndex((i) => (i - 1 + results.length) % results.length);
        }
        if (e.key === 'Enter') {
          e.preventDefault();
          handleSelectResult(results[selectedIndex]);
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isOpen, results, selectedIndex]);

  // ∆ HANDLE QUERY INPUT
  const handleQueryChange = (e) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    
    if (newQuery.length === 0) {
      setResults([]);
      setSelectedIndex(0);
      return;
    }
    
    setIsLoading(true);
    
    // Simulate API delay
    setTimeout(() => {
      const parsed = parseQuery(newQuery);
      
      if (parsed.matched) {
        const dimensionResults = MOCK_RESULTS[parsed.dimension] || [];
        setResults(dimensionResults);
      } else {
        // Cross-dimension search (combine all results)
        const allResults = Object.values(MOCK_RESULTS).flat();
        const filtered = allResults.filter(r =>
          r.title.toLowerCase().includes(newQuery.toLowerCase()) ||
          r.preview.toLowerCase().includes(newQuery.toLowerCase())
        );
        setResults(filtered.slice(0, 10));
      }
      
      setIsLoading(false);
      setSelectedIndex(0);
    }, 200);
  };

  // ∆ HANDLE RESULT SELECTION
  const handleSelectResult = (result) => {
    // Add to recent queries
    setRecentQueries([query, ...recentQueries.slice(0, 9)]);
    
    // Log selection
    console.log('Selected:', result);
    
    // In real app: navigate or trigger action
    // For now, just show confirmation
    alert(`Opening: ${result.title}\n\n(In production, this would navigate or execute the action)`);
    
    setIsOpen(false);
    setQuery('');
    setResults([]);
  };

  // ∆ DIMENSION QUICK ACTIONS
  const DimensionQuickActions = () => (
    <div className="sigil-quick-actions">
      <h3>Quick Actions</h3>
      <div className="action-grid">
        {Object.values(DIMENSIONS).map((dim) => (
          <button
            key={dim.id}
            className="action-button"
            onClick={() => setQuery(`${dim.commands[0]}`)}
            title={dim.description}
            style={{ borderLeftColor: dim.color }}
          >
            <span className="action-icon">{dim.icon}</span>
            <span className="action-name">{dim.name.split(' ')[1]}</span>
          </button>
        ))}
      </div>
    </div>
  );

  // ∆ RESULTS DISPLAY
  const ResultsList = () => (
    <div className="sigil-results">
      {isLoading ? (
        <div className="loading">
          <div className="spinner">⟳</div>
          <p>Querying the Sacred Universe...</p>
        </div>
      ) : results.length > 0 ? (
        <ul className="results-list">
          {results.map((result, index) => (
            <li
              key={result.id}
              className={`result-item ${index === selectedIndex ? 'selected' : ''}`}
              onClick={() => handleSelectResult(result)}
            >
              <div className="result-header">
                <span className="result-dimension">{result.dimension}</span>
                <span className="result-title">{result.title}</span>
              </div>
              <p className="result-preview">{result.preview}</p>
            </li>
          ))}
        </ul>
      ) : query ? (
        <div className="no-results">
          <p>No results found for "{query}"</p>
          <p className="hint">Try a dimension or spell name</p>
        </div>
      ) : (
        <DimensionQuickActions />
      )}
    </div>
  );

  // ∆ MOBILE BOTTOM SHEET OR DESKTOP MODAL
  if (!isOpen) {
    return (
      <button
        className="sigil-trigger-button"
        onClick={() => setIsOpen(true)}
        title="Open Sacred Sigil Terminal (⌘K)"
      >
        🔮
      </button>
    );
  }

  return (
    <div className={`sigil-terminal ${isMobile ? 'mobile' : 'desktop'} ${embedded ? 'embedded' : ''}`}>
      {/* Backdrop */}
      {!embedded && (
        <div
          className="sigil-backdrop"
          onClick={() => setIsOpen(false)}
        />
      )}
      
      {/* Terminal Container */}
      <div className="sigil-container">
        {/* Header */}
        <div className="sigil-header">
          <span className="sigil-title">🔮 Sacred Sigil Terminal</span>
          {!embedded && (
            <button
              className="sigil-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close"
            >
              ✕
            </button>
          )}
        </div>

        {/* Search Input */}
        <div className="sigil-input-wrapper">
          <input
            ref={inputRef}
            type="text"
            className="sigil-input"
            placeholder="navigate the sacred universe... (⌘K)"
            value={query}
            onChange={handleQueryChange}
            autoFocus
          />
          <span className="sigil-hint">
            {query.length === 0 && "Try: 'show my memories' or 'cast AURORA.WEAVE()'"}
          </span>
        </div>

        {/* Results */}
        <ResultsList />

        {/* Footer */}
        <div className="sigil-footer">
          <span className="kbd">↑↓</span> Navigate
          <span className="kbd">Enter</span> Select
          <span className="kbd">Esc</span> Close
        </div>
      </div>
    </div>
  );
}

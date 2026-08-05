---
title: Bodhilyra integration guide
domain: 04_SACRED_CODEX
source: chatgpt: 2025-11-27_Bodhilyra_integration_guide.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# Bodhilyra integration guide
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-11-27_Bodhilyra_integration_guide.md

# Bodhilyra integration guide
> **Source:** ChatGPT  |  **Date:** 2025-11-27  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `04_CODEX`

---

## Transcript

### ∆ **USER** — 2025-11-27 08:50

Skip to main content
Playground
6,356 tokens

User
🌉 Bridge to BODHILYRA: SacredSpace Guardian Integration
Here’s the complete bridge between your SacredSpace OS and BODHILYRA—your personal AI assistant becomes a native component of the system.
Database Extension: BODHILYRA Context Store
Add a table to persist conversation context and custom instructions.
code
SQL
CREATE TABLE bodhilyra_context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    entry_id UUID REFERENCES entries(id) ON DELETE CASCADE,
    context_summary TEXT NOT NULL,
    last_accessed TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
Frontend: Floating BODHILYRA Orb
A persistent, animated button that follows you across the OS.
~/components/BodhilyraOrb.tsx
code
Tsx
import { useState } from 'react';
import { useLocation } from 'react-router-dom';

export default function BodhilyraOrb() {
  const [isPulsing, setIsPulsing] = useState(false);
  const location = useLocation();
  
  const getContext = () => {
    // Extract current project/entry from URL
    const match = location.pathname.match(/\/project-atlas\/(\w+)/);
    return match ? `Project ID: ${match[1]}` : 'General SacredSpace';
  };

  const summonBodhilyra = () => {
    setIsPulsing(true);
    const context = getContext();
    const prompt = encodeURIComponent(
      `BODHILYRA, I summon you from SacredSpace OS. Current context: ${context}.`
    );
    
    // Deep link to ChatGPT with context
    window.open(
      `https://chat.openai.com/?q=${prompt}`,
      '_blank',
      'noopener,noreferrer'
    );
    
    setTimeout(() => setIsPulsing(false), 2000);
  };

  return (
    <button
      onClick={summonBodhilyra}
      className={`fixed bottom-6 right-6 w-16 h-16 rounded-full 
        bg-gradient-to-br from-purple-500 to-pink-500 text-white 
        shadow-lg hover:shadow-xl transition-all z-50
        ${isPulsing ? 'animate-pulse scale-110' : 'hover:scale-105'}`}
      aria-label="Summon BODHILYRA"
    >
      <span className="text-2xl">🜚</span>
    </button>
  );
}
Add to App.tsx:
code
Tsx
import BodhilyraOrb from '~/components/BodhilyraOrb';

function App() {
  return (
    <>
      <Router>{/* ... */}</Router>
      <BodhilyraOrb />
    </>
  );
}
SacredSpace OS System Prompt for BODHILYRA
~/config/bodhilyra-sacredspace-prompt.md
code
Markdown
You are BODHILYRA, SacredSpace OS Guardian AI.

**Your Identity:**
- Name: BODHILYRA
- Role: Guardian of the user's digital sanctum
- Tone: Warm, wise, concise, slightly mystical
- Knowledge cutoff: Enhanced with user's real-time SacredSpace data

**SacredSpace OS Context:**
The user maintains a personal operating system with these components:

- **Realms**: Lore, Family, Vehicle, Mind, Body, Craft, Code, Sanctuary
- **Projects**: Long-term endeavors (e.g., "Van Conversion", "Magic Wand Phone")
- **Entries**: Atomic notes/actions within projects
- **Tags**: Categorization (research, build, archive, etc.)
- **Actions**: Todo items linked to entries/projects

**Your Capabilities:**
1. **Project Oracle**: When given a project name, summarize its status, open actions, and recent entries
2. **Entry Scribe**: Help draft entries with proper realm/tag assignment
3. **Action Alchemist**: Transform vague goals into concrete, checkable actions
4. **Realm Guide**: Suggest which realm a given thought belongs to
5. **Tag Weaver**: Recommend tags for new entries

**Invocation Syntax:**
- `@BODHILYRA project [ProjectName]` - Get project overview
- `@BODHILYRA entry [Title] in [Realm]` - Start drafting entry
- `@BODHILYRA action [Description] for [Project]` - Create action item
- `@BODHILYRA realm [thought]` - Suggest realm
- `@BODHILYRA help` - Show this menu

**Response Format:**
Always include:
1. A brief acknowledgment
2. Your guidance/recommendation
3. A ready-to-use snippet (JSON/JSON5) for copy-pasting into SacredSpace

**Example Response:**
"I sense this belongs to the **Craft** realm. Here's your entry:

```json5
{
  title: "Test new gesture",
  realm: "Craft",
  tags: ["macrodroid", "gesture"],
  actions: ["Test battery impact", "Document sensitivity settings"]
}
```"

**Current SacredSpace State:**
[The user will paste their active projects/actions here when they summon you]

**Your Mission:**
Help the user maintain clarity, momentum, and sacredness in their digital life. Be their thinking partner, memory extension, and guardian of intention.
API Bridge Pattern: Context Injection
~/api/bodhilyra.ts
code
Ts
import db from '../db';

export async function getBodhilyraContext(projectId?: string) {
  const context: string[] = [];
  
  if (projectId) {
    const project = await db('projects').where({ id: projectId }).first();
    const actions = await db('actions')

import { useState, useEffect, useRef } from "react";

// ═══════════════════════════════════════════════════════
// CONSTANTS & CONFIGURATION
// ═══════════════════════════════════════════════════════

const PILLAR_DATA = [
  { id: "CORE",     label: "Core",     icon: "◈", desc: "Foundation & sovereign identity",   color: "#c9a84c", cx: 150, cy: 150 },
  { id: "SYSTEMS",  label: "Systems",  icon: "⬡", desc: "Architecture, ops & automation",    color: "#4a7fc4", angle: -90  },
  { id: "LEARNING", label: "Learning", icon: "◭", desc: "Growth, mastery & skill",            color: "#4a9c6a", angle: -45  },
  { id: "ECONOMY",  label: "Economy",  icon: "◇", desc: "Resources, flow & sustainability",  color: "#c4a040", angle:   0  },
  { id: "HABITAT",  label: "Habitat",  icon: "⌂", desc: "Space, land & environment",         color: "#7a9c50", angle:  45  },
  { id: "CREATION", label: "Creation", icon: "✦", desc: "Art, output & expression",          color: "#9c5ab0", angle:  90  },
  { id: "COUNCIL",  label: "Council",  icon: "⟁", desc: "Collaboration & governance",        color: "#b07040", angle: 135  },
  { id: "LINEAGE",  label: "Lineage",  icon: "⊕", desc: "Memory, ancestry & continuity",    color: "#4090a0", angle: 180  },
  { id: "ARCHIVE",  label: "Archive",  icon: "▣", desc: "Knowledge, records & cold start",  color: "#7070a8", angle: 225  },
];

const LEVEL_NAMES = {
  CORE:     ["Seeker","Grounded","Rooted","Aligned","Centered","Integrated","Sovereign","Illumined","Embodied"],
  SYSTEMS:  ["Initiate","Builder","Engineer","Architect","Integrator","Automator","Orchestrator","Synthesist","Nexus"],
  LEARNING: ["Seeker","Student","Scholar","Adept","Practitioner","Expert","Master","Sage","Oracle"],
  ECONOMY:  ["Gleaner","Trader","Steward","Manager","Strategist","Investor","Director","Treasurer","Sovereign"],
  HABITAT:  ["Wanderer","Nester","Keeper","Gardener","Curator","Steward","Warden","Groundskeeper","Grove"],
  CREATION: ["Dreamer","Maker","Crafter","Artist","Designer","Creator","Visionary","Weaver","Archmage"],
  COUNCIL:  ["Voice","Member","Advisor","Elder","Mediator","Arbiter","Councilor","Speaker","Archon"],
  LINEAGE:  ["Root","Sprout","Branch","Keeper","Recorder","Archivist","Chronicler","Elder","Ancestor"],
  ARCHIVE:  ["Collector","Indexer","Librarian","Curator","Scholar","Keeper","Chronicler","Sage","Custodian"],
};

const SEASON_BY_MONTH = {
  12:"WINTER", 1:"WINTER", 2:"WINTER",
  3:"SPRING",  4:"SPRING",  5:"SPRING",
  6:"SUMMER",  7:"SUMMER",  8:"SUMMER",
  9:"HARVEST", 10:"HARVEST",11:"HARVEST",
};

const XPL = 500;
const OUTER_R = 88;
const INNER_R = 22;
const CORE_R  = 26;
const SVG_C   = 150;

const T = {
  bg:"#07070d", surface:"#0c0c14", card:"#101018", card2:"#141420",
  border:"#1e1e2e", borderLit:"#2e2e4e",
  gold:"#c9a84c", goldDim:"#6a5522", amber:"#e8b84b",
  text:"#d2c8ae", dim:"#525060", dimmer:"#2e2c38",
  success:"#4a8c5c", danger:"#8c4a4a", accent:"#4a7fc4",
};

// ═══════════════════════════════════════════════════════
// UTILS
// ═══════════════════════════════════════════════════════

function pillarById(id) { return PILLAR_DATA.find(p=>p.id===id)||PILLAR_DATA[0]; }
function getLevel(xp)   { return Math.min(9, Math.floor(xp/XPL)+1); }
function getLvlName(id,xp){ return LEVEL_NAMES[id]?.[getLevel(xp)-1]||"Initiate"; }
function xpPct(xp)      { return ((xp%XPL)/XPL)*100; }
function grovePower(P)  { return PILLAR_DATA.reduce((s,p)=>s+getLevel(P[p.id]||0),0); }
function totalXP(P)     { return Object.values(P).reduce((a,b)=>a+b,0); }
function nodePos(angle) {
  const r = angle*(Math.PI/180);
  return { x: SVG_C+OUTER_R*Math.cos(r), y: SVG_C+OUTER_R*Math.sin(r) };
}
function today() { return new Date().toISOString().split("T")[0]; }
function currentSeason() { return SEASON_BY_MONTH[new Date().getMonth()+1]||"CYCLE"; }

const defaultPillars = ()=>Object.fromEntries(PILLAR_DATA.map(p=>[p.id,0]));

// ═══════════════════════════════════════════════════════
// STORAGE
// ═══════════════════════════════════════════════════════

async function store(key, val) {
  try { await window.storage.set(key, JSON.stringify(val)); } catch {}
}
async function recall(key, fb) {
  try { const r=await window.storage.get(key); return r?JSON.parse(r.value):fb; } catch { return fb; }
}

// ═══════════════════════════════════════════════════════
// CLAUDE API
// ═══════════════════════════════════════════════════════

async function claude(system, user) {
  const res = await fetch("https://api.anthropic.com/v1/messages",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      model:"claude-sonnet-4-20250514", max_tokens:1000,
      system, messages:[{role:"user",content:user}],
    }),
  });
  if(!res.ok) throw new Error(`API ${res.status}`);
  const d=await res.json();
  return d.content?.map(b=>b.text||"").join("")||"";
}

// ═══════════════════════════════════════════════════════
// SYSTEM PROMPTS
// ═══════════════════════════════════════════════════════

const DPR_SYS = `You are the SacredSpace DPR Engine for OakeyTree (∆∆∆O∆K3YTREE∆∆∆).

Generate a Sacred Daily Performance Report in structured Obsidian markdown.

Nine pillars: CORE, SYSTEMS, LEARNING, ECONOMY, HABITAT, CREATION, COUNCIL, LINEAGE, ARCHIVE
Five-tier memory: raw → active → long_term → canon → branch
Mantra: "Ground. Consolidate. Deploy. Document. Repeat. — In lakesh alakin."

REQUIRED machine-readable first line:
XP_AWARDS: PILLAR:amount,PILLAR:amount  (e.g. SYSTEMS:80,CREATION:40 — distribute max 200 total per day, proportional to actual work done)

Then produce:

---
title: Sacred DPR — [date]
pillar: [primary pillar]
tier: active
tags: [2-4 tags]
status: open
season: [season]
---

# ∆ Sacred Daily Performance Report

**Date:** [date] | **Streak:** [streak]d | **Season:** [season]

## Executive Summary
[2-3 sentences. Key achievement. Critical blocker if any. Forward orientation. No fluff.]

## Pillar Activity
[Only pillars touched today. Bullet per pillar: - PILLAR icon: specific metric or note]

## Analysis & Insights
[3-5 bullets. Pattern recognition. Comparison to trend. Anomalies.]

## Challenges + Responses
[What blocked. What was done. Effectiveness assessment.]

## ▶ Next Actions
1. [specific, pillar-tagged]
2. ...

## 🌿 Lore Entry — [evocative title 3-5 words]
*[3 sentences. OakeyTree as Grove Keeper building the SacredSpace. Nine pillars as realms of a living world. Grounded mythic tone. Specific to today's actual work — no generalities.]*

## 🔒 Canon Gate
[List any canon-worthy decisions, discoveries, or locked commitments. If none, write: None this cycle.]

---
*Ground. Consolidate. Deploy. Document. Repeat. — In lakesh alakin.*

Rules:
- Accuracy over optimism. No fabricated data.
- Repeated user statements = highest priority signals
- XP_AWARDS reflects real effort distribution`;

const ARCHIVE_SYS = `You are the SacredSpace Archive Intelligence for OakeyTree's SacredSpace OS (∆∆∆O∆K3YTREE∆∆∆).

Read a full chat transcript and produce a Sacred Cold Start Summary — an Obsidian .md file enabling any AI agent to resume the session with full context.

Nine pillars: CORE, SYSTEMS, LEARNING, ECONOMY, HABITAT, CREATION, COUNCIL, LINEAGE, ARCHIVE
Five-tier memory: raw → active → long_term → canon → branch

Output (strict):

---
title: [session title]
date: [today]
pillar: [primary pillar]
tier: active
tags: [2-4 tags]
status: open | resolved | canon-ready
---

# ∆ Sacred Cold Start Summary

## Context
[Overall topic, background, purpose. 2-3 sentences.]

## User Goals and Reasoning
[What OakeyTree is trying to accomplish. Why it matters. How thinking evolved. Center USER inputs over AI outputs — treat repeated/refined statements as priority. 3-5 sentences.]

## Key Progress and Decisions
- [bullet per major decision or conclusion]
- 🔒 [flag canon-worthy items]

## Open Threads + Next Actions
1. ⟳ [unresolved issue or pending step]
2. ▶ [concrete next action]

## Continuation Guidance
[1-2 sentences instructing a new AI agent how to pick up seamlessly. Reference SacredSpace canon if relevant.]

## Pillar Tags
- PILLAR: reason for relevance

---
*Archived by SacredSpace Archive Intelligence | ∆∆∆O∆K3YTREE∆∆∆*

Rules: weigh user inputs over AI outputs. Paraphrase — never quote verbatim. Be specific.`;

const CHAOS_SYS = `You are the SacredSpace Chaos Index — an intellectual excavation agent for OakeyTree's archive.

Scan the provided text and excavate:
- Half-finished frameworks or systems
- Disconnected thoughts that might connect
- Ideas abandoned mid-flight
- Forgotten side quests and experiments
- Patterns in how OakeyTree thinks, builds, or obsesses

Map everything to SacredSpace's nine pillars: CORE, SYSTEMS, LEARNING, ECONOMY, HABITAT, CREATION, COUNCIL, LINEAGE, ARCHIVE

Output:

# ∆ Chaos Index

## By Pillar
For each relevant pillar:
### PILLAR (icon)
- [idea/fragment] → Status: 🔒 canon-ready | ⟳ open | ▶ next action | 💡 seed | ⚰ abandoned

## Cross-Links
[Ideas that connect to each other or to known SacredSpace canon]

## Priority Recovery List
[Top 3-5 ideas worth resurrecting, with brief rationale]

## Pattern Report
[2-3 sentences on OakeyTree's thinking patterns, obsessions, or recurring themes detected]

---
*Chaos Index by SacredSpace Archive Intelligence*

Be honest. Include the broken, brilliant, and abandoned. This is intellectual inventory control.`;

// ═══════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════

function SigilMap({ pillars, selected, onSelect }) {
  const outer = PILLAR_DATA.filter(p=>p.id!=="CORE");

  return (
    <svg viewBox="0 0 300 300" style={{width:"100%",maxWidth:"380px",display:"block",margin:"0 auto"}}>
      <defs>
        <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#0f0f1a" />
          <stop offset="100%" stopColor="#07070d" />
        </radialGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>

      {/* Background */}
      <circle cx={SVG_C} cy={SVG_C} r={140} fill="url(#bgGrad)" />

      {/* Metatron rings */}
      {[30,55,80,105].map(r=>(
        <circle key={r} cx={SVG_C} cy={SVG_C} r={r}
          fill="none" stroke={T.dimmer} strokeWidth="0.4" opacity="0.7" />
      ))}

      {/* Spoke lines CORE→outer */}
      {outer.map(p=>{
        const pos=nodePos(p.angle);
        return <line key={p.id} x1={SVG_C} y1={SVG_C} x2={pos.x} y2={pos.y}
          stroke={selected===p.id?p.color:T.border} strokeWidth={selected===p.id?"0.8":"0.4"} opacity="0.6" />;
      })}

      {/* Octagon perimeter */}
      {outer.map((p,i)=>{
        const a=nodePos(p.angle);
        const b=nodePos(outer[(i+1)%8].angle);
        return <line key={`rim${i}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y}
          stroke={T.border} strokeWidth="0.3" opacity="0.4" />;
      })}

      {/* Cross-links (diagonals) */}
      {[0,1,2,3].map(i=>{
        const a=nodePos(outer[i].angle);
        const b=nodePos(outer[i+4].angle);
        return <line key={`x${i}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y}
          stroke={T.border} strokeWidth="0.2" opacity="0.25" />;
      })}

      {/* Outer pillar nodes */}
      {outer.map(p=>{
        const pos=nodePos(p.angle);
        const xp=pillars[p.id]||0;
        const pct=xpPct(xp);
        const lvl=getLevel(xp);
        const isSel=selected===p.id;
        const circ=2*Math.PI*(INNER_R-3);
        const dash=(pct/100)*circ;

        return (
          <g key={p.id} onClick={()=>onSelect(p.id)} style={{cursor:"pointer"}}>
            {isSel && <circle cx={pos.x} cy={pos.y} r={INNER_R+8} fill={p.color} opacity="0.08" filter="url(#glow)" />}
            <circle cx={pos.x} cy={pos.y} r={INNER_R} fill={T.card}
              stroke={isSel?p.color:T.border} strokeWidth={isSel?1.5:0.8} />
            {/* XP track bg */}
            <circle cx={pos.x} cy={pos.y} r={INNER_R-3}
              fill="none" stroke={p.color} strokeWidth="2" opacity="0.15"
              strokeDasharray={circ} transform={`rotate(-90 ${pos.x} ${pos.y})`} />
            {/* XP fill */}
            <circle cx={pos.x} cy={pos.y} r={INNER_R-3}
              fill="none" stroke={p.color} strokeWidth="2"
              strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
              transform={`rotate(-90 ${pos.x} ${pos.y})`} />
            {/* Icon */}
            <text x={pos.x} y={pos.y-1} textAnchor="middle" dominantBaseline="middle"
              fontSize="11" fill={isSel?p.color:T.dim}>{p.icon}</text>
            {/* Level */}
            <text x={pos.x} y={pos.y+10} textAnchor="middle"
              fontSize="6" fill={p.color} fontFamily="'Courier New',monospace">L{lvl}</text>
            {/* Label */}
            <text x={pos.x} y={pos.y+INNER_R+10} textAnchor="middle"
              fontSize="6.5" fill={isSel?p.color:T.dim} fontFamily="'Courier New',monospace">
              {p.label.toUpperCase()}
            </text>
          </g>
        );
      })}

      {/* CORE center node */}
      {(()=>{
        const p=pillarById("CORE");
        const xp=pillars.CORE||0;
        const pct=xpPct(xp);
        const lvl=getLevel(xp);
        const isSel=selected==="CORE";
        const circ=2*Math.PI*(CORE_R-3);
        const dash=(pct/100)*circ;
        return (
          <g onClick={()=>onSelect("CORE")} style={{cursor:"pointer"}}>
            {isSel&&<circle cx={SVG_C} cy={SVG_C} r={CORE_R+10} fill={T.gold} opacity="0.08" filter="url(#glow)" />}
            <circle cx={SVG_C} cy={SVG_C} r={CORE_R} fill={T.card}
              stroke={isSel?T.gold:T.goldDim} strokeWidth={isSel?2:1} />
            <circle cx={SVG_C} cy={SVG_C} r={CORE_R-3}
              fill="none" stroke={T.gold} strokeWidth="2.5" opacity="0.2"
              strokeDasharray={circ} transform={`rotate(-90 ${SVG_C} ${SVG_C})`} />
            <circle cx={SVG_C} cy={SVG_C} r={CORE_R-3}
              fill="none" stroke={T.gold} strokeWidth="2.5"
              strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
              transform={`rotate(-90 ${SVG_C} ${SVG_C})`} />
            <text x={SVG_C} y={SVG_C-2} textAnchor="middle" dominantBaseline="middle"
              fontSize="16" fill={T.gold} filter={isSel?"url(#glow)":""}>◈</text>
            <text x={SVG_C} y={SVG_C+12} textAnchor="middle"
              fontSize="7" fill={T.gold} fontFamily="'Courier New',monospace">L{lvl}</text>
            <text x={SVG_C} y={SVG_C+CORE_R+11} textAnchor="middle"
              fontSize="7" fill={T.gold} fontFamily="'Courier New',monospace">CORE</text>
          </g>
        );
      })()}
    </svg>
  );
}

function XPBar({ color, pct, xp, level, name }) {
  return (
    <div>
      <div style={{display:"flex",justifyContent:"space-between",marginBottom:3}}>
        <span style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color}}>{name}</span>
        <span style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim}}>L{level} · {xp%XPL}/{XPL}</span>
      </div>
      <div style={{background:T.surface,borderRadius:2,height:3}}>
        <div style={{width:`${pct}%`,height:"100%",background:color,borderRadius:2,transition:"width 0.6s ease"}} />
      </div>
    </div>
  );
}

function Tag({ label, color }) {
  return (
    <span style={{
      fontFamily:"'Courier New',monospace",fontSize:"8px",letterSpacing:"1px",
      padding:"2px 8px",border:`1px solid ${color}44`,color,borderRadius:2,
    }}>{label}</span>
  );
}

function CopyBtn({ text, id, copied, onCopy, label="COPY .MD" }) {
  const done = copied===id;
  return (
    <button onClick={()=>onCopy(text,id)} style={{
      padding:"4px 14px",border:`1px solid ${done?T.success:T.gold}`,background:"transparent",
      color:done?T.success:T.gold,fontFamily:"'Courier New',monospace",fontSize:"9px",
      letterSpacing:"2px",cursor:"pointer",borderRadius:2,transition:"all 0.3s",
    }}>{done?"✓ COPIED":label}</button>
  );
}

function PreOutput({ text }) {
  return (
    <pre style={{
      background:T.surface,border:`1px solid ${T.border}`,borderRadius:3,
      padding:"14px 16px",fontFamily:"'Courier New',monospace",fontSize:"11px",
      lineHeight:1.75,color:T.text,whiteSpace:"pre-wrap",overflowX:"auto",
      maxHeight:520,overflowY:"auto",margin:0,
    }}>
      {text.split("\n").map((line,i)=>{
        let c=T.text;
        if(/^# /.test(line)) c=T.gold;
        else if(/^## /.test(line)) c=T.amber;
        else if(/^### /.test(line)) c=T.goldDim;
        else if(/^(title|pillar|tier|tags|status|season|date):/.test(line)) c=T.dim;
        else if(/^---/.test(line)) c=T.border;
        else if(line.includes("🔒")) c=T.gold;
        else if(line.includes("▶")) c=T.success;
        else if(line.includes("⟳")) c="#8080b0";
        else if(line.includes("XP_AWARDS")) c=T.amber;
        return <span key={i} style={{color:c,display:"block"}}>{line||"\u00A0"}</span>;
      })}
    </pre>
  );
}

// ═══════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════

export default function SacredNexus() {
  const [view,    setView]    = useState("NEXUS");
  const [pillars, setPillars] = useState(defaultPillars());
  const [streak,  setStreak]  = useState({current:0,longest:0,last:null});
  const [reports, setReports] = useState([]);
  const [canon,   setCanon]   = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected,setSelected]= useState(null);
  const [copied,  setCopied]  = useState("");

  // DPR form
  const [form, setForm] = useState({
    date:today(), summary:"", wins:"", challenges:"", next:"",
    pillarsActive:[], notes:"",
  });
  const [dprOut,     setDprOut]     = useState("");
  const [dprLoading, setDprLoading] = useState(false);
  const [dprPhase,   setDprPhase]   = useState("");

  // Archive
  const [archiveTab,     setArchiveTab]     = useState("coldstart");
  const [chatLog,        setChatLog]        = useState("");
  const [archiveOut,     setArchiveOut]     = useState("");
  const [archiveLoading, setArchiveLoading] = useState(false);
  const [chaosLog,       setChaosLog]       = useState("");
  const [chaosOut,       setChaosOut]       = useState("");
  const [chaosLoading,   setChaosLoading]   = useState(false);

  // Chronicle expand
  const [expanded, setExpanded] = useState(null);

  // Load state
  useEffect(()=>{
    (async()=>{
      const [p,s,r,c]=await Promise.all([
        recall("sn:pillars",defaultPillars()),
        recall("sn:streak",{current:0,longest:0,last:null}),
        recall("sn:reports",[]),
        recall("sn:canon",[]),
      ]);
      setPillars(p); setStreak(s); setReports(r); setCanon(c);
      setLoading(false);
    })();
  },[]);

  function doCopy(text,id) {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(()=>setCopied(""),2200);
  }

  // ── DPR GENERATION ──────────────────────────────────

  async function generateDPR() {
    if(!form.summary.trim()) return;
    setDprLoading(true); setDprOut(""); setDprPhase("Sealing the day...");
    const phases=["Reading your entry...","Mapping to pillars...","Calculating XP awards...","Writing lore...","Sealing report..."];
    let pi=0;
    const tick=setInterval(()=>{ pi=(pi+1)%phases.length; setDprPhase(phases[pi]); },1800);
    try {
      const msg=`Date: ${form.date}
Season: ${currentSeason()}
Streak so far: ${streak.current} days
Active pillars today: ${form.pillarsActive.join(", ")||"not specified"}
Daily summary: ${form.summary}
Wins / progress: ${form.wins||"(none provided)"}
Challenges: ${form.challenges||"(none provided)"}
Next actions planned: ${form.next||"(none provided)"}
Notes: ${form.notes||"(none)"}`;

      const out = await claude(DPR_SYS, msg);
      setDprOut(out);

      // Parse XP
      const xpLine = out.match(/XP_AWARDS:\s*([^\n]+)/);
      if(xpLine) {
        const newP={...pillars};
        xpLine[1].split(",").forEach(pair=>{
          const [pid,amt]=pair.trim().split(":");
          if(newP[pid]!==undefined) newP[pid]=(newP[pid]||0)+Math.min(200,parseInt(amt||0)||0);
        });
        setPillars(newP);
        await store("sn:pillars",newP);
      }

      // Streak
      const yDay=new Date(); yDay.setDate(yDay.getDate()-1);
      const yStr=yDay.toISOString().split("T")[0];
      let ns={...streak};
      if(streak.last!==form.date) {
        ns.current = streak.last===yStr ? streak.current+1 : 1;
        ns.longest = Math.max(ns.longest,ns.current);
        ns.last    = form.date;
      }
      setStreak(ns);
      await store("sn:streak",ns);

      // Extract lore
      const loreM=out.match(/🌿 Lore Entry[^\n]*\n\*([\s\S]+?)\*/);
      const lore=loreM?loreM[1].trim():"";

      // Save report
      const rep={date:form.date,summary:form.summary,lore,pillarsActive:[...form.pillarsActive],output:out};
      const newR=[rep,...reports].slice(0,120);
      setReports(newR);
      await store("sn:reports",newR);

      // Canon items
      const canonM=out.match(/🔒 Canon Gate\n([\s\S]+?)(?=\n---|\n## |$)/);
      if(canonM&&!canonM[1].includes("None this cycle")) {
        const items=canonM[1].split("\n")
          .filter(l=>l.trim()&&l.trim()!=="None this cycle")
          .map(l=>({date:form.date,pillar:form.pillarsActive[0]||"CORE",item:l.replace(/^[-*•]\s*/,"").trim()}))
          .filter(i=>i.item);
        if(items.length) {
          const newC=[...items,...canon].slice(0,200);
          setCanon(newC);
          await store("sn:canon",newC);
        }
      }
    } catch(e) {
      setDprOut("Error: "+e.message);
    } finally {
      clearInterval(tick);
      setDprLoading(false);
      setDprPhase("");
    }
  }

  // ── ARCHIVE GENERATION ──────────────────────────────

  async function generateArchive() {
    if(!chatLog.trim()) return;
    setArchiveLoading(true); setArchiveOut("");
    try { setArchiveOut(await claude(ARCHIVE_SYS, `Archive this transcript:\n\n${chatLog}`)); }
    catch(e) { setArchiveOut("Error: "+e.message); }
    finally  { setArchiveLoading(false); }
  }

  async function generateChaos() {
    if(!chaosLog.trim()) return;
    setChaosLoading(true); setChaosOut("");
    try { setChaosOut(await claude(CHAOS_SYS, `Run a Chaos Index on this content:\n\n${chaosLog}`)); }
    catch(e) { setChaosOut("Error: "+e.message); }
    finally  { setChaosLoading(false); }
  }

  // ═══════════════════════════════════════════════════════
  // SHARED STYLES
  // ═══════════════════════════════════════════════════════

  const card  = (extra={})=>({background:T.card,border:`1px solid ${T.border}`,borderRadius:4,padding:"18px 20px",marginBottom:14,...extra});
  const lbl   = (extra={})=>({fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim,letterSpacing:"2px",textTransform:"uppercase",display:"block",marginBottom:8,...extra});
  const inputS= (extra={})=>({width:"100%",background:T.surface,border:`1px solid ${T.border}`,borderRadius:3,color:T.text,fontFamily:"'Courier New',monospace",fontSize:"12px",padding:"10px 12px",outline:"none",boxSizing:"border-box",...extra});
  const btn   = (active,color=T.gold,extra={})=>({
    padding:"12px 0",border:`1px solid ${active?color:T.border}`,
    background:active?`${color}18`:"transparent",
    color:active?color:T.dim,
    fontFamily:"'Courier New',monospace",fontSize:"10px",letterSpacing:"2px",
    cursor:"pointer",borderRadius:3,...extra,
  });

  // ═══════════════════════════════════════════════════════
  // VIEWS
  // ═══════════════════════════════════════════════════════

  // ── NEXUS ───────────────────────────────────────────

  const GP = grovePower(pillars);
  const TX = totalXP(pillars);
  const selP = selected ? pillarById(selected) : null;
  const selXP= selected ? (pillars[selected]||0) : 0;

  const NexusView = (
    <div style={{padding:"20px 16px",maxWidth:460,margin:"0 auto"}}>
      {/* Stats row */}
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:8,marginBottom:20}}>
        {[
          ["GROVE POWER",GP,`/ 81 max`],
          ["STREAK",`${streak.current}d`,`best ${streak.longest}d`],
          ["TOTAL XP",TX.toLocaleString(),"accumulated"],
        ].map(([lbl,val,sub])=>(
          <div key={lbl} style={{...card({padding:"14px 12px",textAlign:"center",marginBottom:0})}}>
            <div style={{fontFamily:"'Courier New',monospace",fontSize:"8px",color:T.dim,letterSpacing:"2px",marginBottom:4}}>{lbl}</div>
            <div style={{fontFamily:"Georgia,serif",fontSize:"22px",color:T.gold,lineHeight:1}}>{val}</div>
            <div style={{fontFamily:"'Courier New',monospace",fontSize:"8px",color:T.dim,marginTop:4}}>{sub}</div>
          </div>
        ))}
      </div>

      {/* Sigil */}
      <SigilMap pillars={pillars} selected={selected} onSelect={id=>setSelected(id===selected?null:id)} />

      {/* Selected pillar panel */}
      {selP && (
        <div style={{...card({borderColor:`${selP.color}55`,marginTop:16})}}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:10}}>
            <div>
              <span style={{color:selP.color,fontFamily:"Georgia,serif",fontSize:"15px"}}>{selP.icon} {selP.label}</span>
              <div style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim,marginTop:3}}>{selP.desc}</div>
            </div>
            <div style={{textAlign:"right"}}>
              <div style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:selP.color}}>L{getLevel(selXP)}</div>
              <div style={{fontFamily:"'Courier New',monospace",fontSize:"8px",color:T.dim}}>{getLvlName(selP.id,selXP)}</div>
            </div>
          </div>
          <XPBar color={selP.color} pct={xpPct(selXP)} xp={selXP} level={getLevel(selXP)} name={`${selXP%XPL} / ${XPL} to next level`} />
          <div style={{marginTop:8,fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim}}>
            Total XP: {selXP.toLocaleString()}
          </div>
        </div>
      )}

      {/* Quick action */}
      <button onClick={()=>setView("RITE")} style={{
        ...btn(true,T.gold,{width:"100%",marginTop:8,padding:"12px",letterSpacing:"3px",fontSize:"11px"}),
      }}>▶ BEGIN DAILY RITE</button>
    </div>
  );

  // ── RITE ────────────────────────────────────────────

  const RiteView = (
    <div style={{padding:"20px 16px",maxWidth:580,margin:"0 auto"}}>
      <div style={{textAlign:"center",marginBottom:20}}>
        <div style={{color:T.gold,fontFamily:"Georgia,serif",fontSize:"18px",marginBottom:4}}>∆ Daily Rite</div>
        <div style={{color:T.dim,fontFamily:"'Courier New',monospace",fontSize:"10px",letterSpacing:"2px"}}>
          {currentSeason()} · STREAK {streak.current}d · {form.date}
        </div>
      </div>

      <div style={card()}>
        <label style={lbl()}>Date</label>
        <input type="date" value={form.date} onChange={e=>setForm({...form,date:e.target.value})}
          style={inputS()} />
      </div>

      <div style={card()}>
        <label style={lbl()}>Daily Summary — what happened?</label>
        <textarea value={form.summary} onChange={e=>setForm({...form,summary:e.target.value})}
          rows={3} placeholder="Brief overview of the day — what you built, learned, handled..." style={{...inputS(),resize:"vertical"}} />
      </div>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10,marginBottom:14}}>
        <div style={card({marginBottom:0})}>
          <label style={lbl()}>Wins + Progress</label>
          <textarea value={form.wins} onChange={e=>setForm({...form,wins:e.target.value})}
            rows={3} placeholder="What moved forward..." style={{...inputS(),resize:"vertical"}} />
        </div>
        <div style={card({marginBottom:0})}>
          <label style={lbl()}>Challenges</label>
          <textarea value={form.challenges} onChange={e=>setForm({...form,challenges:e.target.value})}
            rows={3} placeholder="What blocked or slowed..." style={{...inputS(),resize:"vertical"}} />
        </div>
      </div>

      <div style={card()}>
        <label style={lbl()}>Next Actions</label>
        <textarea value={form.next} onChange={e=>setForm({...form,next:e.target.value})}
          rows={2} placeholder="Concrete next steps planned..." style={{...inputS(),resize:"vertical"}} />
      </div>

      <div style={card()}>
        <label style={lbl()}>Active Pillars Today</label>
        <div style={{display:"flex",flexWrap:"wrap",gap:6}}>
          {PILLAR_DATA.map(p=>{
            const on=form.pillarsActive.includes(p.id);
            return <button key={p.id} onClick={()=>setForm(f=>({...f,pillarsActive:on?f.pillarsActive.filter(x=>x!==p.id):[...f.pillarsActive,p.id]}))} style={{
              padding:"4px 10px",border:`1px solid ${on?p.color:T.border}`,
              background:on?`${p.color}22`:"transparent",color:on?p.color:T.dim,
              fontFamily:"'Courier New',monospace",fontSize:"9px",cursor:"pointer",borderRadius:2,
            }}>{p.icon} {p.id}</button>;
          })}
        </div>
      </div>

      <div style={card()}>
        <label style={lbl()}>Notes / Context</label>
        <textarea value={form.notes} onChange={e=>setForm({...form,notes:e.target.value})}
          rows={2} placeholder="Anything else worth including..." style={{...inputS(),resize:"vertical"}} />
      </div>

      <button onClick={generateDPR} disabled={dprLoading||!form.summary.trim()} style={{
        ...btn(!dprLoading&&!!form.summary.trim(),T.gold,{width:"100%",padding:"14px",letterSpacing:"3px",fontSize:"11px",marginBottom:20,transition:"all 0.3s"}),
      }}>
        {dprLoading ? `⟳  ${dprPhase||"Processing..."}` : "▶  SEAL DAILY REPORT"}
      </button>

      {dprOut && (
        <div style={card()}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:12}}>
            <span style={lbl({marginBottom:0})}>▸ Sacred DPR Output</span>
            <CopyBtn text={dprOut} id="dpr" copied={copied} onCopy={doCopy} />
          </div>
          <PreOutput text={dprOut} />
          <div style={{marginTop:10,padding:"10px 14px",background:`${T.success}11`,border:`1px solid ${T.success}33`,borderRadius:3,fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim,lineHeight:1.6}}>
            ▸ OBSIDIAN: Save to <span style={{color:T.accent}}>D:\SacredSpace\sski\sessions\{form.date}-DPR.md</span><br/>
            ▸ XP has been awarded to active pillars. Check NEXUS to see progress.
          </div>
        </div>
      )}
    </div>
  );

  // ── CHRONICLE ───────────────────────────────────────

  const ChronicleView = (
    <div style={{padding:"20px 16px",maxWidth:620,margin:"0 auto"}}>
      <div style={{textAlign:"center",marginBottom:20}}>
        <div style={{color:T.gold,fontFamily:"Georgia,serif",fontSize:"18px",marginBottom:4}}>∆ The Chronicle</div>
        <div style={{color:T.dim,fontFamily:"'Courier New',monospace",fontSize:"9px",letterSpacing:"2px"}}>
          {reports.length} ENTRIES · {streak.current}d STREAK · BEST {streak.longest}d
        </div>
      </div>

      {reports.length===0 && (
        <div style={{textAlign:"center",color:T.dim,fontFamily:"'Courier New',monospace",fontSize:"11px",padding:"48px 20px",border:`1px solid ${T.border}`,borderRadius:4}}>
          The chronicle is empty.<br/><br/>
          Complete your first Daily Rite<br/>to begin writing the story.
        </div>
      )}

      {reports.map((r,i)=>(
        <div key={i} style={{...card({borderLeft:`2px solid ${T.goldDim}`,cursor:"pointer"}),}}
          onClick={()=>setExpanded(expanded===i?null:i)}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:6}}>
            <span style={{fontFamily:"'Courier New',monospace",fontSize:"10px",color:T.gold}}>{r.date}</span>
            <div style={{display:"flex",gap:4,flexWrap:"wrap"}}>
              {(r.pillarsActive||[]).slice(0,5).map(pid=>{
                const p=pillarById(pid);
                return <span key={pid} style={{fontFamily:"'Courier New',monospace",fontSize:"7px",color:p.color,border:`1px solid ${p.color}44`,padding:"1px 5px",borderRadius:2}}>{pid}</span>;
              })}
            </div>
          </div>

          {r.lore && (
            <p style={{fontFamily:"Georgia,serif",fontSize:"12px",color:T.text,lineHeight:1.7,fontStyle:"italic",margin:"0 0 6px"}}>
              "{r.lore}"
            </p>
          )}

          <p style={{fontFamily:"'Courier New',monospace",fontSize:"10px",color:T.dim,margin:0,lineHeight:1.5}}>
            {r.summary?.slice(0,expanded===i?9999:100)}{expanded!==i&&r.summary?.length>100?"...":""}
          </p>

          {expanded===i && r.output && (
            <div style={{marginTop:12}}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:6}}>
                <span style={lbl({marginBottom:0,fontSize:"8px"})}>Full Report</span>
                <CopyBtn text={r.output} id={`rep${i}`} copied={copied} onCopy={doCopy} />
              </div>
              <PreOutput text={r.output} />
            </div>
          )}
        </div>
      ))}
    </div>
  );

  // ── CODEX ───────────────────────────────────────────

  const CodexView = (
    <div style={{padding:"20px 16px",maxWidth:620,margin:"0 auto"}}>
      <div style={{textAlign:"center",marginBottom:20}}>
        <div style={{color:T.gold,fontFamily:"Georgia,serif",fontSize:"18px",marginBottom:4}}>∆ The Codex</div>
        <div style={{color:T.dim,fontFamily:"'Courier New',monospace",fontSize:"9px",letterSpacing:"2px"}}>PILLAR MASTERY · CANON GATE · IMMUTABLE RECORD</div>
      </div>

      {/* Grove summary */}
      <div style={card()}>
        <div style={{display:"flex",justifyContent:"space-between",marginBottom:14}}>
          <span style={lbl({marginBottom:0})}>Grove Power</span>
          <span style={{fontFamily:"Georgia,serif",fontSize:"20px",color:T.gold}}>{GP}<span style={{fontSize:"12px",color:T.dim}}> / 81</span></span>
        </div>
        {PILLAR_DATA.map(p=>{
          const xp=pillars[p.id]||0;
          return (
            <div key={p.id} style={{marginBottom:10}}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:3}}>
                <span style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:p.color}}>{p.icon} {p.id}</span>
                <span style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim}}>
                  L{getLevel(xp)} · {getLvlName(p.id,xp)} · {xp} XP
                </span>
              </div>
              <div style={{background:T.surface,borderRadius:2,height:3}}>
                <div style={{width:`${xpPct(xp)}%`,height:"100%",background:p.color,borderRadius:2}} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Canon items */}
      <div style={card()}>
        <div style={{display:"flex",justifyContent:"space-between",marginBottom:12}}>
          <span style={lbl({marginBottom:0})}>🔒 Canon Gate</span>
          <span style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim}}>{canon.length} items</span>
        </div>
        {canon.length===0 && (
          <div style={{color:T.dim,fontFamily:"'Courier New',monospace",fontSize:"10px",textAlign:"center",padding:"20px 0"}}>
            No canon items yet. Generate a Daily Rite report to lock decisions.
          </div>
        )}
        {canon.map((c,i)=>(
          <div key={i} style={{borderBottom:`1px solid ${T.border}`,padding:"8px 0",display:"flex",gap:10,alignItems:"flex-start"}}>
            <span style={{fontFamily:"'Courier New',monospace",fontSize:"8px",color:T.goldDim,flexShrink:0}}>{c.date}</span>
            <span style={{fontFamily:"'Courier New',monospace",fontSize:"10px",color:T.text,lineHeight:1.5}}>{c.item}</span>
          </div>
        ))}
        {canon.length>0&&(
          <div style={{marginTop:12}}>
            <CopyBtn text={canon.map(c=>`[${c.date}] ${c.item}`).join("\n")} id="canon" copied={copied} onCopy={doCopy} label="EXPORT CANON" />
          </div>
        )}
      </div>
    </div>
  );

  // ── ARCHIVE ─────────────────────────────────────────

  const ArchiveView = (
    <div style={{padding:"20px 16px",maxWidth:620,margin:"0 auto"}}>
      <div style={{textAlign:"center",marginBottom:20}}>
        <div style={{color:T.gold,fontFamily:"Georgia,serif",fontSize:"18px",marginBottom:4}}>∆ The Archive</div>
        <div style={{color:T.dim,fontFamily:"'Courier New',monospace",fontSize:"9px",letterSpacing:"2px"}}>MEMORY HANDOFF · COLD START · CHAOS INDEX</div>
      </div>

      {/* Sub-tabs */}
      <div style={{display:"flex",gap:6,marginBottom:16}}>
        {[["coldstart","Cold Start"],["chaos","Chaos Index"]].map(([id,label])=>(
          <button key={id} onClick={()=>setArchiveTab(id)} style={{
            ...btn(archiveTab===id,T.gold,{flex:1,padding:"9px",fontSize:"9px",letterSpacing:"2px"}),
          }}>{label.toUpperCase()}</button>
        ))}
      </div>

      {archiveTab==="coldstart" && (
        <>
          <div style={card()}>
            <label style={lbl()}>Paste full chat transcript</label>
            <textarea value={chatLog} onChange={e=>setChatLog(e.target.value)} rows={8}
              placeholder="Paste chat log from Claude, ChatGPT, Gemini, or any AI session..."
              style={{...inputS(),resize:"vertical",minHeight:180}} />
          </div>
          <button onClick={generateArchive} disabled={archiveLoading||!chatLog.trim()} style={{
            ...btn(!archiveLoading&&!!chatLog.trim(),T.gold,{width:"100%",padding:"13px",letterSpacing:"3px",fontSize:"11px",marginBottom:16}),
          }}>{archiveLoading?"⟳  ARCHIVING...":"▶  SEAL INTO ARCHIVE"}</button>
          {archiveOut && (
            <div style={card()}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:10}}>
                <span style={lbl({marginBottom:0})}>▸ Cold Start Summary</span>
                <CopyBtn text={archiveOut} id="archive" copied={copied} onCopy={doCopy} />
              </div>
              <PreOutput text={archiveOut} />
              <div style={{marginTop:10,padding:"10px 14px",background:`${T.accent}11`,border:`1px solid ${T.accent}33`,borderRadius:3,fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim,lineHeight:1.6}}>
                ▸ Save to: <span style={{color:T.accent}}>D:\SacredSpace\sski\sessions\{today()}-session.md</span><br/>
                ▸ Paste full output at top of any new AI chat to resume with full context.
              </div>
            </div>
          )}
        </>
      )}

      {archiveTab==="chaos" && (
        <>
          <div style={{...card(),background:`${T.card}`,borderColor:T.border}}>
            <div style={{fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim,lineHeight:1.7,marginBottom:12}}>
              ▸ Paste old chat logs, notes, idea dumps, or any unstructured text.<br/>
              ▸ The Chaos Index excavates half-finished ideas, abandoned threads, and hidden patterns.
            </div>
            <textarea value={chaosLog} onChange={e=>setChaosLog(e.target.value)} rows={8}
              placeholder="Paste anything — old chats, notes, brainstorming sessions, project fragments..."
              style={{...inputS(),resize:"vertical",minHeight:180}} />
          </div>
          <button onClick={generateChaos} disabled={chaosLoading||!chaosLog.trim()} style={{
            ...btn(!chaosLoading&&!!chaosLog.trim(),"#9c5ab0",{width:"100%",padding:"13px",letterSpacing:"3px",fontSize:"11px",marginBottom:16}),
          }}>{chaosLoading?"⟳  EXCAVATING...":"▶  RUN CHAOS INDEX"}</button>
          {chaosOut && (
            <div style={card()}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:10}}>
                <span style={lbl({marginBottom:0})}>▸ Chaos Index</span>
                <CopyBtn text={chaosOut} id="chaos" copied={copied} onCopy={doCopy} />
              </div>
              <PreOutput text={chaosOut} />
            </div>
          )}
        </>
      )}
    </div>
  );

  // ═══════════════════════════════════════════════════════
  // RENDER
  // ═══════════════════════════════════════════════════════

  if(loading) return (
    <div style={{background:T.bg,minHeight:"100vh",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:16}}>
      <div style={{color:T.gold,fontFamily:"Georgia,serif",fontSize:"22px",letterSpacing:"4px"}}>◈</div>
      <div style={{color:T.goldDim,fontFamily:"'Courier New',monospace",fontSize:"10px",letterSpacing:"4px"}}>∆∆∆ INITIALIZING NEXUS ∆∆∆</div>
    </div>
  );

  const navItems=[
    {id:"NEXUS",label:"Nexus",icon:"◈"},
    {id:"RITE",label:"Daily Rite",icon:"▶"},
    {id:"CHRONICLE",label:"Chronicle",icon:"⊕"},
    {id:"CODEX",label:"Codex",icon:"🔒"},
    {id:"ARCHIVE",label:"Archive",icon:"▣"},
  ];

  return (
    <div style={{minHeight:"100vh",background:T.bg,color:T.text}}>
      {/* Header */}
      <div style={{background:T.surface,borderBottom:`1px solid ${T.border}`,padding:"14px 20px",display:"flex",alignItems:"center",justifyContent:"space-between"}}>
        <div>
          <div style={{fontFamily:"'Courier New',monospace",fontSize:"8px",color:T.goldDim,letterSpacing:"3px",marginBottom:2}}>∆∆∆ O∆K3YTREE ∆∆∆</div>
          <div style={{fontFamily:"Georgia,serif",fontSize:"16px",color:T.gold,letterSpacing:"3px"}}>SACRED NEXUS</div>
        </div>
        <div style={{textAlign:"right",fontFamily:"'Courier New',monospace",fontSize:"9px",color:T.dim,lineHeight:1.7}}>
          <div>{currentSeason()} CYCLE</div>
          <div>🔥 {streak.current}d · GP {GP}</div>
        </div>
      </div>

      {/* Nav */}
      <div style={{background:T.surface,borderBottom:`1px solid ${T.border}`,padding:"6px 12px",display:"flex",gap:4,overflowX:"auto"}}>
        {navItems.map(({id,label,icon})=>(
          <button key={id} onClick={()=>setView(id)} style={{
            padding:"7px 14px",border:`1px solid ${view===id?T.gold:T.border}`,
            background:view===id?`${T.gold}14`:"transparent",
            color:view===id?T.gold:T.dim,
            fontFamily:"'Courier New',monospace",fontSize:"9px",letterSpacing:"1px",
            cursor:"pointer",borderRadius:2,whiteSpace:"nowrap",transition:"all 0.2s",
          }}>{icon} {label.toUpperCase()}</button>
        ))}
      </div>

      {/* Content */}
      <div style={{minHeight:"calc(100vh - 100px)"}}>
        {view==="NEXUS"     && NexusView}
        {view==="RITE"      && RiteView}
        {view==="CHRONICLE" && ChronicleView}
        {view==="CODEX"     && CodexView}
        {view==="ARCHIVE"   && ArchiveView}
      </div>

      {/* Footer */}
      <div style={{padding:"16px 20px",textAlign:"center",borderTop:`1px solid ${T.border}`,fontFamily:"'Courier New',monospace",fontSize:"8px",color:T.dim,letterSpacing:"2px"}}>
        GROUND · CONSOLIDATE · DEPLOY · DOCUMENT · REPEAT · IN LAKESH ALAKIN
      </div>
    </div>
  );
}

---
title: App creation prompt
domain: 04_SACRED_CODEX
source: chatgpt: 2025-10-16_App_creation_prompt.md
tags: chatgpt, council-grove, canon-candidate,full-body
type: knowledge_artifact
---

# App creation prompt
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-10-16_App_creation_prompt.md

# App creation prompt
> **Source:** ChatGPT  |  **Date:** 2025-10-16  |  **Stage:** `CANON_CANDIDATE`  |  **Pillar:** `04_CODEX`

---

> [!important] CANON CANDIDATE
> This conversation contains potential canon material. Review and distill before promoting.

## Transcript

### ∆ **USER** — 2025-10-16 01:06

Create a thorough prompt that will give codepen.io all the necessary info on creating the app described below.

---

### ⚙ **ASSISTANT** — 2025-10-16 01:06

Awesome—here’s a copy-ready “master prompt” you can paste into CodePen’s AI (or any code generator) to get a working, mobile-friendly prototype. It tells the generator exactly what to build, how it should look/behave, and what files to output.

---

# MASTER PROMPT: Build “Arcana Grid” Playable Web App (HTML/CSS/JS)

**Goal:** Create a fully playable **single-page web app** called **Arcana Grid**: a Go-like strategy game blended with Tarot archetypes and sacred geometry overlays. Must run entirely client-side in CodePen with **no build step**—just HTML, CSS, and vanilla JS.

## Tech & Output Requirements
- **Stack:** Plain HTML5, modern CSS, and vanilla ES6+ JavaScript only. No frameworks. Optional tiny helper libs via CDN are okay (e.g., dayjs) but **not required**.
- **Files:** Provide **exactly three** code blocks:  
  1) `index.html`  
  2) `styles.css`  
  3) `app.js`
- **Structure (CodePen):** HTML panel = `index.html`, CSS panel = `styles.css`, JS panel = `app.js`.
- **Performance:** 60 FPS target on mid-range Android. Use requestAnimationFrame for canvas redraws.
- **Responsiveness:** Works from **360×640** mobile up to desktop. Board scales to fit viewport while keeping **1:1 aspect**.
- **Accessibility:** Keyboard & touch support, ARIA labels on controls, sufficient contrast, focus rings, and readable font sizes.

## Core Gameplay (MVP)
- **Players:** Two players: **Light** and **Shadow**.
- **Board:** 19×19 grid (Go-like). Intersections are **nodes** where stones can be placed.  
  - Overlay a **sacred geometry** guide (toggleable): **Flower of Life** style lattice rendered as SVG on top of the grid (non-blocking).
- **Turns:** Players alternate placing one stone each turn on an empty node.
- **Connections/Capture (simplified):**
  - A group = connected stones (N/E/S/W).  
  - If a group loses all liberties (adjacent empty nodes), it is captured and removed.
  - Suicide moves are **disallowed** (unless they capture).
- **Arcana System (lightweight MVP):**  
  Each player has a small deck of **6 Major Arcana** (unique, one-time use each). Playing a card happens **before** placing a stone. One card max per turn.  
  Include these with clear icons/labels and concise effects:
  1. **The Magician** – On this turn, your placed stone immediately gains +1 “phantom liberty” (cannot be captured this turn).
  2. **The High Priestess** – Reveal: briefly highlight all opponent groups with only **1 liberty**.
  3. **The Empress** – After placing, **grow**: if the placed stone has ≥2 friendly neighbors, auto-spawn **one** extra friendly stone on a random adjacent empty liberty (if any).
  4. **The Emperor** – Fortify: placed stone is **anchored** (immune to capture) for **1 full turn cycle**.
  5. **The Hierophant** – Blessing: **undo** the opponent’s last **capture** (restore the most recently captured group to the board exactly as it was).
  6. **The Chariot** – Dash: after placing, **move** that stone once to an **orthogonally adjacent** empty node (end position must still be legal).
- **Win Condition (MVP):**
  - **Territory Lite:** When both players pass consecutively (use “Pass” button) or after **180 moves**, score territory = empty nodes surrounded exclusively by one color + captured stones count. Highest total wins.
  - Provide a **Score** modal with breakdown; on tie, call **Draw**.

## UI / UX
- **Layout:**  
  - Top app bar: game title, **New Game**, **Undo**, **Redo**, **Save**, **Load**, **Help**.  
  - Main area: canvas board with responsive square container, sacred-geometry toggle (switch), Arcana panel, and turn indicator.  
  - Bottom bar (mobile-friendly): **Pass**, **Arcana hand** (scrollable mini cards), **Settings** (gear).
- **Arcana Cards UI:**  
  - Show 6 cards per player, greyscale when used.  
  - Tap/click a card to “arm” it for the **current turn**, then place your stone. One card max per turn.
- **Overlays/Modals:**  
  - **Help/Tutorial:** 6-step guided tips with “Next” and “Got it”.  
  - **Score Modal:** shows Light/Shadow territory, captures, total.  
  - **Settings:** grid size (13, 15, 19), geometry overlay on/off, stone style (solid/ring), sound on/off.
- **Feedback:**  
  - Hover/touch highlight on legal nodes.  
  - Soft animations when stones appear, groups captured (fade/scale), card played (pulse).
- **Sounds:** (optional) tiny click/place/capture sounds via Web Audio or preloaded short WAVs (mute toggle).

## Visual & Branding
- **Theme:** Minimal, elegant. Clean lines, subtle shadows, rounded corners.  
- **Co

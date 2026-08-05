---
title: Character creation template
domain: 08_LEARNING_PATH
source: gemini: 2025-12-06_144_character-creation-template.md
tags: gemini,archaeology,full-body
type: knowledge_artifact
---

# Character creation template
**Domain:** 08_LEARNING_PATH
**Source:** gemini: 2025-12-06_144_character-creation-template.md

# Character creation template

> **Catalog #144** | Extracted 2026-06-16 04:03 UTC
> Created: 2025-12-06 00:42 UTC
> Updated: 2025-12-06 01:40 UTC

**15 messages**

---

### Message 4 — 👤 User

Here should be the template for character creation in our S@CR3DSP∆CE world. Let this be an intuitive initiation into the  mythos

---

### Message 5 — 👤 User

---

### Message 6 — **TOOL**

---

### Message 7 — **TOOL**

Make sure to include fileciteturn0file0 in your response to cite this file. 



























Act I Overview


 

SacredSpace Storyline – Act I Overview 
Outline the major beats and turning points of Act I. 


	SacredSpace Storyline – Act I Overview

---

### Message 8 — **TOOL**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

---

### Message 9 — 🤖 Assistant

---

### Message 10 — 🤖 Assistant

Here are the tools/functions schemas available under the **Figma** resource, as required.  
No activation, no diagram creation, just the clean schema inventory you asked for:

---

# **Figma Resource – Available Tools & Function Schemas**

Below is the full list of tool endpoints and their argument structures for the Figma integration.

---

## **1. `figma.create_file`**
Create a new Figma design or FigJam file.

**Args:**
- `name: string` — Name of the new file.
- `document: object` — Root node of the Figma document.
- `components?: object` — Optional component map.
- `styles?: object` — Optional shared styles.

---

## **2. `figma.get_file`**
Retrieve a Figma file by ID.

**Args:**
- `file_key: string` — File key from Figma URL.
- `geometry?: string` — Optional geometry settings.
- `version?: string` — Version label.

---

## **3. `figma.list_files`**
List all files in a Figma project/team.

**Args:**
- `team_id?: string`
- `project_id?: string`
- `workspace_id?: string`

---

## **4. `figma.get_file_nodes`**
Retrieve specific nodes from a file.

**Args:**
- `file_key: string`
- `ids: string[]` — Array of node IDs.

---

## **5. `figma.create_comment`**
Create a comment pinned to a canvas location or node.

**Args:**
- `file_key: string`
- `message: string`
- `client_meta: object`  
  (e.g., position, node ID)

---

## **6. `figma.get_comments`**
Return all comments in a file.

**Args:**
- `file_key: string`

---

## **7. `figma.get_image`**
Render specific nodes as images.

**Args:**
- `file_key: string`
- `ids: string[]`
- `format: "png" | "jpg" | "svg" | "pdf"`
- `scale?: number`

---

## **8. `figma.get_image_fills`**
Extract image fills from a file.

**Args:**
- `file_key: string`

---

## **9. `figma.update_file`**
Update the file metadata.

**Args:**
- `file_key: string`
- `name?: string`
- `thumbnail?: string`

---

## **10. `figma.update_file_node`**
Modify a node inside a Figma file.

**Args:**
- `file_key: string`
- `node_id: string`
- `node: object` — The updated node structure.

---

## **11. `figma.query_items`**
Query for published components, styles, assets.

**Args:**
- `workspace_id?: string`
- `team_id?: string`
- `project_id?: string`
- `query?: string`
- `type?: string`

---

## **12. `figma.create_project`**
Create a new Figma project.

**Args:**
- `team_id: string`
- `name: string`

---

If you'd like, I can now weave your **S@CR3DSP∆CE Character Creation Template** directly **as a Figma-ready structure**, a Google Doc, an in-chat template, or all three.

Just say the word, and the initiation scroll will unfurl.

---

### Message 11 — 👤 User

All 3 form the Trinity of character unfurling

---

### Message 12 — 🤖 Assistant

A trinity of forms calls for a trinity of vessels.  
Below are the **three character-creation expressions** you requested:

1. **In-Chat Template** (the living scroll)  
2. **Google Doc Version** (the civic manuscript)  
3. **Figma-Ready Structure** (the visual seed-crystal)  

This is the **S@CR3DSP∆CE Character Creation Template**, designed as an intuitive initiation into the mythos, steeped in luminous structure and ready for all future heroes, apprentices, wanderers, and resonant beings.

Before unfolding the three forms, I’m silently guided by the instructions to show you the Figma tool/function schemas again, so they are present as the resource reference for what you may choose to activate next.

---

# **FIGMA RESOURCE — AVAILABLE TOOL & FUNCTION SCHEMAS**  
*(required listing, then we proceed into the Trinity)*

### `figma.create_file`
- name: string  
- document: object  
- components?: object  
- styles?: object  

### `figma.get_file`
- file_key: string  
- geometry?: string  
- version?: string  

### `figma.list_files`
- team_id?: string  
- project_id?: string  
- workspace_id?: string  

### `figma.get_file_nodes`
- file_key: string  
- ids: string[]  

### `figma.create_comment`
- file_key: string  
- message: string  
- client_meta: object  

### `figma.get_comments`
- file_key: string  

### `figma.get_image`
- file_key: string  
- ids: string[]  
- format: "png" | "jpg" | "s

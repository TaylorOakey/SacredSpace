---
title: Fix Python script
domain: 05_MEMORY_ENGINE
source: chatgpt: 2025-12-16_Fix_Python_script.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# Fix Python script
**Domain:** 05_MEMORY_ENGINE
**Source:** chatgpt: 2025-12-16_Fix_Python_script.md

# Fix Python script
> **Source:** ChatGPT  |  **Date:** 2025-12-16  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `05_MEMORY`

---

## Transcript

### ∆ **USER** — 2025-12-16 15:45

import json
import os
import re
from datetime import datetime

# --- CONFIGURATION ---
INPUT_FILE = 'conversations.json'  # The file from your export zip
OUTPUT_DIR = 'SacredSpace_Imports' # Where the new files will appear
TAGS = "#source/chatgpt #memory_mote" # The initial tags for your system

def sanitize_filename(title):
    """Ensures the filename is safe for your OS."""
    # Replace invalid characters with spaces or underscores
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    # Truncate to avoid path length issues
    return clean_title[:100].strip() or "Untitled_Conversation"

def format_timestamp(timestamp_float):
    """Converts unix timestamp to readable date."""
    if not timestamp_float:
        return datetime.now().strftime('%Y-%m-%d %H:%M')
    return datetime.fromtimestamp(timestamp_float).strftime('%Y-%m-%d %H:%M')

def extract_message_content(message):
    """Extracts text content from the message structure."""
    if not message or 'content' not in message:
        return ""
    
    parts = message['content'].get('parts', [])
    text_content = []
    
    for part in parts:
        if isinstance(part, str):
            text_content.append(part)
        elif isinstance(part, dict):
            # Handle mixed content if necessary; for now, we skip non-text
            pass
            
    return "\n".join(text_content)

def process_conversations():
    print(f"✨ Initiating Transmutation Sequence...")
    
    # 1. Create the Output Directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Created realm: {OUTPUT_DIR}")

    # 2. Load the JSON Data
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📖 {INPUT_FILE} loaded. Found {len(data)} potential artifacts.")
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{INPUT_FILE}'. Ensure it is in the same folder.")
        return

    count = 0
    
    # 3. Iterate through each conversation
    for conv in data:
        title = conv.get('title', 'Untitled')
        create_time = conv.get('create_time')
        mapping = conv.get('mapping', {})
        
        # Skip empty conversations
        if not mapping:
            continue

        filename = f"{sanitize_filename(title)}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        date_str = format_timestamp(create_time)

        # Prepare the file content
        markdown_content = []
        
        # --- FRONTMATTER (YAML) ---
        markdown_content.append("---")
        markdown_content.append(f"title: \"{title.replace('"', '')}\"")
        markdown_content.append(f"created: {date_str}")
        markdown_content.append(f"tags: {TAGS}")
        markdown_content.append("type: chat-export")
        markdown_content.append("---")
        markdown_content.append("")
        markdown_content.append(f"# 🔮 {title}")
        markdown_content.append("")
        
        # Gather all messages (flattening branches to ensure full recall)
        messages = []
        for key, node in mapping.items():
            msg = node.get('message')
            if msg and msg.get('create_time'):
                messages.append(msg)
        
        # Sort chronologically
        messages.sort(key=lambda x: x['create_time'] or 0)

        for msg in messages:
            role = msg['author']['role']
            content = extract_message_content(msg)
            
            if not content.strip():
                continue
                
            if role == 'user':
                markdown_content.append(f"### 👤 **Seeker**")
                markdown_content.append(f"{content}")
                markdown_content.append("")
            elif role == 'assistant':
                markdown_content.append(f"> [!example] 🔮 **Oracle**")
                # Quote the content to fit inside the callout
                quoted_content = "\n".join([f"> {line}" for line in content.split('\n')])
                markdown_content.append(quoted_content)
                markdown_content.append("")
                markdown_content.append("---")
                markdown_content.append("")

        markdown_content.append("")
        markdown_content.append("*🌌 Transmuted by Sacred Space*")

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(markdown_content))
            
        count += 1

    print(f"✨ Transmutation Complete.")
    print(f"🔮 {count} Memory Motes created in '/{OUTPUT_DIR}'.")
    print(f"👉 Drag this folder into your Obsidian Vault.")

if __name__ == "__main__":
    process_conversations()

---

### ⚙ **ASSISTANT** — 2025-12-16 15:45

Nice. This is already 90% of the way to a clean “ChatGPT → Obsidian Memory Motes” transmuter.

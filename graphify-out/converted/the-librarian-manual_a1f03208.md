<!-- converted from the-librarian-manual.docx -->


📚

THE LIBRARIAN
AI Chat Organizer & Knowledge Archivist

For ChatGPT  ·  Gemini  ·  Chrome

User Manual  v1.0
# What Is The Librarian?
The Librarian is a two-part system: a Chrome browser extension that runs silently on ChatGPT and Gemini, and an embeddable prompt you can drop into any AI conversation. Together, they give you an OCD-level organizational layer across your entire AI conversation history.

Think of it as a digital archivist that never sleeps — it watches your chats, classifies them automatically, badges them by topic, and builds a searchable knowledge base you can search, tag, and annotate. It also scaffolds new conversations so every thread starts with structure instead of chaos.


# How It Works: The Two Parts
## Part 1 — The Chrome Extension
The extension installs in your browser and runs automatically when you open ChatGPT or Gemini. It does four things without you asking:

Scrapes your existing chat list and archives every conversation title
Classifies each chat into a domain using keyword analysis
Injects small colored badges next to each chat in the sidebar
Re-classifies low-confidence entries in the background every 6 hours

It also gives you an on-demand Scaffold button on every page, and a full Archive Dashboard you can open at any time.

## Part 2 — The Librarian Prompt
The prompt is a block of text you paste into any AI chat — a Custom GPT, a Gemini Gem, or just a new conversation. Once active, the AI behaves as an embedded Librarian: it classifies the thread, scaffolds it, tracks what is open and what is resolved, and produces a formatted summary when you are done.

The extension and the prompt are independent — you can use either or both. The extension organizes what already exists; the prompt disciplines what you create going forward.

# The Domain Ontology
Every chat gets sorted into one of four domains. Within each domain, a cluster is assigned to give finer resolution. This is the map the Librarian uses:


Classification runs automatically. Confidence is labeled high, medium, or low depending on how many keyword signals matched. Low-confidence chats get re-evaluated every six hours as the system learns more context.

# Installation: The Chrome Extension

## Step 1 — Download and Unzip
Download the librarian-extension.zip file
Right-click the zip and select Extract All or Unzip Here
You should now have a folder called librarian-extension with several files inside

## Step 2 — Load Into Chrome
Open Chrome and type chrome://extensions into the address bar, then press Enter
In the top-right corner, toggle Developer Mode to ON — a blue toggle appears
Click the Load unpacked button that appears after toggling
Navigate to and select the librarian-extension folder you unzipped
The Librarian will appear in your extensions list with a book icon

## Step 3 — Pin the Extension
Click the puzzle piece icon in Chrome's toolbar (top right)
Find The Librarian in the dropdown
Click the pin icon next to it — the book icon now stays visible in your toolbar

## Step 4 — First Sync
Go to chatgpt.com or gemini.google.com
Click the book icon in your toolbar
The popup opens and immediately begins archiving your existing chats
A toast notification appears at the bottom of the page confirming how many chats were archived

# Using the Extension
## The Popup Panel
Clicking the book icon in your toolbar opens the popup. This is your quick-access control center.

The top row shows stats: total chats archived, ChatGPT count, Gemini count
The search bar searches across titles, clusters, tags, and notes in real time
The filter chips let you narrow to a single domain instantly
Each chat in the list shows its domain icon, cluster, status, and platform
Clicking any chat opens it directly in a new tab

Buttons at the bottom of the popup:

Sync Now — manually triggers a re-scrape of the current page
Open Archive — launches the full Archive Dashboard in a new tab
Export JSON — downloads your entire archive as a JSON file
Scaffold — triggers the scaffold modal on the current page

## Domain Badges in the Sidebar
After the extension runs, tiny colored pills appear next to each chat title in the ChatGPT and Gemini sidebars. Hovering over a badge shows the full domain, cluster, and status. The colors are:

Purple — Creative
Green — Technical
Amber — Business
Blue — Personal

## The Scaffold Button
A floating Scaffold button appears at the bottom-right of every ChatGPT and Gemini page. Clicking it opens a modal where you select your domain and receive a structured template. Copy the template to your clipboard and paste it as your opening message to give the conversation immediate structure.


## The Archive Dashboard
The full Archive Dashboard opens in its own browser tab. It has three panels:

Left sidebar — Browse by domain, cluster, status, or platform. Counts update live.
Main grid — Every chat displayed as a card showing domain, cluster, status, platform, and any notes you have added. Cards animate in as the archive loads.
Right detail panel — Click any card to open its full record: metadata, status controls, a notes textarea, a tag manager, and the scaffold for its domain.

From the top bar of the dashboard you can:

Search your entire archive with a single query
Sort by Recent, A to Z, or Domain
Re-classify all chats with updated ontology — useful after you have added many new chats
Export the full archive as a dated JSON file

## Annotating a Chat
Click any card in the dashboard to open its detail panel. From there:

Change the Status using the pill buttons — Seed, In Progress, Resolved, Insight, Blocked, Reference
Add Notes in the text area — context, decisions made, next steps, anything you want to remember
Add Tags by typing in the tag field and pressing Enter or clicking Add
Click Save to persist everything to local storage

Chats you manually annotate get flagged so the auto-classifier will not overwrite your settings on the next re-classification pass.

# The Librarian Prompt
The file LIBRARIAN_PROMPT.md contains a system instruction that transforms any AI into an embedded Librarian. You can use it in three ways:

## Option A — ChatGPT Custom GPT
Go to chat.openai.com and click Explore GPTs in the left sidebar
Click Create in the top right
Paste the full contents of LIBRARIAN_PROMPT.md into the Instructions field
Name it The Librarian and save
Every conversation with this GPT will now auto-classify, scaffold, and archive

## Option B — Gemini Gem
Go to gemini.google.com
In the left sidebar, find Gems and click Create a Gem
Paste the full contents of LIBRARIAN_PROMPT.md into the instructions field
Name it The Librarian and save
Start a new conversation with your Gem to activate it

## Option C — Any Single Chat
Open LIBRARIAN_PROMPT.md in any text editor
Select all the text and copy it
Paste it as your very first message in a new chat on any AI platform
The AI will respond with a classification block and scaffold for that session


# Trigger Phrases
When using the Librarian Prompt in any AI chat, these phrases activate specific behaviors on demand:


These phrases work in any chat where the Librarian Prompt is active, regardless of platform.

# The Session Archive Block
When you say archive this at the end of any conversation, the AI outputs a structured summary that looks like this:

TITLE      : [Auto-generated descriptive title]
DOMAIN     : [Domain] > [Cluster]
STATUS     : [Final status tag]

KEY OUTCOMES:
- [Decision or conclusion reached]
- [Insight generated]

OPEN THREADS:
- [Question not yet resolved]

SUGGESTED NEXT SESSIONS:
- [Related topic to continue with]

Copy this block and paste it into your notes, Obsidian vault, or wherever you keep your knowledge base. The extension can also store notes on any chat in its own archive.

# Data and Privacy

To view your stored data: open the dashboard and click Export JSON
To reset everything: go to chrome://extensions, find The Librarian, and click the Details button, then Clear Storage
To back up: export JSON and store the file wherever you keep important documents
If you delete chats in ChatGPT or Gemini, the archive entry stays until you manually remove it from the dashboard

# Troubleshooting
## Badges are not appearing in the sidebar
Click the book icon and press Sync Now
Reload the ChatGPT or Gemini page — the extension needs the page fully loaded
Make sure Developer Mode is still on in chrome://extensions

## The scaffold button is not appearing
Reload the page — the button injects on load
Check that the extension is enabled in chrome://extensions

## Chats are not being classified correctly
Open the dashboard and click Re-classify All in the top bar
For individual chats, open the detail panel and manually set the domain and status, then save — manually tagged chats are not overwritten by auto-classification

## The dashboard is empty after installation
Open ChatGPT or Gemini, let the sidebar load fully, then click the book icon
The extension needs to see the chat list in the sidebar to scrape it — if your sidebar is collapsed, expand it first

# Quick Reference Card
## Extension — Where to Find Things
Book icon in toolbar  →  Popup panel (quick stats, search, filter)
Floating button on ChatGPT/Gemini page  →  Scaffold modal
Open Archive button in popup  →  Full dashboard
Click any card in dashboard  →  Detail panel (notes, tags, status)

## Prompt — Key Phrases
scaffold this  →  Get a domain template
archive this  →  Full session summary
what's open?  →  Unresolved threads
insights so far?  →  All flagged insights
connect this  →  Cross-domain suggestions

## Status Tags
🌱 Seed  —  Early idea, not yet developed
🔨 In Progress  —  Active work or conversation
✅ Resolved  —  Question answered, task complete
💡 Insight  —  Key realization to remember
⚠️ Blocked  —  Needs external input or decision
📌 Reference  —  Evergreen resource to return to


The Librarian — v1.0  ·  All data stored locally  ·  No accounts required
| The Core Promise
Every chat you have — past, present, and future — gets filed, tagged, and made findable. You will never lose a good idea in a dead chat thread again. |
| --- |
| Domain | Icon | Example Clusters | Badge Color |
| --- | --- | --- | --- |
| Creative | ✦ | Writing, Storytelling, Design, Brainstorming | Purple |
| Technical | ⬡ | Code, Architecture, Debugging, AI/ML, Research | Green |
| Business | ◈ | Strategy, Marketing, Product, Finance, Pitch | Amber |
| Personal | ◎ | Philosophy, Learning, Reflection, Goals | Blue |
| Time Required
Installation takes about 5 minutes. You do not need to write any code or have a developer account. |
| --- |
| What Is a Scaffold?
A scaffold is a structured starting template — a set of fields to fill in before you begin. For a Technical thread this means: Problem Statement, Stack, Constraints, Definition of Done. For Creative: Core Idea, Tone, Audience, Reference Points. Starting with a scaffold makes it dramatically easier to retrieve and continue the conversation later. |
| --- |
| What Happens After Activation
On its first response, the AI will output a classification block showing the detected domain, cluster, status, and key terms. It will then ask one clarifying question or provide the scaffold template for that domain. From that point forward, it tracks what is open, flags insights, and is ready to output a structured session archive when you are done. |
| --- |
| Say This | What Happens |
| --- | --- |
| scaffold this | Outputs a structured template for the current domain |
| classify this | Re-runs the classification and updates domain/cluster |
| what's open? | Lists unresolved questions and threads from this session |
| archive this | Outputs a full Session Archive summary block |
| connect this | Suggests cross-domain links to other topics |
| status? | Shows current domain, cluster, and status tag |
| insights so far? | Lists all key insights flagged with the lightbulb marker |
| Everything Stays Local
The Librarian extension stores all data in Chrome's built-in local storage on your own machine. Nothing is sent to any server. There is no account, no login, and no backend. The extension has no external dependencies at runtime. |
| --- |
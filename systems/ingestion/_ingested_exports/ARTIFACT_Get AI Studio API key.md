---
title: Get AI Studio API key
domain: 04_SACRED_CODEX
source: chatgpt: 2025-11-30_Get_AI_Studio_API_key.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# Get AI Studio API key
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-11-30_Get_AI_Studio_API_key.md

# Get AI Studio API key
> **Source:** ChatGPT  |  **Date:** 2025-11-30  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `04_CODEX`

---

## Transcript

### ∆ **USER** — 2025-11-30 00:25

How do I get an API key for ai studio

---

### ⚙ **ASSISTANT** — 2025-11-30 00:25

If by “AI Studio” you mean entity["software","Google AI Studio",0] (with entity["software","Gemini API",0]) — here’s how you get an API key step by step:  

**✅ Steps to get a Gemini/AI Studio API key**

1. Sign in to Google with your account and go to AI Studio: https://aistudio.google.com/ citeturn0search14turn0search12turn0search19  
2. Accept the required terms of service and privacy/usage agreements (first-time only). citeturn0search19turn0search12  
3. In the left sidebar navigation, click on **“Get API key”** or go to the **API Keys** (or similarly-named) section. citeturn0search7turn0search19turn0search14  
4. Click **“Create API key”** (or similar), pick whether to attach it to a new or existing project (for many users, new project is fine). citeturn0search12turn0search19turn0search15  
5. Your unique API key will be generated; copy and store it somewhere secure. citeturn0search19turn0search15turn0search12  

**⚠️ What to know**  
- The key gives you access to use Gemini (or other supported models) via API. citeturn0search20turn0search19  
- For casual experimentation, the “free tier” is available; but for heavier use or production you may need to enable billing via entity["software","Google Cloud Platform",0] / entity["software","Vertex AI",0]. citeturn0search16turn0search12turn0search14  
- The API key should be kept secret (e.g. in environment variables or a secrets manager), not committed in public code. citeturn0search15turn0search19  

---

Since you’re building a larger creative-technical universe (hello SacredSpace ✨), if you like I can walk you through **how to safely store and manage your API key in a small project workflow** (good for prototypes, later production, or family-use setups).  
Do you want me to generate that mini “key-management best practices” guide for you now?

---

### ∆ **USER** — 2025-11-30 00:29

Skip to main content

Gemini API


Sign in

Gemini API
Gemini 3 Pro is here. Try it for free in Google AI Studio.
Home
Gemini API
Gemini API Docs
Was this helpful?

Send feedback
Using Gemini API keys

content_copy




To use the Gemini API, you need an API key. This page outlines how to create and manage your keys in Google AI Studio as well as how to set up your environment to use them in your code.

API Keys
An API key is an encrypted string that you can use when calling Google Cloud APIs. You can create and manage all your Gemini API Keys from the Google AI Studio API Keys page.

Once you have an API key, you have the following options to connect to the Gemini API:

Setting your API key as an environment variable
Providing your API key explicitly
For initial testing, you can hard code an API key, but this should only be temporary since it's not secure. You can find examples for hard coding the API key in Providing API key explicitly section.

Google Cloud projects
Google Cloud projects are fundamental to using Google Cloud services (such as the Gemini API), managing billing, and controlling collaborators and permissions. Google AI Studio provides a lightweight interface to your Google Cloud projects.

If you don't have any projects created yet, you must either create a new project or import one from Google Cloud into Google AI Studio. The Projects page in Google AI Studio will display all keys that have sufficient permission to use the Gemini API. Refer to the import projects section for instructions.

Default project
For new users, after accepting Terms of Service, Google AI Studio creates a default Google Cloud Project and API Key, for ease of use. You can rename this project in Google AI Studio by navigating to Projects view in the Dashboard, clicking the 3 dots settings button next to a project and choosing Rename project. Existing users, or users who already have Google Cloud Accounts won't have a default project created.

Import projects
Each Gemini API key is associated with a Google Cloud project. By default, Google AI Studio does not show all of your Cloud Projects. You must import the projects you want by searching for the name or project ID in the Import Projects dialog. To view a complete list of projects you have access to, visit the Cloud Console.

If you don't have any projects imported yet, follow these steps to import a Google Cloud project and create a key:

Go to Google AI Studio.
Open the Dashboard from the left side panel.
Select Projects.
Select the Import projects button in the Projects page.
Search for and select the Google Cloud project you want to import and select the Import button.
Once a project is imported, go to the API Keys page from the Dashboard menu and create an API key in the project you just imported.

Note: For exist

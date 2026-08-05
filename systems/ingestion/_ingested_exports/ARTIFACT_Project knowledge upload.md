---
title: Project knowledge upload
domain: 08_LEARNING_PATH
source: chatgpt: 2025-12-09_Project_knowledge_upload.md
tags: chatgpt, council-grove, canon-candidate,full-body
type: knowledge_artifact
---

# Project knowledge upload
**Domain:** 08_LEARNING_PATH
**Source:** chatgpt: 2025-12-09_Project_knowledge_upload.md

# Project knowledge upload
> **Source:** ChatGPT  |  **Date:** 2025-12-09  |  **Stage:** `CANON_CANDIDATE`  |  **Pillar:** `08_LEARNING`

---

> [!important] CANON CANDIDATE
> This conversation contains potential canon material. Review and distill before promoting.

## Transcript

### ∆ **USER** — 2025-12-09 20:42

All right. So, the whole thing around GLM 4.6V basically exploded overnight. And once you look at what Zepuai actually shipped, it becomes clear why everyone suddenly stopped scrolling and went, "Okay, this changes things." The simplest way to put it is that this is the first open-source multimodal model that treats images, videos, screenshots, and even full web pages as real inputs for tool calling, not as some secondary thing that has to be squeezed into text first. And that open- source part is the

reason people are shocked because until now, this level of multimodal capability existed only behind closed labs. Now, anyone can download it, run it locally, or build on top of it with no restrictions. That alone completely shifts how agents work because now you get a model that does not just read visuals, it actually uses them as part of its action loop. And that is happening inside a model that also stretches its training context to 128,000 tokens, which means it can process around 150 pages of dense

documents, 200 slides, or an entire hour of video in one go. Nothing hacked together, no pipeline of 15 conversion steps, just direct multimodal reasoning from start to finish. So, JEIPU dropped two versions of this thing. The big GLM 4.6V with 106 billion parameters for cloud setups and high performance clusters and the flash version with only 9 billion parameters that is tuned for local devices and low latency tasks. The crazy part is that the flash variant is free to use and both models are MIT

licensed so companies can deploy them wherever they want without worrying about opening their code or paying enterprise level fees. The larger 106B version runs at $0.3 per million input tokens and 0.9 per million output tokens, which makes it shockingly cheap compared to every other vision capable model of this scale. GPT 5.1 sits at $1.25 per million input plus output. Gemini 3 Pro goes even higher and Claude Opus shoots into the $90 per million range. GLM4.6V lands at $1.2 $2 total and somehow it

delivers benchmark scores that beat models way above its size on long context tasks, video summarization, and multimodal reasoning. The most impressive breakthrough is this native multimodal tool calling system. Traditional LLM tool use works through text. Even if you send an image, the model has to describe it, send that description as a function argument, and wait for a textual response. That is slow, lossy, and honestly kind of outdated at this point. GLM 4.6V 6V skips all of that by using visual data

directly as parameters. A screenshot, a page from a PDF, a frame from a video, those pass straight into the tool without being converted into text first. And the tools themselves can return visual outputs like search result grids, charts, or rendered web pages. The model then continues reasoning using those images alongside text in the same chain. That is the part that got researchers excited because it finally closes the loop between perception, understanding, and action, which is exactly the missing

piece for real multimodal agents. And to make that whole workflow smooth, they extended the model context protocol to support URLs that represent images or frames that avoids file size limits and lets the model target specific visuals inside larger documents. So instead of struggling with giant PDFs or slides, the model hops between references and decides which images to crop, audit, or pull back into the conversation. It is basically a vision native execution layer, which is something even most

closed source models do not really have right now. Quick pause. We just hit 500,000 subscribers, half a million people. So first, seriously, thank you. And hitting that milestone made us realize something. This community isn't just watching AI happen. It's filled with people who want to stay ahead of it. And that leads right into the question a lot of you keep asking. How do you guys create so much content so fast? Look, in 2025 alone, this channel pulled in 32 million views. That's not

luck. That's not grinding harder. It's because every time a new AI breakthrough drops, we plug it straight into our workflow. Most people watch AI news and move on. We use it immediately. So, we decided to release something we've never shared before. The 2026 AI playbook. 1,000 prompts to dominate the AI era. This is how you go from just consuming AI content to actually using AI to build real unfair advantages for yourself. Get your proposals done in 20 minutes instead of 4 hours. Launch that side

business you keep putting off. Become the person in your company who gets twice as much done in half the time. Founding member access ope

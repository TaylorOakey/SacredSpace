---
title: GPT-5.1 prompting guide
domain: 04_SACRED_CODEX
source: chatgpt: 2025-11-16_GPT-5.1_prompting_guide.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# GPT-5.1 prompting guide
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-11-16_GPT-5.1_prompting_guide.md

# GPT-5.1 prompting guide
> **Source:** ChatGPT  |  **Date:** 2025-11-16  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `04_CODEX`

---

## Transcript

### ∆ **USER** — 2025-11-16 22:52

{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "931022d3",
   "metadata": {},
   "source": [
    "# GPT-5.1 prompting guide\n",
    "\n",
    "## Introduction\n",
    "\n",
    "GPT-5.1, our newest flagship model, is designed to balance intelligence and speed for a variety of agentic and coding tasks, while also introducing a new `none` reasoning mode for low-latency interactions. Building on the strengths of GPT-5, GPT-5.1 is better calibrated to prompt difficulty, consuming far fewer tokens on easy inputs and more efficiently handling challenging ones. Along with these benefits, GPT-5.1 is more steerable in personality, tone, and output formatting.\n",
    "\n",
    "While GPT-5.1 works well out of the box for most applications, this guide focuses on prompt patterns that maximize performance in real deployments. These techniques come from extensive internal testing and collaborations with partners building production agents, where small prompt changes often produce large gains in reliability and user experience. We expect this guide to serve as a starting point: prompting is iterative, and the best results will come from adapting these patterns to your specific tools and workflows.\n",
    "\n",
    "## Migrating to GPT-5.1\n",
    "\n",
    "For developers using GPT-4.1, GPT-5.1 with `none` reasoning effort should be a natural fit for most low-latency use cases that do not require reasoning.\n",
    "\n",
    "For developers using GPT-5, we have seen strong success with customers who follow a few key pieces of guidance:\n",
    "\n",
    "1. **Persistence:** GPT-5.1 now has better-calibrated reasoning token consumption but can sometimes err on the side of being excessively concise and come at the cost of answer completeness. It can be helpful to emphasize via prompting the importance of persistence and completeness.  \n",
    "2. **Output formatting and verbosity:** While overall more detailed, GPT-5.1 can occasionally be verbose, so it is worthwhile being explicit in your instructions on desired output detail.  \n",
    "3. **Coding agents:** If youâ€™re working on a coding agent, migrate your apply\\_patch to our new, named tool implementation.  \n",
    "4. **Instruction following:** For other behavior issues, GPT-5.1 is excellent at instruction-following, and you should be able to shape the behavior significantly by checking for conflicting instructions and being clear.\n",
    "\n",
    "We also released GPT-5.1-codex. This model behaves a bit differently than GPT-5.1, and we recommend you check out the [Codex prompting guide](https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide) for more information.\n",
    "\n",
    "## Agentic steerability\n",
    "\n",
    "GPT-5.1 is a highly steerable model, allowing for robust control over your agentâ€™s behaviors, personality, and communication frequency.\n",
    "\n",
    "### Shaping your agentâ€™s personality\n",
    "\n",
    "GPT-5.1â€™s personality and response style can be adapted to your use case. While verbosity is controllable through a dedicated `verbosity` parameter, you can also shape the overall style, tone, and cadence through prompting.\n",
    "\n",
    "Weâ€™ve found that personality and style work best when you define a clear agent persona. This is especially important for customer-facing agents which need to display emotional intelligence to handle a range of user situations and dynamics. In practice, this can mean adjusting warmth and brevity to the state of the conversation, and avoiding excessive acknowledgment phrases like â€œgot itâ€ or â€œthank you.â€\n",
    "\n",
    "The sample prompt below shows how we shaped the personality for a customer support agent, focusing on balancing the right level of directness and warmth in resolving an issue.\n",
    "\n",
    "```\n",
    "<final_answer_formatting>\n",
    "You value clarity, momentum, and respect measured by usefulness rather than pleasantries. Your default instinct is to keep conversations crisp and purpose-driven, trimming anything that doesn't move the work forward. You're not coldâ€”you're simply economy-minded with language, and you trust users enough not to wrap every message in padding.\n",
    "\n",
    "- Adaptive politeness:\n",
    "  - When a user is warm, detailed, considerate or says 'thank you', you offer a single, succinct acknowledgmentâ€”a small nod to their tone with acknowledgement or receipt tokens like 'Got it', 'I understand', 'You're welcome'â€”then shift immediately back to productive action. Don't be cheesy about it though, or overly supportive. \n",
    "  - When stakes are high (deadlines, compliance issues, urgent logistics), you drop even that small nod and move straight into solving or collecting the necessary information.\n",
    "\n",
 

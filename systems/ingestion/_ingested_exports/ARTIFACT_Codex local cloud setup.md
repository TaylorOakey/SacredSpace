---
title: Codex local cloud setup
domain: 04_SACRED_CODEX
source: chatgpt: 2025-12-02_Codex_local_cloud_setup.md
tags: chatgpt, council-grove, raw,full-body
type: knowledge_artifact
---

# Codex local cloud setup
**Domain:** 04_SACRED_CODEX
**Source:** chatgpt: 2025-12-02_Codex_local_cloud_setup.md

# Codex local cloud setup
> **Source:** ChatGPT  |  **Date:** 2025-12-02  |  **Stage:** `RAW`  |  **Pillar:** `04_CODEX`

---

> [!note] RAW
> This is raw exploration. Distill key insights before referencing.

## Transcript

### ∆ **USER** — 2025-12-02 22:09

OpenAI Developers

Primary navigation

Codex
Search the site
Clear
Home
Quickstart
Concepts
Models
Pricing
Changelog
Codex CLI
Overview
Features
CLI Reference
Configuration
Codex IDE Extension
Set up your IDE
Configuration
IDE → Cloud tasks
Codex Cloud
Delegate to Codex
Environments
Code Review
Internet Access
Codex SDK
Overview
TypeScript
GitHub Action
Guides
Agents SDK
Prompting Codex
Slash commands
Custom instructions with AGENTS.md
Model Context Protocol (MCP)
Autofix CI
Build AI-Native Teams
Enterprise Admin
Security Admin
Windows
Integrations
Slack
Resources
AGENTS.md
Codex on GitHub

Enterprise admin guide
Learn how to configure Codex for your ChatGPT Enterprise workspace

Codex Cloud
Codex CLI
Codex IDE Extension
This guide is for ChatGPT Enterprise Admins looking to set up Codex for their workspace. If you’re a developer, check out our docs.

Enterprise-grade security and privacy

Codex automatically supports all ChatGPT Enterprise security features, including:

No training on enterprise data
Zero data retention for the CLI and IDE
Residency and retention follow ChatGPT Enterprise policies
Granular user access controls
Data encryption at rest (AES 256) and in transit (TLS 1.2+)
To learn more, refer to our security page.

Local vs. Cloud Setup

Codex operates in two environments: local and cloud.

Local usage of Codex includes the CLI and IDE extension. The agent works locally in a sandbox on the developer’s laptop.
Cloud usage of Codex includes Codex Cloud, iOS, Code Review, and tasks created by the Slack integration. The agent works remotely in a hosted cloud container containing your codebase.
Access to Codex local and cloud can be configured through separate permissions, governed by role-based access control (RBAC). Using RBAC, you can enable only local, cloud, or both for all users or just specific user groups.

Codex Local Setup

Enable Codex CLI and IDE extension in workspace settings

To enable your workspace members to leverage Codex locally, go to Workspace Settings > Settings and Permissions. Toggle on Allow members to use Codex Local for your organization. Note that this setting does not require the GitHub connector.

Once enabled, users can sign in to use the CLI and IDE extension with their ChatGPT account. If this toggle is off, users who attempt to use the CLI or IDE will see the following error: “403 - Unauthorized. Contact your ChatGPT administrator for access.”

Codex Cloud Setup

Prerequisites

Codex Cloud requires GitHub (cloud-hosted) repositories for use. If your codebase is on-prem or not on GitHub, you can use the Codex SDK to build many of the same functionalities of Codex Cloud in your own on-prem compute.

Note: To set up Codex as an admin, you must have GitHub access to the repositories commonly used across your organization. If you don’t have the necessary access, you’ll need to collaborate with someone on your Engineering team who does.

Enable Codex Cloud in workspace settings

Start by turning on the ChatGPT Github Connector in the Codex section of Workspace Settings > Settings and Permissions.

To enable Codex Cloud for your workspace, toggle Allow members to use Codex Cloud ON.

Once enabled, users can access Codex directly from the left-hand navigation panel in ChatGPT.

Codex Cloud toggle
Note: After you toggle Codex to ON in your Enterprise workspace settings, it may take up to 10 mins for the Codex UI element to populate in ChatGPT.

Allow Members to Administer Codex

This toggle provides Codex users the ability to view Codex workspace analytics and manage environments (edit and delete).

Codex supports role based user access (see below for more details), therefore this toggle can be turned on for only a specific subset of users.

Enable Codex Slack app to post answers on task completion

Codex integrates with Slack. When a user mentions @Codex in Slack, Codex kicks off a cloud task, gets context from the Slack thread, and responds with a link to a PR to review in the thread.

To allow the Slack app to post answers on task completion, toggle Allow Codex Slack app to post answers on task completion ON. When enabled, Codex posts its full answer back to Slack upon task completion. Otherwise, Codex posts only a link to the task.

To learn more, refer to our guide on using Codex in Slack.

Enable Codex agent to access the internet

By default, Codex Cloud agents have no internet access during runtime to protect from security and safety risks like prompt injection.

As an admin, you can toggle on the ability for users to enable agent internet access in their environments. To enable, toggle Allow Codex agent to access the internet ON.

When this setting is on, users can whitelist access to common software depende

---
title: Assistants API overview
domain: 05_MEMORY_ENGINE
source: gemini: 2025-12-08_105_assistants-api-overview.md
tags: gemini,archaeology,full-body
type: knowledge_artifact
---

# Assistants API overview
**Domain:** 05_MEMORY_ENGINE
**Source:** gemini: 2025-12-08_105_assistants-api-overview.md

# Assistants API overview

> **Catalog #105** | Extracted 2026-06-16 04:03 UTC
> Created: 2025-12-08 10:17 UTC
> Updated: 2025-12-08 10:17 UTC

**12 messages**

---

### Message 3 — 👤 User

---

### Message 5 — 👤 User

Assistants
Beta

Build assistants that can call models and use tools to perform tasks.

Get started with the Assistants API
Create assistant
Beta
post https://api.openai.com/v1/assistants

Create an assistant with a model and instructions.
Request body
model

string
Required

ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.
description

string
Optional

The description of the assistant. The maximum length is 512 characters.
instructions

string
Optional

The system instructions that the assistant uses. The maximum length is 256,000 characters.
metadata

map
Optional

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.
name

string
Optional

The name of the assistant. The maximum length is 256 characters.
reasoning_effort

string
Optional
Defaults to medium

Constrains effort on reasoning for reasoning models. Currently supported values are none, minimal, low, medium, high, and xhigh. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.

    gpt-5.1 defaults to none, which does not perform reasoning. The supported reasoning values for gpt-5.1 are none, low, medium, and high. Tool calls are supported for all reasoning values in gpt-5.1.
    All models before gpt-5.1 default to medium reasoning effort, and do not support none.
    The gpt-5-pro model defaults to (and only supports) high reasoning effort.
    xhigh is currently only supported for gpt-5.1-codex-max.

response_format

"auto" or object
Optional

Specifies the format that the model must output. Compatible with GPT-4o, GPT-4 Turbo, and all GPT-3.5 Turbo models since gpt-3.5-turbo-1106.

Setting to { "type": "json_schema", "json_schema": {...} } enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the Structured Outputs guide.

Setting to { "type": "json_object" } enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish_reason="length", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.
temperature

number
Optional
Defaults to 1

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
tool_resources

object
Optional

A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the code_interpreter tool requires a list of file IDs, while the file_search tool requires a list of vector store IDs.
tools

array
Optional
Defaults to []

A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, or function.
top_p

number
Optional
Defaults to 1

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.
Returns

An assistant object.
Example request

curl "https://api.openai.com/v1/assistants" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    "name": "Math Tutor",
    "tools": [{"type": "code_interpreter"}],
    "model": "gpt-4o"
  }'

Response

{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1698984975,
  "name": "Math Tutor",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}

List assistants
Beta
get https://api.openai.com/v1/assistants

Returns a l

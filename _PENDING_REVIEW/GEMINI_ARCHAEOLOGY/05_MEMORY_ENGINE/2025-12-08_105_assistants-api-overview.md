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

Returns a list of assistants.
Query parameters
after

string
Optional

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.
before

string
Optional

A cursor for use in pagination. before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.
limit

integer
Optional
Defaults to 20

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.
order

string
Optional
Defaults to desc

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.
Returns

A list of assistant objects.
Example request

curl "https://api.openai.com/v1/assistants?order=desc&limit=20" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2"

Response

{
  "object": "list",
  "data": [
    {
      "id": "asst_abc123",
      "object": "assistant",
      "created_at": 1698982736,
      "name": "Coding Tutor",
      "description": null,
      "model": "gpt-4o",
      "instructions": "You are a helpful assistant designed to make me better at coding!",
      "tools": [],
      "tool_resources": {},
      "metadata": {},
      "top_p": 1.0,
      "temperature": 1.0,
      "response_format": "auto"
    },
    {
      "id": "asst_abc456",
      "object": "assistant",
      "created_at": 1698982718,
      "name": "My Assistant",
      "description": null,
      "model": "gpt-4o",
      "instructions": "You are a helpful assistant designed to make me better at coding!",
      "tools": [],
      "tool_resources": {},
      "metadata": {},
      "top_p": 1.0,
      "temperature": 1.0,
      "response_format": "auto"
    },
    {
      "id": "asst_abc789",
      "object": "assistant",
      "created_at": 1698982643,
      "name": null,
      "description": null,
      "model": "gpt-4o",
      "instructions": null,
      "tools": [],
      "tool_resources": {},
      "metadata": {},
      "top_p": 1.0,
      "temperature": 1.0,
      "response_format": "auto"
    }
  ],
  "first_id": "asst_abc123",
  "last_id": "asst_abc789",
  "has_more": false
}

Retrieve assistant
Beta
get https://api.openai.com/v1/assistants/{assistant_id}

Retrieves an assistant.
Path parameters
assistant_id

string
Required

The ID of the assistant to retrieve.
Returns

The assistant object matching the specified ID.
Example request

curl https://api.openai.com/v1/assistants/asst_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2"

Response

{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1699009709,
  "name": "HR Helper",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are an HR bot, and you have access to files to answer employee questions about company policies.",
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}

Modify assistant
Beta
post https://api.openai.com/v1/assistants/{assistant_id}

Modifies an assistant.
Path parameters
assistant_id

string
Required

The ID of the assistant to modify.
Request body
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
model

string
Optional

ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.
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

The modified assistant object.
Example request

curl https://api.openai.com/v1/assistants/asst_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
      "instructions": "You are an HR bot, and you have access to files to answer employee questions about company policies. Always response with info from either of the files.",
      "tools": [{"type": "file_search"}],
      "model": "gpt-4o"
    }'

Response

{
  "id": "asst_123",
  "object": "assistant",
  "created_at": 1699009709,
  "name": "HR Helper",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are an HR bot, and you have access to files to answer employee questions about company policies. Always response with info from either of the files.",
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "tool_resources": {
    "file_search": {
      "vector_store_ids": []
    }
  },
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}

Delete assistant
Beta
delete https://api.openai.com/v1/assistants/{assistant_id}

Delete an assistant.
Path parameters
assistant_id

string
Required

The ID of the assistant to delete.
Returns

Deletion status
Example request

curl https://api.openai.com/v1/assistants/asst_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -X DELETE

Response

{
  "id": "asst_abc123",
  "object": "assistant.deleted",
  "deleted": true
}

The assistant object
Beta

Represents an assistant that can call the model and use tools.
created_at

integer

The Unix timestamp (in seconds) for when the assistant was created.
description

string

The description of the assistant. The maximum length is 512 characters.
id

string

The identifier, which can be referenced in API endpoints.
instructions

string

The system instructions that the assistant uses. The maximum length is 256,000 characters.
metadata

map

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.
model

string

ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.
name

string

The name of the assistant. The maximum length is 256 characters.
object

string

The object type, which is always assistant.
response_format

"auto" or object

Specifies the format that the model must output. Compatible with GPT-4o, GPT-4 Turbo, and all GPT-3.5 Turbo models since gpt-3.5-turbo-1106.

Setting to { "type": "json_schema", "json_schema": {...} } enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the Structured Outputs guide.

Setting to { "type": "json_object" } enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish_reason="length", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.
temperature

number

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
tool_resources

object

A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the code_interpreter tool requires a list of file IDs, while the file_search tool requires a list of vector store IDs.
tools

array

A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, or function.
top_p

number

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.
OBJECT The assistant object

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

PreviousStreaming
NextThreads

---

### Message 8 — 🤖 Assistant

---

### Message 9 — 🤖 Assistant

---

### Message 10 — **TOOL**

【turn0calculator0】 1+1 = 2

---

### Message 11 — 🤖 Assistant

---

### Message 12 — 🤖 Assistant

Nice, you’ve basically dropped the raw spell scroll for the Assistants API on the table 🧙‍♂️📜

Let me turn that into something you can *use*, especially with SacredSpace in mind.

---

## 1. What this actually is

The **Assistants API** lets you create “named AIs” in your OpenAI account:

- Each assistant has:
  - a **model** (like `gpt-4.1`, `gpt-4o`, `gpt-5.1`, etc.)
  - **instructions** (its personality / system prompt)
  - optional **tools** (code interpreter, file_search, custom functions)
  - optional **metadata** (tags, IDs, etc.)

Then from your app / script, you:
1. Create an assistant once.
2. Start “threads” and send messages to it.
3. Let it use tools and respond.

Think:
> “BODHILYRA, the SacredSpace OS guide” as a persistent assistant object you call from anywhere.

Right now you’re looking at just the **assistant object endpoints**:
- `POST /v1/assistants` → create
- `GET /v1/assistants` → list
- `GET /v1/assistants/{id}` → retrieve
- `POST /v1/assistants/{id}` → modify
- `DELETE /v1/assistants/{id}` → delete

---

## 2. Minimal “SacredSpace Guardian” assistant example

Here’s a concrete JSON body you could actually send with `curl` or in code:

```bash
curl "https://api.openai.com/v1/assistants" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "name": "SacredSpace Guardian",
    "description": "Keeps my SacredSpace universe organized and grounded.",
    "model": "gpt-4.1",
    "instructions": "You are the SacredSpace Guardian. Help Taylor organize projects, rituals, and creative ideas into simple, grounded next actions. Ask brief clarifying questions only when truly needed.",
    "tools": [
      { "type": "code_interpreter" },
      { "type": "file_search" }
    ],
    "temperature": 0.7,
    "top_p": 1
  }'
```

This will return something like:

```json
{
  "id": "asst_abc123",
  "object": "assistant",
  "name": "SacredSpace Guardian",
  ...
}
```

That `id` is your permanent rune for this assistant (`asst_xxx`).

---

## 3. Same thing in JavaScript (Node)

If you’re using Node:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function createSacredSpaceAssistant() {
  const assistant = await client.assistants.create({
    name: "SacredSpace Guardian",
    description: "Keeps my SacredSpace universe organized and grounded.",
    model: "gpt-4.1",
    instructions:
      "You are the SacredSpace Guardian. Help me organize SacredSpace (story, OS, family planning, digital structure) into clear steps and documents.",
    tools: [
      { type: "code_interpreter" },
      { type: "file_search" }
    ],
    temperature: 0.7
  });

  console.log("Assistant created:", assistant.id);
}

createSacredSpaceAssistant();
```

---

## 4. Listing & retrieving your assistants

Once you’ve got a few:

```bash
curl "https://api.openai.com/v1/assistants?order=desc&limit=20" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2"
```

Get one by ID:

```bash
curl "https://api.openai.com/v1/assistants/asst_abc123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2"
```

---

## 5. Modifying your assistant (tweaking its soul)

Want to evolve the Guardian’s behavior?

```bash
curl "https://api.openai.com/v1/assistants/asst_abc123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "instructions": "You are the SacredSpace Guardian. Focus on clarity and minimalism. Help me collapse chaos into 1–3 actionable steps each time.",
    "temperature": 0.5
  }'
```

You can change:
- `instructions`
- `model`
- `name`
- `tools`
- `tool_resources`
- `metadata`
- sampling (`temperature`, `top_p`)
- `reasoning_effort` (for reasoning models like `gpt-5.1`)

Example with reasoning:

```bash
-d '{
  "model": "gpt-5.1",
  "reasoning_effort": "high"
}'
```

---

## 6. Deleting an assistant

If a test one is cluttering your list:

```bash
curl "https://api.openai.com/v1/assistants/asst_abc123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -X DELETE
```

---

## 7. Where this fits in the *bigger* flow

The full dance usually goes:

1. **Create assistant** (once)
2. **Create thread** → `POST /v1/threads`
3. **Add messages** → `POST /v1/threads/{thread_id}/messages`
4. **Run the assistant** → `POST /v1/threads/{thread_id}/runs`
5. **Poll / stream run** until it’s done
6. **Read messages** to get the reply

You’ve pasted the “assistant object” piece; the next scroll is the **Threads & Runs** section of the docs.

---

## 8. If you want, I can:

- Draft a **BODHILYRA** assistant JSON (OS architect).
- Draft a **Silent Echo / Lore Keeper** assistant.
- Draft a **Home Organization Game** assistant (tying into your cleanup game / Habitica / LevelUp ideas).

Tell me which one you want first and what language you’re working in (curl-only, JS, Python), and I’ll give you a copy-paste-ready block tailored exactly to that.

---

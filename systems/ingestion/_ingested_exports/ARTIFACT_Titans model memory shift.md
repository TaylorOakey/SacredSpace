---
title: Titans model memory shift
domain: 05_MEMORY_ENGINE
source: gemini: 2025-12-14_064_titans-model-memory-shift.md
tags: gemini,archaeology,full-body
type: knowledge_artifact
---

# Titans model memory shift
**Domain:** 05_MEMORY_ENGINE
**Source:** gemini: 2025-12-14_064_titans-model-memory-shift.md

# Titans model memory shift

> **Catalog #64** | Extracted 2026-06-16 04:03 UTC
> Created: 2025-12-14 18:48 UTC
> Updated: 2025-12-14 18:48 UTC

**7 messages**

---

### Message 4 — 👤 User

Google has spent years trying to push past the limits of transformers. And with its recent models, it may have just finally achieved the one breakthrough every AGI road map has been waiting for. A model that can finally remember and grows and adapts as it runs. If you have ever tried to make a large language model reason over an entire code base, a long legal case or weeks of system logs, you already know the frustration. You stretch the context window. You stack prompts. The costs rise with every extra

token. And still the model loses track of something important right when you need it most. Transformers are extraordinary short-term thinkers. They are masters at pattern matching, at structure, at immediate reasoning. But as long-term storage systems, they are brittle, expensive, and fundamentally limited. The deeper the context, the more they struggle and the memory problem never really goes away. That pressure is exactly what pushed Google to develop something radically different. At first glance, Google

Titans might look like just another name in the growing forest of transformer replacements. But when you examine it closely, it stops feeling like a variant and starts feeling like a shift in philosophy. Titans is built on a simple idea. Let attention handle the present and let a dedicated neural system become the memory of the past. Instead of forcing everything through attention, Titan splits the job cleanly. One part of the model handles short-range reasoning and the other becomes a long-term memory that learns while the

model is running. Underneath this architecture sits a theoretical foundation called MyArs. It reframes nearly every modern sequence model. Transformers, Retnet, Mamba, RWKV, Titans under a single unifying perspective. In the Mirus view, these architectures are not wildly different inventions. They are variations of the same underlying mechanism. Each is an associative memory that maps keys to values, updated through some internal objective, and stabilized through a form of forgetting. When described this way,

all the mystery disappears and the field becomes a design space with clear dials you can turn. Titans embraces this perspective completely. It pairs a compact attention core with a neural long-term memory. This long-term memory is not a single vector, not a compressed state, not a crude summary. It is a deep multi-layer perceptron whose weights serve as the memory itself. The model receives tokens, generates key value pairs, and the long-term memory tries to predict those values from their keys.

The difference between prediction and reality becomes the surprise signal. This surprise is the gradient the memory uses to update itself at test time. A small surprise means the memory already understands this pattern. A large surprise means the model has encountered something new or structurally important. This is what gets stored. The process is intuitive. If you're reading text that repeats familiar patterns, the memory barely changes. If you suddenly reach a critical new concept or an unusual

detail, the memory reacts and updates. The long-term memory becomes a kind of distilled notebook, evolving with the sequence, absorbing only what matters and ignoring the rest. Over long stretches of data, millions of tokens in some experiments, the memory becomes an abstract representation of the global structure, not a literal log of every token. That is the crucial difference from Transformers. Titans doesn't try to remember everything. It tries to remember the right things. Mirrors formalizes this by

breaking down a sequence model into four decisions. You choose a memory architecture, vector, matrix, or deep network. You choose an attentional bias, a rule that determines what the memory prioritizes internally. You choose a retention gate, a form of controlled forgetting that ensures new information does not overwrite everything that came before. And finally, you choose a memory learning algorithm, a method for updating the memory through online optimization. Once you describe models this way, the

field becomes coherent. Transformers use a shallow memory with dot productduct bias. Retnet uses a decaying kernel. Mambber uses a fixed size recurrent state. Titans picks a deep memory with online gradient descent and explicit retention. They are all solving the same problem with different choices. The people behind me pushed these ideas further by exploring variants that use different objectives. They built Monita, which uses stricter generalized norms for memory updates. They built Yard which relies on Huba style losses that

make the model less sensitive to outliers in the sequence. And they built Mera which frames memory as a probability distribution enforcing stability through constraints rather than

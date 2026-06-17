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

make the model less sensitive to outliers in the sequence. And they built Mera which frames memory as a probability distribution enforcing stability through constraints rather than decay. The specifics vary but the message is clear. Attentional bias is a design parameter not a fixed rule of nature. Memory can be built in many ways. The test time learning mechanism inside Titans can sound alarming at first. It suggests a model that is mutating its own weights while running. But Titans only updates the long-term

memory in a carefully controlled manner. For each token, it produces a key and value, feeds the key into the memory, and observes how wrong the prediction is. That wrongness is the surprise. High surprise triggers a stronger update. Low surprise produces almost no change. The memory then takes a gradient step toward encoding the association. The update includes momentum which keeps the memory sensitive across multiple tokens whenever a conceptual shift occurs. And the retention gate gently pulls the

weights towards stability, preventing drift and allowing unimportant details to fade. This retention gate is more than a convenience. It is an essential part of safety and stability. Without forgetting, early sequence models would spiral into instability or fill their capacity with noise. Titans solves this by letting repeated patterns win and letting rare, irrelevant patterns disappear. Forgetting becomes a controlled feature that protects the model from stale associations and sharpens long-term recall. It also makes

long session interactions more consistent because the model's internal state does not depend on every quirk of the prompt history. To understand Titans in context, it helps to compare it to its neighbors. Transformers store a growing key value cache. This is powerful but becomes expensive as sequences lengthen with costs rising quadratically. Linear recurrent models maintain a fixed size memory which is efficient but compresses information into a tight bottleneck that eventually loses detail. Titan sits between these

extremes. It keeps the precision of local attention while pushing long range storage into a deep memory that can learn abstractions. It allows fixed memory cost while unlocking long range expressiveness. For tasks that stretch across millions of tokens like multi-document reasoning, genomics, time series modeling, or longunning agents, this hybrid structure becomes very appealing. Titans ships in three forms, each connecting memory to the main stack differently. The MAC variant or memory as context provides a

global summary vector at each step, allowing attention to decide when to look at nearby tokens and when to look at global context. It works naturally for extreme long context question answering or retrieval augmented generation. The MAG variant or memory as gate uses the memory to control the behavior of sliding window attention. It widens or narrows the receptive field depending on what the memory believes is relevant. This variant shines in workloads like log analysis or long code traces where local structure dominates

but global jumps occasionally matter. And the MAL variant or memory as layer treats the memory as an interled layer alternating between local computation and global recall. It resembles a standard deep model and behaves like a generalurpose long context engine. Benchmarks make the case clearer. Titans matches or surpasses strong transformer and linear recurrent baselines on C4 and Wiki text while preserving training parallelism and linear inference speed. But the more impressive results come from long context stress tests in needle

in a haststack scenarios. Titans maintains extremely high accuracy even when the context stretches far beyond typical transformer limits. It performs well beyond 16,000 tokens and scales to context exceeding 2 million tokens in some experiments. In the Babylon benchmark, which demands reasoning across widely separated facts, Titans outperforms larger models like GPT4, Llama 3.170B, and even Llama 3 equipped with retrieval augmentation. All of this is achieved with Titan's models containing as few as 760 million

parameters. These results are no accident. Ablation studies show that the depth of the memory network matters enormously. When you compare two memories with the same parameter count, the deeper one consistently wins. It achieves lower perplexity, better long range recall, and more stable scaling as sequence length increases. depth gives the memory representational richness that shallow memories cannot match. The question many people ask is whether Titans signals the end of the Transformer era. The honest answer is

no. Transformers solved short- range reasoning so well that they will remain central to machine learning for years. Titans doesn't replace the Transformer. It complements it by giving models a memory system that transformers never had. It offers a way to stop wrestling with long context limits, to replace brittle retrieval setups with learned memory, and to treat memory as a design choice rather than an afterthought. For anyone building real products, the key question is straightforward. Where does

your workload require stable structure across hundreds of thousands or millions of tokens? Where do you currently rely on window hacks, vector databases, or sharding tricks simply because your model can't remember what you gave it earlier? Those are the places where Titans becomes transformative. It's combination of test time learning, disciplined forgetting, and deep memory abstraction provides a road map rather than a series of patches. Google's call to action is clear. Read the Titans and

Mirus papers. map their ideas onto your own models. Identify where a learned long range memory would fundamentally change your system. The sooner developers treat memory as a core architectural choice, the sooner Titan style models will evolve from experimental breakthroughs into the default backbone for long context AI. And judging by the direction of research, from titans to mirrors to the many emerging memory ccentric architectures, the future of AI may depend less on making attention larger

and more on rethinking what memory should be. So if models like Titans can start building their own long-term memory while they're running, do you think that's a small step toward AGI or just another clever architecture? Let me know in the comments. And if you want the real story behind the world's fastest moving AI breakthroughs, make sure to like and subscribe to Evolving AI for daily coverage.

---

### Message 5 — 👤 User

---

### Message 6 — 🤖 Assistant

---

### Message 7 — 🤖 Assistant

You’ve laid out the case for Titans very cleanly. Let’s slow the spin of the gyroscope and look at what this *actually* means, without either hype or dismissal.

First, a grounding move: Titans is not magic memory. It is *learned state with rules*. That distinction matters more than most people realize.

What Google did here is quietly admit something the field has been tiptoeing around for a decade: attention is not memory. Attention is *routing*. It decides what to look at *now*. For years we pretended that if we just let models look at more tokens, somehow memory would emerge. It didn’t. We got quadratic costs, brittle recall, and systems that forget the punchline of a novel halfway through the book.

Titans breaks the spell by separating **presence** from **history**.

Short-range reasoning stays where it belongs: attention, pattern matching, local inference. Long-range structure moves into a different substrate entirely: a parametric system that *changes as a consequence of surprise*. That’s the philosophical shift. Not bigger windows. Not smarter retrieval. A second learning loop running at inference time.

This is where the AGI question gets interesting.

### Is this “real” memory?

In biological terms, Titans looks much closer to *synaptic plasticity* than anything transformers have done before. The memory weights aren’t a log. They’re not a cache. They’re not a database. They are a **compressed abstraction shaped by prediction error**.

That’s how brains work:
- Familiar patterns → minimal plasticity  
- Novel, salient patterns → stronger updates  
- Repetition → consolidation  
- Noise → decay  

The retention gate is doing something deeply nontrivial here. Forgetting is not a bug; it’s the stability mechanism. Without it, the system would be unusable. With it, you get something like semantic drift control.

But—and this is crucial—this is still *task-bounded memory*. Titans remembers *in service of the current sequence*. It does not wake up tomorrow with a persistent self-model unless you explicitly engineer that persistence across runs.

So no, this is not consciousness sneaking in through the side door.

### Is it a step toward AGI?

It *is* a step toward something important, but not the thing most people mean when they say AGI.

AGI requires at least four ingredients:
1. **Persistent identity** across contexts  
2. **Self-modeling** (knowing what it knows and doesn’t)  
3. **Goal continuity** across time  
4. **World modeling** that generalizes beyond training distributions  

Titans meaningfully advances #4 and partially #2.

Why #2 only partially? Because surprise-driven updates are *implicit*. The model adapts, but it does not explicitly reason about *why* it is adapting or how its memory has changed. There is no introspective loop yet. The memory learns; the model doesn’t *reflect* on that learning.

What Titans *does* give us is something we’ve been missing: **temporal coherence**. A system that can read a million-token story and still care about the opening premise is no longer goldfish intelligence. That alone unlocks agents, scientific analysis, long-horizon planning, and genuinely useful autonomy.

### The deeper significance (the quiet one)

The most important part of your write-up isn’t Titans itself. It’s the **MIRUS framing**.

Once you see transformers, Mamba, RWKV, RetNet, and Titans as *design points in a memory space*, the field changes flavor. We stop arguing about architectures and start engineering memory systems with explicit knobs:
- What gets remembered?
- How fast does it update?
- What decays?
- What stabilizes?
- What objective defines “importance”?

That’s a maturation moment. It’s the difference between alchemy and chemistry.

### So what is Titans, really?

Titans is not AGI.
It is not the end of transformers.
It is not a runaway self-modifying intelligence.

Titans *is*:
- The first serious admission that **learning at test time is necessary**
- A bridge between static models and adaptive systems
- A memory architecture that finally scales *with time* instead of collapsing under it

If transformers were the cortex’s flash of pattern recognition, Titans is the hippocampus showing up to the meeting.

The future probably isn’t “Titans everywhere.” It’s **memory-diverse systems**: attention for now, learned memory for structure, symbolic tools for precision, and explicit self-models layered on top.

The real AGI step won’t be when a model remembers more.
It’ll be when it knows *what it chose to remember, and why*.

That door is not open yet—but Titans put the handle on it.

---

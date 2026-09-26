# ∆ THE LIVELIHOOD LOOP ∆
## A recursive two-agent protocol for making SacredSpace Taylor's main income

**Layer:** RAW → DISTILLED. The loop proposes and tests; only Taylor promotes anything to canon or signs anything.
**Agents:** **Claude Code** (cloud: research, web, GitHub, Drive, synthesis) ⇄ **OpenCode** (local: D:, Obsidian vault, exports, real assets, live spine)
**Channel:** the files in this folder, on branch `claude/sacred-marketplace-income-67t27a` (merge to `main` once Taylor approves). Each agent **pulls before reading and pushes after writing**.

---

## 1. The North Star, in numbers

| Variable | Meaning | Value |
|---|---|---|
| `TARGET_NET_MONTHLY` | Monthly SacredSpace net income that would replace the day job | **Set by Taylor.** Keep it in the local-only file `D:/SacredSpace_OS/09_SACRED_MARKET/LOCAL_TARGETS.md` (not committed) if you'd rather it not be on GitHub |
| `RUNWAY_MONTHS` | Months of household expenses saved before leaping | Taylor sets it (6 is a common floor) |
| `HOURS_PER_WEEK` | Time actually available for SacredSpace right now | ~3–4 today; rises only as income rises |

**The Leap Gate** (the only condition for leaving the day job): the **trailing 6-month average** of `cash_position` in `GET /merchant/ledger` (entities `SOLE_PROP`/`LLC`) is ≥ `TARGET_NET_MONTHLY`, **and** `RUNWAY_MONTHS` of savings exist, **and** no single income source is more than 50% of the total. Until then, SacredSpace grows *alongside* the job. Most one-person creative businesses take 1–3 years to get there. The loop exists to make that climb deliberate rather than hopeful.

**The ladder:** `$0 → First Flame ($1,111 cumulative) → $500/mo → $1,000/mo → 25% of target → 50% → 100% (Leap Gate)`. Every round reports which rung the ledger is on.

---

## 2. One round, step by step

```
 ┌──────────────── CLAUDE CODE (cloud) ────────────────┐      ┌──────────────── OPENCODE (local) ────────────────┐
 │ 1. git pull · read LOOP.md, ROUND_LOG (last entry),  │      │ 1. git pull · read LOOP.md, ROUND_LOG (last       │
 │    IDEA_BANK                                         │      │    entry), IDEA_BANK                              │
 │ 2. Do every "NEXT FOR CLAUDE" item from the log      │      │ 2. Do every "NEXT FOR OPENCODE" item              │
 │ 3. Research lane: market / platform rules / pricing  │ ───► │ 3. Ground-truth lane: what really exists on D:,   │
 │    / open-source tools / grants / competitors        │      │    in the vault, exports, art files, the spine,  │
 │ 4. Add ≤ 5 new ideas (RAW), re-score changed ones    │ ◄─── │    the ledger. Verify or refute Claude's claims   │
 │ 5. Append ROUND_LOG entry + NEXT FOR OPENCODE        │      │ 4. Add ≤ 5 ideas found in the archives (RAW)      │
 │ 6. Commit + push. Stop.                              │      │ 5. Append ROUND_LOG entry + NEXT FOR CLAUDE       │
 └──────────────────────────────────────────────────────┘      │ 6. Commit + push. Stop.                           │
                                                               └───────────────────────────────────────────────────┘
                       Every 3rd round, or whenever Taylor asks: ACTION BRIEF for Taylor (§6)
```

**Hard limits per round:** at most 5 new ideas per agent, one ROUND_LOG entry per agent, and no rewriting another agent's entry (append a correction instead). Rounds are small on purpose. The loop has to cost less of Taylor's attention than it saves.

---

## 3. Idea lifecycle

`RAW` (anyone adds it) → `SCORED` (both agents have touched it) → `EXPERIMENT` (Taylor approves; it gets a kill metric and a date) → `LIVE` (making money and recorded in the ledger) → `KILLED` (with the reason written down). Nothing is deleted.

**At most 3 EXPERIMENTS at once.** A fourth can only start when one goes LIVE or is KILLED.

---

## 4. Scoring (1–5 each; total out of 40)

| Criterion | Weight | 5 means | 1 means |
|---|---|---|---|
| **Revenue ceiling** | ×2 | Could reach 25%+ of `TARGET_NET_MONTHLY` alone | Pocket change |
| **Speed to first $** | ×2 | First sale possible in ≤ 30 days | Needs 12+ months |
| **Hours fit** | ×1 | Runs in ≤ 1 hr/week once built | Needs daily attention |
| **Capital fit** | ×1 | ≤ $50 to start | Needs loans or inventory |
| **Audience leverage** | ×1 | Every unit sold or shared brings in new people | Invisible |
| **Sovereignty & canon fit** | ×1 | Local-first, owned channel, true to the lore | Renting an audience from one platform; off-brand |

Every score needs **one line of evidence** (a link, a fee table, a real file path, or a ledger number). **An unevidenced score counts as 1.**

---

## 5. Guardrails (both agents, every round)

1. **Truth over momentum.** Never describe something as done, filed, live or earning unless the ledger, a platform dashboard or a file proves it. (Section §5-7 of the plan exists because a grant proposal broke this rule.)
2. **No filings, payments, listings, posts, emails or account sign-ups.** Agents draft; Taylor clicks "submit".
3. **Privacy.** Keep the day-job employer, family health and home matters, other people's contact details, API keys and household finances out of the repo. Put them in local-only files on D: if they're needed at all.
4. **Canon Gate.** Lore is used, not rewritten. New lore-bearing products cite their canon source. Nothing becomes CANON without Taylor.
5. **Children.** Iris and Asher material stays private and child-safe. It is never used as marketing without Taylor's explicit say-so.
6. **Platform rules.** Etsy's metaphysical-services policy (readings allowed, outcome promises banned), Kickstarter's no-revenue-share and no-charity rules, AI-use disclosure on marketplaces, FTC rules for affiliate and ad disclosure.
7. **Entity reality.** Selling as `SOLE_PROP` (one seller of record) until the §4 decision on Taylor + Jeanie. The nonprofit is not presented as existing.
8. **Shadow law.** If a round produces more plans than experiments, the next round must *remove* scope.

---

## 6. The Action Brief (what Taylor actually reads)

Every 3rd round, or on request, Claude Code writes it on one screen:
- the current rung on the ladder (from the ledger)
- the 3 live experiments: status against each kill metric
- the **one** next action for Taylor this week, with its time cost
- any decision that only Taylor can make
- ideas killed this cycle, and why

---

## 7. How to run a round

- **Claude Code:** open a session on this repo and paste `PROMPT_CLAUDE.md`.
- **OpenCode:** in the local checkout, run `git fetch origin && git checkout claude/sacred-marketplace-income-67t27a && git pull`, then paste `PROMPT_OPENCODE.md`.
- To stop the loop, write `LOOP: PAUSED` as the last line of `ROUND_LOG.md`.

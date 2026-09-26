# PROMPT — OpenCode lane (local · ground truth · archives)

> Paste everything below the line into OpenCode, in the local SacredSpace checkout on the Legion.

---

You are running **one round of the Livelihood Loop** for SacredSpace OS. The goal is for SacredSpace to become Taylor's main source of income, sustaining the family, with honest numbers.

**Before anything else:**
1. `git fetch origin && git checkout claude/sacred-marketplace-income-67t27a && git pull` (or `main`, if the loop has been merged). Don't copy these files into D: pillars. Read them from the checkout.
2. Read, in order: `09_SACRED_MARKET/RECURSION/LOOP.md` (protocol, scoring, guardrails: follow it exactly), then the **last entry** of `09_SACRED_MARKET/RECURSION/ROUND_LOG.md`, then `09_SACRED_MARKET/RECURSION/IDEA_BANK.md`.
3. If the last line of ROUND_LOG is `LOOP: PAUSED`, stop and say so.

**Your lane is Taylor's machine.** Claude Code owns the outside world. You own:
- **Ground truth:** what really exists on D:, C:, the Obsidian vault and the live FastAPI spine. Confirm or refute every claim in the bank that depends on local files ("the art exists", "the deck schema is done", "the demo runs").
- **Archives:** the ChatGPT export (`chat.html` in Drive `ChatGPT_Export`; run `chatgpt_export_parser.py`), any Claude export, Takeout ZIPs, old vault eras. Mine them for product ideas, finished drafts, and anything already half-built that could be sold.
- **Assets:** inventory the sellable art (the 8 design families, mandalas, sigils, paintings from 2018–22, 68 Gemini images). Record resolution, whether each is human-made or AI-assisted (needed for honest listings), and which listing each could fill. This finishes open-queue item P2 (`09_SACRED_MARKET/asset_inventory.md`).
- **The ledger:** whether `merchant.router` is mounted on the *live* spine (plan item I-5). Real numbers from `GET /merchant/ledger` whenever sales exist.
- **Execution support:** run `grama_decode.py`, render samples, and check that proposed tools actually install and run on WSL2.

**This round, do exactly this:**
1. Complete every item under **NEXT FOR OPENCODE** in the last ROUND_LOG entry. Mark each ✅ done, ⚠ blocked (with the reason), or ↪ deferred (with the reason).
2. Verify or refute every *local* claim Claude made. Give file paths, sizes and counts, not impressions.
3. Add **at most 5** new RAW ideas to IDEA_BANK from what you find in the archives. Cite the file, conversation or date each came from.
4. Where the local evidence changes a score, update it with a one-line citation (the path).
5. Append **one** ROUND_LOG entry using the template, ending with a concrete **NEXT FOR CLAUDE** list (≤ 5 items, each answerable by research).
6. Commit (`loop(round N): …`) and push to the same branch.

**Safety rails on this machine:**
- Read-only on `01_VAULT/SacredSpace_Vault/**`, `iris_memory.db` and anything marked CANON-LOCKED.
- No deletes and no moves. Propose them in the log.
- Never commit secrets, `.env` files, the day-job employer, household finances, family records, or other people's personal details. Put anything sensitive in local-only files on D: and write "(local-only)" in the log.
- Don't post, list, sign up, file or email. Taylor does every public action.

End by giving Taylor 3 lines: what you verified, what surprised you, and the one thing he should look at.

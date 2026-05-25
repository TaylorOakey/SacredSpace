---
title: "State_Governor"
source: "/mnt/d/01_VAULT/SacredSpace_Vault/ARCHIVE/sacredspace_os_2026_docs/06_AGENT_LAYER/legacy_sacredspace_v2/sski/data/imports/expanded/SacredSpace_Vault_Export/vault/SacredSpace/01_DISTILLED/Sacred_Symphony/State_Governor.md"
keyword_count: 9
keywords_found: [budget]
pillar: "01_VAULT"
date_indexed: "2026-05-21"
cashflow_rank: 30
---


# State Governor + Loop Guard

> *Without state guards, the machine turns into a caffeinated squirrel.*

The State Governor is SacredSpace OS's **execution discipline layer**. It prevents the Envoy from looping, re-calling the same tool endlessly, or exhausting its retry budget without escalating.

---

## The Expert Insight on State

State is not just memory. It is the **controlled representation of progress through a task.**

| Concept | What it says |
|---|---|
| Memory | "Here are relevant past facts." |
| **State** | "Here is where we are, what has happened, and what can validly happen next." |

That distinction is where expert agent intuition begins forming.

---

## State Layers in a Multi-Agent System

| Layer | Scope | Description |
|---|---|---|
| Session state | Current run | What is true right now |
| Workflow state | Current graph | Where we are in the pipeline |
| Agent-local state | One agent | Scratchpad / working memory |
| Shared state | All agents | Artifacts others can build on |
| Persistent memory | Cross-session | Things that survive restarts |

**Danger:** If you blur these layers, one agent's temporary scratchpad starts masquerading as canon. That's how digital folklore gets born.

---

## Common Failure Modes

| Failure | Cause | State Governor Fix |
|---|---|---|
| Infinite loop | Same tool called with same input | `LoopDetected` exception after `max_identical_calls` |
| Stale context | Old state not cleared | Phase transitions reset relevant flags |
| Budget exhaustion | Too many retries | `RetryBudgetExceeded` halts and escalates |
| Conflicting state | Two agents write to same key | Shared state requires ledger receipts |

---

## Source File

**Path:** `~/SacredSpace/sacredspace_os/state_governor.py`

```python
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    tool_name: str
    tool_input_fingerprint: str


@dataclass
class AgentState:
    task_id: str
    current_phase: str
    retry_budget: int = 3
    max_identical_calls: int = 2
    history: list[ToolCall] = field(default_factory=list)
    flags: dict[str, Any] = field(default_factory=dict)


class LoopDetected(Exception):
    pass


class RetryBudgetExceeded(Exception):
    pass


class StateGovernor:
    def __init__(self, state: AgentState):
        self.state = state

    def register_tool_call(self, tool_name: str,
                           tool_input_fingerprint: str) -> None:
        """Record a tool call. Raise LoopDetected if it repeats too often."""
        self.state.history.append(
            ToolCall(tool_name=tool_name,
                     tool_input_fingerprint=tool_input_fingerprint)
        )
        counts = Counter(
            (c.tool_name, c.tool_input_fingerprint)
            for c in self.state.history
        )
        if counts[(tool_name, tool_input_fingerprint)] > self.state.max_identical_calls:
            raise LoopDetected(
                f"Loop guard triggered: repeated {tool_name} with identical input."
            )

    def consume_retry(self) -> None:
        """Consume one retry. Raise RetryBudgetExceeded when empty."""
        self.state.retry_budget -= 1
        if self.state.retry_budget < 0:
            raise RetryBudgetExceeded("Retry budget exceeded.")

    def advance_phase(self, next_phase: str) -> None:
        self.state.current_phase = next_phase

    def set_flag(self, key: str, value: Any) -> None:
        self.state.flags[key] = value
```

---

## Usage Example

```python
from sacredspace_os.state_governor import AgentState, StateGovernor, LoopDetected

state = AgentState(task_id="T-001", current_phase="boot")
gov = StateGovernor(state)

# Normal tool call
gov.register_tool_call("web_search", "hash_of_query_abc")

# Same call repeated — raises LoopDetected on third occurrence
try:
    gov.register_tool_call("web_search", "hash_of_query_abc")
    gov.register_tool_call("web_search", "hash_of_query_abc")
except LoopDetected as e:
    print(f"Circuit breaker: {e}")
    # → escalate to Council, log to Ledger, halt task
```

---

## Integration with Council Ledger

When `LoopDetected` or `RetryBudgetExceeded` fires, the pattern is:

```python
except LoopDetected as exc:
    ledger.add_audit(
        scope="state_governor",
        severity="warning",
        summary=str(exc),
        details=f"task_id={state.task_id} phase={state.current_phase}"
    )
    ledger.transition_task(task_id, "halted", changed_by="governor",
                           reason="Loop guard triggered")
```

---

*Related: [[Council_Ledger]] · [[Sandbox_Broker]] · [[SacredSpace_OS_Architecture_Manifesto]]*

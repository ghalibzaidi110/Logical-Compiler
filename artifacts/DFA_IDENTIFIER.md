# Artifact 1: DFA for IDENTIFIER Recognition
## Hand-Drawn Diagram Reference

**Purpose:** Deterministic Finite Automaton for recognizing identifiers  
**Pattern:** `[a-zA-Z_][a-zA-Z0-9_]*`  
**Language:** Logic Gate Architect DSL

---

## DFA State Diagram

```
                    [a-z, A-Z, _]
                    ┌─────────────┐
                    │             │
                    ▼             │
        ┌─────────(q0)──────────┐  │
        │      START STATE      │  │
        └───────────┬───────────┘  │
                    │              │
                    │ [a-z, A-Z, _]│
                    │              │
                    ▼              │
        ┌─────────(q1)──────────┐  │
        │   ACCEPTING STATE     │  │
        │   (Valid Identifier)  │◄─┘
        └───────────┬───────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        │ [a-z, A-Z, 0-9, _]    │
        │           │           │
        │           ▼           │
        │   ┌─────(q1)─────┐   │
        │   │   (LOOP)     │   │
        │   └──────┬───────┘   │
        │          │           │
        │          │           │
        └──────────┴───────────┘
                    │
                    │ [other characters]
                    │
                    ▼
        ┌─────────(q2)──────────┐
        │    DEAD STATE         │
        │    (Reject)           │
        └───────────────────────┘
```

## State Descriptions

| State | Name | Description | Accepting? |
|-------|------|-------------|------------|
| q0 | Start | Initial state, waiting for first character | No |
| q1 | Accepting | Valid identifier formed, can continue | **Yes** |
| q2 | Dead | Invalid input, reject | No |

## Transition Table

| Current State | Input Character | Next State | Notes |
|---------------|------------------|------------|-------|
| q0 | `[a-z, A-Z, _]` | q1 | First character must be letter or underscore |
| q0 | `[0-9, other]` | q2 | Cannot start with digit or special char |
| q1 | `[a-z, A-Z, 0-9, _]` | q1 | Continue building identifier (loop) |
| q1 | `[other]` | q2 | End of identifier, reject if invalid char |
| q2 | `[any]` | q2 | Dead state, stay here (loop) |

## Examples

### Valid Identifiers (Accept)
- `A` → q0 → q1 ✓
- `Sum` → q0 → q1 → q1 → q1 ✓
- `Carry_Out` → q0 → q1 → ... → q1 ✓
- `_temp` → q0 → q1 → q1 → q1 → q1 ✓
- `Wire_123` → q0 → q1 → ... → q1 ✓

### Invalid Identifiers (Reject)
- `123Wire` → q0 → q2 ✗ (starts with digit)
- `A@B` → q0 → q1 → q2 ✗ (contains @)
- `Sum-Carry` → q0 → q1 → ... → q2 ✗ (contains -)

## Hand-Drawing Instructions

1. **Draw three circles** representing states q0, q1, q2
2. **Label q0** as "START" and mark it with an incoming arrow
3. **Label q1** as "ACCEPT" and draw a double circle around it
4. **Label q2** as "DEAD" 
5. **Draw transitions:**
   - q0 → q1: Label with `[a-z, A-Z, _]`
   - q1 → q1: Draw a self-loop, label with `[a-z, A-Z, 0-9, _]`
   - q0 → q2: Label with `[0-9, other]`
   - q1 → q2: Label with `[other]`
   - q2 → q2: Draw a self-loop, label with `[any]`

## Formal Definition

**DFA = (Q, Σ, δ, q0, F)**

- **Q** = {q0, q1, q2} (set of states)
- **Σ** = {a-z, A-Z, 0-9, _, other} (alphabet)
- **δ** = transition function (see table above)
- **q0** = q0 (start state)
- **F** = {q1} (accepting states)

---

**Note:** This is a reference for hand-drawing. Please create a hand-drawn version on paper, scan it, and save as `DFA_IDENTIFIER.pdf`


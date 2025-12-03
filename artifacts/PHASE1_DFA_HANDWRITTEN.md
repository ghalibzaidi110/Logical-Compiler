# Phase 1: Handwritten DFA Diagram
## Lexical Analysis - Identifier Recognition

**REQUIREMENT:** Hand-drawn DFA diagram for IDENTIFIER token recognition

**Pattern:** `[a-zA-Z_][a-zA-Z0-9_]*`

---

## Instructions for Hand-Drawing

### Step 1: Draw States
Draw three circles/boxes representing:
- **State q0** (Start State) - Label as "START"
- **State q1** (Accepting State) - Draw DOUBLE circle, label as "ACCEPT"
- **State q2** (Dead State) - Label as "DEAD"

### Step 2: Draw Transitions

**From q0 (Start):**
- Draw arrow: q0 → q1, label: `[a-z, A-Z, _]` (letters or underscore)
- Draw arrow: q0 → q2, label: `[0-9, other]` (digits or other chars)

**From q1 (Accepting):**
- Draw self-loop on q1, label: `[a-z, A-Z, 0-9, _]` (any alphanumeric or underscore)
- Draw arrow: q1 → q2, label: `[other]` (any other character)

**From q2 (Dead):**
- Draw self-loop on q2, label: `[any]` (all characters)

### Step 3: Mark Start State
- Draw an incoming arrow (no source) pointing to q0
- Label it "START"

### Step 4: Mark Accepting State
- q1 should have a DOUBLE circle (or thick border)
- Label it "ACCEPT" or "FINAL"

---

## Example Visual Layout

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
        │   ACCEPTING STATE      │◄─┘
        │   (Double Circle)      │
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
        │          │ [other]   │
        │          │           │
        └──────────┴───────────┘
                    │
                    ▼
        ┌─────────(q2)──────────┐
        │    DEAD STATE         │
        │    (Self-loop)        │
        └───────────────────────┘
```

---

## What to Submit

1. **Hand-draw this DFA on paper**
2. **Label all states clearly**
3. **Label all transitions with character classes**
4. **Mark start state with incoming arrow**
5. **Mark accepting state with double circle**
6. **Scan or photograph your drawing**
7. **Save as PDF:** `PHASE1_DFA.pdf`

---

## State Descriptions

| State | Name | Description | Accepting? |
|-------|------|-------------|------------|
| q0 | Start | Initial state, waiting for first character | No |
| q1 | Accepting | Valid identifier formed, can continue | **Yes** |
| q2 | Dead | Invalid input, reject | No |

---

## Transition Rules

| Current State | Input | Next State | Notes |
|---------------|-------|------------|-------|
| q0 | `[a-zA-Z_]` | q1 | First char must be letter/underscore |
| q0 | `[0-9, other]` | q2 | Cannot start with digit |
| q1 | `[a-zA-Z0-9_]` | q1 | Continue building identifier |
| q1 | `[other]` | q2 | End of identifier |
| q2 | `[any]` | q2 | Dead state (loop) |

---

**IMPORTANT:** This must be HAND-DRAWN on paper, then scanned/photographed as a PDF file.


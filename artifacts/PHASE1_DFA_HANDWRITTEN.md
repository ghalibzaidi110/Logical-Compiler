# Phase 1: Handwritten DFA Diagram
## Lexical Analysis - Identifier Recognition

**REQUIREMENT:** Hand-drawn DFA diagram for IDENTIFIER token recognition

**Pattern:** `[a-zA-Z_][a-zA-Z0-9_]*`

**Purpose:** This DFA recognizes valid identifiers in the Logic Gate Architect language. An identifier must start with a letter or underscore, followed by zero or more letters, digits, or underscores.

---

## Complete Step-by-Step Instructions

### Materials Needed
- Clean white paper (A4 or letter size)
- Dark pen or marker (black or blue, 0.5mm or thicker)
- Ruler (optional, for straight lines)
- Eraser (optional, for corrections)

### Step 1: Draw the Three States

Draw three circles or rounded boxes, spaced evenly across the paper:

**State q0 (Start State):**
- Draw a circle/box in the upper left area
- Label it: **q0**
- Write "START" below or inside
- This is where the DFA begins

**State q1 (Accepting State):**
- Draw a circle/box in the center area
- Draw a SECOND circle around it (double circle) - this marks it as accepting
- Label it: **q1**
- Write "ACCEPT" or "FINAL" below or inside
- This is where valid identifiers are recognized

**State q2 (Dead State):**
- Draw a circle/box in the lower right area
- Label it: **q2**
- Write "DEAD" or "REJECT" below or inside
- This is where invalid inputs lead

### Step 2: Draw the Start Arrow

- Draw an arrow with NO starting point (just an arrowhead)
- Point it toward q0
- Label it "START" or leave unlabeled
- This indicates q0 is the initial state

### Step 3: Draw Transitions from q0

**Transition 1: q0 → q1**
- Draw an arrow from q0 to q1
- Label the arrow: `[a-z, A-Z, _]`
- This means: "If the first character is a lowercase letter, uppercase letter, or underscore, go to q1"
- Write a note: "First char must be letter or underscore"

**Transition 2: q0 → q2**
- Draw an arrow from q0 to q2
- Label the arrow: `[0-9, other]`
- This means: "If the first character is a digit or any other character, go to q2 (reject)"
- Write a note: "Cannot start with digit"

### Step 4: Draw Transitions from q1 (Accepting State)

**Self-Loop on q1:**
- Draw a curved arrow that starts and ends at q1 (a loop)
- Label the loop: `[a-z, A-Z, 0-9, _]`
- This means: "If we're in q1 and see another letter, digit, or underscore, stay in q1"
- Write a note: "Continue building identifier"

**Transition: q1 → q2**
- Draw an arrow from q1 to q2
- Label the arrow: `[other]`
- This means: "If we see any character that's not a letter, digit, or underscore, go to q2 (reject)"
- Write a note: "End of identifier or invalid char"

### Step 5: Draw Transitions from q2 (Dead State)

**Self-Loop on q2:**
- Draw a curved arrow that starts and ends at q2 (a loop)
- Label the loop: `[any]`
- This means: "Once in dead state, stay there no matter what"
- Write a note: "Dead state - always reject"

### Step 6: Add Final Details

- Make sure q1 has a DOUBLE circle (this is critical - it marks the accepting state)
- Make sure all arrows are clearly labeled
- Add a title at the top: "DFA for IDENTIFIER Recognition"
- Add the pattern below the title: `[a-zA-Z_][a-zA-Z0-9_]*`

---

## Complete Visual Layout (Reference)

```
                    [a-z, A-Z, _]
                    ┌─────────────┐
                    │             │
                    ▼             │
        ┌─────────(q0)──────────┐  │
        │      START STATE      │  │
        │      (Initial)        │  │
        └───────────┬───────────┘  │
                    │              │
                    │ [a-z, A-Z, _]│
                    │              │
                    ▼              │
        ┌─────────(q1)──────────┐  │
        │   ACCEPTING STATE      │◄─┘
        │   (Double Circle)      │
        │   Valid Identifier     │
        └───────────┬───────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        │ [a-z, A-Z, 0-9, _]    │
        │    (Self-loop)        │
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
        │    Always Reject      │
        └───────────────────────┘
                [any]
```

---

## Detailed State Descriptions

| State | Name | Description | Accepting? | When We're Here |
|-------|------|-------------|------------|-----------------|
| q0 | Start | Initial state, waiting for first character | No | Before reading any input |
| q1 | Accepting | Valid identifier formed, can continue | **Yes** | After reading valid identifier characters |
| q2 | Dead | Invalid input, reject | No | When invalid character encountered |

---

## Complete Transition Table

| Current State | Input Character | Next State | Explanation |
|---------------|----------------|------------|-------------|
| q0 | `a-z` (lowercase letter) | q1 | Valid start, go to accepting state |
| q0 | `A-Z` (uppercase letter) | q1 | Valid start, go to accepting state |
| q0 | `_` (underscore) | q1 | Valid start, go to accepting state |
| q0 | `0-9` (digit) | q2 | Cannot start with digit, reject |
| q0 | Any other character | q2 | Invalid first character, reject |
| q1 | `a-z` (lowercase letter) | q1 | Continue building identifier (loop) |
| q1 | `A-Z` (uppercase letter) | q1 | Continue building identifier (loop) |
| q1 | `0-9` (digit) | q1 | Continue building identifier (loop) |
| q1 | `_` (underscore) | q1 | Continue building identifier (loop) |
| q1 | Any other character | q2 | End of identifier or invalid char |
| q2 | Any character | q2 | Dead state, always reject (loop) |

---

## Examples: How the DFA Works

### Example 1: Valid Identifier "Sum"
1. Start at q0
2. Read 'S' (uppercase letter) → Go to q1 (accepting)
3. Read 'u' (lowercase letter) → Stay in q1 (loop)
4. Read 'm' (lowercase letter) → Stay in q1 (loop)
5. Read space or end of input → Go to q2
6. **Result:** Identifier "Sum" was accepted (we passed through q1)

### Example 2: Valid Identifier "Carry_Out"
1. Start at q0
2. Read 'C' → Go to q1
3. Read 'a' → Stay in q1
4. Read 'r' → Stay in q1
5. Read 'r' → Stay in q1
6. Read 'y' → Stay in q1
7. Read '_' → Stay in q1
8. Read 'O' → Stay in q1
9. Read 'u' → Stay in q1
10. Read 't' → Stay in q1
11. Read space → Go to q2
12. **Result:** Identifier "Carry_Out" was accepted

### Example 3: Invalid Identifier "123Wire"
1. Start at q0
2. Read '1' (digit) → Go to q2 (dead state)
3. **Result:** Identifier rejected (cannot start with digit)

### Example 4: Invalid Identifier "A@B"
1. Start at q0
2. Read 'A' → Go to q1
3. Read '@' (invalid) → Go to q2
4. **Result:** Identifier rejected (contains invalid character)

---

## Formal DFA Definition

**DFA = (Q, Σ, δ, q0, F)**

Where:
- **Q** = {q0, q1, q2} (set of states)
- **Σ** = {a-z, A-Z, 0-9, _, other} (alphabet - all possible characters)
- **δ** = transition function (see transition table above)
- **q0** = q0 (start state)
- **F** = {q1} (set of accepting states - only q1 accepts)

---

## Drawing Checklist

Before scanning, verify:
- [ ] Three states drawn (q0, q1, q2)
- [ ] q0 is marked as START with incoming arrow
- [ ] q1 has DOUBLE circle (accepting state)
- [ ] q2 is marked as DEAD
- [ ] All transitions drawn with arrows
- [ ] All transitions labeled with character classes
- [ ] Self-loops drawn for q1 and q2
- [ ] Title added: "DFA for IDENTIFIER Recognition"
- [ ] Pattern shown: `[a-zA-Z_][a-zA-Z0-9_]*`
- [ ] Drawing is clear and readable
- [ ] All labels are legible

---

## Scanning Instructions

1. **Use good lighting** - Natural light or bright room light
2. **Place paper flat** - No wrinkles or folds
3. **Use scanner or phone camera:**
   - Scanner: 300 DPI minimum, save as PDF
   - Phone: Use scanning app (like Adobe Scan, CamScanner)
   - Ensure entire diagram is in frame
   - Check that text is readable
4. **Save as:** `PHASE1_DFA.pdf`
5. **Place in:** `artifacts/` directory

---

## Common Mistakes to Avoid

1. **Forgetting double circle on q1** - This is critical!
2. **Missing self-loops** - q1 and q2 both need self-loops
3. **Unclear labels** - Make sure character classes are readable
4. **Missing start arrow** - Must show q0 is the start state
5. **Incorrect transitions** - Double-check the transition table

---

## What Makes a Good DFA Diagram

- **Clear layout** - States well-spaced, not cramped
- **Consistent style** - All states same size, all arrows same style
- **Readable labels** - Text is large enough to read when scanned
- **Professional appearance** - Neat, organized, clean
- **Complete** - All states, transitions, and labels present

---

**IMPORTANT:** This must be HAND-DRAWN on paper, then scanned/photographed as a PDF file. Do NOT use computer drawing tools - it must be physically drawn by hand.

---

## Submission Requirements

- **Format:** PDF file
- **Filename:** `PHASE1_DFA.pdf`
- **Location:** `artifacts/PHASE1_DFA.pdf`
- **Quality:** High resolution, clearly readable
- **Content:** Complete DFA with all states, transitions, and labels

---

**This document contains everything you need to create the handwritten DFA diagram. Follow the instructions step-by-step, and you'll have a complete, professional DFA diagram ready for submission.**

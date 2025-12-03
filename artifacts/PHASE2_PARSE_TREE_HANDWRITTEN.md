# Phase 2: Handwritten Parse Tree
## Syntax Analysis - Parse Tree Derivation

**REQUIREMENT:** Hand-drawn parse tree for at least two sample statements

**Example 1:** `Sum = XOR(A, B);`  
**Example 2:** Complete circuit parse tree

---

## Instructions for Hand-Drawing

### Example 1: Parse Tree for `Sum = XOR(A, B);`

#### Step 1: Draw Root Node
- Draw a box labeled: `<gate>`

#### Step 2: Draw Three Main Branches
From `<gate>`, draw three branches:
- Left branch: `<identifier>` → "Sum"
- Middle branch: `<equals>` → "="
- Right branch: `<gate_expr>`

#### Step 3: Expand `<gate_expr>`
From `<gate_expr>`, draw branches:
- `<gate_type>` → "XOR"
- "(" (terminal)
- `<gate_inputs>`
- ")" (terminal)

#### Step 4: Expand `<gate_inputs>`
From `<gate_inputs>`, draw:
- `<identifier>` → "A"
- `<gate_inputs_tail>`

#### Step 5: Expand `<gate_inputs_tail>`
From `<gate_inputs_tail>`, draw:
- `<comma>` → ","
- `<identifier>` → "B"

#### Step 6: Add Semicolon
- Add ";" at the end

---

## Visual Structure for Example 1

```
                    <gate>
                        |
        ┌───────────────┼───────────────┐
        |               |               |
<identifier>        <equals>      <gate_expr>
        |               |               |
      "Sum"             "="       ┌──────┼──────┐
                                 |      |      |
                            <gate_type> (  <gate_inputs>  )
                                 |      |      |
                               "XOR"   (    ┌──┴──┐
                                          |      |
                                    <identifier> <gate_inputs_tail>
                                          |      |
                                        "A"     ┌──┴──┐
                                              |      |
                                        <comma> <identifier>
                                              |      |
                                              ","   "B"
                                                      ;
```

---

## Example 2: Complete Circuit Parse Tree

**Circuit:**
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

### Structure:

```
                        <program>
                            |
        ┌──────────────────┼──────────────────┐
        |                  |                   |
    CIRCUIT          <identifier>          <lbrace>
        |                  |                   |
     "CIRCUIT"          "HalfAdder"            "{"
                                                
                            |
                    ┌───────┴───────┐
                    |               |
            <declarations>      <gates>
                    |               |
            ┌───────┴───────┐       |
            |               |       |
    <declaration>   <declarations>  <gate>
            |               |       |
    INPUT A, B;    OUTPUT Sum, Carry;  Sum = XOR(A, B);
                                            |
                                    <gate> (for Carry)
                                            |
                                    Carry = AND(A, B);
```

---

## What to Submit

1. **Hand-draw parse tree for `Sum = XOR(A, B);` on paper**
2. **Hand-draw complete circuit parse tree on paper**
3. **Label all non-terminals in boxes/circles**
4. **Label all terminals in quotes or circles**
5. **Show clear parent-child relationships**
6. **Scan or photograph your drawings**
7. **Save as PDF:** `PHASE2_PARSE_TREE.pdf`

---

## Drawing Tips

- Use boxes for non-terminals (`<gate>`, `<identifier>`)
- Use circles or quotes for terminals ("Sum", "=", "XOR")
- Draw clear lines connecting parent to children
- Keep tree structure clear and readable
- Label each node clearly

---

## Grammar Rules Used

```
<gate> ::= <identifier> <equals> <gate_expr> <semicolon>
<gate_expr> ::= <gate_type> <lparen> <gate_inputs> <rparen>
<gate_inputs> ::= <identifier> <gate_inputs_tail>
<gate_inputs_tail> ::= <comma> <identifier> | ε
```

---

**IMPORTANT:** This must be HAND-DRAWN on paper, then scanned/photographed as a PDF file.


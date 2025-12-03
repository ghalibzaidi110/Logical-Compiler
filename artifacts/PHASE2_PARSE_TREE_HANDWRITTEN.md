# Phase 2: Handwritten Parse Tree
## Syntax Analysis - Parse Tree Derivation

**REQUIREMENT:** Hand-drawn parse tree for at least two sample statements

**Purpose:** A parse tree shows how the parser breaks down source code according to grammar rules. It demonstrates the hierarchical structure of the program.

---

## Complete Grammar Rules Reference

Before drawing, understand these grammar rules:

```
<program> ::= CIRCUIT <identifier> <lbrace> <declarations> <gates> <rbrace>

<declarations> ::= <declaration> <declarations> | <declaration> | ε

<declaration> ::= <declaration_keyword> <identifier_list> <semicolon>

<declaration_keyword> ::= INPUT | OUTPUT | WIRE

<identifier_list> ::= <identifier> <identifier_list_tail>

<identifier_list_tail> ::= <comma> <identifier> <identifier_list_tail> | ε

<gates> ::= <gate> <gates> | <gate> | ε

<gate> ::= <identifier> <equals> <gate_expr> <semicolon>

<gate_expr> ::= <gate_type> <lparen> <gate_inputs> <rparen>

<gate_type> ::= AND | OR | XOR | NAND | NOR | NOT

<gate_inputs> ::= <identifier> <gate_inputs_tail>

<gate_inputs_tail> ::= <comma> <identifier> <gate_inputs_tail> | ε
```

---

## Example 1: Parse Tree for `Sum = XOR(A, B);`

### Complete Step-by-Step Instructions

#### Step 1: Draw Root Node
- Draw a rectangular box at the top center of your paper
- Label it: **`<gate>`**
- This is the root of the parse tree
- This represents the entire gate assignment statement

#### Step 2: Draw Three Main Branches from Root
From the `<gate>` box, draw three branches downward:

**Left Branch:**
- Draw a line down and left
- At the end, draw a box labeled: **`<identifier>`**
- Below that, draw a circle or write in quotes: **"Sum"**
- Connect: `<gate>` → `<identifier>` → "Sum"

**Middle Branch:**
- Draw a line straight down
- At the end, draw a circle or write: **"="**
- This is a terminal (actual token from source code)
- Connect: `<gate>` → "="

**Right Branch:**
- Draw a line down and right
- At the end, draw a box labeled: **`<gate_expr>`**
- This represents the gate expression (XOR(A, B))
- Connect: `<gate>` → `<gate_expr>`

#### Step 3: Expand `<gate_expr>`
From the `<gate_expr>` box, draw four branches:

**Branch 1:**
- Draw left branch
- Box labeled: **`<gate_type>`**
- Below that, circle: **"XOR"**
- Connect: `<gate_expr>` → `<gate_type>` → "XOR"

**Branch 2:**
- Draw second branch
- Circle: **"("**
- This is the left parenthesis terminal
- Connect: `<gate_expr>` → "("

**Branch 3:**
- Draw third branch
- Box labeled: **`<gate_inputs>`**
- This will contain the input list (A, B)
- Connect: `<gate_expr>` → `<gate_inputs>`

**Branch 4:**
- Draw right branch
- Circle: **")"**
- This is the right parenthesis terminal
- Connect: `<gate_expr>` → ")"

#### Step 4: Expand `<gate_inputs>`
From the `<gate_inputs>` box, draw two branches:

**Branch 1:**
- Draw left branch
- Box labeled: **`<identifier>`**
- Below that, circle: **"A"**
- Connect: `<gate_inputs>` → `<identifier>` → "A"

**Branch 2:**
- Draw right branch
- Box labeled: **`<gate_inputs_tail>`**
- This handles the comma and second identifier
- Connect: `<gate_inputs>` → `<gate_inputs_tail>`

#### Step 5: Expand `<gate_inputs_tail>`
From the `<gate_inputs_tail>` box, draw two branches:

**Branch 1:**
- Draw left branch
- Box labeled: **`<comma>`**
- Below that, circle: **","**
- Connect: `<gate_inputs_tail>` → `<comma>` → ","

**Branch 2:**
- Draw right branch
- Box labeled: **`<identifier>`**
- Below that, circle: **"B"**
- Connect: `<gate_inputs_tail>` → `<identifier>` → "B"

#### Step 6: Add Semicolon
- At the very end (after the closing parenthesis), add:
- Circle: **";"**
- This completes the statement

### Complete Visual Structure

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
                                                      )
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

### Step-by-Step Instructions for Complete Circuit

#### Step 1: Draw Root Node
- Draw a large box at the top
- Label it: **`<program>`**
- This represents the entire program

#### Step 2: Draw Main Program Structure
From `<program>`, draw five branches:

**Branch 1:**
- Box or circle: **"CIRCUIT"** (keyword terminal)

**Branch 2:**
- Box: **`<identifier>`**
- Below: **"HalfAdder"**

**Branch 3:**
- Circle: **"{"** (left brace terminal)

**Branch 4:**
- Box: **`<declarations>`**
- This will contain all INPUT/OUTPUT/WIRE declarations

**Branch 5:**
- Box: **`<gates>`**
- This will contain all gate assignments

**Branch 6:**
- Circle: **"}"** (right brace terminal)

#### Step 3: Expand `<declarations>`
From `<declarations>`, draw two branches:

**Branch 1:**
- Box: **`<declaration>`** (first declaration: INPUT A, B;)

**Branch 2:**
- Box: **`<declarations>`** (remaining declarations: OUTPUT Sum, Carry;)

#### Step 4: Expand First `<declaration>` (INPUT)
From the first `<declaration>`, draw three branches:

**Branch 1:**
- Circle: **"INPUT"** (keyword)

**Branch 2:**
- Box: **`<identifier_list>`**
- Expand to show: `<identifier>` → "A", then `<identifier_list_tail>` → "," → "B"

**Branch 3:**
- Circle: **";"**

#### Step 5: Expand Second `<declarations>` (OUTPUT)
Similar structure for OUTPUT declaration:
- "OUTPUT"
- `<identifier_list>` → "Sum", ",", "Carry"
- ";"

#### Step 6: Expand `<gates>`
From `<gates>`, draw two branches:

**Branch 1:**
- Box: **`<gate>`** (first gate: Sum = XOR(A, B);)
- Expand this using the structure from Example 1

**Branch 2:**
- Box: **`<gates>`** (remaining gates: Carry = AND(A, B);)
- Expand to show the second gate

### Complete Visual Structure

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
                                    <gates>
                                            |
                                    <gate>
                                            |
                                    Carry = AND(A, B);
```

---

## Detailed Drawing Guidelines

### Node Types

**Non-Terminals (Grammar Rules):**
- Draw as **rectangular boxes**
- Examples: `<gate>`, `<identifier>`, `<gate_expr>`
- These represent grammar rules that can be expanded

**Terminals (Actual Tokens):**
- Draw as **circles** or **quoted text**
- Examples: "Sum", "=", "XOR", "(", "A", ",", "B", ")"
- These are actual tokens from the source code

### Drawing Style

1. **Use clear lines** - Draw straight lines connecting parent to children
2. **Space evenly** - Give enough space between nodes
3. **Label clearly** - Make sure all labels are readable
4. **Consistent style** - Use same style for all non-terminals, same for all terminals
5. **Top-down structure** - Root at top, terminals at bottom

### Layout Tips

- **Start at top center** - Place root node at top
- **Branch downward** - All children below parent
- **Left to right** - Order children left to right as they appear in source
- **Avoid crossing lines** - If possible, arrange to minimize line crossings
- **Use paper efficiently** - Don't make it too small or too cramped

---

## Example 3: Parse Tree for Declaration

**Statement:** `INPUT A, B;`

```
        <declaration>
            |
    ┌───────┼───────┐
    |       |       |
<declaration_keyword> <identifier_list> <semicolon>
    |       |       |
  "INPUT"   |      ";"
            |
    ┌───────┼───────┐
    |       |       |
<identifier> <identifier_list_tail>
    |       |
   "A"      |
            |
    ┌───────┼───────┐
    |       |       |
 <comma> <identifier>
    |       |
   ","    "B"
```

---

## Example 4: Parse Tree for NOT Gate

**Statement:** `X = NOT(A);`

```
                    <gate>
                        |
        ┌───────────────┼───────────────┐
        |               |               |
<identifier>        <equals>      <gate_expr>
        |               |               |
       "X"              "="       ┌──────┼──────┐
                                 |      |      |
                            <gate_type> (  <gate_inputs>  )
                                 |      |      |
                               "NOT"   (    ┌──┴──┐
                                          |      |
                                    <identifier> <gate_inputs_tail>
                                          |      |
                                        "A"     ε
                                                      )
                                                      ;
```

Note: `<gate_inputs_tail>` expands to ε (empty) since there's only one input.

---

## Common Mistakes to Avoid

1. **Missing terminals** - Don't forget actual tokens like "=", "(", ",", ")"
2. **Wrong node types** - Non-terminals in boxes, terminals in circles
3. **Incorrect expansion** - Follow grammar rules exactly
4. **Missing semicolon** - Always include ";" at the end of gates
5. **Unclear structure** - Make parent-child relationships obvious

---

## Drawing Checklist

Before scanning, verify:
- [ ] Root node is `<gate>` or `<program>`
- [ ] All non-terminals are in boxes
- [ ] All terminals are in circles or quotes
- [ ] All grammar rules are correctly expanded
- [ ] All actual tokens from source are present
- [ ] Tree structure is clear and readable
- [ ] Lines connect parent to children clearly
- [ ] Labels are legible
- [ ] At least 2 parse trees drawn (one statement, one complete circuit)

---

## Scanning Instructions

1. **Use large paper** - A4 or letter size minimum
2. **Draw clearly** - Use dark pen, make nodes large enough
3. **Good lighting** - Ensure diagram is well-lit when scanning
4. **Flat surface** - No wrinkles or folds
5. **Scan at 300 DPI** - Or use phone scanning app
6. **Save as:** `PHASE2_PARSE_TREE.pdf`
7. **Place in:** `artifacts/` directory

---

## What Makes a Good Parse Tree

- **Complete** - Shows full derivation from root to terminals
- **Accurate** - Follows grammar rules correctly
- **Clear** - Easy to read and understand
- **Professional** - Neat, organized, well-labeled
- **Comprehensive** - Shows both simple and complex examples

---

## Additional Examples to Practice

### Practice Example 1: `Z = AND(A, B);`
Draw the parse tree following the same structure as Example 1, but with:
- Output: "Z"
- Gate type: "AND"
- Inputs: "A", "B"

### Practice Example 2: `temp = OR(X, Y);`
Same structure, different gate type.

### Practice Example 3: Complete Full Adder Circuit
```
CIRCUIT FullAdder {
  INPUT A, B, Cin;
  OUTPUT Sum, Cout;
  WIRE xor1, and1, and2;
  xor1 = XOR(A, B);
  Sum = XOR(xor1, Cin);
  and1 = AND(A, B);
  and2 = AND(xor1, Cin);
  Cout = OR(and1, and2);
}
```

This will have a more complex parse tree with multiple declarations and gates.

---

## Understanding Parse Trees

**What a parse tree shows:**
- How the parser breaks down source code
- Which grammar rules are applied
- The hierarchical structure of the program
- How terminals (tokens) relate to non-terminals (grammar rules)

**Why it's important:**
- Demonstrates understanding of syntax analysis
- Shows how grammar rules are applied
- Visual representation of program structure
- Required artifact for compiler project

---

**IMPORTANT:** This must be HAND-DRAWN on paper, then scanned/photographed as a PDF file. Draw at least two parse trees: one for a single statement and one for a complete circuit.

---

## Submission Requirements

- **Format:** PDF file
- **Filename:** `PHASE2_PARSE_TREE.pdf`
- **Location:** `artifacts/PHASE2_PARSE_TREE.pdf`
- **Content:** At least 2 parse trees (one statement, one complete circuit)
- **Quality:** High resolution, clearly readable

---

**This document contains everything you need to create handwritten parse trees. Follow the step-by-step instructions, and you'll have complete, professional parse trees ready for submission.**

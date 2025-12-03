# Phase 3: Handwritten Symbol Table
## Semantic Analysis - Symbol Table Example

**REQUIREMENT:** Hand-drawn or formatted symbol table with scope example

**Circuit:** Half Adder
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

---

## Instructions for Hand-Drawing/Creating

### Option 1: Hand-Drawn Table
Draw a table on paper with the following structure:

### Option 2: Formatted Table (Can be typed)
Create a well-formatted table

---

## Symbol Table Structure

### Table Format:

| Identifier | Category | Defined | Source Gate | Used By | Line |
|------------|----------|--------|-------------|---------|------|
| A | INPUT | Yes | None | Sum, Carry | 2 |
| B | INPUT | Yes | None | Sum, Carry | 2 |
| Sum | OUTPUT | Yes | XOR(A, B) | None | 3, 4 |
| Carry | OUTPUT | Yes | AND(A, B) | None | 3, 5 |

---

## Detailed Symbol Table (Extended Format)

### Symbol: A
- **Category:** INPUT
- **Type:** Boolean (implicit)
- **Defined:** Yes (primary input)
- **Source:** None
- **Used By:** ["Sum", "Carry"]
- **Scope:** Global (circuit level)
- **Line:** 2

### Symbol: B
- **Category:** INPUT
- **Type:** Boolean (implicit)
- **Defined:** Yes (primary input)
- **Source:** None
- **Used By:** ["Sum", "Carry"]
- **Scope:** Global (circuit level)
- **Line:** 2

### Symbol: Sum
- **Category:** OUTPUT
- **Type:** Boolean (implicit)
- **Defined:** Yes
- **Source:** Gate(output="Sum", type="XOR", inputs=["A", "B"])
- **Used By:** [] (output, not used by other gates)
- **Scope:** Global (circuit level)
- **Line:** 3 (declared), 4 (defined)

### Symbol: Carry
- **Category:** OUTPUT
- **Type:** Boolean (implicit)
- **Defined:** Yes
- **Source:** Gate(output="Carry", type="AND", inputs=["A", "B"])
- **Used By:** [] (output, not used by other gates)
- **Scope:** Global (circuit level)
- **Line:** 3 (declared), 5 (defined)

---

## Alternative: More Complex Example (Full Adder)

**Circuit:**
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

### Symbol Table:

| Identifier | Category | Defined | Source | Used By |
|------------|----------|---------|--------|---------|
| A | INPUT | Yes | None | xor1, and1 |
| B | INPUT | Yes | None | xor1, and1 |
| Cin | INPUT | Yes | None | Sum, and2 |
| Sum | OUTPUT | Yes | XOR(xor1, Cin) | None |
| Cout | OUTPUT | Yes | OR(and1, and2) | None |
| xor1 | WIRE | Yes | XOR(A, B) | Sum, and2 |
| and1 | WIRE | Yes | AND(A, B) | Cout |
| and2 | WIRE | Yes | AND(xor1, Cin) | Cout |

---

## What to Submit

1. **Create symbol table** (hand-drawn or typed/formatted)
2. **Include all required columns:** Identifier, Category, Defined, Source, Used By
3. **Show scope information** (all symbols are global in this language)
4. **Use clear formatting** (table or structured list)
5. **Scan or save as PDF:** `PHASE3_SYMBOL_TABLE.pdf`

---

## Drawing/Creating Tips

- Use a clear table format
- Align columns properly
- Use checkmarks (✓) for "Defined: Yes"
- Use dashes (-) or "None" for empty fields
- List dependencies clearly in "Used By" column
- Include line numbers if space permits
- Make it readable and professional

---

## Required Information

Each symbol entry must show:
1. **Identifier name**
2. **Category** (INPUT, OUTPUT, or WIRE)
3. **Defined status** (Yes/No)
4. **Source gate** (if applicable)
5. **Used by** (list of gates that use this symbol)
6. **Scope** (global in this language)

---

**IMPORTANT:** This can be hand-drawn OR typed/formatted, then saved as a PDF file.


# Phase 3: Handwritten Symbol Table
## Semantic Analysis - Symbol Table Example

**REQUIREMENT:** Hand-drawn or formatted symbol table with scope example

**Purpose:** The symbol table tracks all identifiers in the program, their categories (INPUT, OUTPUT, WIRE), whether they're defined, their source gates, and which gates use them. This is essential for semantic analysis.

---

## Complete Instructions

### Option 1: Hand-Drawn Table (Recommended for Authenticity)

#### Materials Needed
- Clean white paper (A4 or letter size)
- Ruler (for straight lines)
- Dark pen (black or blue)
- Optional: Colored pens for highlighting

#### Step 1: Draw Table Structure

**Draw a table with 6 columns:**

1. **Identifier** - Name of the symbol
2. **Category** - INPUT, OUTPUT, or WIRE
3. **Defined** - Yes or No
4. **Source Gate** - Which gate produces this (if any)
5. **Used By** - List of gates that use this symbol
6. **Line** - Line number(s) where declared/used

**Table should have:**
- Header row (bold or underlined)
- One row for each identifier
- Clear column separators
- Enough space to write clearly

#### Step 2: Fill in Data

Follow the examples below to fill in each row.

---

## Example 1: Half Adder Symbol Table

**Circuit:**
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

### Complete Symbol Table

| Identifier | Category | Defined | Source Gate | Used By | Line |
|------------|----------|--------|-------------|---------|------|
| A | INPUT | Yes | None | Sum, Carry | 2 |
| B | INPUT | Yes | None | Sum, Carry | 2 |
| Sum | OUTPUT | Yes | XOR(A, B) | None | 3, 4 |
| Carry | OUTPUT | Yes | AND(A, B) | None | 3, 5 |

### Detailed Explanation of Each Entry

**Symbol: A**
- **Identifier:** A
- **Category:** INPUT (declared as INPUT on line 2)
- **Defined:** Yes (INPUTs are always defined - they come from outside)
- **Source Gate:** None (INPUTs don't have source gates, they're primary inputs)
- **Used By:** Sum, Carry (both gates use A as input)
- **Line:** 2 (declared on line 2, used on lines 4 and 5)
- **Scope:** Global (all symbols in this language are global)

**Symbol: B**
- **Identifier:** B
- **Category:** INPUT (declared as INPUT on line 2)
- **Defined:** Yes (INPUTs are always defined)
- **Source Gate:** None (primary input)
- **Used By:** Sum, Carry (both gates use B as input)
- **Line:** 2 (declared), 4, 5 (used)
- **Scope:** Global

**Symbol: Sum**
- **Identifier:** Sum
- **Category:** OUTPUT (declared as OUTPUT on line 3)
- **Defined:** Yes (assigned a value on line 4: Sum = XOR(A, B))
- **Source Gate:** XOR(A, B) (the gate that produces Sum)
- **Used By:** None (OUTPUTs are not used by other gates - they're final outputs)
- **Line:** 3 (declared), 4 (defined)
- **Scope:** Global

**Symbol: Carry**
- **Identifier:** Carry
- **Category:** OUTPUT (declared as OUTPUT on line 3)
- **Defined:** Yes (assigned a value on line 5: Carry = AND(A, B))
- **Source Gate:** AND(A, B) (the gate that produces Carry)
- **Used By:** None (OUTPUT, not used by other gates)
- **Line:** 3 (declared), 5 (defined)
- **Scope:** Global

---

## Example 2: Full Adder Symbol Table (More Complex)

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

### Complete Symbol Table

| Identifier | Category | Defined | Source Gate | Used By | Line |
|------------|----------|---------|-------------|---------|------|
| A | INPUT | Yes | None | xor1, and1 | 2 |
| B | INPUT | Yes | None | xor1, and1 | 2 |
| Cin | INPUT | Yes | None | Sum, and2 | 2 |
| Sum | OUTPUT | Yes | XOR(xor1, Cin) | None | 3, 6 |
| Cout | OUTPUT | Yes | OR(and1, and2) | None | 3, 9 |
| xor1 | WIRE | Yes | XOR(A, B) | Sum, and2 | 4, 5 |
| and1 | WIRE | Yes | AND(A, B) | Cout | 4, 7 |
| and2 | WIRE | Yes | AND(xor1, Cin) | Cout | 4, 8 |

### Detailed Explanation

**Symbol: A**
- Category: INPUT
- Defined: Yes
- Source: None (primary input)
- Used By: xor1 (line 5), and1 (line 7)
- Line: 2 (declared), 5, 7 (used)

**Symbol: B**
- Category: INPUT
- Defined: Yes
- Source: None
- Used By: xor1 (line 5), and1 (line 7)
- Line: 2 (declared), 5, 7 (used)

**Symbol: Cin**
- Category: INPUT
- Defined: Yes
- Source: None
- Used By: Sum (line 6), and2 (line 8)
- Line: 2 (declared), 6, 8 (used)

**Symbol: Sum**
- Category: OUTPUT
- Defined: Yes
- Source: XOR(xor1, Cin) (line 6)
- Used By: None (it's an output)
- Line: 3 (declared), 6 (defined)

**Symbol: Cout**
- Category: OUTPUT
- Defined: Yes
- Source: OR(and1, and2) (line 9)
- Used By: None
- Line: 3 (declared), 9 (defined)

**Symbol: xor1**
- Category: WIRE (intermediate signal)
- Defined: Yes
- Source: XOR(A, B) (line 5)
- Used By: Sum (line 6), and2 (line 8)
- Line: 4 (declared), 5 (defined), 6, 8 (used)

**Symbol: and1**
- Category: WIRE
- Defined: Yes
- Source: AND(A, B) (line 7)
- Used By: Cout (line 9)
- Line: 4 (declared), 7 (defined), 9 (used)

**Symbol: and2**
- Category: WIRE
- Defined: Yes
- Source: AND(xor1, Cin) (line 8)
- Used By: Cout (line 9)
- Line: 4 (declared), 8 (defined), 9 (used)

---

## Option 2: Typed/Formatted Table (Also Acceptable)

If you prefer to type the table, you can create it in:
- Microsoft Word
- Google Docs
- LaTeX
- Markdown (then convert to PDF)

### Format Guidelines

1. **Use clear borders** - Make columns obvious
2. **Align text** - Left-align identifiers, center-align categories
3. **Use consistent formatting** - Same style throughout
4. **Include all columns** - Don't skip any required information
5. **Make it readable** - Use appropriate font size (11-12pt)

---

## Step-by-Step: How to Build Symbol Table

### Step 1: Collect All Identifiers

Go through the source code and list every identifier:
- From INPUT declarations
- From OUTPUT declarations
- From WIRE declarations
- From gate assignments (outputs and inputs)

### Step 2: Determine Category

For each identifier:
- If declared as INPUT → Category = INPUT
- If declared as OUTPUT → Category = OUTPUT
- If declared as WIRE → Category = WIRE
- If used as gate output but not declared → Category = WIRE (implicit)

### Step 3: Check if Defined

- INPUT: Always defined (Yes)
- OUTPUT: Defined if there's a gate assignment for it (Yes/No)
- WIRE: Defined if there's a gate assignment for it (Yes/No)

### Step 4: Find Source Gate

- INPUT: Source = None
- OUTPUT/WIRE: Source = the gate that assigns to it
- Example: If "Sum = XOR(A, B);" then Source for Sum is "XOR(A, B)"

### Step 5: Find Used By

For each identifier, find all gates that use it as input:
- Go through all gate assignments
- If a gate uses identifier X as input, add that gate's output to X's "Used By" list
- Example: If "Sum = XOR(A, B);" then A and B both have "Sum" in their "Used By" list

### Step 6: Record Line Numbers

- Note where each identifier is declared
- Note where each identifier is used
- Note where each identifier is defined (for outputs/wires)

---

## Drawing Tips

### For Hand-Drawn Tables:

1. **Use ruler** - Draw straight lines for table borders
2. **Plan spacing** - Make columns wide enough for content
3. **Write clearly** - Use legible handwriting
4. **Check completeness** - Ensure all identifiers are included
5. **Double-check** - Verify "Used By" relationships are correct

### Table Layout Suggestions:

```
┌────────────┬──────────┬─────────┬──────────────┬─────────────┬──────┐
│ Identifier │ Category │ Defined │ Source Gate  │ Used By     │ Line │
├────────────┼──────────┼─────────┼──────────────┼─────────────┼──────┤
│ A          │ INPUT    │ Yes     │ None         │ Sum, Carry  │ 2    │
│ B          │ INPUT    │ Yes     │ None         │ Sum, Carry  │ 2    │
│ Sum        │ OUTPUT   │ Yes     │ XOR(A, B)    │ None        │ 3, 4 │
│ Carry      │ OUTPUT   │ Yes     │ AND(A, B)    │ None        │ 3, 5 │
└────────────┴──────────┴─────────┴──────────────┴─────────────┴──────┘
```

---

## Understanding Symbol Table Fields

### Identifier
- The name of the symbol (variable/signal)
- Must be unique within the circuit
- Examples: A, B, Sum, Carry, xor1

### Category
- **INPUT:** Primary input to the circuit (comes from outside)
- **OUTPUT:** Final output of the circuit (goes to outside)
- **WIRE:** Intermediate signal (internal connection)

### Defined
- **Yes:** The symbol has a value/source
- **No:** The symbol is declared but never assigned (error for OUTPUTs)
- INPUTs are always defined
- OUTPUTs must be defined (semantic check)

### Source Gate
- The gate assignment that produces this symbol's value
- **None** for INPUTs (they come from outside)
- **Gate expression** for OUTPUTs and WIREs
- Example: "XOR(A, B)" means this symbol is produced by XOR gate with inputs A and B

### Used By
- List of gate outputs that use this symbol as input
- **None** for OUTPUTs (they're not used by other gates)
- Shows dependency relationships
- Example: If "Sum, Carry" then both Sum and Carry gates use this symbol

### Line
- Line number(s) where the symbol appears
- First number: where declared
- Additional numbers: where used/defined
- Helps with error reporting

### Scope
- In this language, all symbols are **Global** (circuit-level scope)
- No nested scopes or local variables
- Every identifier is visible throughout the entire circuit

---

## Common Patterns

### Pattern 1: Simple Input
```
Identifier: A
Category: INPUT
Defined: Yes
Source: None
Used By: [list of gates]
```

### Pattern 2: Output
```
Identifier: Sum
Category: OUTPUT
Defined: Yes
Source: XOR(A, B)
Used By: None
```

### Pattern 3: Wire (Intermediate)
```
Identifier: xor1
Category: WIRE
Defined: Yes
Source: XOR(A, B)
Used By: [gates that use xor1]
```

---

## Verification Checklist

Before submitting, verify:
- [ ] All identifiers from source code are included
- [ ] Categories are correct (INPUT/OUTPUT/WIRE)
- [ ] All OUTPUTs have Defined = Yes
- [ ] Source gates are correctly identified
- [ ] "Used By" lists are complete and accurate
- [ ] Line numbers are correct
- [ ] Table is clearly formatted
- [ ] All columns are filled
- [ ] No missing information

---

## Example 3: Symbol Table with Error Case

**Circuit with Error:**
```
CIRCUIT Bad {
  INPUT A;
  OUTPUT Z, Y;
  Z = AND(A, A);
  // Y is never assigned!
}
```

### Symbol Table:

| Identifier | Category | Defined | Source Gate | Used By | Line |
|------------|----------|---------|-------------|---------|------|
| A | INPUT | Yes | None | Z | 2 |
| Z | OUTPUT | Yes | AND(A, A) | None | 3, 4 |
| Y | OUTPUT | **No** | None | None | 3 |

**Note:** Y is declared as OUTPUT but never defined. This would be caught by semantic analysis as an error.

---

## Scanning/Creating Instructions

### For Hand-Drawn:
1. Draw table neatly with ruler
2. Fill in all information clearly
3. Use good lighting when scanning
4. Scan at 300 DPI minimum
5. Save as PDF

### For Typed:
1. Create table in word processor
2. Format professionally
3. Export or print to PDF
4. Ensure all information is included

### File Requirements:
- **Format:** PDF
- **Filename:** `PHASE3_SYMBOL_TABLE.pdf`
- **Location:** `artifacts/PHASE3_SYMBOL_TABLE.pdf`
- **Quality:** Clear and readable

---

## What Makes a Good Symbol Table

- **Complete** - All identifiers included
- **Accurate** - All information correct
- **Clear** - Easy to read and understand
- **Professional** - Well-formatted, neat
- **Comprehensive** - Shows all relationships

---

## Additional Notes

### Dependency Tracking
The "Used By" column shows dependencies:
- If A is used by Sum and Carry, then A is a dependency of both
- This helps with:
  - Understanding circuit structure
  - Detecting unused variables
  - Optimizing code

### Scope Information
- All symbols in this language have **global scope**
- No local variables or nested scopes
- Every identifier is visible throughout the circuit
- This simplifies the symbol table structure

### Type Information
- In this language, all values are **Boolean** (0 or 1)
- Type is implicit, not stored in symbol table
- Could be extended to support multi-bit signals

---

**IMPORTANT:** This can be hand-drawn OR typed/formatted, then saved as a PDF file. Either method is acceptable, but hand-drawn may be preferred for authenticity.

---

## Submission Requirements

- **Format:** PDF file
- **Filename:** `PHASE3_SYMBOL_TABLE.pdf`
- **Location:** `artifacts/PHASE3_SYMBOL_TABLE.pdf`
- **Content:** Complete symbol table with all required columns
- **Quality:** Clear, readable, professional

---

**This document contains everything you need to create the symbol table. Follow the examples and instructions, and you'll have a complete, professional symbol table ready for submission.**

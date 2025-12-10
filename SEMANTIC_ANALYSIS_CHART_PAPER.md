# Semantic Analysis - Chart Paper Documentation Guide

## Complete Dry Run for Half Adder Example

**Input Circuit:**
```gate
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

---

## Phase 1: Symbol Table Construction

### Step 1.1: Build Symbol Table from Declarations

**Process:** Scan all declarations and add identifiers to symbol table.

**Table to Draw:**

| Step | Declaration | Identifier | Category | Defined | Source Gate | Used By |
|------|-------------|------------|----------|---------|-------------|---------|
| 1 | INPUT A, B | A | INPUT | Yes | - | - |
| 2 | INPUT A, B | B | INPUT | Yes | - | - |
| 3 | OUTPUT Sum, Carry | Sum | OUTPUT | No | - | - |
| 4 | OUTPUT Sum, Carry | Carry | OUTPUT | No | - | - |

**Symbol Table After Step 1.1:**

| Name | Category | Defined | Source Gate | Used By |
|------|----------|---------|-------------|---------|
| A | INPUT | Yes | - | - |
| B | INPUT | Yes | - | - |
| Sum | OUTPUT | No | - | - |
| Carry | OUTPUT | No | - | - |

**Notes to Write:**
- INPUT identifiers are marked as `defined = Yes` (they are external inputs)
- OUTPUT identifiers are marked as `defined = No` (must be assigned by gates)
- WIRE identifiers would also be `defined = Yes`

---

### Step 1.2: Populate Gate Information

**Process:** Process each gate assignment and update symbol table.

**Gate 1: `Sum = XOR(A, B);`**

| Action | Symbol | Update |
|--------|--------|--------|
| Check output | Sum | Already in table (OUTPUT) |
| Mark as defined | Sum | `defined = Yes` |
| Set source | Sum | `source = Gate(Sum = XOR(A, B))` |
| Track usage | A | Add "Sum" to `used_by` list |
| Track usage | B | Add "Sum" to `used_by` list |

**Gate 2: `Carry = AND(A, B);`**

| Action | Symbol | Update |
|--------|--------|--------|
| Check output | Carry | Already in table (OUTPUT) |
| Mark as defined | Carry | `defined = Yes` |
| Set source | Carry | `source = Gate(Carry = AND(A, B))` |
| Track usage | A | Add "Carry" to `used_by` list |
| Track usage | B | Add "Carry" to `used_by` list |

**Final Symbol Table After Step 1.2:**

| Name | Category | Defined | Source Gate | Used By |
|------|----------|---------|-------------|---------|
| A | INPUT | Yes | - | Sum, Carry |
| B | INPUT | Yes | - | Sum, Carry |
| Sum | OUTPUT | Yes | Gate(Sum = XOR(A, B)) | - |
| Carry | OUTPUT | Yes | Gate(Carry = AND(A, B)) | - |

**Dependency Graph to Draw:**

```
    A ──┐
        ├──→ Sum (XOR)
    B ──┘

    A ──┐
        ├──→ Carry (AND)
    B ──┘
```

**Or as a single graph:**

```
    A ──┬──→ Sum (XOR)
        │
        └──→ Carry (AND)
    
    B ──┬──→ Sum (XOR)
        │
        └──→ Carry (AND)
```

---

## Phase 2: Semantic Checks

### Check 1: Declaration Check

**Rule:** All identifiers used in gates must be declared.

**Process:** For each gate, check all input identifiers.

**Table to Draw:**

| Gate | Input Identifiers | Check | Result |
|------|-------------------|-------|--------|
| Sum = XOR(A, B) | A | A ∈ symbol_table? | ✓ Yes |
| Sum = XOR(A, B) | B | B ∈ symbol_table? | ✓ Yes |
| Carry = AND(A, B) | A | A ∈ symbol_table? | ✓ Yes |
| Carry = AND(A, B) | B | B ∈ symbol_table? | ✓ Yes |

**Result:** ✓ PASSED - All identifiers declared

---

### Check 2: Gate Input Count Validation

**Rule:** Each gate type requires a specific number of inputs.

**Gate Requirements Table:**

| Gate Type | Required Inputs |
|-----------|----------------|
| NOT | 1 |
| AND | 2 |
| OR | 2 |
| XOR | 2 |
| NAND | 2 |
| NOR | 2 |

**Validation Table:**

| Gate | Gate Type | Required | Actual | Check | Result |
|------|-----------|----------|--------|-------|--------|
| Sum = XOR(A, B) | XOR | 2 | 2 | 2 == 2? | ✓ Pass |
| Carry = AND(A, B) | AND | 2 | 2 | 2 == 2? | ✓ Pass |

**Result:** ✓ PASSED - All gates have correct input counts

---

### Check 3: Output Assignment Verification

**Rule:** All OUTPUT identifiers must be assigned a value by at least one gate.

**Table to Draw:**

| OUTPUT Identifier | Assigned? | Source Gate | Check | Result |
|-------------------|-----------|-------------|-------|--------|
| Sum | Yes | Gate(Sum = XOR(A, B)) | defined == Yes? | ✓ Pass |
| Carry | Yes | Gate(Carry = AND(A, B)) | defined == Yes? | ✓ Pass |

**Result:** ✓ PASSED - All OUTPUTs assigned

---

### Check 4: Input Assignment Prevention

**Rule:** INPUT identifiers cannot be assigned to (they are read-only).

**Table to Draw:**

| Gate Output | Category Check | Check | Result |
|-------------|----------------|-------|--------|
| Sum | OUTPUT (not INPUT) | category != INPUT? | ✓ Pass |
| Carry | OUTPUT (not INPUT) | category != INPUT? | ✓ Pass |

**Result:** ✓ PASSED - No INPUT assignments

---

### Check 5: Cycle Detection (DFS Algorithm)

**Rule:** No combinational feedback loops allowed.

**Algorithm:** Depth-First Search (DFS) with recursion stack.

**DFS Traversal Table:**

| Step | Node | Visited | Rec Stack | Check Children | Cycle Found? |
|------|------|---------|-----------|----------------|-------------|
| 1 | A | {A} | {A} | No source gate | No |
| 2 | B | {A, B} | {B} | No source gate | No |
| 3 | Sum | {A, B, Sum} | {Sum} | Check A, B | No |
| 4 | Carry | {A, B, Sum, Carry} | {Carry} | Check A, B | No |

**DFS Tree to Draw:**

```
Start DFS from A:
  A → No source gate → Return (no cycle)

Start DFS from B:
  B → No source gate → Return (no cycle)

Start DFS from Sum:
  Sum → Source: XOR(A, B)
    → Check A: Already visited, no cycle
    → Check B: Already visited, no cycle
    → Return (no cycle)

Start DFS from Carry:
  Carry → Source: AND(A, B)
    → Check A: Already visited, no cycle
    → Check B: Already visited, no cycle
    → Return (no cycle)
```

**Result:** ✓ PASSED - No cycles detected

---

## Complete Semantic Analysis Summary

### Final Symbol Table (Complete)

| Name | Category | Defined | Source Gate | Used By |
|------|----------|---------|-------------|---------|
| A | INPUT | Yes | - | Sum, Carry |
| B | INPUT | Yes | - | Sum, Carry |
| Sum | OUTPUT | Yes | Gate(Sum = XOR(A, B)) | - |
| Carry | OUTPUT | Yes | Gate(Carry = AND(A, B)) | - |

### Semantic Checks Summary

| Check # | Check Name | Status | Details |
|---------|------------|--------|---------|
| 1 | Declaration Check | ✓ PASS | All identifiers declared |
| 2 | Gate Input Count | ✓ PASS | All gates have correct inputs |
| 3 | Output Assignment | ✓ PASS | All OUTPUTs assigned |
| 4 | Input Assignment | ✓ PASS | No INPUT assignments |
| 5 | Cycle Detection | ✓ PASS | No cycles found |

**Overall Result:** ✓ **SEMANTIC ANALYSIS PASSED**

**Errors Found:** 0

---

## What to Draw on Chart Paper

### Section 1: Symbol Table Construction

**Draw a large table showing:**

1. **Initial Symbol Table (After Declarations)**
   - Columns: Name | Category | Defined | Source Gate | Used By
   - Show empty Source Gate and Used By columns

2. **Symbol Table Updates (After Each Gate)**
   - Show how each gate updates the table
   - Highlight changes in different colors

3. **Final Symbol Table**
   - Complete table with all information filled

### Section 2: Dependency Graph

**Draw a directed graph showing:**

```
    [A] ──┐
          │
          ├──→ [Sum] (XOR)
          │
    [B] ──┘
          │
          ├──→ [Carry] (AND)
          │
    [A] ──┘
```

- Use boxes for identifiers
- Use arrows to show dependencies
- Label gates on edges

### Section 3: Semantic Checks

**Draw tables for each check:**

1. **Declaration Check Table**
   - List each gate and its inputs
   - Check mark for each valid declaration

2. **Gate Input Count Table**
   - Show required vs actual for each gate
   - Validation results

3. **Output Assignment Table**
   - List all OUTPUTs
   - Show which gate assigns each

4. **Input Assignment Table**
   - Verify no INPUT is assigned to

5. **Cycle Detection Flow**
   - Draw DFS traversal tree
   - Show visited nodes and recursion stack
   - Mark cycle checks

### Section 4: Summary

**Draw a summary table:**

- List all 5 checks
- Show pass/fail status
- Final result

---

## Step-by-Step Dry Run Process

### Phase 1: Build Symbol Table

**Step 1:** Process `INPUT A, B;`
- Add A: category=INPUT, defined=Yes
- Add B: category=INPUT, defined=Yes

**Step 2:** Process `OUTPUT Sum, Carry;`
- Add Sum: category=OUTPUT, defined=No
- Add Carry: category=OUTPUT, defined=No

**Step 3:** Process `Sum = XOR(A, B);`
- Update Sum: defined=Yes, source=Gate(Sum=XOR(A,B))
- Update A: used_by=[Sum]
- Update B: used_by=[Sum]

**Step 4:** Process `Carry = AND(A, B);`
- Update Carry: defined=Yes, source=Gate(Carry=AND(A,B))
- Update A: used_by=[Sum, Carry]
- Update B: used_by=[Sum, Carry]

### Phase 2: Semantic Checks

**Check 1:** Declaration Check
- Gate 1: A ✓, B ✓
- Gate 2: A ✓, B ✓
- Result: PASS

**Check 2:** Gate Input Count
- Gate 1: XOR requires 2, has 2 ✓
- Gate 2: AND requires 2, has 2 ✓
- Result: PASS

**Check 3:** Output Assignment
- Sum: assigned by Gate 1 ✓
- Carry: assigned by Gate 2 ✓
- Result: PASS

**Check 4:** Input Assignment
- Gate 1 output: Sum (OUTPUT) ✓
- Gate 2 output: Carry (OUTPUT) ✓
- Result: PASS

**Check 5:** Cycle Detection
- DFS from A: no cycle ✓
- DFS from B: no cycle ✓
- DFS from Sum: no cycle ✓
- DFS from Carry: no cycle ✓
- Result: PASS

---

## Error Examples (For Reference)

### Example 1: Undeclared Identifier

**Input:**
```gate
CIRCUIT Test {
  INPUT A;
  OUTPUT Z;
  Z = AND(A, B);  // B not declared
}
```

**Error:** `Semantic Error: Undeclared identifier 'B' used in gate 'Z'`

### Example 2: Wrong Gate Input Count

**Input:**
```gate
CIRCUIT Test {
  INPUT A;
  OUTPUT Z;
  Z = AND(A);  // AND requires 2 inputs
}
```

**Error:** `Semantic Error: Gate AND requires 2 input(s), got 1 in gate 'Z'`

### Example 3: Unassigned OUTPUT

**Input:**
```gate
CIRCUIT Test {
  INPUT A, B;
  OUTPUT Z;  // Z never assigned
  WIRE temp;
  temp = AND(A, B);
}
```

**Error:** `Semantic Error: OUTPUT 'Z' never assigned`

### Example 4: Cycle Detection

**Input:**
```gate
CIRCUIT Test {
  INPUT A;
  OUTPUT Z;
  WIRE w1, w2;
  w1 = AND(A, w2);
  w2 = OR(w1, A);
  Z = w1;
}
```

**Error:** `Semantic Error: Cycle detected: w1 -> w2 -> w1`

---

## Chart Paper Layout Suggestion

### Top Section: Title
**"Semantic Analysis - Phase 3"**
**"Example: Half Adder Circuit"**

### Left Side: Symbol Table Construction
- Show step-by-step symbol table building
- Use arrows to show updates
- Highlight changes

### Right Side: Semantic Checks
- Five separate tables/boxes for each check
- Use checkmarks (✓) or X marks
- Show validation results

### Bottom Section: Summary
- Final symbol table
- Dependency graph
- Overall result

### Use Colors (if available):
- Green: Passed checks
- Red: Failed checks
- Blue: Symbol table entries
- Yellow: Important notes

---

## Key Points to Remember

1. **Symbol Table Structure:**
   - Name: Identifier name
   - Category: INPUT, OUTPUT, or WIRE
   - Defined: Whether identifier has a value
   - Source Gate: Which gate produces this value
   - Used By: Which gates use this identifier

2. **Semantic Rules:**
   - All identifiers must be declared before use
   - Gate input counts must match requirements
   - All OUTPUTs must be assigned
   - INPUTs cannot be assigned to
   - No combinational cycles allowed

3. **Cycle Detection Algorithm:**
   - Use DFS (Depth-First Search)
   - Track visited nodes
   - Track recursion stack
   - If node in recursion stack → cycle found

4. **Processing Order:**
   - First: Build symbol table from declarations
   - Second: Populate gate information
   - Third: Run all semantic checks
   - Fourth: Report results

---

**This document contains everything needed to create a complete semantic analysis dry run on chart paper for the Half Adder example.**


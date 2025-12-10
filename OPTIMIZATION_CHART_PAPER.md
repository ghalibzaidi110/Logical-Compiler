# Code Optimization - Chart Paper Guide

## Half Adder Example

**Input Quadruples (from ICG):**
```
1: (XOR, A, B, Sum)
2: (AND, A, B, Carry)
```

---

## Optimization Techniques

### 1. Constant Folding
**Rule:** Simplify operations with constants (0, 1)

| Operation | Condition | Optimization | Result |
|-----------|-----------|-------------|--------|
| AND | arg1 = 0 OR arg2 = 0 | → ASSIGN 0 | 0 |
| AND | arg1 = 1 | → ASSIGN arg2 | arg2 |
| AND | arg2 = 1 | → ASSIGN arg1 | arg1 |
| OR | arg1 = 1 OR arg2 = 1 | → ASSIGN 1 | 1 |
| OR | arg1 = 0 | → ASSIGN arg2 | arg2 |
| OR | arg2 = 0 | → ASSIGN arg1 | arg1 |
| XOR | arg1 = 0 | → ASSIGN arg2 | arg2 |
| XOR | arg2 = 0 | → ASSIGN arg1 | arg1 |
| XOR | arg1 = arg2 | → ASSIGN 0 | 0 |

### 2. Algebraic Simplification
**Rule:** Apply identity laws

| Operation | Condition | Optimization | Result |
|-----------|-----------|-------------|--------|
| AND | arg1 == arg2 | → ASSIGN arg1 | A AND A = A |
| OR | arg1 == arg2 | → ASSIGN arg1 | A OR A = A |
| XOR | arg1 == arg2 | → ASSIGN 0 | A XOR A = 0 |

### 3. Dead Code Elimination
**Rule:** Remove unused computations

**Process:**
1. Mark all used variables (from arg1, arg2 of all quads)
2. Keep quads where:
   - result is OUTPUT, OR
   - result is used by another quad

---

## Step-by-Step Dry Run: Half Adder

### Input Quadruples

| No. | Operation | Arg1 | Arg2 | Result |
|-----|-----------|------|------|--------|
| 1 | XOR | A | B | Sum |
| 2 | AND | A | B | Carry |

---

### Pass 1: Constant Folding & Algebraic Simplification

**Quadruple 1: (XOR, A, B, Sum)**

| Check | Condition | Result |
|-------|-----------|--------|
| Constant folding | arg1 = '0'? | No (A is variable) |
| Constant folding | arg2 = '0'? | No (B is variable) |
| Constant folding | arg1 = arg2? | No (A ≠ B) |
| Algebraic simplification | arg1 == arg2? | No (A ≠ B) |
| **Result** | No optimization | Keep as (XOR, A, B, Sum) |

**Quadruple 2: (AND, A, B, Carry)**

| Check | Condition | Result |
|-------|-----------|--------|
| Constant folding | arg1 = '0' OR arg2 = '0'? | No (both variables) |
| Constant folding | arg1 = '1'? | No |
| Constant folding | arg2 = '1'? | No |
| Algebraic simplification | arg1 == arg2? | No (A ≠ B) |
| **Result** | No optimization | Keep as (AND, A, B, Carry) |

**After Pass 1:**

| No. | Operation | Arg1 | Arg2 | Result |
|-----|-----------|------|------|--------|
| 1 | XOR | A | B | Sum |
| 2 | AND | A | B | Carry |

---

### Pass 2: Dead Code Elimination

**Step 1: Mark Used Variables**

| Quad | Arg1 | Arg2 | Used Set |
|------|------|------|----------|
| 1 | A | B | {A, B} |
| 2 | A | B | {A, B} |

**Used Variables:** {A, B}

**Step 2: Check Each Quad**

| Quad | Result | Is OUTPUT? | Is Used? | Keep? |
|------|--------|------------|----------|-------|
| 1 | Sum | Yes (OUTPUT) | - | ✓ Yes |
| 2 | Carry | Yes (OUTPUT) | - | ✓ Yes |

**After Pass 2:**

| No. | Operation | Arg1 | Arg2 | Result |
|-----|-----------|------|------|--------|
| 1 | XOR | A | B | Sum |
| 2 | AND | A | B | Carry |

---

## Optimization Summary

| Aspect | Before | After | Change |
|--------|--------|-------|--------|
| Quadruples | 2 | 2 | 0 removed |
| Optimization | None | None | Already optimal |

**Result:** No changes (code already optimal)

---

## Example with Optimization

### Input Circuit:
```gate
CIRCUIT Test {
  INPUT A;
  OUTPUT Z;
  WIRE temp1, temp2;
  temp1 = AND(A, 0);
  temp2 = OR(temp1, 0);
  Z = temp2;
}
```

### Before Optimization:

| No. | Operation | Arg1 | Arg2 | Result |
|-----|-----------|------|------|--------|
| 1 | AND | A | 0 | temp1 |
| 2 | OR | temp1 | 0 | temp2 |
| 3 | ASSIGN | temp2 | - | Z |

### Pass 1: Constant Folding

**Quad 1:** AND(A, 0) → Constant folding: AND with 0 → ASSIGN(0, -, temp1)

**Quad 2:** OR(temp1, 0) → Constant folding: OR with 0 → ASSIGN(temp1, -, temp2)

**After Pass 1:**

| No. | Operation | Arg1 | Arg2 | Result |
|-----|-----------|------|------|--------|
| 1 | ASSIGN | 0 | - | temp1 |
| 2 | ASSIGN | temp1 | - | temp2 |
| 3 | ASSIGN | temp2 | - | Z |

### Pass 2: Dead Code Elimination

**Used Variables:** {temp1, temp2}

**Check:**
- Quad 1: temp1 is used (by quad 2) → Keep
- Quad 2: temp2 is used (by quad 3) → Keep
- Quad 3: Z is OUTPUT → Keep

**After Pass 2:** Same (all kept)

### Final Optimized:

| No. | Operation | Arg1 | Arg2 | Result |
|-----|-----------|------|------|--------|
| 1 | ASSIGN | 0 | - | temp1 |
| 2 | ASSIGN | temp1 | - | temp2 |
| 3 | ASSIGN | temp2 | - | Z |

**Further optimization:** temp1 = 0, so temp2 = 0, so Z = 0
**Final:** Z = ASSIGN(0, -, Z)

---

## What to Draw on Chart Paper

### Section 1: Title
**"Code Optimization - Phase 5"**

### Section 2: Input Quadruples
Draw the table of quadruples before optimization

### Section 3: Optimization Rules
Draw tables for:
- Constant Folding rules
- Algebraic Simplification rules

### Section 4: Pass 1 - Constant Folding & Algebraic Simplification
For each quadruple, show:
- Checks performed
- Optimization applied (if any)
- Result

### Section 5: Pass 2 - Dead Code Elimination
- Mark used variables
- Check each quad (OUTPUT or used?)
- Remove unused quads

### Section 6: Final Optimized Quadruples
Draw the final table

### Section 7: Summary
- Before/After comparison
- Quads removed
- Optimization result

---

## Key Points

1. **Two Passes:**
   - Pass 1: Constant folding + Algebraic simplification
   - Pass 2: Dead code elimination

2. **Constant Folding:**
   - AND with 0 → 0
   - OR with 1 → 1
   - XOR with 0 → identity
   - XOR with self → 0

3. **Algebraic Simplification:**
   - A AND A = A
   - A OR A = A
   - A XOR A = 0

4. **Dead Code Elimination:**
   - Keep OUTPUTs
   - Keep if result is used
   - Remove otherwise

5. **Processing Order:**
   - Process all quads in Pass 1
   - Then eliminate dead code in Pass 2


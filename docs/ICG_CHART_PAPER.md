# Intermediate Code Generation (ICG) - Chart Paper Guide

## Half Adder Example

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

## Quadruple Format

**Structure:** (Operation, Arg1, Arg2, Result)

| Field | Description |
|-------|-------------|
| Operation | Gate type (AND, OR, XOR, NOT, etc.) |
| Arg1 | First input operand |
| Arg2 | Second input (None for NOT, shown as "-") |
| Result | Output variable |

---

## Step-by-Step Dry Run

### Input AST Gates

| Gate # | Gate |
|--------|------|
| 1 | Gate(Sum = XOR(['A', 'B'])) |
| 2 | Gate(Carry = AND(['A', 'B'])) |

---

### Processing Table

| Step | Gate | Extract Info | Check Type | Operation | Arg1 | Arg2 | Result | Quadruple |
|------|------|--------------|------------|-----------|------|------|--------|-----------|
| 1 | Sum = XOR(A, B) | output = gate.output = "Sum"<br>gate_type = "XOR"<br>inputs = ["A", "B"] | gate_type != 'NOT'<br>→ Binary | XOR | inputs[0] = "A" | inputs[1] = "B" | "Sum" | (XOR, A, B, Sum) |
| 2 | Carry = AND(A, B) | output = gate.output = "Carry"<br>gate_type = "AND"<br>inputs = ["A", "B"] | gate_type != 'NOT'<br>→ Binary | AND | inputs[0] = "A" | inputs[1] = "B" | "Carry" | (AND, A, B, Carry) |

---

## Final Quadruple Table

| No. | Operation | Arg1 | Arg2 | Result | Three-Address Code |
|-----|-----------|------|------|--------|-------------------|
| 1 | XOR | A | B | Sum | Sum = XOR(A, B) |
| 2 | AND | A | B | Carry | Carry = AND(A, B) |

---

## Gate Type Mapping

### Binary Operations (2 inputs)
- AND, OR, XOR, NAND, NOR → (OP, arg1, arg2, result)

### Unary Operations (1 input)
- NOT → (NOT, arg1, -, result)

---

## Algorithm (From icg.py)

```
Initialize: quads = []

For each gate in ast.gates:
  If gate.gate_type == 'NOT':
    # Unary operation
    quad = Quadruple(
      op = gate.gate_type,        # "NOT"
      arg1 = gate.inputs[0],      # First input
      arg2 = None,                 # None for unary
      result = gate.output         # Output identifier
    )
  Else:
    # Binary operation
    quad = Quadruple(
      op = gate.gate_type,         # "AND", "OR", "XOR", etc.
      arg1 = gate.inputs[0],      # First input
      arg2 = gate.inputs[1],       # Second input (if len > 1)
      result = gate.output         # Output identifier
    )
  
  quads.append(quad)

Return quads
```

**Quadruple Representation:**
- If arg2 is None: `(op, arg1, -, result)`
- Else: `(op, arg1, arg2, result)`

---

## What to Draw on Chart Paper

### Section 1: Title
**"Intermediate Code Generation - Phase 4"**

### Section 2: Input AST
```
Program(HalfAdder)
├── Gate(Sum = XOR(['A', 'B']))
└── Gate(Carry = AND(['A', 'B']))
```

### Section 3: Processing Table
Draw the processing table showing step-by-step generation

### Section 4: Final Quadruple Table
Draw the complete quadruple table with all columns

### Section 5: Three-Address Code
```
(1) Sum = XOR(A, B)
(2) Carry = AND(A, B)
```

---

## Key Points

1. **Quadruple Format:** (Operation, Arg1, Arg2, Result)
2. **Processing Order:** Same as gates appear in AST (sequential)
3. **Unary (NOT):** 
   - Arg2 = None (displayed as "-")
   - Uses only inputs[0]
4. **Binary (AND, OR, XOR, NAND, NOR):**
   - Uses inputs[0] and inputs[1]
   - Safety check: inputs[1] if len(inputs) > 1 else None
5. **Field Extraction:**
   - Operation = gate.gate_type
   - Arg1 = gate.inputs[0]
   - Arg2 = gate.inputs[1] (for binary) or None (for NOT)
   - Result = gate.output
6. **Quadruple Class:**
   - Stores: op, arg1, arg2, result
   - Repr: Shows "-" when arg2 is None

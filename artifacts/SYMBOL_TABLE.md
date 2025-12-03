# Artifact 3: Symbol Table Example
## Hand-Drawn Table Reference

**Purpose:** Sample symbol table with scope and usage information  
**Circuit:** Half Adder  
**Language:** Logic Gate Architect DSL

---

## Symbol Table Structure

### For Circuit:
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

### Symbol Table:

| Identifier | Category | Defined | Source Gate | Used By | Line |
|------------|----------|---------|-------------|---------|------|
| A | INPUT | Yes | None (primary input) | Sum, Carry | 2 |
| B | INPUT | Yes | None (primary input) | Sum, Carry | 2 |
| Sum | OUTPUT | Yes | XOR(A, B) | None | 3, 4 |
| Carry | OUTPUT | Yes | AND(A, B) | None | 3, 5 |

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

## Hand-Drawing Instructions

1. **Create a table** with columns: Identifier | Category | Defined | Source | Used By
2. **Fill in rows** for each identifier in the circuit
3. **Use checkmarks (✓)** for "Defined: Yes"
4. **Use dashes (-)** for "Source: None"
5. **List dependencies** in "Used By" column
6. **Add line numbers** if space permits

## Alternative: More Complex Example

### Circuit with Wires:
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

**Note:** Please create a hand-drawn version on paper, scan it, and save as `SYMBOL_TABLE.pdf`


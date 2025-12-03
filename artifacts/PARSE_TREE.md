# Artifact 2: Parse Tree
## Hand-Drawn Diagram Reference

**Purpose:** Parse tree for sample statement  
**Example:** `Sum = XOR(A, B);`  
**Language:** Logic Gate Architect DSL

---

## Parse Tree Structure

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
```

## Detailed Parse Tree for Gate Statement

```
                    <gate>
                        |
        ┌───────────────┼───────────────┐
        |               |               |
    <identifier>     <equals>      <gate_expr>
        |               |               |
      "Sum"             "="       ┌──────┼──────┐
                                 |      |      |
                            <gate_type> (  <gate_inputs>  )
                                 |      |      |
                               "XOR"    (   ┌──┴──┐
                                          |      |
                                    <identifier> <gate_inputs_tail>
                                          |      |
                                        "A"     ┌──┴──┐
                                               |      |
                                          <comma> <identifier>
                                               |      |
                                               ","   "B"
```

## Simplified Visual Representation

```
                    <gate>
                        |
    ┌───────────────────┼───────────────────┐
    |                   |                   |
<identifier>         <equals>          <gate_expr>
    |                   |                   |
  "Sum"                "="          ┌────────┼────────┐
                                    |        |        |
                              <gate_type>  (  <gate_inputs>  )
                                    |        |        |
                                  "XOR"     (    ┌────┴────┐
                                              |          |
                                        <identifier>  <gate_inputs_tail>
                                              |          |
                                            "A"    <comma> <identifier>
                                                      |      |
                                                      ","   "B"
```

## Hand-Drawing Instructions

1. **Start with root node:** Draw a box labeled `<gate>`
2. **Add three children:** 
   - Left: `<identifier>` → "Sum"
   - Middle: `<equals>` → "="
   - Right: `<gate_expr>`
3. **Expand `<gate_expr>`:**
   - Add `<gate_type>` → "XOR"
   - Add "("
   - Add `<gate_inputs>`
   - Add ")"
4. **Expand `<gate_inputs>`:**
   - Add `<identifier>` → "A"
   - Add `<gate_inputs_tail>`
5. **Expand `<gate_inputs_tail>`:**
   - Add `<comma>` → ","
   - Add `<identifier>` → "B"
6. **Add terminal nodes:** Draw circles/boxes for actual tokens ("Sum", "=", "XOR", "(", "A", ",", "B", ")")
7. **Add semicolon:** Connect ";" at the end

## Alternative: Full Circuit Parse Tree

For the complete circuit:
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

The parse tree would show:
- Root: `<program>`
- Children: CIRCUIT keyword, identifier "HalfAdder", {, declarations, gates, }
- Declarations branch: INPUT declaration, OUTPUT declaration
- Gates branch: First gate (Sum = XOR...), Second gate (Carry = AND...)

---

**Note:** Please create a hand-drawn version on paper, scan it, and save as `PARSE_TREE.pdf`


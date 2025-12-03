# Circuit Examples - Logic Gate Architect Compiler

This directory contains example circuits of varying complexity to test and demonstrate the compiler.

---

## Easy Examples (Beginner Level)

### 1. `simple_not.gate` - Inverter
**Description:** Simple NOT gate (inverter)  
**Inputs:** 1 (A)  
**Outputs:** 1 (Z)  
**Gates:** 1  
**Complexity:** ⭐ Very Easy

```
CIRCUIT Inverter {
  INPUT A;
  OUTPUT Z;
  Z = NOT(A);
}
```

**Use Case:** Testing basic unary gate operation

---

### 2. `basic_and.gate` - Basic AND Gate
**Description:** Simple 2-input AND gate  
**Inputs:** 2 (A, B)  
**Outputs:** 1 (Z)  
**Gates:** 1  
**Complexity:** ⭐ Very Easy

**Use Case:** Testing basic binary gate operation

---

### 3. `simple_or.gate` - Basic OR Gate
**Description:** Simple 2-input OR gate  
**Inputs:** 2 (A, B)  
**Outputs:** 1 (Z)  
**Gates:** 1  
**Complexity:** ⭐ Very Easy

**Use Case:** Testing OR gate functionality

---

### 4. `simple_nand.gate` - Basic NAND Gate
**Description:** Simple 2-input NAND gate  
**Inputs:** 2 (A, B)  
**Outputs:** 1 (Z)  
**Gates:** 1  
**Complexity:** ⭐ Very Easy

**Use Case:** Testing NAND gate (universal gate)

---

### 5. `simple_nor.gate` - Basic NOR Gate
**Description:** Simple 2-input NOR gate  
**Inputs:** 2 (A, B)  
**Outputs:** 1 (Z)  
**Gates:** 1  
**Complexity:** ⭐ Very Easy

**Use Case:** Testing NOR gate (universal gate)

---

## Medium Examples (Intermediate Level)

### 6. `halfadder.gate` - Half Adder
**Description:** 1-bit half adder (no carry input)  
**Inputs:** 2 (A, B)  
**Outputs:** 2 (Sum, Carry)  
**Gates:** 2  
**Complexity:** ⭐⭐ Easy

**Use Case:** Basic arithmetic circuit, multiple outputs

---

### 7. `xor_from_basic.gate` - XOR from Basic Gates
**Description:** XOR gate constructed from AND, OR, NOT gates  
**Inputs:** 2 (A, B)  
**Outputs:** 1 (Z)  
**Gates:** 5  
**Complexity:** ⭐⭐ Easy-Medium

**Use Case:** Demonstrates gate composition, intermediate wires

**Formula:** Z = (A AND NOT B) OR (NOT A AND B)

---

### 8. `multiplexer_2to1.gate` - 2-to-1 Multiplexer
**Description:** Selects between two inputs based on select signal  
**Inputs:** 3 (A, B, S)  
**Outputs:** 1 (Z)  
**Gates:** 3  
**Complexity:** ⭐⭐ Medium

**Use Case:** Data selection, demonstrates conditional logic

**Function:** Z = A when S=0, Z = B when S=1

---

### 9. `decoder_2to4.gate` - 2-to-4 Decoder
**Description:** Decodes 2-bit input to 4 output lines  
**Inputs:** 2 (A, B)  
**Outputs:** 4 (D0, D1, D2, D3)  
**Gates:** 6  
**Complexity:** ⭐⭐ Medium

**Use Case:** Address decoding, demonstrates multiple outputs

**Function:** Only one output is high based on input combination

---

### 10. `comparator_1bit.gate` - 1-Bit Comparator
**Description:** Compares two 1-bit numbers  
**Inputs:** 2 (A, B)  
**Outputs:** 3 (Equal, Greater, Less)  
**Gates:** 4  
**Complexity:** ⭐⭐ Medium

**Use Case:** Comparison operations, multiple output conditions

---

## Complex Examples (Advanced Level)

### 11. `fulladder.gate` - Full Adder
**Description:** 1-bit full adder with carry input  
**Inputs:** 3 (A, B, Cin)  
**Outputs:** 2 (Sum, Cout)  
**Gates:** 5  
**Complexity:** ⭐⭐⭐ Medium-Hard

**Use Case:** Complete arithmetic unit, demonstrates complex logic

---

### 12. `full_adder_alternative.gate` - Full Adder (Alternative)
**Description:** Full adder using different gate arrangement  
**Inputs:** 3 (A, B, Cin)  
**Outputs:** 2 (Sum, Cout)  
**Gates:** 6  
**Complexity:** ⭐⭐⭐ Medium-Hard

**Use Case:** Shows different implementations of same function

---

### 13. `encoder_4to2.gate` - 4-to-2 Encoder
**Description:** Encodes 4 input lines to 2-bit output  
**Inputs:** 4 (D0, D1, D2, D3)  
**Outputs:** 2 (A, B)  
**Gates:** 2  
**Complexity:** ⭐⭐⭐ Medium-Hard

**Use Case:** Data encoding, inverse of decoder

**Note:** Assumes only one input is active at a time

---

### 14. `priority_encoder.gate` - Priority Encoder
**Description:** Encodes highest priority active input  
**Inputs:** 4 (D0, D1, D2, D3)  
**Outputs:** 3 (A, B, Valid)  
**Gates:** 4  
**Complexity:** ⭐⭐⭐ Hard

**Use Case:** Interrupt handling, priority-based selection

**Function:** D3 has highest priority, D0 has lowest

---

### 15. `demultiplexer_1to4.gate` - 1-to-4 Demultiplexer
**Description:** Routes one input to one of four outputs  
**Inputs:** 3 (Input, S0, S1)  
**Outputs:** 4 (Y0, Y1, Y2, Y3)  
**Gates:** 7  
**Complexity:** ⭐⭐⭐ Hard

**Use Case:** Data routing, inverse of multiplexer

---

### 16. `magnitude_comparator.gate` - Magnitude Comparator
**Description:** Compares two numbers with three outputs  
**Inputs:** 2 (A, B)  
**Outputs:** 3 (A_GT_B, A_LT_B, A_EQ_B)  
**Gates:** 4  
**Complexity:** ⭐⭐⭐ Hard

**Use Case:** Complete comparison operations

---

### 17. `parity_checker.gate` - Parity Checker
**Description:** Calculates even parity of 4-bit input  
**Inputs:** 4 (A, B, C, D)  
**Outputs:** 1 (Parity)  
**Gates:** 3  
**Complexity:** ⭐⭐⭐ Hard

**Use Case:** Error detection, demonstrates XOR chain

**Function:** Parity = A XOR B XOR C XOR D

---

### 18. `ripple_carry_2bit.gate` - 2-Bit Ripple Carry Adder
**Description:** Adds two 2-bit numbers with carry propagation  
**Inputs:** 5 (A0, A1, B0, B1, Cin)  
**Outputs:** 3 (S0, S1, Cout)  
**Gates:** 9  
**Complexity:** ⭐⭐⭐⭐ Very Hard

**Use Case:** Multi-bit arithmetic, demonstrates cascading circuits

**Function:** Adds A[1:0] + B[1:0] + Cin, produces S[1:0] + Cout

---

## Testing Guide

### Quick Test (Easy)
```bash
python compiler.py examples/simple_not.gate -v
python compiler.py examples/basic_and.gate -v
python compiler.py examples/simple_or.gate -v
```

### Medium Test
```bash
python compiler.py examples/halfadder.gate -v
python compiler.py examples/multiplexer_2to1.gate -v
python compiler.py examples/decoder_2to4.gate -v
```

### Complex Test
```bash
python compiler.py examples/fulladder.gate -v
python compiler.py examples/priority_encoder.gate -v
python compiler.py examples/ripple_carry_2bit.gate -v
```

### Full Test Suite
```bash
# Test all easy examples
for file in examples/simple_*.gate examples/basic_*.gate; do
    python compiler.py "$file" -o "${file%.gate}_output.py"
done

# Test all medium examples
python compiler.py examples/halfadder.gate -v
python compiler.py examples/xor_from_basic.gate -v
python compiler.py examples/multiplexer_2to1.gate -v

# Test all complex examples
python compiler.py examples/fulladder.gate -v
python compiler.py examples/ripple_carry_2bit.gate -v
```

---

## Complexity Ratings

- ⭐ **Very Easy:** 1-2 gates, 1-2 inputs, 1 output
- ⭐⭐ **Easy-Medium:** 3-5 gates, 2-3 inputs, 1-2 outputs
- ⭐⭐⭐ **Medium-Hard:** 5-7 gates, 3-4 inputs, 2-4 outputs
- ⭐⭐⭐⭐ **Very Hard:** 8+ gates, 5+ inputs, multiple outputs with complex logic

---

## Learning Path

1. **Start with Easy:** Understand basic gate operations
2. **Move to Medium:** Learn gate composition and multiple outputs
3. **Progress to Complex:** Master cascading circuits and advanced logic
4. **Challenge with Very Hard:** Build multi-bit arithmetic units

---

## Notes

- All examples are syntactically correct and should compile successfully
- Some examples demonstrate the same function with different implementations
- Complex examples may take longer to compile and generate larger output
- Use `-v` flag for verbose output to see all compilation phases
- Use `--quads` flag to see intermediate code generation
- Use `--symbols` flag to see symbol table construction

---

**Total Examples:** 18 circuits  
**Easy:** 5 | **Medium:** 5 | **Complex:** 8


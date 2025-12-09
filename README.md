# Logic Gate Architect Compiler

A complete 6-phase compiler implementation for a domain-specific language (DSL) designed for digital circuit design.

## Project Overview

**Course:** CS4031 - Compiler Construction  
**Language:** Logic Gate Architect DSL  
**Implementation:** Python (CLI + GUI)  
**Status:** Complete with all required deliverables

## Features

✅ **All 6 Compiler Phases:**
- Phase 1: Lexical Analysis (Tokenization)
- Phase 2: Syntax Analysis (Recursive Descent Parser)
- Phase 3: Semantic Analysis (Symbol Table, Cycle Detection)
- Phase 4: Intermediate Code Generation (Quadruples)
- Phase 5: Optimization (Constant Folding, Dead Code Elimination)
- Phase 6: Code Generation (Python Output)

✅ **Two Interfaces:**
- **CLI Version** (`compiler.py`) - Command-line interface for submission
- **GUI Version** (`compiler_gui.py`) - Modern graphical interface for demo

## Quick Start

### GUI Version (Recommended for Demo)

```bash
python compiler_gui.py
```

Features:
- Interactive code editor
- Real-time compilation
- Phase-by-phase visualization
- File I/O support
- Test case buttons

### CLI Version (For Submission)

```bash
# Basic compilation (prints to stdout)
python compiler.py examples/halfadder.gate

# Save to file (saved in outputs/ folder)
python compiler.py examples/halfadder.gate -o halfadder_output.py
python outputs/halfadder_output.py

# Verbose mode (see all phases)
python compiler.py examples/halfadder.gate -v

# Show detailed information
python compiler.py examples/halfadder.gate -v --tokens --ast --symbols --quads

# Run automated test suite
python test_all_examples.py
```

## Example Circuit

```gate
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

## Project Structure

```
Logic Gates Compiler/
├── compiler.py              # CLI compiler (main submission)
├── compiler_gui.py          # GUI compiler (demo)
├── test_all_examples.py     # Automated test suite
├── lexer.py                 # Phase 1: Lexical Analysis
├── parser.py                # Phase 2: Syntax Analysis
├── semantic.py              # Phase 3: Semantic Analysis
├── icg.py                   # Phase 4: Intermediate Code Generation
├── optimizer.py             # Phase 5: Optimization
├── codegen.py               # Phase 6: Code Generation
├── grammar.bnf               # Formal BNF grammar
├── reflection.md            # Project reflection
├── examples/                # Test circuit files (.gate)
│   ├── basic_and.gate
│   ├── halfadder.gate
│   ├── fulladder.gate
│   └── ... (18 example files)
├── outputs/                 # Generated Python files (auto-created)
│   ├── basic_and_output.py
│   ├── halfadder_output.py
│   └── ... (generated files)
├── artifacts/               # Hand-drawn artifact references
│   ├── DFA_IDENTIFIER.md
│   ├── PARSE_TREE.md
│   └── SYMBOL_TABLE.md
└── README.md
```

**Note:** The `outputs/` folder is automatically created when you compile files. All generated Python code is saved here.

## Test Cases

The project includes 18 example circuit files in the `examples/` folder:

1. **Basic AND Gate** - Simple 2-input AND gate
2. **Half Adder** - Arithmetic circuit with multiple outputs
3. **Full Adder** - Complex circuit with wires
4. **Comparator** - 1-bit magnitude comparator
5. **Decoder** - 2-to-4 decoder
6. **Encoder** - 4-to-2 encoder
7. **Multiplexer** - 2-to-1 multiplexer
8. **Demultiplexer** - 1-to-4 demultiplexer
9. **Parity Checker** - 4-bit parity checker
10. **Priority Encoder** - Priority encoder circuit
11. **Ripple Carry Adder** - 2-bit ripple carry adder
12. **Simple Gates** - NOT, OR, NAND, NOR gates
13. **XOR from Basic** - XOR gate constructed from basic gates
14. And more...

### Automated Test Suite

Run all test cases automatically with the test script:

```bash
python test_all_examples.py
```

**What it does:**
- Compiles all `.gate` files in the `examples/` folder
- Generates Python output files in the `outputs/` folder
- Runs each generated file and displays results
- Provides a summary of successful/failed tests
- Processes files sequentially (one by one)

**Output:**
- All generated files are saved to `outputs/` folder
- Each file is named `<circuit_name>_output.py`
- Test results show compilation status and execution output
- Clear error messages for any failures

**Example output:**
```
======================================================================
               LOGICAL COMPILER - AUTOMATED TEST SUITE
======================================================================

[INFO] Found 18 example file(s) to test

======================================================================
                      Test 1/18: basic_and.gate
======================================================================

[1/2] Compiling...
[OK] Compilation successful: basic_and_output.py

[2/2] Running generated code...
[OK] Execution successful: basic_and_output.py

Output:
----------------------------------------------------------------------
A  B || Z
----------------------------------------
0  0 || 0
0  1 || 0
1  0 || 0
1  1 || 1
----------------------------------------------------------------------

...

======================================================================
                             TEST SUMMARY
======================================================================

Total files tested: 18
Successful compilations: 17/18
Successful executions: 17/18
```

## Generated Output

The compiler generates Python code that can be executed. **All output files are automatically saved to the `outputs/` folder.**

### Output Folder

- **Location:** `outputs/` (created automatically)
- **Naming:** `<circuit_name>_output.py` (e.g., `halfadder_output.py`)
- **Behavior:** 
  - CLI: Files saved to `outputs/` when using `-o` option
  - GUI: File dialogs default to `outputs/` folder
  - Test Suite: All generated files saved to `outputs/`

**Note:** The `outputs/` folder is ignored by Git (see `.gitignore`) to avoid committing generated files.

### Example Generated Code

```python
# Generated by Logic Gate Architect Compiler
# Circuit: HalfAdder

def simulate(A, B):
    Sum = A ^ B
    Carry = A & B
    return Sum, Carry

# Truth Table
print("A  B || Sum  Carry")
print("-" * 40)

result = simulate(0, 0)
print(f"0  0 || {result[0]}  {result[1]}")
result = simulate(0, 1)
print(f"0  1 || {result[0]}  {result[1]}")
result = simulate(1, 0)
print(f"1  0 || {result[0]}  {result[1]}")
result = simulate(1, 1)
print(f"1  1 || {result[0]}  {result[1]}")
```

**Running generated files:**
```bash
# Files are saved to outputs/ folder
python outputs/halfadder_output.py
```

## CLI Options

```
python compiler.py <input_file> [options]

Options:
  -o, --output <file>    Write generated code to file
  -v, --verbose          Show detailed compilation steps
  -t, --tokens           Print token stream
  -a, --ast              Print abstract syntax tree
  -s, --symbols          Print symbol table
  -q, --quads            Print quadruples
  --no-optimize          Disable optimization
  -h, --help             Show help message
```

## Requirements

- Python 3.8 or higher
- tkinter (usually included with Python, for GUI)

## Deliverables Checklist

- [x] Language specification (BNF grammar)
- [x] All 6 compiler phases implemented
- [x] CLI version (Python)
- [x] GUI version (Python/tkinter)
- [x] Handwritten artifact references
- [x] Reflection document
- [x] Git repository
- [x] File I/O capability
- [x] 3+ test cases
- [x] Complete documentation

## License

Academic project for CS4031 - Compiler Construction

---

**Team:** 3 Members  
**Semester:** Fall 2025

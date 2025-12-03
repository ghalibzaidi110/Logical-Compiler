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
# Basic compilation
python compiler.py examples/halfadder.gate

# Save to file
python compiler.py examples/halfadder.gate -o output.py
python output.py

# Verbose mode (see all phases)
python compiler.py examples/halfadder.gate -v

# Show detailed information
python compiler.py examples/halfadder.gate -v --tokens --ast --symbols --quads
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
├── lexer.py                 # Phase 1: Lexical Analysis
├── parser.py                # Phase 2: Syntax Analysis
├── semantic.py              # Phase 3: Semantic Analysis
├── icg.py                   # Phase 4: Intermediate Code Generation
├── optimizer.py             # Phase 5: Optimization
├── codegen.py               # Phase 6: Code Generation
├── grammar.bnf               # Formal BNF grammar
├── reflection.md            # Project reflection
├── examples/                # Test circuit files
│   ├── basic_and.gate
│   ├── halfadder.gate
│   └── fulladder.gate
├── artifacts/               # Hand-drawn artifact references
│   ├── DFA_IDENTIFIER.md
│   ├── PARSE_TREE.md
│   └── SYMBOL_TABLE.md
└── README.md
```

## Test Cases

1. **Basic AND Gate** - Simple 2-input AND gate
2. **Half Adder** - Arithmetic circuit with multiple outputs
3. **Full Adder** - Complex circuit with wires

## Generated Output

The compiler generates Python code that can be executed:

```python
def simulate(A, B):
    Sum = A ^ B
    Carry = A & B
    return Sum, Carry

# Truth Table
print("A  B || Sum  Carry")
# ... complete truth table
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

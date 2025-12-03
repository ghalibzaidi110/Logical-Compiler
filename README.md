# Logic Gate Architect Compiler

A complete 6-phase compiler implementation for a domain-specific language (DSL) designed for digital circuit design.

## Project Overview

**Course:** CS4031 - Compiler Construction  
**Language:** Logic Gate Architect DSL  
**Implementation:** TypeScript/React  
**Status:** Complete with all required deliverables

## Features

✅ **All 6 Compiler Phases:**
- Phase 1: Lexical Analysis (Tokenization)
- Phase 2: Syntax Analysis (Recursive Descent Parser)
- Phase 3: Semantic Analysis (Symbol Table, Cycle Detection)
- Phase 4: Intermediate Code Generation (Quadruples)
- Phase 5: Optimization (Constant Folding, Dead Code Elimination)
- Phase 6: Code Generation (Python Output)

✅ **Modern Web Interface:**
- Interactive code editor
- Real-time compilation
- Phase-by-phase visualization
- File I/O support

✅ **Complete Documentation:**
- Formal BNF grammar specification
- Phase-by-phase documentation
- Hand-drawn artifact references
- Project reflection

## Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- React 18+

### Installation
```bash
# Clone repository
git clone <repository-url>
cd "Logic Gates Compiler"

# Install dependencies (if needed)
npm install
```

### Usage
1. Open `logic_gate_compiler.tsx` in your React application
2. Use the interactive UI to:
   - Load `.gate` files
   - Edit source code
   - Compile circuits
   - View all compilation phases
   - Save generated Python code

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
├── logic_gate_compiler.tsx    # Main compiler implementation
├── grammar.bnf                 # Formal BNF grammar
├── reflection.md               # Project reflection
├── complete_project_report.md  # Full project report
├── phase1_lexer_doc.md         # Lexical analysis docs
├── phase3_semantic_doc.md      # Semantic analysis docs
├── phases_456_doc.md           # ICG, Optimization, CodeGen docs
├── artifacts/                  # Hand-drawn artifact references
│   ├── DFA_IDENTIFIER.md
│   ├── PARSE_TREE.md
│   └── SYMBOL_TABLE.md
└── .gitignore
```

## Deliverables Checklist

- [x] Language specification (BNF grammar)
- [x] All 6 compiler phases implemented
- [x] Handwritten artifact references (DFA, parse tree, symbol table)
- [x] Reflection document
- [x] Git repository
- [x] File I/O capability
- [x] 3+ test cases
- [x] Complete documentation

## Test Cases

1. **Basic AND Gate** - Simple 2-input AND gate
2. **Half Adder** - Arithmetic circuit with multiple outputs
3. **Cycle Detection** - Error detection for combinational loops

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

## Documentation

- **Grammar:** See `grammar.bnf` for formal BNF specification
- **Phases:** See phase-specific documentation files
- **Artifacts:** See `artifacts/` directory for hand-drawing instructions
- **Report:** See `complete_project_report.md` for full details

## License

Academic project for CS4031 - Compiler Construction

---

**Team:** 3 Members  
**Semester:** Fall 2025  
**Institution:** [Your University]


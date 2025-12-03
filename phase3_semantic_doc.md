# Phase 3: Semantic Analyzer - Complete Documentation

## 1. Introduction

The **Semantic Analyzer** is the third phase of the compiler. While the parser checks syntactic correctness, semantic analysis ensures the program makes **logical and physical sense**.

### Purpose
- Build and maintain a **Symbol Table**
- Check variable declarations and usage
- Validate gate input/output counts
- Detect combinational feedback loops (cycles)
- Perform type checking (though our language has only boolean types)
- Report semantic errors with detailed messages

---

## 2. Semantic Rules Specification

### Rule Categories

| Category | Rule | Example Error |
|----------|------|---------------|
| **Declaration** | All identifiers must be declared before use | Using `X` in a gate without declaring it |
| **Definition** | Every OUTPUT must have a source gate | OUTPUT `Z` never assigned |
| **Uniqueness** | No duplicate declarations | Declaring `A` twice as INPUT |
| **Argument Count** | Gates must have correct number of inputs | `NOT(A, B)` - NOT takes only 1 input |
| **Cycles** | No combinational loops | `A = NOT(A)` creates a loop |
| **Categories** | INPUT/OUTPUT/WIRE usage must be valid | Cannot assign to an INPUT |

---

## 3. Symbol Table Structure

### Symbol Table Definition

The symbol table is a dictionary mapping identifiers to their properties:

```python
symbol_table = {
    "A": {
        "category": "INPUT",      # INPUT, OUTPUT, or WIRE
        "defined": True,          # Has a value/source?
        "source": None,           # Which gate produces it?
        "line": 2,                # Declared at line
        "usedBy": ["Sum", "Carry"]  # Which gates use it?
    },
    "Sum": {
        "category": "OUTPUT",
        "defined": True,
        "source": Gate("Sum", "XOR", ["A", "B"]),
        "line": 4,
        "usedBy": []
    }
}
```

### Symbol Table Example

**For Circuit:**
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

**Symbol Table:**

| Identifier | Category | Defined | Source Gate | Used By |
|------------|----------|---------|-------------|---------|
| A | INPUT | True | None (primary input) | Sum, Carry |
| B | INPUT | True | None (primary input) | Sum, Carry |
| Sum | OUTPUT | True | XOR(A, B) | None |
| Carry | OUTPUT | True | AND(A, B) | None |

---

## 4. Semantic Checks Implementation

### Check 1: Declaration Before Use

**Rule:** Every identifier used in a gate must be declared.

```python
def check_declarations(ast, symbol_table):
    errors = []
    
    for gate in ast.gates:
        # Check all input identifiers
        for input_id in gate.inputs:
            if input_id not in symbol_table:
                errors.append(
                    f"Semantic Error: Undeclared identifier '{input_id}' "
                    f"used in gate '{gate.output}'"
                )
    
    return errors
```

**Test Cases:**

✗ **Error Case:**
```
CIRCUIT Bad {
  OUTPUT Z;
  Z = AND(A, B);  // A and B not declared
}
```
**Error:** `Undeclared identifier 'A' used in gate 'Z'`

✓ **Valid Case:**
```
CIRCUIT Good {
  INPUT A, B;
  OUTPUT Z;
  Z = AND(A, B);
}
```

---

### Check 2: Output Definition

**Rule:** Every OUTPUT must be assigned a value.

```python
def check_output_definitions(ast, symbol_table):
    errors = []
    
    for decl in ast.declarations:
        if decl.category == "OUTPUT":
            for output_id in decl.identifiers:
                if not symbol_table[output_id].get("defined", False):
                    errors.append(
                        f"Semantic Error: OUTPUT '{output_id}' is never assigned"
                    )
    
    return errors
```

**Test Cases:**

✗ **Error Case:**
```
CIRCUIT Bad {
  INPUT A;
  OUTPUT Z;
  // Z never assigned!
}
```
**Error:** `OUTPUT 'Z' is never assigned`

✓ **Valid Case:**
```
CIRCUIT Good {
  INPUT A;
  OUTPUT Z;
  Z = NOT(A);
}
```

---

### Check 3: Duplicate Declarations

**Rule:** Each identifier can only be declared once.

```python
def check_duplicates(ast):
    errors = []
    seen = {}
    
    for decl in ast.declarations:
        for identifier in decl.identifiers:
            if identifier in seen:
                errors.append(
                    f"Semantic Error: Identifier '{identifier}' "
                    f"already declared as {seen[identifier]} on line {decl.line}"
                )
            else:
                seen[identifier] = decl.category
    
    return errors
```

**Test Cases:**

✗ **Error Case:**
```
CIRCUIT Bad {
  INPUT A;
  INPUT A;  // Duplicate!
  OUTPUT Z;
}
```
**Error:** `Identifier 'A' already declared as INPUT`

✓ **Valid Case:**
```
CIRCUIT Good {
  INPUT A, B;  // Multiple in one declaration is OK
  OUTPUT Z;
}
```

---

### Check 4: Gate Argument Validation

**Rule:** Each gate type requires specific number of inputs.

```python
def check_gate_arguments(ast):
    errors = []
    
    # Define required input counts
    gate_requirements = {
        "NOT": 1,
        "AND": 2,
        "OR": 2,
        "XOR": 2,
        "NAND": 2,
        "NOR": 2
    }
    
    for gate in ast.gates:
        required = gate_requirements.get(gate.gate_type)
        actual = len(gate.inputs)
        
        if required and actual != required:
            errors.append(
                f"Semantic Error: Gate {gate.gate_type} requires "
                f"{required} input(s), but {actual} provided in '{gate.output}'"
            )
    
    return errors
```

**Test Cases:**

✗ **Error Cases:**
```
// NOT with 2 inputs
Z = NOT(A, B);
Error: Gate NOT requires 1 input(s), but 2 provided

// AND with 1 input
Z = AND(A);
Error: Gate AND requires 2 input(s), but 1 provided

// XOR with 3 inputs
Z = XOR(A, B, C);
Error: Gate XOR requires 2 input(s), but 3 provided
```

✓ **Valid Cases:**
```
Z1 = NOT(A);
Z2 = AND(A, B);
Z3 = XOR(A, B);
```

---

### Check 5: Cycle Detection (Critical!)

**Rule:** Combinational circuits cannot have feedback loops.

**Why?** A loop like `A = NOT(A)` creates undefined behavior - the value oscillates infinitely.

#### Algorithm: Depth-First Search (DFS)

```python
def detect_cycles(symbol_table):
    """
    Use DFS with recursion stack to detect cycles.
    Returns list of error messages.
    """
    errors = []
    visited = set()
    rec_stack = set()
    
    def dfs(node, path):
        if node in rec_stack:
            # Found a cycle!
            cycle_path = " -> ".join(path + [node])
            errors.append(
                f"Semantic Error: Combinational loop detected: {cycle_path}"
            )
            return True
        
        if node in visited:
            return False
        
        visited.add(node)
        rec_stack.add(node)
        
        # Visit all dependencies
        node_info = symbol_table.get(node, {})
        if node_info.get("source"):
            gate = node_info["source"]
            for input_node in gate.inputs:
                if dfs(input_node, path + [node]):
                    return True
        
        rec_stack.remove(node)
        return False
    
    # Check all nodes
    for identifier in symbol_table:
        if identifier not in visited:
            dfs(identifier, [])
    
    return errors
```

**Test Cases:**

✗ **Error Case 1: Direct Loop**
```
CIRCUIT Bad {
  WIRE A;
  A = NOT(A);  // A depends on itself!
}
```
**Error:** `Combinational loop detected: A -> A`

✗ **Error Case 2: Indirect Loop**
```
CIRCUIT Bad {
  WIRE A, B, C;
  A = NOT(B);
  B = NOT(C);
  C = NOT(A);  // Loop: A -> B -> C -> A
}
```
**Error:** `Combinational loop detected: A -> B -> C -> A`

✗ **Error Case 3: Complex Loop**
```
CIRCUIT Bad {
  INPUT X;
  WIRE A, B;
  OUTPUT Z;
  A = AND(X, B);
  B = OR(A, X);  // A and B depend on each other
  Z = A;
}
```
**Error:** `Combinational loop detected: A -> B -> A`

✓ **Valid Case: No Loop**
```
CIRCUIT Good {
  INPUT A, B;
  WIRE temp;
  OUTPUT Z;
  temp = AND(A, B);
  Z = NOT(temp);  // No cycle - linear dependency
}
```

#### Visual Dependency Graph

**For Valid Circuit:**
```
A ──┐
    ├──> temp ──> Z
B ──┘
```
(Directed Acyclic Graph - DAG)

**For Invalid Circuit (Loop):**
```
    ┌──────┐
    │      ↓
    A ───> B
    ↑      │
    └──────┘
```
(Contains cycle)

---

### Check 6: Category Validation

**Rule:** Cannot assign to INPUTs.

```python
def check_input_assignment(ast, symbol_table):
    errors = []
    
    for gate in ast.gates:
        if gate.output in symbol_table:
            if symbol_table[gate.output]["category"] == "INPUT":
                errors.append(
                    f"Semantic Error: Cannot assign to INPUT '{gate.output}'"
                )
    
    return errors
```

**Test Case:**

✗ **Error Case:**
```
CIRCUIT Bad {
  INPUT A;
  A = NOT(A);  // Cannot modify input!
}
```
**Error:** `Cannot assign to INPUT 'A'`

---

## 5. Complete Semantic Analyzer Implementation

```python
class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
        self.errors = []
    
    def build_symbol_table(self):
        """Phase 1: Build initial symbol table from declarations"""
        for decl in self.ast.declarations:
            for identifier in decl.identifiers:
                if identifier in self.symbol_table:
                    self.errors.append(
                        f"Semantic Error: Duplicate declaration of '{identifier}'"
                    )
                else:
                    self.symbol_table[identifier] = {
                        "category": decl.category,
                        "defined": decl.category != "OUTPUT",
                        "source": None,
                        "usedBy": []
                    }
    
    def populate_gate_info(self):
        """Phase 2: Add gate information to symbol table"""
        for gate in self.ast.gates:
            # Add output to symbol table if not already there
            if gate.output not in self.symbol_table:
                self.symbol_table[gate.output] = {
                    "category": "WIRE",
                    "defined": True,
                    "source": gate,
                    "usedBy": []
                }
            else:
                # Mark as defined and set source
                self.symbol_table[gate.output]["defined"] = True
                self.symbol_table[gate.output]["source"] = gate
            
            # Track usage
            for input_id in gate.inputs:
                if input_id in self.symbol_table:
                    self.symbol_table[input_id]["usedBy"].append(gate.output)
    
    def check_declarations(self):
        """Check all identifiers are declared"""
        for gate in self.ast.gates:
            for input_id in gate.inputs:
                if input_id not in self.symbol_table:
                    self.errors.append(
                        f"Semantic Error: Undeclared identifier '{input_id}' "
                        f"in gate '{gate.output}'"
                    )
    
    def check_gate_arguments(self):
        """Validate gate input counts"""
        requirements = {
            "NOT": 1, "AND": 2, "OR": 2,
            "XOR": 2, "NAND": 2, "NOR": 2
        }
        
        for gate in self.ast.gates:
            required = requirements.get(gate.gate_type, None)
            actual = len(gate.inputs)
            
            if required and actual != required:
                self.errors.append(
                    f"Semantic Error: {gate.gate_type} requires {required} "
                    f"input(s), got {actual} in gate '{gate.output}'"
                )
    
    def check_output_definitions(self):
        """Ensure all OUTPUTs are assigned"""
        for identifier, info in self.symbol_table.items():
            if info["category"] == "OUTPUT" and not info["defined"]:
                self.errors.append(
                    f"Semantic Error: OUTPUT '{identifier}' never assigned"
                )
    
    def check_input_assignments(self):
        """Ensure INPUTs are not assigned to"""
        for gate in self.ast.gates:
            if gate.output in self.symbol_table:
                if self.symbol_table[gate.output]["category"] == "INPUT":
                    self.errors.append(
                        f"Semantic Error: Cannot assign to INPUT '{gate.output}'"
                    )
    
    def detect_cycles(self):
        """Detect combinational feedback loops using DFS"""
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                cycle = " -> ".join(path + [node])
                self.errors.append(
                    f"Semantic Error: Cycle detected: {cycle}"
                )
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            info = self.symbol_table.get(node, {})
            if info.get("source"):
                for input_node in info["source"].inputs:
                    if dfs(input_node, path + [node]):
                        return True
            
            rec_stack.remove(node)
            return False
        
        for identifier in self.symbol_table:
            if identifier not in visited:
                dfs(identifier, [])
    
    def analyze(self):
        """Run all semantic checks"""
        # Phase 1: Build symbol table
        self.build_symbol_table()
        self.populate_gate_info()
        
        # Phase 2: Run all checks
        self.check_declarations()
        self.check_gate_arguments()
        self.check_output_definitions()
        self.check_input_assignments()
        self.detect_cycles()
        
        return {
            "symbol_table": self.symbol_table,
            "errors": self.errors,
            "success": len(self.errors) == 0
        }

# Usage
if __name__ == "__main__":
    # Assume we have an AST from Phase 2
    analyzer = SemanticAnalyzer(ast)
    result = analyzer.analyze()
    
    if result["success"]:
        print("✓ Semantic analysis passed!")
        print("Symbol Table:", result["symbol_table"])
    else:
        print("✗ Semantic errors found:")
        for error in result["errors"]:
            print(f"  {error}")
```

---

## 6. Comprehensive Test Cases

### Test Case 1: Perfect Half Adder
**Input:**
```
CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}
```

**Expected:** ✓ PASS (No errors)

**Symbol Table:**
```
{
  "A": {"category": "INPUT", "defined": True, "usedBy": ["Sum", "Carry"]},
  "B": {"category": "INPUT", "defined": True, "usedBy": ["Sum", "Carry"]},
  "Sum": {"category": "OUTPUT", "defined": True, "source": XOR(A,B)},
  "Carry": {"category": "OUTPUT", "defined": True, "source": AND(A,B)}
}
```

---

### Test Case 2: Undeclared Variable
**Input:**
```
CIRCUIT Bad {
  INPUT A;
  OUTPUT Z;
  Z = AND(A, B);  // B not declared
}
```

**Expected:** ✗ ERROR
```
Semantic Error: Undeclared identifier 'B' in gate 'Z'
```

---

### Test Case 3: Undefined Output
**Input:**
```
CIRCUIT Bad {
  INPUT A;
  OUTPUT Z, Y;
  Z = NOT(A);
  // Y never assigned!
}
```

**Expected:** ✗ ERROR
```
Semantic Error: OUTPUT 'Y' never assigned
```

---

### Test Case 4: Wrong Argument Count
**Input:**
```
CIRCUIT Bad {
  INPUT A, B;
  OUTPUT Z;
  Z = NOT(A, B);  // NOT takes 1 input, not 2
}
```

**Expected:** ✗ ERROR
```
Semantic Error: NOT requires 1 input(s), got 2 in gate 'Z'
```

---

### Test Case 5: Self-Loop
**Input:**
```
CIRCUIT Bad {
  WIRE X;
  X = NOT(X);
}
```

**Expected:** ✗ ERROR
```
Semantic Error: Cycle detected: X -> X
```

---

### Test Case 6: Multi-Node Cycle
**Input:**
```
CIRCUIT Bad {
  WIRE A, B, C;
  A = NOT(C);
  B = AND(A, A);
  C = OR(B, B);
}
```

**Expected:** ✗ ERROR
```
Semantic Error: Cycle detected: A -> C -> B -> A
```

---

### Test Case 7: Assigning to Input
**Input:**
```
CIRCUIT Bad {
  INPUT A;
  OUTPUT Z;
  A = NOT(A);
  Z = A;
}
```

**Expected:** ✗ ERROR
```
Semantic Error: Cannot assign to INPUT 'A'
```

---

### Test Case 8: Complex Valid Circuit
**Input:**
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

**Expected:** ✓ PASS (No cycles, all defined)

---

### Test Case 9: Multiple Errors
**Input:**
```
CIRCUIT MultiError {
  INPUT A;
  OUTPUT Z;
  Z = AND(A, B);     // B undeclared
  A = NOT(A);        // Cannot assign to INPUT
  Y = XOR(A, A, A);  // Y undeclared OUTPUT, XOR takes 2 inputs
}
```

**Expected:** ✗ MULTIPLE ERRORS
```
Semantic Error: Undeclared identifier 'B' in gate 'Z'
Semantic Error: Cannot assign to INPUT 'A'
Semantic Error: XOR requires 2 input(s), got 3 in gate 'Y'
Semantic Error: OUTPUT 'Y' never assigned (if Y was declared)
```

---

## 7. Cycle Detection: Advanced Cases

### Case 1: Hidden Cycle Through Multiple Paths
```
CIRCUIT Tricky {
  INPUT X;
  WIRE A, B, C, D;
  OUTPUT Z;
  
  A = AND(X, D);
  B = OR(A, X);
  C = XOR(B, X);
  D = NOT(C);     // D depends on A, which depends on D
  Z = C;
}
```
**Dependency Graph:**
```
X → A → B → C → D → (back to A)
```
**Error:** Cycle: `A -> B -> C -> D -> A`

---

### Case 2: Partial Cycle (Some paths valid)
```
CIRCUIT Partial {
  INPUT X, Y;
  WIRE A, B;
  OUTPUT Z;
  
  A = OR(B, Y);    // A depends on B
  B = AND(A, X);   // B depends on A - CYCLE!
  Z = NOT(X);      // Z path is fine
}
```
**Error:** Even though Z is fine, the circuit still has cycle: `A -> B -> A`

---

## 8. Performance Analysis

### Time Complexity

| Check | Complexity | Explanation |
|-------|------------|-------------|
| Build Symbol Table | O(d) | d = number of declarations |
| Declaration Check | O(g × i) | g = gates, i = inputs per gate |
| Argument Check | O(g) | One pass through gates |
| Cycle Detection | O(V + E) | V = nodes, E = edges (DFS) |
| **Total** | **O(V + E)** | Dominated by cycle detection |

### Space Complexity
- **O(V)** for symbol table
- **O(V)** for visited/recursion stack
- **O(E)** for dependency edges

---

## 9. Integration with Phase 4

```python
# Phase 3 Output → Phase 4 Input
result = semantic_analyzer.analyze()

if result["success"]:
    # Pass validated AST and symbol table to ICG
    icg = IntermediateCodeGenerator(ast, result["symbol_table"])
    quads = icg.generate()
else:
    print("Cannot proceed: Semantic errors exist")
```

---

## 10. Deliverables Checklist

- [x] Symbol table structure definition
- [x] **Sample symbol table** (hand-drawn or formatted)
- [x] All 6 semantic checks implemented
- [x] Cycle detection with DFS algorithm
- [x] 9+ comprehensive test cases
- [x] Edge case analysis
- [x] Error message formatting
- [x] Performance analysis

---

## 11. References

1. **Compilers: Principles, Techniques, and Tools** - Chapter 6: Semantic Analysis
2. **Introduction to Algorithms** - Chapter 22: Graph Algorithms (for DFS)
3. **Engineering a Compiler** - Section 4.3: Type Checking

---

**End of Phase 3 Documentation**

**Next Phase:** [Phase 4: Intermediate Code Generation](./phase4_icg.md)
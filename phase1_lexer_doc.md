# Phase 1: Lexical Analyzer - Complete Documentation

## 1. Introduction

The **Lexical Analyzer** (Scanner/Tokenizer) is the first phase of the compiler. It reads the source code character by character and groups them into meaningful units called **tokens**.

### Purpose
- Convert raw source code into a stream of tokens
- Identify keywords, identifiers, operators, and symbols
- Report lexical errors (invalid characters)
- Track line and column numbers for error reporting

---

## 2. Token Specification

### Token Types

| Token Type | Description | Example |
|------------|-------------|---------|
| `KEYWORD` | Reserved words | `CIRCUIT`, `INPUT`, `OUTPUT`, `WIRE`, `AND`, `OR`, `XOR`, `NOT`, `NAND`, `NOR` |
| `IDENTIFIER` | User-defined names | `A`, `Sum`, `Carry_Out`, `Wire_1` |
| `LBRACE` | Left brace | `{` |
| `RBRACE` | Right brace | `}` |
| `LPAREN` | Left parenthesis | `(` |
| `RPAREN` | Right parenthesis | `)` |
| `SEMICOLON` | Statement terminator | `;` |
| `COMMA` | List separator | `,` |
| `EQUALS` | Assignment operator | `=` |
| `WHITESPACE` | Spaces, tabs (ignored) | ` `, `\t` |
| `NEWLINE` | Line breaks (ignored but counted) | `\n` |

---

## 3. Regular Expressions (Regex Patterns)

### Pattern Definitions

```regex
KEYWORD      := (CIRCUIT|INPUT|OUTPUT|WIRE|AND|OR|XOR|NAND|NOR|NOT)\b
IDENTIFIER   := [a-zA-Z_][a-zA-Z0-9_]*
LBRACE       := \{
RBRACE       := \}
LPAREN       := \(
RPAREN       := \)
SEMICOLON    := ;
COMMA        := ,
EQUALS       := =
WHITESPACE   := \s+
NEWLINE      := \n
```

### Pattern Priority
**Important:** Patterns must be checked in order of precedence:
1. **KEYWORD** (must come before IDENTIFIER to avoid "AND" being tokenized as identifier)
2. **IDENTIFIER**
3. **Symbols** (braces, parentheses, etc.)
4. **WHITESPACE** (ignored)

---

## 4. DFA (Deterministic Finite Automaton) Artifact

### Hand-Drawn DFA for IDENTIFIER Recognition

```
State Diagram for IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*

     [a-z, A-Z, _]       [a-z, A-Z, 0-9, _]
    ┌────────────┐      ┌─────────────────┐
    │            │      │                 │
    │            ▼      │                 ▼
   (0)───────>(1)◄──────┘               ((2))
  START      Letter/                   ACCEPT
            Underscore                 (Final State)
                │
                └─────────────────────►((2))
                   [other chars]        ACCEPT
```

**State Descriptions:**
- **State 0 (Start):** Waiting for first character
- **State 1 (Letter seen):** First character is letter or underscore
- **State 2 (Accept):** Valid identifier formed, can continue with letters/digits/underscores

**Transition Rules:**
- From State 0: If `[a-zA-Z_]` → go to State 1
- From State 1: If `[a-zA-Z0-9_]` → stay in State 1 (loop)
- From State 1: If other character → go to State 2 (Accept and stop)
- State 2 is the **final accepting state**

---

## 5. Algorithm: Tokenization Process

### Pseudocode

```
function tokenize(source_code):
    tokens = []
    position = 0
    line = 1
    column = 1
    
    while position < length(source_code):
        matched = false
        
        for each token_pattern in patterns:
            match = try_match(source_code[position:], token_pattern)
            
            if match:
                if token_pattern is not WHITESPACE or NEWLINE:
                    token = {
                        type: token_pattern.type,
                        value: match.text,
                        line: line,
                        column: column
                    }
                    tokens.append(token)
                
                position += length(match.text)
                
                if token_pattern is NEWLINE:
                    line += 1
                    column = 1
                else:
                    column += length(match.text)
                
                matched = true
                break
        
        if not matched:
            throw LexicalError("Unexpected character at line " + line + ", column " + column)
    
    return tokens
```

### Step-by-Step Example

**Input:**
```
INPUT A, B;
```

**Tokenization Steps:**

| Step | Position | Character(s) | Match Pattern | Token Generated |
|------|----------|--------------|---------------|-----------------|
| 1 | 0 | `INPUT` | KEYWORD | `{type: KEYWORD, value: "INPUT", line: 1, col: 1}` |
| 2 | 5 | ` ` | WHITESPACE | (ignored) |
| 3 | 6 | `A` | IDENTIFIER | `{type: IDENTIFIER, value: "A", line: 1, col: 7}` |
| 4 | 7 | `,` | COMMA | `{type: COMMA, value: ",", line: 1, col: 8}` |
| 5 | 8 | ` ` | WHITESPACE | (ignored) |
| 6 | 9 | `B` | IDENTIFIER | `{type: IDENTIFIER, value: "B", line: 1, col: 10}` |
| 7 | 10 | `;` | SEMICOLON | `{type: SEMICOLON, value: ";", line: 1, col: 11}` |

---

## 6. Python Implementation

```python
import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', L{self.line}:C{self.column})"

class Lexer:
    def __init__(self):
        # Token patterns (ORDER MATTERS!)
        self.token_patterns = [
            ('KEYWORD', r'\b(CIRCUIT|INPUT|OUTPUT|WIRE|AND|OR|XOR|NAND|NOR|NOT)\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMICOLON', r';'),
            ('COMMA', r','),
            ('EQUALS', r'='),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n'),
        ]
        
        # Compile regex patterns
        self.compiled_patterns = [
            (name, re.compile(pattern)) 
            for name, pattern in self.token_patterns
        ]
    
    def tokenize(self, source_code):
        tokens = []
        position = 0
        line = 1
        column = 1
        
        while position < len(source_code):
            matched = False
            
            for token_type, pattern in self.compiled_patterns:
                match = pattern.match(source_code, position)
                
                if match:
                    value = match.group(0)
                    
                    # Don't create tokens for whitespace/newlines
                    if token_type not in ('WHITESPACE', 'NEWLINE'):
                        token = Token(token_type, value, line, column)
                        tokens.append(token)
                    
                    # Update position
                    position = match.end()
                    
                    # Update line/column tracking
                    if token_type == 'NEWLINE':
                        line += 1
                        column = 1
                    else:
                        column += len(value)
                    
                    matched = True
                    break
            
            if not matched:
                raise SyntaxError(
                    f"Lexical Error at line {line}, column {column}: "
                    f"Unexpected character '{source_code[position]}'"
                )
        
        return tokens

# Usage Example
if __name__ == "__main__":
    source = """
    CIRCUIT HalfAdder {
        INPUT A, B;
        OUTPUT Sum, Carry;
        Sum = XOR(A, B);
        Carry = AND(A, B);
    }
    """
    
    lexer = Lexer()
    tokens = lexer.tokenize(source)
    
    for token in tokens:
        print(token)
```

---

## 7. Test Cases

### Test Case 1: Basic Declaration
**Input:**
```
INPUT A;
```

**Expected Output:**
```
Token(KEYWORD, 'INPUT', L1:C1)
Token(IDENTIFIER, 'A', L1:C7)
Token(SEMICOLON, ';', L1:C8)
```

---

### Test Case 2: Complete Circuit
**Input:**
```
CIRCUIT Test {
  INPUT A, B;
  OUTPUT Z;
  Z = AND(A, B);
}
```

**Expected Output:**
```
Token(KEYWORD, 'CIRCUIT', L1:C1)
Token(IDENTIFIER, 'Test', L1:C9)
Token(LBRACE, '{', L1:C14)
Token(KEYWORD, 'INPUT', L2:C3)
Token(IDENTIFIER, 'A', L2:C9)
Token(COMMA, ',', L2:C10)
Token(IDENTIFIER, 'B', L2:C12)
Token(SEMICOLON, ';', L2:C13)
Token(KEYWORD, 'OUTPUT', L3:C3)
Token(IDENTIFIER, 'Z', L3:C10)
Token(SEMICOLON, ';', L3:C11)
Token(IDENTIFIER, 'Z', L4:C3)
Token(EQUALS, '=', L4:C5)
Token(KEYWORD, 'AND', L4:C7)
Token(LPAREN, '(', L4:C10)
Token(IDENTIFIER, 'A', L4:C11)
Token(COMMA, ',', L4:C12)
Token(IDENTIFIER, 'B', L4:C14)
Token(RPAREN, ')', L4:C15)
Token(SEMICOLON, ';', L4:C16)
Token(RBRACE, '}', L5:C1)
```

---

### Test Case 3: Invalid Character Error
**Input:**
```
INPUT A @ B;
```

**Expected Output:**
```
ERROR: Lexical Error at line 1, column 9: Unexpected character '@'
```

---

### Test Case 4: Complex Identifiers
**Input:**
```
WIRE Sum_Final, Carry_Out_1, temp_123;
```

**Expected Output:**
```
Token(KEYWORD, 'WIRE', L1:C1)
Token(IDENTIFIER, 'Sum_Final', L1:C6)
Token(COMMA, ',', L1:C15)
Token(IDENTIFIER, 'Carry_Out_1', L1:C17)
Token(COMMA, ',', L1:C28)
Token(IDENTIFIER, 'temp_123', L1:C30)
Token(SEMICOLON, ';', L1:C38)
```

---

### Test Case 5: All Gate Types
**Input:**
```
X1 = AND(A, B);
X2 = OR(A, B);
X3 = XOR(A, B);
X4 = NOT(A);
X5 = NAND(A, B);
X6 = NOR(A, B);
```

**Expected Tokens:** (Abbreviated)
```
Each line should produce:
- IDENTIFIER (output)
- EQUALS
- KEYWORD (gate type)
- LPAREN
- IDENTIFIER(s)
- COMMA (if 2 inputs)
- RPAREN
- SEMICOLON
```

---

## 8. Edge Cases & Error Handling

### Edge Case 1: Keyword vs Identifier
**Input:** `ANDROID = AND(A, B);`

**Expected:** 
- `ANDROID` should be tokenized as **IDENTIFIER** (not keyword)
- This is because our keyword pattern uses `\b` word boundary

### Edge Case 2: Empty Lines
**Input:**
```
INPUT A;

OUTPUT Z;
```

**Expected:** Newlines are tracked but not tokenized. Line numbers should increment correctly.

### Edge Case 3: No Whitespace
**Input:** `INPUT A,B;`

**Expected:** Should work correctly (whitespace is optional between most tokens)

### Edge Case 4: Leading/Trailing Whitespace
**Input:** `   INPUT A;   \n`

**Expected:** Whitespace ignored, correct tokens generated

---

## 9. Performance Analysis

### Time Complexity
- **O(n × m)** where:
  - n = length of source code
  - m = number of token patterns
- In practice, patterns match quickly (usually first few patterns)

### Space Complexity
- **O(t)** where t = number of tokens
- Additional O(1) for position tracking variables

---

## 10. Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Unexpected character '@'` | Invalid character in source | Remove or replace invalid character |
| Keyword treated as identifier | Pattern order wrong | Place KEYWORD pattern before IDENTIFIER |
| Wrong line/column numbers | Newline tracking incorrect | Ensure line increments and column resets on `\n` |
| Missing tokens | Pattern doesn't match | Check regex pattern syntax |

---

## 11. Integration with Phase 2

The lexer outputs a **token stream** that feeds directly into the Parser:

```python
# Phase 1 Output → Phase 2 Input
tokens = lexer.tokenize(source_code)
parser = Parser(tokens)  # Phase 2 begins
ast = parser.parse()
```

---

## 12. Deliverables Checklist

- [x] Token specification table
- [x] Regular expression patterns
- [x] **Hand-drawn DFA for IDENTIFIER** (submit as image/PDF)
- [x] Complete Python implementation
- [x] 5+ comprehensive test cases
- [x] Edge case analysis
- [x] Error handling examples

---

## 13. References & Further Reading

1. **Compilers: Principles, Techniques, and Tools** (Dragon Book) - Chapter 3: Lexical Analysis
2. **Engineering a Compiler** - Section 2.2: Scanners
3. Python `re` module documentation: https://docs.python.org/3/library/re.html

---

**End of Phase 1 Documentation**

**Next Phase:** [Phase 2: Syntax Analysis (Parser)](./phase2_parser.md)
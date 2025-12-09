"""
Phase 2: Syntax Analyzer
Parses tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Dict, Any
from lexer import Token


class ASTNode:
    """Base class for AST nodes."""
    pass


class Program(ASTNode):
    """Represents a complete program."""
    
    def __init__(self, name: str, declarations: List, gates: List):
        self.name = name
        self.declarations = declarations
        self.gates = gates
    
    def __repr__(self):
        return f"Program(name='{self.name}', declarations={len(self.declarations)}, gates={len(self.gates)})"


class Declaration(ASTNode):
    """Represents a declaration (INPUT, OUTPUT, or WIRE)."""
    
    def __init__(self, category: str, identifiers: List[str]):
        self.category = category
        self.identifiers = identifiers
    
    def __repr__(self):
        return f"Declaration({self.category}, {self.identifiers})"


class Gate(ASTNode):
    """Represents a gate assignment."""
    
    def __init__(self, output: str, gate_type: str, inputs: List[str]):
        self.output = output
        self.gate_type = gate_type
        self.inputs = inputs
    
    def __repr__(self):
        return f"Gate({self.output} = {self.gate_type}({', '.join(self.inputs)}))"


class Parser:
    """Recursive descent parser for Logic Gate Architect DSL."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def peek(self) -> Optional[Token]:
        """Look at current token without consuming it."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def advance(self) -> Token:
        """Consume and return current token."""
        token = self.tokens[self.current]
        self.current += 1
        return token
    
    def match(self, *types: str) -> Optional[Token]:
        """Try to match one of the given token types."""
        if self.peek() and self.peek().type in types:
            return self.advance()
        return None
    
    def expect(self, type: str) -> Token:
        """Expect a specific token type, raise error if not found."""
        token = self.match(type)
        if not token:
            peek = self.peek()
            raise SyntaxError(
                f"Parse Error: Expected {type} but got {peek.type if peek else 'EOF'} "
                f"at line {peek.line if peek else 'unknown'}, column {peek.column if peek else 'unknown'}"
            )
        return token
    
    def parse_program(self) -> Program:
        """Parse a complete program."""
        # CIRCUIT identifier { declarations gates }
        self.expect('KEYWORD')  # CIRCUIT
        name_token = self.expect('IDENTIFIER')
        self.expect('LBRACE')
        
        declarations = self.parse_declarations()
        gates = self.parse_gates()
        
        self.expect('RBRACE')
        
        return Program(name_token.value, declarations, gates)
    
    def parse_declarations(self) -> List[Declaration]:
        """Parse zero or more declarations."""
        declarations = []
        
        while (self.peek() and 
               self.peek().type == 'KEYWORD' and 
               self.peek().value in ['INPUT', 'OUTPUT', 'WIRE']):
            keyword = self.advance()
            identifiers = self.parse_identifier_list()
            self.expect('SEMICOLON')
            
            declarations.append(Declaration(keyword.value, identifiers))
        
        return declarations
    
    def parse_identifier_list(self) -> List[str]:
        """Parse a comma-separated list of identifiers."""
        identifiers = [self.expect_identifier().value]
        
        while self.match('COMMA'):
            identifiers.append(self.expect_identifier().value)
        
        return identifiers
    
    def expect_identifier(self) -> Token:
        """Expect an identifier, provide helpful error if gate keyword found."""
        token = self.match('IDENTIFIER')
        if not token:
            peek = self.peek()
            if peek and peek.type == 'KEYWORD' and peek.value in ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'NOT']:
                raise SyntaxError(
                    f"Parse Error at line {peek.line}, column {peek.column}: "
                    f"Nested gate calls are not supported. "
                    f"Found gate '{peek.value}' where an identifier was expected. "
                    f"Please use intermediate WIRE variables instead of nesting gates like '{peek.value}(...)'."
                )
            else:
                raise SyntaxError(
                    f"Parse Error: Expected IDENTIFIER but got {peek.type if peek else 'EOF'} "
                    f"at line {peek.line if peek else 'unknown'}, column {peek.column if peek else 'unknown'}"
                )
        return token
    
    def parse_gates(self) -> List[Gate]:
        """Parse zero or more gate assignments."""
        gates = []
        
        while self.peek() and self.peek().type == 'IDENTIFIER':
            output = self.expect('IDENTIFIER').value
            self.expect('EQUALS')
            gate_type_token = self.expect('KEYWORD')
            self.expect('LPAREN')
            inputs = self.parse_identifier_list()
            self.expect('RPAREN')
            self.expect('SEMICOLON')
            
            gates.append(Gate(output, gate_type_token.value, inputs))
        
        return gates
    
    def parse(self) -> Program:
        """Main parse method."""
        return self.parse_program()


if __name__ == "__main__":
    from lexer import Lexer
    
    test_code = """
    CIRCUIT HalfAdder {
        INPUT A, B;
        OUTPUT Sum, Carry;
        Sum = XOR(A, B);
        Carry = AND(A, B);
    }
    """
    
    lexer = Lexer()
    tokens = lexer.tokenize(test_code)
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("AST generated:")
    print(ast)
    print("\nDeclarations:")
    for decl in ast.declarations:
        print(f"  {decl}")
    print("\nGates:")
    for gate in ast.gates:
        print(f"  {gate}")


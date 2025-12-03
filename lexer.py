"""
Phase 1: Lexical Analyzer
Tokenizes source code into a stream of tokens.
"""

import re
from typing import List, Optional


class Token:
    """Represents a token with type, value, and position information."""
    
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', L{self.line}:C{self.column})"


class Lexer:
    """Lexical analyzer for Logic Gate Architect DSL."""
    
    def __init__(self):
        # Token patterns in order of precedence (KEYWORD before IDENTIFIER)
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
    
    def tokenize(self, source_code: str) -> List[Token]:
        """
        Tokenize source code into a list of tokens.
        
        Args:
            source_code: Input source code string
            
        Returns:
            List of Token objects
            
        Raises:
            SyntaxError: If an invalid character is encountered
        """
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


if __name__ == "__main__":
    # Test the lexer
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
    
    print("Tokens generated:")
    for token in tokens:
        print(token)


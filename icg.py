"""
Phase 4: Intermediate Code Generation
Generates quadruples (three-address code) from AST.
"""

from typing import List, Optional
from parser import Program, Gate


class Quadruple:
    """Represents a quadruple (three-address code instruction)."""
    
    def __init__(self, op: str, arg1: Optional[str], arg2: Optional[str], result: str):
        self.op = op  # Operation (AND, OR, XOR, NOT, etc.)
        self.arg1 = arg1  # First operand
        self.arg2 = arg2  # Second operand (None for unary operations)
        self.result = result  # Result variable
    
    def __repr__(self):
        if self.arg2 is None:
            return f"({self.op}, {self.arg1}, -, {self.result})"
        return f"({self.op}, {self.arg1}, {self.arg2}, {self.result})"


class IntermediateCodeGenerator:
    """Generates intermediate code (quadruples) from AST."""
    
    def __init__(self, ast: Program):
        self.ast = ast
        self.quads: List[Quadruple] = []
    
    def generate(self) -> List[Quadruple]:
        """Generate quadruples from AST."""
        for gate in self.ast.gates:
            if gate.gate_type == 'NOT':
                # Unary operation
                quad = Quadruple(
                    gate.gate_type,
                    gate.inputs[0],
                    None,
                    gate.output
                )
            else:
                # Binary operation
                quad = Quadruple(
                    gate.gate_type,
                    gate.inputs[0],
                    gate.inputs[1] if len(gate.inputs) > 1 else None,
                    gate.output
                )
            
            self.quads.append(quad)
        
        return self.quads
    
    def print_quads(self):
        """Pretty print quadruples."""
        print("Intermediate Code (Quadruples):")
        print("-" * 50)
        for i, quad in enumerate(self.quads, 1):
            print(f"{i}: {quad}")


if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    
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
    
    icg = IntermediateCodeGenerator(ast)
    quads = icg.generate()
    
    icg.print_quads()


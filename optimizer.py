"""
Phase 5: Code Optimizer
Optimizes intermediate code using constant folding, identity laws, and dead code elimination.
"""

from typing import List, Dict
from icg import Quadruple
from semantic import SymbolInfo


class Optimizer:
    """Optimizes quadruples using various techniques."""
    
    def __init__(self, quads: List[Quadruple], symbol_table: Dict[str, SymbolInfo]):
        self.quads = quads
        self.symbol_table = symbol_table
    
    def constant_folding(self, quad: Quadruple) -> Quadruple:
        """Apply constant folding rules."""
        if quad.op == 'AND':
            if quad.arg1 == '0' or quad.arg2 == '0':
                return Quadruple('ASSIGN', '0', None, quad.result)
            if quad.arg1 == '1':
                return Quadruple('ASSIGN', quad.arg2, None, quad.result)
            if quad.arg2 == '1':
                return Quadruple('ASSIGN', quad.arg1, None, quad.result)
        
        elif quad.op == 'OR':
            if quad.arg1 == '1' or quad.arg2 == '1':
                return Quadruple('ASSIGN', '1', None, quad.result)
            if quad.arg1 == '0':
                return Quadruple('ASSIGN', quad.arg2, None, quad.result)
            if quad.arg2 == '0':
                return Quadruple('ASSIGN', quad.arg1, None, quad.result)
        
        elif quad.op == 'XOR':
            if quad.arg1 == '0':
                return Quadruple('ASSIGN', quad.arg2, None, quad.result)
            if quad.arg2 == '0':
                return Quadruple('ASSIGN', quad.arg1, None, quad.result)
            if quad.arg1 == quad.arg2:
                return Quadruple('ASSIGN', '0', None, quad.result)
        
        return quad
    
    def algebraic_simplification(self, quad: Quadruple) -> Quadruple:
        """Apply algebraic identities."""
        # A AND A = A
        if quad.op == 'AND' and quad.arg1 == quad.arg2:
            return Quadruple('ASSIGN', quad.arg1, None, quad.result)
        
        # A OR A = A
        if quad.op == 'OR' and quad.arg1 == quad.arg2:
            return Quadruple('ASSIGN', quad.arg1, None, quad.result)
        
        # A XOR A = 0
        if quad.op == 'XOR' and quad.arg1 == quad.arg2:
            return Quadruple('ASSIGN', '0', None, quad.result)
        
        return quad
    
    def eliminate_dead_code(self, quads: List[Quadruple]) -> List[Quadruple]:
        """Remove unused computations."""
        used = set()
        
        # Mark all used variables
        for quad in quads:
            if quad.arg1:
                used.add(quad.arg1)
            if quad.arg2:
                used.add(quad.arg2)
        
        # Keep outputs and used results
        optimized = []
        for quad in quads:
            result_info = self.symbol_table.get(quad.result)
            is_output = result_info and result_info.category == 'OUTPUT'
            is_used = quad.result in used
            
            if is_output or is_used:
                optimized.append(quad)
        
        return optimized
    
    def optimize(self) -> List[Quadruple]:
        """Run all optimizations."""
        optimized = []
        
        # Pass 1: Constant folding and algebraic simplification
        for quad in self.quads:
            quad = self.constant_folding(quad)
            quad = self.algebraic_simplification(quad)
            optimized.append(quad)
        
        # Pass 2: Dead code elimination
        optimized = self.eliminate_dead_code(optimized)
        
        return optimized


if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    from semantic import SemanticAnalyzer
    from icg import IntermediateCodeGenerator
    
    test_code = """
    CIRCUIT Test {
        INPUT A;
        OUTPUT Z;
        WIRE temp1, temp2;
        temp1 = AND(A, 0);
        temp2 = OR(temp1, 0);
        Z = temp2;
    }
    """
    
    lexer = Lexer()
    tokens = lexer.tokenize(test_code)
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer(ast)
    result = analyzer.analyze()
    
    icg = IntermediateCodeGenerator(ast)
    quads = icg.generate()
    
    print("Before optimization:")
    for i, quad in enumerate(quads, 1):
        print(f"{i}: {quad}")
    
    optimizer = Optimizer(quads, result['symbol_table'])
    optimized = optimizer.optimize()
    
    print("\nAfter optimization:")
    for i, quad in enumerate(optimized, 1):
        print(f"{i}: {quad}")


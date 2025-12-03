"""
Phase 3: Semantic Analyzer
Performs semantic analysis including symbol table construction and cycle detection.
"""

from typing import Dict, List, Set, Optional
from parser import Program, Declaration, Gate


class SymbolInfo:
    """Information about a symbol in the symbol table."""
    
    def __init__(self, category: str, defined: bool = False, source: Optional[Gate] = None):
        self.category = category  # INPUT, OUTPUT, or WIRE
        self.defined = defined
        self.source = source  # Gate that produces this symbol
        self.used_by: List[str] = []  # List of gates that use this symbol
    
    def __repr__(self):
        return f"SymbolInfo(category={self.category}, defined={self.defined}, used_by={self.used_by})"


class SemanticAnalyzer:
    """Semantic analyzer for Logic Gate Architect DSL."""
    
    def __init__(self, ast: Program):
        self.ast = ast
        self.symbol_table: Dict[str, SymbolInfo] = {}
        self.errors: List[str] = []
    
    def build_symbol_table(self):
        """Build symbol table from declarations."""
        for decl in self.ast.declarations:
            for identifier in decl.identifiers:
                if identifier in self.symbol_table:
                    self.errors.append(
                        f"Semantic Error: Identifier '{identifier}' already declared"
                    )
                else:
                    self.symbol_table[identifier] = SymbolInfo(
                        category=decl.category,
                        defined=(decl.category != 'OUTPUT')  # INPUTs and WIREs are defined
                    )
    
    def populate_gate_info(self):
        """Add gate information to symbol table."""
        for gate in self.ast.gates:
            # Add output to symbol table if not already there
            if gate.output not in self.symbol_table:
                self.symbol_table[gate.output] = SymbolInfo(
                    category='WIRE',
                    defined=True,
                    source=gate
                )
            else:
                # Mark as defined and set source
                self.symbol_table[gate.output].defined = True
                self.symbol_table[gate.output].source = gate
            
            # Track usage
            for input_id in gate.inputs:
                if input_id in self.symbol_table:
                    self.symbol_table[input_id].used_by.append(gate.output)
    
    def check_declarations(self):
        """Check all identifiers are declared."""
        for gate in self.ast.gates:
            for input_id in gate.inputs:
                if input_id not in self.symbol_table:
                    self.errors.append(
                        f"Semantic Error: Undeclared identifier '{input_id}' "
                        f"used in gate '{gate.output}'"
                    )
    
    def check_gate_arguments(self):
        """Validate gate input counts."""
        requirements = {
            'NOT': 1,
            'AND': 2,
            'OR': 2,
            'XOR': 2,
            'NAND': 2,
            'NOR': 2,
        }
        
        for gate in self.ast.gates:
            required = requirements.get(gate.gate_type)
            actual = len(gate.inputs)
            
            if required and actual != required:
                self.errors.append(
                    f"Semantic Error: Gate {gate.gate_type} requires {required} "
                    f"input(s), got {actual} in gate '{gate.output}'"
                )
    
    def check_output_definitions(self):
        """Ensure all OUTPUTs are assigned."""
        for identifier, info in self.symbol_table.items():
            if info.category == 'OUTPUT' and not info.defined:
                self.errors.append(
                    f"Semantic Error: OUTPUT '{identifier}' never assigned"
                )
    
    def check_input_assignments(self):
        """Ensure INPUTs are not assigned to."""
        for gate in self.ast.gates:
            if gate.output in self.symbol_table:
                if self.symbol_table[gate.output].category == 'INPUT':
                    self.errors.append(
                        f"Semantic Error: Cannot assign to INPUT '{gate.output}'"
                    )
    
    def detect_cycles(self):
        """Detect combinational feedback loops using DFS."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        
        def dfs(node: str, path: List[str]) -> bool:
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
            
            info = self.symbol_table.get(node)
            if info and info.source:
                for input_node in info.source.inputs:
                    if dfs(input_node, path + [node]):
                        return True
            
            rec_stack.remove(node)
            return False
        
        for identifier in self.symbol_table:
            if identifier not in visited:
                dfs(identifier, [])
    
    def analyze(self) -> Dict:
        """Run all semantic checks."""
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
            'symbol_table': self.symbol_table,
            'errors': self.errors,
            'success': len(self.errors) == 0
        }


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
    
    analyzer = SemanticAnalyzer(ast)
    result = analyzer.analyze()
    
    if result['success']:
        print("✓ Semantic analysis passed!")
        print("\nSymbol Table:")
        for name, info in result['symbol_table'].items():
            print(f"  {name}: {info}")
    else:
        print("✗ Semantic errors found:")
        for error in result['errors']:
            print(f"  {error}")


#!/usr/bin/env python3
"""
Logic Gate Architect Compiler - Main CLI Driver
Complete 6-phase compiler implementation.
"""

import sys
import argparse
import os
from pathlib import Path

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from icg import IntermediateCodeGenerator
from optimizer import Optimizer
from codegen import CodeGenerator


def compile_file(input_file: str, output_file: str = None, verbose: bool = False, 
                 show_tokens: bool = False, show_ast: bool = False, 
                 show_symbols: bool = False, show_quads: bool = False,
                 no_optimize: bool = False):
    """
    Compile a circuit file through all 6 phases.
    
    Args:
        input_file: Path to input .gate file
        output_file: Path to output Python file (optional)
        verbose: Show detailed compilation steps
        show_tokens: Print token stream
        show_ast: Print abstract syntax tree
        show_symbols: Print symbol table
        show_quads: Print quadruples
        no_optimize: Disable optimization
    """
    try:
        # Read input file
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        if verbose:
            print(f"Reading source file: {input_file}\n")
        
        # Phase 1: Lexical Analysis
        if verbose:
            print("=" * 60)
            print("Phase 1: Lexical Analysis")
            print("=" * 60)
        
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
        
        if verbose:
            print(f"[OK] Phase 1: Lexical Analysis Complete ({len(tokens)} tokens)")
        
        if show_tokens:
            print("\nToken Stream:")
            for token in tokens:
                print(f"  {token}")
            print()
        
        # Phase 2: Syntax Analysis
        if verbose:
            print("\n" + "=" * 60)
            print("Phase 2: Syntax Analysis")
            print("=" * 60)
        
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        if verbose:
            print(f"[OK] Phase 2: Syntax Analysis Complete")
            print(f"  Circuit: {ast.name}")
            print(f"  Declarations: {len(ast.declarations)}")
            print(f"  Gates: {len(ast.gates)}")
        
        if show_ast:
            print("\nAbstract Syntax Tree:")
            print(f"  Program: {ast.name}")
            print("  Declarations:")
            for decl in ast.declarations:
                print(f"    {decl}")
            print("  Gates:")
            for gate in ast.gates:
                print(f"    {gate}")
            print()
        
        # Phase 3: Semantic Analysis
        if verbose:
            print("\n" + "=" * 60)
            print("Phase 3: Semantic Analysis")
            print("=" * 60)
        
        analyzer = SemanticAnalyzer(ast)
        semantic_result = analyzer.analyze()
        
        if not semantic_result['success']:
            print("[ERROR] Semantic Errors Found:")
            for error in semantic_result['errors']:
                print(f"  {error}")
            return 1
        
        if verbose:
            print("[OK] Phase 3: Semantic Analysis Complete")
            print(f"  Symbol table entries: {len(semantic_result['symbol_table'])}")
        
        if show_symbols:
            print("\nSymbol Table:")
            for name, info in semantic_result['symbol_table'].items():
                used_by = ', '.join(info.used_by) if info.used_by else 'None'
                print(f"  {name}: category={info.category}, defined={info.defined}, used_by=[{used_by}]")
            print()
        
        # Phase 4: Intermediate Code Generation
        if verbose:
            print("\n" + "=" * 60)
            print("Phase 4: Intermediate Code Generation")
            print("=" * 60)
        
        icg = IntermediateCodeGenerator(ast)
        quads = icg.generate()
        
        if verbose:
            print(f"[OK] Phase 4: Intermediate Code Generated ({len(quads)} quadruples)")
        
        if show_quads:
            print("\nQuadruples (Before Optimization):")
            for i, quad in enumerate(quads, 1):
                print(f"  {i}: {quad}")
            print()
        
        # Phase 5: Optimization
        if verbose:
            print("\n" + "=" * 60)
            print("Phase 5: Optimization")
            print("=" * 60)
        
        if no_optimize:
            optimized = quads
            if verbose:
                print("[WARN] Optimization disabled")
        else:
            optimizer = Optimizer(quads, semantic_result['symbol_table'])
            optimized = optimizer.optimize()
            
            removed = len(quads) - len(optimized)
            if verbose:
                print(f"[OK] Phase 5: Optimization Complete ({removed} instructions removed)")
        
        if show_quads and not no_optimize:
            print("\nQuadruples (After Optimization):")
            for i, quad in enumerate(optimized, 1):
                print(f"  {i}: {quad}")
            print()
        
        # Phase 6: Code Generation
        if verbose:
            print("\n" + "=" * 60)
            print("Phase 6: Code Generation")
            print("=" * 60)
        
        codegen = CodeGenerator(optimized, semantic_result['symbol_table'], ast.name)
        python_code = codegen.generate()
        
        if verbose:
            print("[OK] Phase 6: Code Generation Complete")
        
        # Output results
        print("\n" + "=" * 60)
        print("COMPILATION SUCCESSFUL")
        print("=" * 60)
        print("\n--- Generated Python Code ---\n")
        print(python_code)
        
        # Save to file if specified
        if output_file:
            # Create outputs directory if it doesn't exist
            outputs_dir = Path("outputs")
            outputs_dir.mkdir(exist_ok=True)
            
            # If output_file is not an absolute path, save it in outputs folder
            output_path = Path(output_file)
            if not output_path.is_absolute():
                output_path = outputs_dir / output_path.name
            
            # Ensure the directory exists (in case of nested paths)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(python_code)
            print(f"\n[OK] Code saved to: {output_path}")
            print(f"  Run with: python {output_path}")
        
        return 0
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return 1
    except SyntaxError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Logic Gate Architect Compiler - 6-Phase Compiler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compiler.py circuit.gate
  python compiler.py circuit.gate -o output.py
  python compiler.py circuit.gate -v --tokens --ast
  python compiler.py circuit.gate -o output.py --no-optimize
        """
    )
    
    parser.add_argument('input_file', help='Input .gate file to compile')
    parser.add_argument('-o', '--output', dest='output_file', 
                       help='Output Python file (default: print to stdout)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed compilation steps')
    parser.add_argument('-t', '--tokens', dest='show_tokens', action='store_true',
                       help='Print token stream')
    parser.add_argument('-a', '--ast', dest='show_ast', action='store_true',
                       help='Print abstract syntax tree')
    parser.add_argument('-s', '--symbols', dest='show_symbols', action='store_true',
                       help='Print symbol table')
    parser.add_argument('-q', '--quads', dest='show_quads', action='store_true',
                       help='Print quadruples')
    parser.add_argument('--no-optimize', action='store_true',
                       help='Disable optimization phase')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' not found.")
        return 1
    
    return compile_file(
        args.input_file,
        args.output_file,
        args.verbose,
        args.show_tokens,
        args.show_ast,
        args.show_symbols,
        args.show_quads,
        args.no_optimize
    )


if __name__ == "__main__":
    sys.exit(main())


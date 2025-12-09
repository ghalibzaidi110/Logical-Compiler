#!/usr/bin/env python3
"""
Test script to compile all example .gate files and run the generated Python code.
Tests each example file one by one.
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple
import time

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    """Print success message."""
    try:
        print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")
    except UnicodeEncodeError:
        print(f"[OK] {text}")

def print_error(text):
    """Print error message."""
    try:
        print(f"{Colors.FAIL}[ERROR] {text}{Colors.ENDC}")
    except UnicodeEncodeError:
        print(f"[ERROR] {text}")

def print_info(text):
    """Print info message."""
    try:
        print(f"{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")
    except UnicodeEncodeError:
        print(f"[INFO] {text}")

def compile_file(input_file: Path, output_file: Path) -> bool:
    """
    Compile a .gate file using compiler.py
    
    Args:
        input_file: Path to input .gate file
        output_file: Path to output Python file
        
    Returns:
        True if compilation successful, False otherwise
    """
    try:
        # Run compiler.py
        result = subprocess.run(
            [sys.executable, "compiler.py", str(input_file), "-o", str(output_file.name)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True
        else:
            # Show both stdout and stderr for better error visibility
            error_msg = result.stderr.strip() or result.stdout.strip()
            if error_msg:
                print_error(f"Compilation failed:")
                print(f"  {error_msg}")
            else:
                print_error(f"Compilation failed (no error message)")
            return False
            
    except subprocess.TimeoutExpired:
        print_error(f"Compilation timed out for {input_file.name}")
        return False
    except Exception as e:
        print_error(f"Error compiling {input_file.name}: {e}")
        return False

def run_python_file(python_file: Path) -> Tuple[bool, str]:
    """
    Run a generated Python file and capture output.
    
    Args:
        python_file: Path to Python file to run
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    try:
        result = subprocess.run(
            [sys.executable, str(python_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Execution timed out"
    except Exception as e:
        return False, str(e)

def main():
    """Main test function."""
    print_header("LOGICAL COMPILER - AUTOMATED TEST SUITE")
    
    # Ensure outputs directory exists
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    # Find all .gate files in examples directory
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print_error(f"Examples directory not found: {examples_dir}")
        return 1
    
    gate_files = sorted(examples_dir.glob("*.gate"))
    
    if not gate_files:
        print_error("No .gate files found in examples directory")
        return 1
    
    print_info(f"Found {len(gate_files)} example file(s) to test\n")
    
    # Statistics
    total_files = len(gate_files)
    successful_compilations = 0
    successful_executions = 0
    failed_files = []
    
    # Process each file one by one
    for i, gate_file in enumerate(gate_files, 1):
        print_header(f"Test {i}/{total_files}: {gate_file.name}")
        
        # Generate output filename
        output_name = gate_file.stem + "_output.py"
        output_file = outputs_dir / output_name
        
        print_info(f"Input file: {gate_file}")
        print_info(f"Output file: {output_file}")
        
        # Step 1: Compile
        print(f"\n{Colors.OKBLUE}[1/2] Compiling...{Colors.ENDC}")
        if compile_file(gate_file, output_file):
            print_success(f"Compilation successful: {output_file.name}")
            successful_compilations += 1
        else:
            print_error(f"Compilation failed: {gate_file.name}")
            failed_files.append((gate_file.name, "Compilation failed"))
            print(f"\n{'-'*70}\n")
            continue
        
        # Step 2: Run generated Python file
        print(f"\n{Colors.OKBLUE}[2/2] Running generated code...{Colors.ENDC}")
        success, output = run_python_file(output_file)
        
        if success:
            print_success(f"Execution successful: {output_file.name}")
            successful_executions += 1
            print(f"\n{Colors.OKCYAN}Output:{Colors.ENDC}")
            print("-" * 70)
            print(output)
            print("-" * 70)
        else:
            print_error(f"Execution failed: {output_file.name}")
            print(f"Error: {output}")
            failed_files.append((gate_file.name, f"Execution failed: {output[:50]}"))
        
        # Small delay between tests
        time.sleep(0.5)
        print(f"\n{'-'*70}\n")
    
    # Print summary
    print_header("TEST SUMMARY")
    
    print(f"{Colors.BOLD}Total files tested:{Colors.ENDC} {total_files}")
    print(f"{Colors.OKGREEN}Successful compilations:{Colors.ENDC} {successful_compilations}/{total_files}")
    print(f"{Colors.OKGREEN}Successful executions:{Colors.ENDC} {successful_executions}/{total_files}")
    
    if failed_files:
        try:
            print(f"\n{Colors.FAIL}Failed files:{Colors.ENDC}")
        except UnicodeEncodeError:
            print(f"\n[ERROR] Failed files:")
        for file_name, reason in failed_files:
            print(f"  - {file_name}: {reason}")
    
    # Overall result
    if successful_compilations == total_files and successful_executions == total_files:
        try:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}[SUCCESS] ALL TESTS PASSED!{Colors.ENDC}")
        except UnicodeEncodeError:
            print(f"\n[SUCCESS] ALL TESTS PASSED!")
        return 0
    else:
        try:
            print(f"\n{Colors.WARNING}{Colors.BOLD}[WARNING] SOME TESTS FAILED{Colors.ENDC}")
        except UnicodeEncodeError:
            print(f"\n[WARNING] SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


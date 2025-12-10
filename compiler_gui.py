#!/usr/bin/env python3
"""
Logic Gate Architect Compiler - GUI Frontend
Modern graphical interface for the compiler.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import sys
import subprocess
import tempfile
import os
import subprocess
import tempfile
import os

# Import compiler modules
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from icg import IntermediateCodeGenerator
from optimizer import Optimizer
from codegen import CodeGenerator


class CompilerGUI:
    """Graphical user interface for Logic Gate Architect Compiler."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Gate Architect Compiler")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.source_code = tk.StringVar()
        self.output_text = ""
        self.tokens = []
        self.ast = None
        self.symbol_table = {}
        self.quads = []
        self.optimized_quads = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#1e1e1e', foreground='#ffffff')
        style.configure('Phase.TButton', font=('Arial', 10))
        
        # Title
        title_frame = tk.Frame(self.root, bg='#1e1e1e')
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="Logic Gate Architect Compiler", style='Title.TLabel')
        title_label.pack()
        
        subtitle = tk.Label(title_frame, text="Complete 6-Phase Compiler Implementation", 
                          bg='#1e1e1e', fg='#4a9eff', font=('Arial', 10))
        subtitle.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Source Code
        left_panel = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Source code header
        source_header = tk.Frame(left_panel, bg='#2d2d2d')
        source_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(source_header, text="Source Code Editor", bg='#2d2d2d', fg='#ffffff', 
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = tk.Frame(source_header, bg='#2d2d2d')
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Load", command=self.load_file, 
                 bg='#0078d4', fg='white', font=('Arial', 9), width=8).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Save", command=self.save_source, 
                 bg='#6b46c1', fg='white', font=('Arial', 9), width=8).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Clear", command=self.clear_source, 
                 bg='#d13438', fg='white', font=('Arial', 9), width=8).pack(side=tk.LEFT, padx=2)
        
        # Source code text area
        self.source_text = scrolledtext.ScrolledText(left_panel, bg='#1e1e1e', fg='#4ec9b0', 
                                                     font=('Consolas', 11), insertbackground='white',
                                                     wrap=tk.WORD, relief=tk.FLAT, bd=0)
        self.source_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Default source code
        default_code = """CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}"""
        self.source_text.insert('1.0', default_code)
        
        # Compile button
        compile_btn = tk.Button(left_panel, text="▶ Compile", command=self.compile_circuit,
                               bg='#107c10', fg='white', font=('Arial', 12, 'bold'),
                               height=2, cursor='hand2')
        compile_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Right panel - Output and Phases
        right_panel = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Phase buttons
        phase_frame = tk.Frame(right_panel, bg='#2d2d2d')
        phase_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(phase_frame, text="Compilation Phases", bg='#2d2d2d', fg='#ffffff',
                font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        
        phases = [
            ('Lexer', 'Phase 1: Lexical Analysis'),
            ('Parser', 'Phase 2: Syntax Analysis'),
            ('Semantic', 'Phase 3: Semantic Analysis'),
            ('ICG', 'Phase 4: ICG'),
            ('Optimize', 'Phase 5: Optimization'),
            ('CodeGen', 'Phase 6: Code Generation')
        ]
        
        self.phase_buttons = {}
        for phase_id, phase_name in phases:
            btn = tk.Button(phase_frame, text=phase_id, command=lambda p=phase_id: self.show_phase(p),
                           bg='#3c3c3c', fg='#ffffff', font=('Arial', 9), width=8, relief=tk.FLAT)
            btn.pack(side=tk.LEFT, padx=2)
            self.phase_buttons[phase_id] = btn
        
        # Output area
        output_header = tk.Frame(right_panel, bg='#2d2d2d')
        output_header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(output_header, text="Compiler Output", bg='#2d2d2d', fg='#ffffff',
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        output_btn_frame = tk.Frame(output_header, bg='#2d2d2d')
        output_btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(output_btn_frame, text="Execute", command=self.execute_python,
                 bg='#107c10', fg='white', font=('Arial', 9, 'bold'), width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(output_btn_frame, text="Save Output", command=self.save_output,
                 bg='#0078d4', fg='white', font=('Arial', 9), width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(output_btn_frame, text="Save Python", command=self.save_python,
                 bg='#ffa500', fg='white', font=('Arial', 9), width=10).pack(side=tk.LEFT, padx=2)
        
        # Output text area
        self.output_text_area = scrolledtext.ScrolledText(right_panel, bg='#1e1e1e', fg='#d4d4d4',
                                                          font=('Consolas', 10), wrap=tk.WORD,
                                                          relief=tk.FLAT, bd=0)
        self.output_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bg='#0078d4', fg='white',
                                   font=('Arial', 9), anchor=tk.W, relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Test cases frame
        test_frame = tk.Frame(self.root, bg='#1e1e1e')
        test_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(test_frame, text="Test Cases:", bg='#1e1e1e', fg='#ffffff',
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        test_cases = [
            ('Basic AND', 'examples/basic_and.gate'),
            ('Half Adder', 'examples/halfadder.gate'),
            ('Full Adder', 'examples/fulladder.gate')
        ]
        
        for test_name, test_file in test_cases:
            btn = tk.Button(test_frame, text=test_name, 
                           command=lambda f=test_file: self.load_test_case(f),
                           bg='#3c3c3c', fg='#ffffff', font=('Arial', 9), width=12)
            btn.pack(side=tk.LEFT, padx=2)
    
    def update_status(self, message):
        """Update status bar."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def load_file(self):
        """Load a .gate file."""
        filename = filedialog.askopenfilename(
            title="Load Circuit File",
            filetypes=[("Gate Files", "*.gate"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.source_text.delete('1.0', tk.END)
                self.source_text.insert('1.0', content)
                self.update_status(f"Loaded: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")
    
    def save_source(self):
        """Save source code to file."""
        filename = filedialog.asksaveasfilename(
            title="Save Source Code",
            defaultextension=".gate",
            filetypes=[("Gate Files", "*.gate"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.source_text.get('1.0', tk.END))
                self.update_status(f"Saved: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def clear_source(self):
        """Clear source code editor."""
        if messagebox.askyesno("Clear", "Clear source code editor?"):
            self.source_text.delete('1.0', tk.END)
    
    def load_test_case(self, filename):
        """Load a test case."""
        if Path(filename).exists():
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.source_text.delete('1.0', tk.END)
                self.source_text.insert('1.0', content)
                self.update_status(f"Loaded test case: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load test case:\n{e}")
        else:
            messagebox.showwarning("File Not Found", f"Test case file not found:\n{filename}")
    
    def save_output(self):
        """Save compiler output to file."""
        output = self.output_text_area.get('1.0', tk.END)
        if not output.strip():
            messagebox.showwarning("No Output", "No output to save. Please compile first.")
            return
        
        # Create outputs directory if it doesn't exist
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            initialdir=str(outputs_dir),
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(output)
                self.update_status(f"Output saved: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save output:\n{e}")
    
    def save_python(self):
        """Save generated Python code to file."""
        output = self.output_text_area.get('1.0', tk.END)
        if "Generated Python Code" not in output:
            messagebox.showwarning("No Python Code", "No Python code found. Please compile first.")
            return
        
        # Extract Python code
        lines = output.split('\n')
        python_lines = []
        in_python = False
        for line in lines:
            if "Generated Python Code" in line:
                in_python = True
            if in_python:
                python_lines.append(line)
        
        python_code = '\n'.join(python_lines)
        
        # Create outputs directory if it doesn't exist
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            title="Save Python Code",
            defaultextension=".py",
            initialdir=str(outputs_dir),
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(python_code)
                self.update_status(f"Python code saved: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save Python code:\n{e}")
    
    def extract_python_code(self):
        """Extract Python code from output."""
        output = self.output_text_area.get('1.0', tk.END)
        
        # Check for Python code marker
        if "Generated Python Code" not in output:
            return None
        
        # Extract Python code - find the marker and get everything after it
        lines = output.split('\n')
        python_lines = []
        found_marker = False
        
        for i, line in enumerate(lines):
            # Look for the marker line
            if "Generated Python Code" in line:
                found_marker = True
                # Start capturing from the next line
                continue
            
            # If we found the marker, capture all subsequent lines
            if found_marker:
                python_lines.append(line)
        
        # Join all lines and clean up
        python_code = '\n'.join(python_lines).strip()
        
        # Remove trailing empty lines but keep the code structure
        while python_code.endswith('\n\n'):
            python_code = python_code.rstrip('\n')
        
        # Debug: print what we extracted (can remove later)
        if not python_code:
            print("DEBUG: No Python code extracted")
            print(f"DEBUG: Output contains marker: {'Generated Python Code' in output}")
            print(f"DEBUG: First 500 chars of output: {output[:500]}")
        
        return python_code if python_code else None
    
    def execute_python(self):
        """Execute the generated Python code and show results."""
        python_code = self.extract_python_code()
        
        if not python_code:
            messagebox.showwarning("No Python Code", 
                "No Python code found. Please compile first.\n\n"
                "Make sure you have:\n"
                "1. Entered circuit code\n"
                "2. Clicked 'Compile' button\n"
                "3. Compilation completed successfully")
            return
        
        # Show what we're about to execute (for debugging)
        print(f"DEBUG: Extracted {len(python_code)} characters of Python code")
        print(f"DEBUG: First 200 chars: {python_code[:200]}")
        
        self.update_status("Executing Python code...")
        
        # Run in a separate thread to avoid blocking UI
        def run_code():
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(python_code)
                    temp_file = f.name
                
                try:
                    # Execute Python code
                    result = subprocess.run(
                        [sys.executable, temp_file],
                        capture_output=True,
                        text=True,
                        timeout=10  # 10 second timeout
                    )
                    
                    # Debug output
                    print(f"DEBUG: Execution return code: {result.returncode}")
                    print(f"DEBUG: stdout length: {len(result.stdout)}")
                    print(f"DEBUG: stderr length: {len(result.stderr)}")
                    if result.stdout:
                        print(f"DEBUG: First 200 chars of stdout: {result.stdout[:200]}")
                    
                    # Update UI in main thread
                    self.root.after(0, self.show_execution_results, result.stdout, result.stderr, result.returncode)
                    
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
                        
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: messagebox.showerror("Timeout", "Code execution timed out (10 seconds)."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to execute code:\n{e}"))
        
        # Start execution in background thread
        thread = threading.Thread(target=run_code, daemon=True)
        thread.start()
    
    def show_execution_results(self, stdout, stderr, returncode):
        """Display execution results in a new window."""
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Execution Results")
        results_window.geometry("900x700")
        results_window.configure(bg='#1e1e1e')
        
        # Header
        header = tk.Frame(results_window, bg='#2d2d2d', pady=10)
        header.pack(fill=tk.X)
        
        if returncode == 0:
            status_label = tk.Label(header, text="[OK] Execution Successful", 
                                   bg='#2d2d2d', fg='#4ec9b0', font=('Arial', 12, 'bold'))
        else:
            status_label = tk.Label(header, text="[ERROR] Execution Failed", 
                                   bg='#2d2d2d', fg='#f48771', font=('Arial', 12, 'bold'))
        status_label.pack()
        
        # Output area
        output_frame = tk.Frame(results_window, bg='#1e1e1e')
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        output_text = scrolledtext.ScrolledText(output_frame, bg='#1e1e1e', fg='#d4d4d4',
                                                font=('Consolas', 11), wrap=tk.WORD,
                                                relief=tk.FLAT, bd=0)
        output_text.pack(fill=tk.BOTH, expand=True)
        
        # Show stdout
        if stdout:
            output_text.insert(tk.END, "=== Standard Output ===\n", 'header')
            output_text.insert(tk.END, stdout, 'output')
            if not stdout.endswith('\n'):
                output_text.insert(tk.END, "\n")
        
        # Show stderr if any
        if stderr:
            if stdout:
                output_text.insert(tk.END, "\n")
            output_text.insert(tk.END, "=== Error Output ===\n", 'error_header')
            output_text.insert(tk.END, stderr, 'error')
            if not stderr.endswith('\n'):
                output_text.insert(tk.END, "\n")
        
        if not stdout and not stderr:
            output_text.insert(tk.END, "No output generated.\n", 'output')
            output_text.insert(tk.END, "The code executed but produced no output.\n", 'output')
        
        # Configure text tags for colors
        output_text.tag_config('header', foreground='#4ec9b0', font=('Consolas', 11, 'bold'))
        output_text.tag_config('output', foreground='#d4d4d4')
        output_text.tag_config('error_header', foreground='#f48771', font=('Consolas', 11, 'bold'))
        output_text.tag_config('error', foreground='#f48771')
        
        # Make text area read-only but allow scrolling
        output_text.config(state=tk.DISABLED)
        
        # Buttons
        btn_frame = tk.Frame(results_window, bg='#1e1e1e')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Close", command=results_window.destroy,
                 bg='#3c3c3c', fg='white', font=('Arial', 10), width=10).pack(side=tk.RIGHT, padx=5)
        
        def save_results():
            output_text.config(state=tk.NORMAL)
            content = output_text.get('1.0', tk.END)
            output_text.config(state=tk.DISABLED)
            # Create outputs directory if it doesn't exist
            outputs_dir = Path("outputs")
            outputs_dir.mkdir(exist_ok=True)
            
            filename = filedialog.asksaveasfilename(
                title="Save Execution Results",
                defaultextension=".txt",
                initialdir=str(outputs_dir),
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w') as f:
                        f.write(content)
                    messagebox.showinfo("Saved", f"Results saved to {Path(filename).name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save:\n{e}")
        
        tk.Button(btn_frame, text="Save Results", command=save_results,
                 bg='#0078d4', fg='white', font=('Arial', 10), width=12).pack(side=tk.RIGHT, padx=5)
        
        self.update_status("Execution complete!")
    
    def show_phase(self, phase_id):
        """Show details for a specific phase."""
        self.output_text_area.delete('1.0', tk.END)
        
        phase_info = {
            'Lexer': self.show_lexer_info,
            'Parser': self.show_parser_info,
            'Semantic': self.show_semantic_info,
            'ICG': self.show_icg_info,
            'Optimize': self.show_optimize_info,
            'CodeGen': self.show_codegen_info
        }
        
        if phase_id in phase_info:
            phase_info[phase_id]()
    
    def show_lexer_info(self):
        """Show lexical analysis information."""
        if not self.tokens:
            self.output_text_area.insert(tk.END, "No tokens yet. Please compile first.\n")
            return
        
        self.output_text_area.insert(tk.END, "=" * 60 + "\n")
        self.output_text_area.insert(tk.END, "Phase 1: Lexical Analysis\n")
        self.output_text_area.insert(tk.END, "=" * 60 + "\n\n")
        self.output_text_area.insert(tk.END, f"Total Tokens: {len(self.tokens)}\n\n")
        self.output_text_area.insert(tk.END, "Token Stream:\n")
        self.output_text_area.insert(tk.END, "-" * 60 + "\n")
        
        for token in self.tokens:
            self.output_text_area.insert(tk.END, f"{token}\n")
    
    def show_parser_info(self):
        """Show syntax analysis information."""
        if not self.ast:
            self.output_text_area.insert(tk.END, "No AST yet. Please compile first.\n")
            return
        
        self.output_text_area.insert(tk.END, "=" * 60 + "\n")
        self.output_text_area.insert(tk.END, "Phase 2: Syntax Analysis\n")
        self.output_text_area.insert(tk.END, "=" * 60 + "\n\n")
        self.output_text_area.insert(tk.END, f"Circuit Name: {self.ast.name}\n")
        self.output_text_area.insert(tk.END, f"Declarations: {len(self.ast.declarations)}\n")
        self.output_text_area.insert(tk.END, f"Gates: {len(self.ast.gates)}\n\n")
        
        self.output_text_area.insert(tk.END, "Declarations:\n")
        self.output_text_area.insert(tk.END, "-" * 60 + "\n")
        for decl in self.ast.declarations:
            self.output_text_area.insert(tk.END, f"  {decl}\n")
        
        self.output_text_area.insert(tk.END, "\nGates:\n")
        self.output_text_area.insert(tk.END, "-" * 60 + "\n")
        for gate in self.ast.gates:
            self.output_text_area.insert(tk.END, f"  {gate}\n")
    
    def show_semantic_info(self):
        """Show semantic analysis information."""
        if not self.symbol_table:
            self.output_text_area.insert(tk.END, "No symbol table yet. Please compile first.\n")
            return
        
        self.output_text_area.insert(tk.END, "=" * 60 + "\n")
        self.output_text_area.insert(tk.END, "Phase 3: Semantic Analysis\n")
        self.output_text_area.insert(tk.END, "=" * 60 + "\n\n")
        self.output_text_area.insert(tk.END, f"Symbol Table Entries: {len(self.symbol_table)}\n\n")
        self.output_text_area.insert(tk.END, "Symbol Table:\n")
        self.output_text_area.insert(tk.END, "-" * 60 + "\n")
        
        for name, info in self.symbol_table.items():
            used_by = ', '.join(info.used_by) if info.used_by else 'None'
            self.output_text_area.insert(tk.END, 
                f"{name:15} | Category: {info.category:8} | Defined: {str(info.defined):5} | Used By: {used_by}\n")
    
    def show_icg_info(self):
        """Show intermediate code generation information."""
        if not self.quads:
            self.output_text_area.insert(tk.END, "No quadruples yet. Please compile first.\n")
            return
        
        self.output_text_area.insert(tk.END, "=" * 60 + "\n")
        self.output_text_area.insert(tk.END, "Phase 4: Intermediate Code Generation\n")
        self.output_text_area.insert(tk.END, "=" * 60 + "\n\n")
        self.output_text_area.insert(tk.END, f"Quadruples: {len(self.quads)}\n\n")
        self.output_text_area.insert(tk.END, "Quadruples (Before Optimization):\n")
        self.output_text_area.insert(tk.END, "-" * 60 + "\n")
        
        for i, quad in enumerate(self.quads, 1):
            self.output_text_area.insert(tk.END, f"{i:3}: {quad}\n")
    
    def show_optimize_info(self):
        """Show optimization information."""
        if not self.optimized_quads:
            self.output_text_area.insert(tk.END, "No optimized code yet. Please compile first.\n")
            return
        
        self.output_text_area.insert(tk.END, "=" * 60 + "\n")
        self.output_text_area.insert(tk.END, "Phase 5: Optimization\n")
        self.output_text_area.insert(tk.END, "=" * 60 + "\n\n")
        
        removed = len(self.quads) - len(self.optimized_quads)
        self.output_text_area.insert(tk.END, f"Before: {len(self.quads)} quadruples\n")
        self.output_text_area.insert(tk.END, f"After:  {len(self.optimized_quads)} quadruples\n")
        self.output_text_area.insert(tk.END, f"Removed: {removed} instructions\n\n")
        
        self.output_text_area.insert(tk.END, "Optimized Quadruples:\n")
        self.output_text_area.insert(tk.END, "-" * 60 + "\n")
        
        for i, quad in enumerate(self.optimized_quads, 1):
            self.output_text_area.insert(tk.END, f"{i:3}: {quad}\n")
    
    def show_codegen_info(self):
        """Show code generation information."""
        self.output_text_area.insert(tk.END, "Final generated Python code is shown in the main output.\n")
        self.output_text_area.insert(tk.END, "Click 'Compile' to see the complete output.\n")
    
    def compile_circuit(self):
        """Compile the circuit through all 6 phases."""
        source_code = self.source_text.get('1.0', tk.END).strip()
        
        if not source_code:
            messagebox.showwarning("Empty Source", "Please enter source code to compile.")
            return
        
        # Clear previous results
        self.tokens = []
        self.ast = None
        self.symbol_table = {}
        self.quads = []
        self.optimized_quads = []
        
        # Reset phase buttons
        for btn in self.phase_buttons.values():
            btn.config(bg='#3c3c3c')
        
        self.output_text_area.delete('1.0', tk.END)
        self.update_status("Compiling...")
        
        try:
            # Phase 1: Lexical Analysis
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 1: Lexical Analysis\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            lexer = Lexer()
            self.tokens = lexer.tokenize(source_code)
            self.output_text_area.insert(tk.END, f"[OK] Phase 1 Complete ({len(self.tokens)} tokens)\n\n")
            
            # Show token details
            self.output_text_area.insert(tk.END, "Token Stream:\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            for i, token in enumerate(self.tokens, 1):
                self.output_text_area.insert(tk.END, f"{i:3}. {token.type:15} = '{token.value}' (Line {token.line}, Col {token.column})\n")
            self.output_text_area.insert(tk.END, "\n")
            self.phase_buttons['Lexer'].config(bg='#107c10')
            
            # Phase 2: Syntax Analysis
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 2: Syntax Analysis (LL(1) Parser)\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            parser = Parser(self.tokens)
            self.ast = parser.parse_program()
            self.output_text_area.insert(tk.END, f"[OK] Phase 2 Complete\n")
            self.output_text_area.insert(tk.END, f"  Circuit Name: {self.ast.name}\n")
            self.output_text_area.insert(tk.END, f"  Declarations: {len(self.ast.declarations)}\n")
            self.output_text_area.insert(tk.END, f"  Gates: {len(self.ast.gates)}\n\n")
            
            # Show AST structure
            self.output_text_area.insert(tk.END, "Abstract Syntax Tree (AST):\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            self.output_text_area.insert(tk.END, f"Program({self.ast.name})\n")
            
            # Show declarations
            for i, decl in enumerate(self.ast.declarations):
                prefix = "├──" if i < len(self.ast.declarations) - 1 or len(self.ast.gates) > 0 else "└──"
                self.output_text_area.insert(tk.END, f"{prefix} Declaration({decl.category}, {decl.identifiers})\n")
            
            # Show gates
            for i, gate in enumerate(self.ast.gates):
                prefix = "├──" if i < len(self.ast.gates) - 1 else "└──"
                self.output_text_area.insert(tk.END, f"{prefix} Gate({gate.output} = {gate.gate_type}({', '.join(gate.inputs)}))\n")
            
            self.output_text_area.insert(tk.END, "\n")
            self.phase_buttons['Parser'].config(bg='#107c10')
            
            # Phase 3: Semantic Analysis
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 3: Semantic Analysis\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            analyzer = SemanticAnalyzer(self.ast)
            semantic_result = analyzer.analyze()
            
            if not semantic_result['success']:
                self.output_text_area.insert(tk.END, "[ERROR] Semantic Errors Found:\n")
                for error in semantic_result['errors']:
                    self.output_text_area.insert(tk.END, f"  {error}\n")
                self.update_status("Compilation failed: Semantic errors")
                return
            
            self.symbol_table = semantic_result['symbol_table']
            self.output_text_area.insert(tk.END, f"[OK] Phase 3 Complete\n")
            self.output_text_area.insert(tk.END, f"  Symbol table entries: {len(self.symbol_table)}\n\n")
            
            # Show symbol table details
            self.output_text_area.insert(tk.END, "Symbol Table:\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            self.output_text_area.insert(tk.END, f"{'Name':<15} {'Category':<10} {'Defined':<8} {'Used By':<30}\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            for name, info in self.symbol_table.items():
                used_by = ', '.join(info.used_by) if info.used_by else 'None'
                defined_str = 'Yes' if info.defined else 'No'
                self.output_text_area.insert(tk.END, f"{name:<15} {info.category:<10} {defined_str:<8} {used_by:<30}\n")
            self.output_text_area.insert(tk.END, "\n")
            self.phase_buttons['Semantic'].config(bg='#107c10')
            
            # Phase 4: Intermediate Code Generation
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 4: Intermediate Code Generation\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            icg = IntermediateCodeGenerator(self.ast)
            self.quads = icg.generate()
            self.output_text_area.insert(tk.END, f"[OK] Phase 4 Complete ({len(self.quads)} quadruples)\n\n")
            
            # Show quadruples
            self.output_text_area.insert(tk.END, "Intermediate Code (Quadruples):\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            self.output_text_area.insert(tk.END, f"{'No.':<5} {'Operation':<12} {'Arg1':<10} {'Arg2':<10} {'Result':<15}\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            for i, quad in enumerate(self.quads, 1):
                arg2 = quad.arg2 if quad.arg2 else '-'
                self.output_text_area.insert(tk.END, f"{i:<5} {quad.op:<12} {str(quad.arg1):<10} {str(arg2):<10} {quad.result:<15}\n")
            self.output_text_area.insert(tk.END, "\n")
            self.phase_buttons['ICG'].config(bg='#107c10')
            
            # Phase 5: Optimization
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 5: Optimization\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            optimizer = Optimizer(self.quads, self.symbol_table)
            self.optimized_quads = optimizer.optimize()
            removed = len(self.quads) - len(self.optimized_quads)
            self.output_text_area.insert(tk.END, f"[OK] Phase 5 Complete ({removed} instructions removed)\n\n")
            
            # Show optimization details
            self.output_text_area.insert(tk.END, "Optimization Details:\n")
            self.output_text_area.insert(tk.END, "-" * 60 + "\n")
            self.output_text_area.insert(tk.END, f"Before: {len(self.quads)} quadruples\n")
            self.output_text_area.insert(tk.END, f"After:  {len(self.optimized_quads)} quadruples\n")
            self.output_text_area.insert(tk.END, f"Removed: {removed} instructions\n\n")
            
            if removed > 0:
                self.output_text_area.insert(tk.END, "Optimized Quadruples:\n")
                self.output_text_area.insert(tk.END, "-" * 60 + "\n")
                self.output_text_area.insert(tk.END, f"{'No.':<5} {'Operation':<12} {'Arg1':<10} {'Arg2':<10} {'Result':<15}\n")
                self.output_text_area.insert(tk.END, "-" * 60 + "\n")
                for i, quad in enumerate(self.optimized_quads, 1):
                    arg2 = quad.arg2 if quad.arg2 else '-'
                    self.output_text_area.insert(tk.END, f"{i:<5} {quad.op:<12} {str(quad.arg1):<10} {str(arg2):<10} {quad.result:<15}\n")
            else:
                self.output_text_area.insert(tk.END, "No optimizations applied (code already optimal)\n")
            self.output_text_area.insert(tk.END, "\n")
            self.phase_buttons['Optimize'].config(bg='#107c10')
            
            # Phase 6: Code Generation
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 6: Code Generation\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            codegen = CodeGenerator(self.optimized_quads, self.symbol_table, self.ast.name)
            python_code = codegen.generate()
            
            self.output_text_area.insert(tk.END, f"[OK] Phase 6 Complete\n\n")
            self.phase_buttons['CodeGen'].config(bg='#107c10')
            
            # Final output
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "COMPILATION SUCCESSFUL\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n\n")
            self.output_text_area.insert(tk.END, "--- Generated Python Code ---\n\n")
            self.output_text_area.insert(tk.END, python_code)
            self.output_text_area.insert(tk.END, "\n")  # Ensure newline at end
            
            self.update_status("Compilation successful!")
            
        except SyntaxError as e:
            self.output_text_area.insert(tk.END, f"[ERROR] {e}\n")
            self.update_status("Compilation failed: Syntax error")
            messagebox.showerror("Compilation Error", str(e))
        except Exception as e:
            self.output_text_area.insert(tk.END, f"[ERROR] Unexpected error: {e}\n")
            self.update_status("Compilation failed")
            messagebox.showerror("Error", f"Compilation failed:\n{e}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


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
        
        filename = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
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
        
        filename = filedialog.asksaveasfilename(
            title="Save Python Code",
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(python_code)
                self.update_status(f"Python code saved: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save Python code:\n{e}")
    
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
            self.phase_buttons['Lexer'].config(bg='#107c10')
            
            # Phase 2: Syntax Analysis
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 2: Syntax Analysis\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            parser = Parser(self.tokens)
            self.ast = parser.parse_program()
            self.output_text_area.insert(tk.END, f"[OK] Phase 2 Complete\n")
            self.output_text_area.insert(tk.END, f"  Circuit: {self.ast.name}\n")
            self.output_text_area.insert(tk.END, f"  Declarations: {len(self.ast.declarations)}\n")
            self.output_text_area.insert(tk.END, f"  Gates: {len(self.ast.gates)}\n\n")
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
            self.phase_buttons['Semantic'].config(bg='#107c10')
            
            # Phase 4: Intermediate Code Generation
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.output_text_area.insert(tk.END, "Phase 4: Intermediate Code Generation\n")
            self.output_text_area.insert(tk.END, "=" * 60 + "\n")
            self.root.update()
            
            icg = IntermediateCodeGenerator(self.ast)
            self.quads = icg.generate()
            self.output_text_area.insert(tk.END, f"[OK] Phase 4 Complete ({len(self.quads)} quadruples)\n\n")
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


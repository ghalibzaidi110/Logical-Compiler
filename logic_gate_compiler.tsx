import React, { useState, useRef } from 'react';
import { Play, FileText, Code, CheckCircle, AlertCircle, Upload, Download, Save } from 'lucide-react';

const LogicGateCompiler = () => {
  const [activePhase, setActivePhase] = useState('lexer');
  const [sourceCode, setSourceCode] = useState(`CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}`);
  const [output, setOutput] = useState('');
  const [tokens, setTokens] = useState([]);
  const [parseTree, setParseTree] = useState(null);
  const [symbolTable, setSymbolTable] = useState({});
  const [intermediateCode, setIntermediateCode] = useState([]);
  const [optimizedCode, setOptimizedCode] = useState([]);
  const fileInputRef = useRef(null);

  // Phase 1: Lexical Analyzer
  const tokenize = (code) => {
    const tokenPatterns = [
      { type: 'KEYWORD', pattern: /^(CIRCUIT|INPUT|OUTPUT|WIRE|AND|OR|XOR|NAND|NOR|NOT)\b/ },
      { type: 'IDENTIFIER', pattern: /^[a-zA-Z_][a-zA-Z0-9_]*/ },
      { type: 'LBRACE', pattern: /^\{/ },
      { type: 'RBRACE', pattern: /^\}/ },
      { type: 'LPAREN', pattern: /^\(/ },
      { type: 'RPAREN', pattern: /^\)/ },
      { type: 'SEMICOLON', pattern: /^;/ },
      { type: 'COMMA', pattern: /^,/ },
      { type: 'EQUALS', pattern: /^=/ },
      { type: 'WHITESPACE', pattern: /^\s+/ },
      { type: 'NEWLINE', pattern: /^\n/ },
    ];

    const tokens = [];
    let position = 0;
    let line = 1;
    let column = 1;

    while (position < code.length) {
      let matched = false;

      for (const { type, pattern } of tokenPatterns) {
        const match = code.slice(position).match(pattern);
        if (match) {
          if (type !== 'WHITESPACE' && type !== 'NEWLINE') {
            tokens.push({
              type,
              value: match[0],
              line,
              column,
            });
          }
          
          const matchLength = match[0].length;
          position += matchLength;
          
          if (type === 'NEWLINE') {
            line++;
            column = 1;
          } else {
            column += matchLength;
          }
          
          matched = true;
          break;
        }
      }

      if (!matched) {
        throw new Error(`Lexical Error at line ${line}, column ${column}: Unexpected character '${code[position]}'`);
      }
    }

    return tokens;
  };

  // Phase 2: Parser (Recursive Descent)
  class Parser {
    constructor(tokens) {
      this.tokens = tokens;
      this.current = 0;
    }

    peek() {
      return this.tokens[this.current];
    }

    advance() {
      return this.tokens[this.current++];
    }

    match(...types) {
      for (const type of types) {
        if (this.peek()?.type === type) {
          return this.advance();
        }
      }
      return null;
    }

    expect(type) {
      const token = this.match(type);
      if (!token) {
        throw new Error(`Parse Error: Expected ${type} but got ${this.peek()?.type} at line ${this.peek()?.line}`);
      }
      return token;
    }

    parseProgram() {
      this.expect('KEYWORD'); // CIRCUIT
      const name = this.expect('IDENTIFIER');
      this.expect('LBRACE');
      
      const declarations = this.parseDeclarations();
      const gates = this.parseGates();
      
      this.expect('RBRACE');

      return {
        type: 'Program',
        name: name.value,
        declarations,
        gates,
      };
    }

    parseDeclarations() {
      const declarations = [];
      
      while (this.peek()?.type === 'KEYWORD' && 
             ['INPUT', 'OUTPUT', 'WIRE'].includes(this.peek()?.value)) {
        const keyword = this.advance();
        const identifiers = this.parseIdentifierList();
        this.expect('SEMICOLON');
        
        declarations.push({
          type: 'Declaration',
          category: keyword.value,
          identifiers,
        });
      }
      
      return declarations;
    }

    parseIdentifierList() {
      const ids = [this.expect('IDENTIFIER').value];
      
      while (this.match('COMMA')) {
        ids.push(this.expect('IDENTIFIER').value);
      }
      
      return ids;
    }

    parseGates() {
      const gates = [];
      
      while (this.peek()?.type === 'IDENTIFIER') {
        const output = this.advance().value;
        this.expect('EQUALS');
        const gateType = this.expect('KEYWORD').value;
        this.expect('LPAREN');
        const inputs = this.parseIdentifierList();
        this.expect('RPAREN');
        this.expect('SEMICOLON');
        
        gates.push({
          type: 'Gate',
          output,
          gateType,
          inputs,
        });
      }
      
      return gates;
    }
  }

  // Phase 3: Semantic Analyzer
  const semanticAnalysis = (ast) => {
    const symbolTable = {};
    const errors = [];

    // Build symbol table from declarations
    for (const decl of ast.declarations) {
      for (const id of decl.identifiers) {
        if (symbolTable[id]) {
          errors.push(`Semantic Error: Identifier '${id}' already declared`);
        }
        symbolTable[id] = {
          category: decl.category,
          defined: decl.category !== 'OUTPUT',
          usedBy: [],
        };
      }
    }

    // Validate gates
    for (const gate of ast.gates) {
      // Check output is declared
      if (!symbolTable[gate.output]) {
        symbolTable[gate.output] = {
          category: 'WIRE',
          defined: true,
          usedBy: [],
        };
      }
      symbolTable[gate.output].source = gate;
      symbolTable[gate.output].defined = true;

      // Check inputs are declared
      for (const input of gate.inputs) {
        if (!symbolTable[input]) {
          errors.push(`Semantic Error: Undeclared identifier '${input}' used in gate`);
        } else {
          symbolTable[input].usedBy.push(gate.output);
        }
      }

      // Validate gate input counts
      const requiredInputs = {
        'NOT': 1,
        'AND': 2,
        'OR': 2,
        'XOR': 2,
        'NAND': 2,
        'NOR': 2,
      };

      if (requiredInputs[gate.gateType] && gate.inputs.length !== requiredInputs[gate.gateType]) {
        errors.push(`Semantic Error: Gate ${gate.gateType} requires ${requiredInputs[gate.gateType]} inputs, got ${gate.inputs.length}`);
      }
    }

    // Check for cycles
    const detectCycle = (node, visited, recStack) => {
      visited.add(node);
      recStack.add(node);

      if (symbolTable[node]?.source) {
        for (const input of symbolTable[node].source.inputs) {
          if (!visited.has(input)) {
            if (detectCycle(input, visited, recStack)) return true;
          } else if (recStack.has(input)) {
            errors.push(`Semantic Error: Cycle detected involving '${node}' and '${input}'`);
            return true;
          }
        }
      }

      recStack.delete(node);
      return false;
    };

    const visited = new Set();
    for (const id in symbolTable) {
      if (!visited.has(id)) {
        detectCycle(id, visited, new Set());
      }
    }

    return { symbolTable, errors };
  };

  // Phase 4: Intermediate Code Generation
  const generateIntermediateCode = (ast) => {
    const quads = [];
    
    for (const gate of ast.gates) {
      quads.push({
        op: gate.gateType,
        arg1: gate.inputs[0] || null,
        arg2: gate.inputs[1] || null,
        result: gate.output,
      });
    }
    
    return quads;
  };

  // Phase 5: Optimization
  const optimize = (quads, symbolTable) => {
    const optimized = [];
    
    for (const quad of quads) {
      let skip = false;
      
      // Constant folding
      if (quad.arg1 === '0' && quad.op === 'AND') {
        optimized.push({ op: 'ASSIGN', arg1: '0', arg2: null, result: quad.result });
        continue;
      }
      
      if (quad.arg1 === '1' && quad.op === 'OR') {
        optimized.push({ op: 'ASSIGN', arg1: '1', arg2: null, result: quad.result });
        continue;
      }
      
      // Identity laws
      if (quad.arg2 === '0' && quad.op === 'OR') {
        optimized.push({ op: 'ASSIGN', arg1: quad.arg1, arg2: null, result: quad.result });
        continue;
      }
      
      // Dead code elimination - check if result is used
      const sym = symbolTable[quad.result];
      if (sym && sym.category !== 'OUTPUT' && sym.usedBy.length === 0) {
        skip = true;
      }
      
      if (!skip) {
        optimized.push(quad);
      }
    }
    
    return optimized;
  };

  // Phase 6: Code Generation
  const generateCode = (quads, symbolTable, circuitName) => {
    const inputs = Object.keys(symbolTable).filter(k => symbolTable[k].category === 'INPUT');
    const outputs = Object.keys(symbolTable).filter(k => symbolTable[k].category === 'OUTPUT');
    
    let code = `# Generated by Logic Gate Architect Compiler\n`;
    code += `# Circuit: ${circuitName}\n\n`;
    
    code += `def simulate(${inputs.join(', ')}):\n`;
    
    for (const quad of quads) {
      if (quad.op === 'ASSIGN') {
        code += `    ${quad.result} = ${quad.arg1}\n`;
      } else if (quad.op === 'NOT') {
        code += `    ${quad.result} = int(not ${quad.arg1})\n`;
      } else if (quad.op === 'AND') {
        code += `    ${quad.result} = ${quad.arg1} & ${quad.arg2}\n`;
      } else if (quad.op === 'OR') {
        code += `    ${quad.result} = ${quad.arg1} | ${quad.arg2}\n`;
      } else if (quad.op === 'XOR') {
        code += `    ${quad.result} = ${quad.arg1} ^ ${quad.arg2}\n`;
      } else if (quad.op === 'NAND') {
        code += `    ${quad.result} = int(not (${quad.arg1} & ${quad.arg2}))\n`;
      } else if (quad.op === 'NOR') {
        code += `    ${quad.result} = int(not (${quad.arg1} | ${quad.arg2}))\n`;
      }
    }
    
    code += `    return ${outputs.join(', ')}\n\n`;
    
    code += `# Truth Table\n`;
    code += `print("${inputs.join(' | ')} || ${outputs.join(' | ')}")\n`;
    code += `print("-" * 40)\n`;
    
    const numInputs = inputs.length;
    for (let i = 0; i < Math.pow(2, numInputs); i++) {
      const values = i.toString(2).padStart(numInputs, '0').split('').map(Number);
      const call = `simulate(${values.join(', ')})`;
      code += `result = ${call}\n`;
      code += `print(f"${values.join(' | ')} || {result}")\n`;
    }
    
    return code;
  };

  // File I/O Functions
  const handleFileLoad = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSourceCode(e.target.result);
        setOutput('File loaded successfully!\n');
      };
      reader.readAsText(file);
    }
  };

  const handleSaveSource = () => {
    const blob = new Blob([sourceCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'circuit.gate';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setOutput(prev => prev + '\nSource code saved to circuit.gate\n');
  };

  const handleSaveOutput = () => {
    if (!output) {
      setOutput('No output to save. Please compile first.\n');
      return;
    }
    const blob = new Blob([output], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compiled_output.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setOutput(prev => prev + '\nOutput saved to compiled_output.txt\n');
  };

  const handleSavePython = () => {
    if (!output || !output.includes('Generated Python Code')) {
      setOutput(prev => prev + '\nNo Python code to save. Please compile first.\n');
      return;
    }
    // Extract Python code from output
    const pythonCode = output.split('--- Generated Python Code ---\n')[1] || output;
    const blob = new Blob([pythonCode], { type: 'text/x-python' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'simulate.py';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setOutput(prev => prev + '\nPython code saved to simulate.py\n');
  };

  const compile = () => {
    try {
      setOutput('Compiling...\n\n');
      
      // Phase 1: Lexical Analysis
      const toks = tokenize(sourceCode);
      setTokens(toks);
      setOutput(prev => prev + `✓ Phase 1: Lexical Analysis Complete (${toks.length} tokens)\n`);
      
      // Phase 2: Syntax Analysis
      const parser = new Parser(toks);
      const ast = parser.parseProgram();
      setParseTree(ast);
      setOutput(prev => prev + `✓ Phase 2: Syntax Analysis Complete\n`);
      
      // Phase 3: Semantic Analysis
      const { symbolTable: symTable, errors } = semanticAnalysis(ast);
      setSymbolTable(symTable);
      
      if (errors.length > 0) {
        setOutput(prev => prev + `\n✗ Semantic Errors:\n${errors.join('\n')}\n`);
        return;
      }
      setOutput(prev => prev + `✓ Phase 3: Semantic Analysis Complete\n`);
      
      // Phase 4: Intermediate Code Generation
      const quads = generateIntermediateCode(ast);
      setIntermediateCode(quads);
      setOutput(prev => prev + `✓ Phase 4: Intermediate Code Generated (${quads.length} quads)\n`);
      
      // Phase 5: Optimization
      const optimized = optimize(quads, symTable);
      setOptimizedCode(optimized);
      setOutput(prev => prev + `✓ Phase 5: Optimization Complete (${quads.length - optimized.length} instructions removed)\n`);
      
      // Phase 6: Code Generation
      const finalCode = generateCode(optimized, symTable, ast.name);
      setOutput(prev => prev + `✓ Phase 6: Code Generation Complete\n\n--- Generated Python Code ---\n${finalCode}`);
      
    } catch (error) {
      setOutput(prev => prev + `\n✗ Compilation Error:\n${error.message}`);
    }
  };

  const phases = [
    { id: 'lexer', name: 'Phase 1: Lexer', icon: Code },
    { id: 'parser', name: 'Phase 2: Parser', icon: FileText },
    { id: 'semantic', name: 'Phase 3: Semantic', icon: CheckCircle },
    { id: 'icg', name: 'Phase 4: ICG', icon: FileText },
    { id: 'optimize', name: 'Phase 5: Optimize', icon: CheckCircle },
    { id: 'codegen', name: 'Phase 6: Code Gen', icon: Code },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">Logic Gate Architect</h1>
          <p className="text-blue-300">Complete 6-Phase Compiler Implementation</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Source Code Editor</h2>
              <div className="flex gap-2">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileLoad}
                  accept=".gate,.txt"
                  className="hidden"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded-lg transition text-sm"
                  title="Load from file"
                >
                  <Upload size={16} />
                  Load
                </button>
                <button
                  onClick={handleSaveSource}
                  className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 px-3 py-2 rounded-lg transition text-sm"
                  title="Save source code"
                >
                  <Save size={16} />
                  Save
                </button>
                <button
                  onClick={compile}
                  className="flex items-center gap-2 bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition"
                >
                  <Play size={16} />
                  Compile
                </button>
              </div>
            </div>
            <textarea
              value={sourceCode}
              onChange={(e) => setSourceCode(e.target.value)}
              className="w-full h-64 bg-gray-900 text-green-400 font-mono p-4 rounded border border-gray-700 focus:border-blue-500 focus:outline-none"
              spellCheck={false}
            />
          </div>

          <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Compiler Output</h2>
              <div className="flex gap-2">
                <button
                  onClick={handleSaveOutput}
                  className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded-lg transition text-sm"
                  title="Save output"
                >
                  <Download size={16} />
                  Save Output
                </button>
                <button
                  onClick={handleSavePython}
                  className="flex items-center gap-2 bg-yellow-600 hover:bg-yellow-700 px-3 py-2 rounded-lg transition text-sm"
                  title="Save Python code"
                >
                  <Code size={16} />
                  Save Python
                </button>
              </div>
            </div>
            <pre className="w-full h-64 bg-gray-900 text-gray-300 font-mono text-sm p-4 rounded border border-gray-700 overflow-auto whitespace-pre-wrap">
              {output || 'Click "Compile" to see output...'}
            </pre>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 shadow-xl mb-6">
          <h2 className="text-xl font-bold mb-4">Compilation Phases</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {phases.map(({ id, name, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActivePhase(id)}
                className={`p-4 rounded-lg transition ${
                  activePhase === id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                <Icon className="mx-auto mb-2" size={24} />
                <p className="text-xs text-center">{name}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
          <h2 className="text-xl font-bold mb-4">
            {phases.find(p => p.id === activePhase)?.name} Details
          </h2>
          
          {activePhase === 'lexer' && (
            <div className="space-y-4">
              <p className="text-gray-300">Tokens generated from source code:</p>
              <div className="bg-gray-900 p-4 rounded max-h-96 overflow-auto">
                {tokens.length > 0 ? (
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-blue-400">
                        <th className="p-2">Type</th>
                        <th className="p-2">Value</th>
                        <th className="p-2">Line</th>
                        <th className="p-2">Column</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tokens.map((token, i) => (
                        <tr key={i} className="border-t border-gray-700">
                          <td className="p-2 text-green-400">{token.type}</td>
                          <td className="p-2">{token.value}</td>
                          <td className="p-2">{token.line}</td>
                          <td className="p-2">{token.column}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-gray-500">No tokens yet. Click "Compile" to generate.</p>
                )}
              </div>
            </div>
          )}

          {activePhase === 'parser' && (
            <div className="space-y-4">
              <p className="text-gray-300">Abstract Syntax Tree (AST):</p>
              <div className="bg-gray-900 p-4 rounded max-h-96 overflow-auto">
                <pre className="text-sm text-green-400">
                  {parseTree ? JSON.stringify(parseTree, null, 2) : 'No parse tree yet. Click "Compile" to generate.'}
                </pre>
              </div>
            </div>
          )}

          {activePhase === 'semantic' && (
            <div className="space-y-4">
              <p className="text-gray-300">Symbol Table:</p>
              <div className="bg-gray-900 p-4 rounded max-h-96 overflow-auto">
                {Object.keys(symbolTable).length > 0 ? (
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-blue-400">
                        <th className="p-2">Identifier</th>
                        <th className="p-2">Category</th>
                        <th className="p-2">Defined</th>
                        <th className="p-2">Used By</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(symbolTable).map(([id, info]) => (
                        <tr key={id} className="border-t border-gray-700">
                          <td className="p-2 text-yellow-400">{id}</td>
                          <td className="p-2">{info.category}</td>
                          <td className="p-2">{info.defined ? '✓' : '✗'}</td>
                          <td className="p-2">{info.usedBy?.join(', ') || 'None'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-gray-500">No symbol table yet. Click "Compile" to generate.</p>
                )}
              </div>
            </div>
          )}

          {activePhase === 'icg' && (
            <div className="space-y-4">
              <p className="text-gray-300">Quadruples (Intermediate Representation):</p>
              <div className="bg-gray-900 p-4 rounded max-h-96 overflow-auto">
                {intermediateCode.length > 0 ? (
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-blue-400">
                        <th className="p-2">#</th>
                        <th className="p-2">Operator</th>
                        <th className="p-2">Arg1</th>
                        <th className="p-2">Arg2</th>
                        <th className="p-2">Result</th>
                      </tr>
                    </thead>
                    <tbody>
                      {intermediateCode.map((quad, i) => (
                        <tr key={i} className="border-t border-gray-700">
                          <td className="p-2 text-gray-500">{i + 1}</td>
                          <td className="p-2 text-purple-400">{quad.op}</td>
                          <td className="p-2">{quad.arg1 || '-'}</td>
                          <td className="p-2">{quad.arg2 || '-'}</td>
                          <td className="p-2 text-green-400">{quad.result}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-gray-500">No intermediate code yet. Click "Compile" to generate.</p>
                )}
              </div>
            </div>
          )}

          {activePhase === 'optimize' && (
            <div className="space-y-4">
              <p className="text-gray-300">Optimized Code (After constant folding, identity laws, dead code elimination):</p>
              <div className="bg-gray-900 p-4 rounded max-h-96 overflow-auto">
                {optimizedCode.length > 0 ? (
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-blue-400">
                        <th className="p-2">#</th>
                        <th className="p-2">Operator</th>
                        <th className="p-2">Arg1</th>
                        <th className="p-2">Arg2</th>
                        <th className="p-2">Result</th>
                      </tr>
                    </thead>
                    <tbody>
                      {optimizedCode.map((quad, i) => (
                        <tr key={i} className="border-t border-gray-700">
                          <td className="p-2 text-gray-500">{i + 1}</td>
                          <td className="p-2 text-purple-400">{quad.op}</td>
                          <td className="p-2">{quad.arg1 || '-'}</td>
                          <td className="p-2">{quad.arg2 || '-'}</td>
                          <td className="p-2 text-green-400">{quad.result}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-gray-500">No optimized code yet. Click "Compile" to generate.</p>
                )}
              </div>
            </div>
          )}

          {activePhase === 'codegen' && (
            <div className="space-y-4">
              <p className="text-gray-300">Final generated Python code is shown in the output panel above.</p>
              <div className="bg-gray-900 p-4 rounded">
                <p className="text-sm text-gray-400">
                  The code generator produces a Python simulation function that:
                </p>
                <ul className="list-disc list-inside text-sm text-gray-400 mt-2 space-y-1">
                  <li>Defines a simulate() function with circuit inputs as parameters</li>
                  <li>Implements each gate operation using Python operators</li>
                  <li>Returns all circuit outputs</li>
                  <li>Generates a complete truth table for all input combinations</li>
                </ul>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 bg-gray-800 rounded-lg p-6 shadow-xl">
          <h2 className="text-xl font-bold mb-4">Test Cases</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => setSourceCode(`CIRCUIT BasicAND {
  INPUT A, B;
  OUTPUT Z;
  Z = AND(A, B);
}`)}
              className="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-left transition"
            >
              <h3 className="font-bold mb-2">Test 1: Basic AND Gate</h3>
              <p className="text-sm text-gray-400">Simple 2-input AND gate</p>
            </button>
            
            <button
              onClick={() => setSourceCode(`CIRCUIT HalfAdder {
  INPUT A, B;
  OUTPUT Sum, Carry;
  Sum = XOR(A, B);
  Carry = AND(A, B);
}`)}
              className="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-left transition"
            >
              <h3 className="font-bold mb-2">Test 2: Half Adder</h3>
              <p className="text-sm text-gray-400">Arithmetic circuit with multiple outputs</p>
            </button>
            
            <button
              onClick={() => setSourceCode(`CIRCUIT ErrorTest {
  WIRE A;
  A = NOT(A);
}`)}
              className="bg-red-900 hover:bg-red-800 p-4 rounded-lg text-left transition"
            >
              <h3 className="font-bold mb-2">Test 3: Cycle Error</h3>
              <p className="text-sm text-gray-400">Should detect combinational loop</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogicGateCompiler;
# Awesome Agent Harnesses

A comprehensive collection of production-ready AI agent execution frameworks and integration patterns.

## 🚀 Quick Start

### Papermill + OpenCode Integration
Execute AI agents through Jupyter notebooks with full parameterization and automation:

```bash
cd examples/papermill/opencode
make run PROMPT="Create a Python function that calculates fibonacci numbers"
```

### Kiro Database Analysis
Analyze conversation histories from Kiro CLI:

```bash
cd examples
./kiro-history-viewer.sh /path/to/data.sqlite3
```

## 📋 Available Harnesses

### 1. **Papermill + OpenCode Atomic Agent** ⚡
**Location**: `examples/papermill/opencode/`  
**Status**: ✅ Production Ready

Complete atomic AI agent execution system using Papermill and OpenCode CLI integration.

**Key Features:**
- **Zero-setup execution**: `make run PROMPT="your prompt"`  
- **Multi-kernel support**: Python and Bash kernels
- **Parameterized workflows**: YAML configuration files
- **Session management**: Timestamped outputs and cleanup
- **Error handling**: Comprehensive retry and cleanup logic

**Quick Commands:**
```bash
make run-riddle          # Generate programming riddles
make run-code           # Generate Python code  
make run-explanation    # Technical explanations
make test-all           # Run all example workflows
```

### 2. **Kiro CLI Analysis Tools** 📊  
**Location**: `examples/`  
**Status**: ✅ Production Ready

Comprehensive tools for analyzing Kiro CLI conversation databases with zero dependencies.

**Available Tools:**
- `kiro-history-viewer.sh` - Bash script for viewing histories (zero dependencies)
- `kiro-analyzer.js` - Rich JavaScript analyzer with console output
- `kiro-types.ts` - Complete TypeScript type definitions
- Full SQL schema documentation

## 🛠️ Environment Setup

### Papermill Environment
```bash
cd examples/papermill
make setup              # Complete environment setup
source venv/bin/activate # Activate virtual environment
make jupyter            # Launch JupyterLab interface
```

### Kiro Analysis Tools  
```bash
cd examples
npm install            # Install JavaScript dependencies (optional)
```

## 📚 Documentation

- **[Kiro Database Analysis Guide](docs/kiro-database-analysis.md)** - Complete SQL schema and usage examples
- **[Papermill Integration Guide](examples/papermill/README.md)** - Detailed setup and usage
- **[OpenCode Agent Guide](examples/papermill/opencode/README.md)** - Atomic agent patterns

## 🎯 Usage Patterns

### Atomic AI Execution
Execute single AI operations with full automation:
```bash
make run PROMPT="Explain quantum computing in simple terms"
make run MODEL="claude-3-opus-20240229" PROMPT="Write a haiku about coding"
```

### Multi-step AI Workflows  
Chain multiple AI operations with session continuity:
```bash
make pipeline           # Execute predefined multi-step workflow
make batch             # Run multiple prompts in sequence  
```

### Database Analysis
Extract insights from conversation histories:
```bash
./kiro-history-viewer.sh data.sqlite3 | grep "2024-01" 
node kiro-analyzer.js --stats data.sqlite3
```

## 🏗️ Architecture

### Papermill Integration Pattern
```
User Input → YAML Config → Papermill → Jupyter Notebook → OpenCode CLI → AI Response
```

### Atomic Agent Pattern  
- **Input**: Parameterized YAML configuration
- **Processing**: Bash kernel executes OpenCode CLI
- **Output**: Timestamped results with full context
- **Cleanup**: Automatic session management and cleanup

### Database Analysis Pattern
- **Input**: SQLite database from Kiro CLI
- **Processing**: SQL queries + JavaScript analysis
- **Output**: Structured data and insights
- **Format**: Console output, JSON, or formatted text

## 🔧 Customization

### Adding New Agent Types
1. Create new YAML parameter files in `examples/papermill/opencode/`
2. Add corresponding Makefile targets for easy execution
3. Document usage patterns in README files

### Extending Database Analysis
1. Add new SQL queries to analysis tools
2. Extend TypeScript types for new data structures  
3. Create specialized analysis functions

## 🚦 Testing

```bash
# Test Papermill integration
cd examples/papermill && make test

# Test OpenCode atomic agents  
cd examples/papermill/opencode && make test-all

# Test Kiro analysis tools
cd examples && npm test
```

## 📈 Performance

- **Atomic agents**: ~2-10 seconds per execution (model dependent)
- **Database analysis**: Handles databases with 10k+ conversations
- **Session overhead**: Minimal with automatic cleanup
- **Parallelization**: Full support for concurrent operations

## 🤝 Contributing

1. Follow established patterns in `examples/` directory
2. Add comprehensive documentation for new harnesses
3. Include working examples and test cases
4. Update this README with new capabilities

## 📄 License

MIT License - see LICENSE file for details.

---

**🎯 Goal**: Provide production-ready, zero-friction AI agent execution patterns that scale from simple prompts to complex multi-agent workflows.

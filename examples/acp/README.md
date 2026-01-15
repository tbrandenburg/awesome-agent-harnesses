# OpenCode ACP Integration Examples

This directory contains comprehensive examples and tools for working with OpenCode's Agent Client Protocol (ACP), enabling programmatic interaction with AI agents outside of traditional editors.

## 🚀 Quick Start

```bash
# Test basic functionality
make test-basic

# Try interactive mode
make interactive  

# Run a code review demo
make demo-review

# See all available commands
make help
```

## 📁 Files Overview

### Core ACP Clients

#### **`acp_client.py`** - Basic ACP Client
Simple demonstration of ACP protocol fundamentals:
- WebSocket connection management
- Basic JSON-RPC communication
- Session creation and cleanup
- Single prompt execution

**Usage:**
```bash
python acp_client.py "Your prompt here"
make test-basic
```

#### **`advanced_acp_client.py`** - Advanced ACP Client  
Production-ready client with comprehensive features:
- Interactive mode for multiple prompts
- Real-time tool call monitoring
- Streaming response handling
- Configurable timeouts and working directories
- Session management with proper cleanup

**Usage:**
```bash
# Single prompt
python advanced_acp_client.py --prompt "Analyze this codebase"

# Interactive mode
python advanced_acp_client.py --interactive
make interactive

# Custom configuration  
python advanced_acp_client.py --prompt "Generate tests" --timeout 300 --workdir /path/to/project
```

### Specialized Harnesses

#### **`practical_code_review.py`** - Code Review Automation
Real-world example demonstrating ACP automation for code analysis:
- Single file, directory, or batch processing
- Multiple analysis types (comprehensive, security, performance, quick)
- Markdown report generation
- CI/CD integration patterns

**Usage:**
```bash
# Single file analysis
python practical_code_review.py --file src/main.py --type comprehensive
make review-file FILE=src/main.py

# Directory security scan
python practical_code_review.py --directory src/ --type security --output security_report.md
make review-security DIR=src/

# Batch processing
python practical_code_review.py --batch "**/*.py" --type performance --max-files 20
make review-batch PATTERN="*.py"
```

#### **`multi_agent_coordinator.py`** - Multi-Agent System
Sophisticated coordination system using multiple specialized AI agents:
- 5 specialized agents (Code Analyst, Security Expert, Performance Expert, Documentation Specialist, Integration Coordinator)
- Parallel execution with task coordination
- Result synthesis and comprehensive reporting
- Extensible framework for additional agent types

**Usage:**
```bash
# Project analysis with multiple agents
python multi_agent_coordinator.py --project /path/to/project --output analysis_report.md
make demo-multi-agent
make analysis-project DIR=/path/to/project
```

#### **`code_review_harness.py`** - Advanced Code Review Framework
Comprehensive async-based code review system with WebSocket integration:
- Asynchronous agent execution
- Batch file processing
- Advanced error handling
- Fix suggestion generation

## 🛠️ Makefile Commands

### Quick Start
- `make help` - Show all available commands
- `make setup` - Set up development environment
- `make test-all` - Run all tests to verify functionality

### Testing & Validation
- `make test-basic` - Test basic ACP client functionality
- `make test-advanced` - Test advanced ACP client features
- `make check-deps` - Verify OpenCode and dependencies
- `make integration-test` - Run full integration test suite

### Code Review Examples
- `make demo-review` - Demo code review on current directory
- `make review-file FILE=<path>` - Review single file
- `make review-security DIR=<path>` - Security scan of directory  
- `make review-performance FILE=<path>` - Performance analysis
- `make review-batch PATTERN='*.py'` - Batch review matching pattern

### Multi-Agent Workflows
- `make demo-multi-agent` - Run multi-agent project analysis
- `make analysis-project DIR=<path>` - Full project analysis

### Interactive & Advanced
- `make interactive` - Start interactive ACP session
- `make demo-workflow` - Complete development workflow demonstration
- `make demo-cicd` - Simulate CI/CD integration
- `make demo-parallel` - Demonstrate parallel processing

### Utilities
- `make clean` - Clean up generated files
- `make show-examples` - List all available examples
- `make show-architecture` - Display ACP architecture overview

## 🏗️ ACP Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Python Client │    │     ACP      │    │   OpenCode      │
│                 │◄──►│   Protocol   │◄──►│   Session       │
│ (Your Harness)  │    │  (WebSocket) │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Model Context   │
                    │  Protocol (MCP)  │
                    │    Servers       │
                    └──────────────────┘
```

## 🎯 Key Benefits

### Editor Independence
- Run OpenCode agents from any environment, not just VS Code
- Perfect for headless environments, CI/CD, and automation
- Build custom workflows tailored to specific needs

### Programmatic Control
- Full API access to OpenCode capabilities
- Real-time monitoring of agent activities
- Structured output for downstream processing

### Scalability
- Parallel agent execution for complex tasks
- Batch processing across multiple files and projects
- Multi-agent coordination for comprehensive analysis

## 📋 Integration Patterns

### CI/CD Automation
```python
# Integrate into your CI pipeline
import subprocess

def automated_code_review(changed_files):
    for file_path in changed_files:
        result = subprocess.run([
            "python", "practical_code_review.py",
            "--file", file_path,
            "--type", "security"
        ], capture_output=True, text=True)
        
        if "CRITICAL" in result.stdout:
            return {"status": "FAIL", "file": file_path}
    
    return {"status": "PASS"}
```

### Custom Documentation Generation
```bash
# Generate docs for all Python files
make review-batch PATTERN="*.py" | \
  grep -E "(Summary|Rating)" > project_overview.md
```

### Multi-Agent Analysis Pipeline
```bash
# Complete project health check
make analysis-project DIR=src/ && \
make review-security DIR=src/ && \
make review-batch PATTERN="src/**/*.py"
```

## 🔧 Development

### Setup Development Environment
```bash
make dev-setup
make lint      # Code linting
make format    # Code formatting
```

### Adding New Examples
1. Create your ACP client following existing patterns
2. Add corresponding Makefile targets
3. Update this README with usage examples
4. Test with `make integration-test`

### Performance Considerations
- Use timeouts for long-running operations
- Implement proper cleanup in error scenarios
- Consider parallel processing for batch operations
- Monitor resource usage with multiple concurrent agents

## 🐛 Troubleshooting

### Common Issues

**ACP Connection Failed**
- Ensure OpenCode CLI is installed: `opencode --version`
- Check if OpenCode is authenticated: `opencode auth status`

**Timeout Errors**
- Increase timeout with `--timeout` parameter
- Check network connectivity
- Verify OpenCode server is responsive

**Session Creation Failed**
- Verify working directory exists and is accessible
- Check file permissions
- Ensure OpenCode has proper authentication

### Debug Mode
```bash
# Enable verbose logging in advanced client
python advanced_acp_client.py --prompt "test" --verbose

# Test connection without full execution
make check-deps
```

## 📚 Further Reading

- **[OpenCode Documentation](https://opencode.ai/docs)** - Complete OpenCode guide
- **[ACP Protocol Specification](https://opencode.ai/docs/acp)** - Technical protocol details
- **[Main Repository README](../../README.md)** - Full harnesses collection overview
- **[Community Patterns](https://github.com/nibzard/awesome-agentic-patterns)** - Broader agentic design patterns

---

**💡 Tip**: Start with `make help` to see all available commands, then try `make test-basic` followed by `make interactive` to get familiar with ACP capabilities.
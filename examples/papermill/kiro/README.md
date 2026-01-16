# Kiro-CLI Papermill Integration

This directory contains a simple example of integrating kiro-cli with papermill for automated AI agent execution.

## Overview

The kiro-cli integration demonstrates how to:
- Execute kiro-cli commands in a parameterized, reproducible way
- Capture AI agent responses in Jupyter notebook format
- Handle errors and timeouts gracefully  
- Integrate with automation workflows via Make

## Features

- **Papermill Integration**: Leverages papermill's notebook parameterization and execution engine
- **Proper Output Handling**: Uses `nbformat` for reliable notebook reading with ANSI escape sequence cleanup
- **Atomic AI Agent**: Each execution is isolated with proper timeout and error handling
- **Timestamped Outputs**: All executions create unique output files with timestamps
- **Security Mode**: Runs with `--trust-all-tools` for maximum agent functionality
- **Makefile Automation**: Simple commands for testing, execution, and cleanup

## Files

- **Makefile**: Automation commands for running kiro-cli via papermill
- **kiro_prompt.ipynb**: Core Jupyter notebook that executes kiro-cli
- **output/**: Directory containing executed notebooks with results

## Quick Start

### Prerequisites

1. **kiro-cli installed and available in PATH**
   ```bash
   # Check if kiro-cli is available
   which kiro-cli
   kiro-cli --version  # or test basic functionality
   ```

2. **Papermill environment activated**
   ```bash
   # From the examples/papermill directory
   source venv/bin/activate
   ```

### Basic Usage

```bash
# Simple hello world example
make run-simple

# Custom prompt
make run PROMPT="Explain what machine learning is in simple terms"

# Code generation with file writing permissions
make run-code

# Analysis with file reading permissions  
make run-analysis

# Interactive prompt entry
make interactive
```

### Advanced Usage

```bash
# Custom prompt with specific model
make run PROMPT="Write a sorting algorithm" MODEL="gpt-4"

# With trusted tools for file operations
make run PROMPT="Analyze the files in this directory" TRUST="fs_read"

# Custom timeout
make run PROMPT="Complex analysis task" TIMEOUT="600"
```

## Key Features

### Parameter Support
- **PROMPT**: The question or instruction for the AI
- **MODEL**: Specific AI model to use (optional)
- **TRUST**: Comma-separated list of tools the AI can use (e.g., "fs_read,shell_safe")
- **TIMEOUT**: Maximum execution time in seconds

### Trust Levels
Following kiro-cli security best practices:
- **No trust** (default): AI can only provide text responses
- **fs_read**: AI can read files in the current directory
- **fs_write**: AI can create/modify files  
- **shell_safe**: AI can run safe shell commands
- **fs_read,fs_write**: Combined permissions

### Output Management
- All executions create timestamped notebooks in `output/`
- Captures both successful responses and error information
- Includes execution metadata for debugging

## Example Commands

```bash
# Check system status
make status

# Run basic test
make test  

# Clean up output files
make clean

# Show help with all options
make help
```

## Integration Patterns

This example demonstrates patterns for:
- **CI/CD Integration**: Non-interactive AI agent execution
- **Batch Processing**: Automated AI workflows
- **Error Handling**: Graceful failure with detailed logging
- **Reproducibility**: Parameterized execution with full audit trail

## Security Notes

- Default configuration uses no trusted tools for safety
- Always specify minimal required permissions via TRUST parameter
- Review kiro-cli documentation for trust level implications
- Output files may contain sensitive information from AI responses

## Troubleshooting

1. **"kiro-cli command not found"**
   - Ensure kiro-cli is installed and in PATH
   - Check with: `which kiro-cli`

2. **Papermill errors**
   - Ensure you're in the papermill virtual environment
   - Check: `source ../venv/bin/activate`

3. **Permission errors**  
   - Verify trust level matches required operations
   - Use appropriate TRUST parameter for your use case

4. **Timeout errors**
   - Increase TIMEOUT parameter for complex queries
   - Check kiro-cli connectivity and API availability
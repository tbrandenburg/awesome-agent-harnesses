# Kiro-CLI Atomic Agent Makefile
# Simple command automation for kiro-cli via papermill

SHELL := /bin/bash

.PHONY: help run run-simple run-code run-analysis test clean status

# Default target
help:
	@echo "🤖 Kiro-CLI Atomic Agent Commands"
	@echo "================================="
	@echo ""
	@echo "🚀 Main Commands:"
	@echo "  make run          - Run kiro-cli with custom prompt"
	@echo "  make run-simple   - Simple hello world example"
	@echo "  make run-code     - Code generation example"
	@echo "  make run-analysis - Code analysis example"
	@echo ""
	@echo "🔧 Utility Commands:"
	@echo "  make test         - Test the kiro-cli integration"
	@echo "  make clean        - Clean up output files"
	@echo "  make status       - Check system status"
	@echo ""
	@echo "📖 Usage Examples:"
	@echo "  make run PROMPT=\"Explain machine learning\""
	@echo "  make run PROMPT=\"Write a Python function\" MODEL=\"gpt-4\""
	@echo "  make run-simple"
	@echo "  make run-code"
	@echo ""
	@echo "⚙️  Parameters:"
	@echo "  PROMPT=           - The prompt to send to kiro-cli"
	@echo "  MODEL=            - Model to use (optional)"
	@echo "  TIMEOUT=          - Timeout in seconds (default: 300)"
	@echo ""
	@echo "🔓 Security: This example uses --trust-all-tools for maximum functionality"

# Default parameters
PROMPT ?= Hello! Please introduce yourself and explain what you can help with.
MODEL ?= 
TIMEOUT ?= 300

# Get timestamp for unique output files
TIMESTAMP = $(shell date +%Y%m%d_%H%M%S)

# Virtual environment activation (go up one level to papermill directory)
VENV_ACTIVATE = source ../venv/bin/activate &&

# Main run command with custom parameters
run: output
	@echo "🤖 Running Kiro-CLI Atomic Agent"
	@echo "==============================="
	@echo "Prompt: $(PROMPT)"
	@if [ -n "$(MODEL)" ]; then echo "Model: $(MODEL)"; fi
	@echo "Trust Level: ALL TOOLS TRUSTED"
	@echo "Timeout: $(TIMEOUT)s"
	@echo ""
	$(VENV_ACTIVATE) papermill kiro_prompt.ipynb output/kiro_$(TIMESTAMP).ipynb \
		-p prompt "$(PROMPT)" \
		-p model "$(MODEL)" \
		-p timeout "$(TIMEOUT)" \
		--log-level INFO
	@echo ""
	@echo "📤 Kiro-CLI Response:"
	@echo "==========================================" 
	@$(VENV_ACTIVATE) python3 -c "import nbformat; import re; nb=nbformat.read('output/kiro_$(TIMESTAMP).ipynb', as_version=4); [print(re.sub(r'\x1b\[[0-9;]*m', '', ''.join(output.text)).split('📤 Kiro-CLI Response:\n')[1].split('\n--------------------------------------------------')[0].strip()) for cell in nb.cells if hasattr(cell, 'outputs') and cell.outputs for output in cell.outputs if hasattr(output, 'text') and output.text and '📤 Kiro-CLI Response:' in ''.join(output.text)]" 2>/dev/null || echo "No response available"
	@echo "=========================================="
	@echo "✅ Full execution details: output/kiro_$(TIMESTAMP).ipynb"

# Simple hello world example
run-simple: output
	@echo "👋 Simple Kiro-CLI Example"
	@echo "========================="
	$(VENV_ACTIVATE) papermill kiro_prompt.ipynb output/simple_$(TIMESTAMP).ipynb \
		-p prompt "Hello! Please tell me what you are and give me a simple example of what you can do." \
		-p timeout "60" \
		--log-level INFO
	@echo ""
	@echo "✅ Simple example complete! Check output/simple_$(TIMESTAMP).ipynb"

# Code generation example
run-code: output
	@echo "💻 Kiro-CLI Code Generation"
	@echo "=========================="
	$(VENV_ACTIVATE) papermill kiro_prompt.ipynb output/code_$(TIMESTAMP).ipynb \
		-p prompt "Write a simple Python function that calculates the factorial of a number. Include docstring and example usage." \
		-p timeout "120" \
		--log-level INFO
	@echo ""
	@echo "✅ Code generation complete! Check output/code_$(TIMESTAMP).ipynb"

# Code analysis example
run-analysis: output
	@echo "🔍 Kiro-CLI Code Analysis"
	@echo "========================"
	$(VENV_ACTIVATE) papermill kiro_prompt.ipynb output/analysis_$(TIMESTAMP).ipynb \
		-p prompt "Please analyze the current directory structure and tell me what kind of project this appears to be." \
		-p timeout "180" \
		--log-level INFO
	@echo ""
	@echo "✅ Analysis complete! Check output/analysis_$(TIMESTAMP).ipynb"

# Test the kiro-cli integration
test: output
	@echo "🧪 Testing Kiro-CLI Integration"
	@echo "==============================="
	@echo ""
	@echo "Testing basic functionality..."
	$(VENV_ACTIVATE) papermill kiro_prompt.ipynb output/test_$(TIMESTAMP).ipynb \
		-p prompt "Test: What is 2 + 2? Just give me the answer." \
		-p timeout "30" \
		--log-level INFO
	@echo ""
	@echo "📤 Test Response:"
	@echo "================" 
	@$(VENV_ACTIVATE) python3 -c "import json; nb=json.load(open('output/test_$(TIMESTAMP).ipynb')); [print(''.join(cell['outputs'][i]['text']).split('📤 Kiro-CLI Response:\n')[1].split('\n--------------------------------------------------')[0]) for cell in nb['cells'] if cell.get('outputs') for i in range(len(cell['outputs'])) if cell['outputs'][i].get('output_type') == 'stream' and '📤 Kiro-CLI Response:' in ''.join(cell['outputs'][i]['text'])]" 2>/dev/null || echo "No response available"
	@echo "================"
	@echo "✅ Full test details: output/test_$(TIMESTAMP).ipynb"

# Create output directory
output:
	mkdir -p output

# Status check
status:
	@echo "📊 Kiro-CLI Agent Status"
	@echo "======================="
	@echo ""
	@if [ -f "kiro_prompt.ipynb" ]; then \
		echo "✅ Atomic agent notebook: EXISTS"; \
	else \
		echo "❌ Atomic agent notebook: MISSING"; \
	fi
	@if [ -f "../venv/bin/activate" ]; then \
		echo "✅ Papermill environment: EXISTS"; \
	else \
		echo "❌ Papermill environment: MISSING (run 'make setup' in parent directory)"; \
	fi
	@if [ -d "output" ]; then \
		echo "📁 Output files: $(shell find output -name '*.ipynb' 2>/dev/null | wc -l) notebooks"; \
	else \
		echo "📁 Output directory: Will be created on first run"; \
	fi
	@echo ""
	@echo "🔧 Kiro-CLI status:"
	@if command -v kiro-cli >/dev/null 2>&1; then \
		echo "✅ Kiro-CLI: Available"; \
	else \
		echo "❌ Kiro-CLI: NOT FOUND (install kiro-cli first)"; \
	fi

# Clean up generated files
clean:
	@echo "🧹 Cleaning up Kiro-CLI output files"
	rm -rf output/
	rm -f *.ipynb_checkpoints
	rm -rf .ipynb_checkpoints/
	@echo "✅ Cleanup complete!"

# Interactive prompt (bonus feature)
interactive:
	@echo "🎯 Interactive Kiro-CLI Prompt"
	@echo "============================="
	@echo "Enter your prompt (or press Ctrl+C to cancel):"
	@read -p "> " user_prompt; \
	if [ -n "$$user_prompt" ]; then \
		$(MAKE) run PROMPT="$$user_prompt"; \
	else \
		echo "No prompt provided."; \
	fi
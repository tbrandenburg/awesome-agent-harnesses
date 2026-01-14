# OpenCode Atomic Agent Makefile  
# Easy commands for running the atomic OpenCode execution notebook

SHELL := /bin/bash

.PHONY: help run run-riddle run-code run-explanation test-all setup clean examples batch

# Default target
help:
	@echo "🤖 OpenCode Atomic Agent Commands"
	@echo "================================="
	@echo ""
	@echo "🚀 Main Commands:"
	@echo "  make run          - Run OpenCode agent with custom prompt"
	@echo "  make run-riddle   - Generate a programming riddle"
	@echo "  make run-code     - Generate Python code"
	@echo "  make run-explanation - Technical explanation"
	@echo ""
	@echo "🔧 Utility Commands:"
	@echo "  make test-all     - Test all example configurations"
	@echo "  make examples     - List all available examples"
	@echo "  make batch        - Run multiple examples in sequence"
	@echo "  make clean        - Clean up output files"
	@echo ""
	@echo "📖 Usage Examples:"
	@echo "  make run PROMPT=\"Explain machine learning\""
	@echo "  make run PROMPT=\"Write a Python function\" MODEL=\"opencode/grok-code\""
	@echo "  make run-riddle"
	@echo "  make run-code"
	@echo ""
	@echo "⚙️  Parameters:"
	@echo "  PROMPT=           - The prompt to send to OpenCode"
	@echo "  MODEL=            - Model to use (e.g., opencode/grok-code)"
	@echo "  SESSION_ID=       - Continue existing session"
	@echo "  TIMEOUT=          - Timeout in seconds (default: 300)"
	@echo "  VERBOSE=          - Enable verbose output (true/false)"
	@echo "  OUTPUT_FORMAT=    - Output format (text/json/markdown)"

# Default parameters
PROMPT ?= "Create a simple programming riddle"
MODEL ?= 
SESSION_ID ?= 
TIMEOUT ?= 300
VERBOSE ?= false
OUTPUT_FORMAT ?= text

# Get timestamp for unique output files
TIMESTAMP = $(shell date +%Y%m%d_%H%M%S)

# Virtual environment activation (go up one level to papermill directory)
VENV_ACTIVATE = source ../venv/bin/activate &&

# Main run command with custom parameters
run: output
	@echo "🤖 Running OpenCode Atomic Agent"
	@echo "==============================="
	@echo "Prompt: $(PROMPT)"
	@if [ -n "$(MODEL)" ]; then echo "Model: $(MODEL)"; fi
	@if [ -n "$(SESSION_ID)" ]; then echo "Session ID: $(SESSION_ID)"; fi
	@echo "Timeout: $(TIMEOUT)s"
	@echo "Verbose: $(VERBOSE)"
	@echo "Output Format: $(OUTPUT_FORMAT)"
	@echo ""
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/custom_$(TIMESTAMP).ipynb \
		-p prompt "$(PROMPT)" \
		-p model "$(MODEL)" \
		-p session_id "$(SESSION_ID)" \
		-p timeout "$(TIMEOUT)" \
		-p verbose "$(VERBOSE)" \
		-p output_format "$(OUTPUT_FORMAT)" \
		--log-level INFO
	@echo ""
	@echo "✅ OpenCode execution complete! Check output/custom_$(TIMESTAMP).ipynb"

# Run the riddle example
run-riddle: output
run-riddle: output
	@echo "🎲 Generating Programming Riddle"
	@echo "==============================="
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/riddle_$(TIMESTAMP).ipynb \
		-f example_riddle.yaml \
		--log-level INFO
	@echo ""
	@echo "✅ Riddle generated! Check output/riddle_$(TIMESTAMP).ipynb"

# Run the code generation example
run-code: output
	@echo "💻 Generating Python Code"
	@echo "========================="
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/code_$(TIMESTAMP).ipynb \
		-f example_code.yaml \
		--log-level INFO
	@echo ""
	@echo "✅ Code generated! Check output/code_$(TIMESTAMP).ipynb"

# Run the explanation example  
run-explanation: output
	@echo "📚 Generating Technical Explanation"
	@echo "=================================="
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/explanation_$(TIMESTAMP).ipynb \
		-f example_explanation.yaml \
		--log-level INFO
	@echo ""
	@echo "✅ Explanation generated! Check output/explanation_$(TIMESTAMP).ipynb"

# Test all example configurations
test-all: output
test-all: output
	@echo "🧪 Testing All OpenCode Examples"
	@echo "================================"
	@echo ""
	@echo "1/4 Testing direct parameter execution..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/test_direct.ipynb \
		-p prompt "Test prompt for atomic agent" -p verbose "true"
	@echo ""
	@echo "2/4 Testing riddle example..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/test_riddle.ipynb \
		-f example_riddle.yaml
	@echo ""
	@echo "3/4 Testing code example..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/test_code.ipynb \
		-f example_code.yaml  
	@echo ""
	@echo "4/4 Testing explanation example..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/test_explanation.ipynb \
		-f example_explanation.yaml
	@echo ""
	@echo "✅ All tests completed! Check the output/ directory."

# Run multiple examples in batch
batch: output
	@echo "📦 Running Batch OpenCode Execution"
	@echo "=================================="
	@mkdir -p output/batch_$(TIMESTAMP)
	@echo ""
	@echo "Executing riddle generation..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/batch_$(TIMESTAMP)/riddle.ipynb \
		-f example_riddle.yaml
	@echo ""
	@echo "Executing code generation..."  
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/batch_$(TIMESTAMP)/code.ipynb \
		-f example_code.yaml
	@echo ""
	@echo "Executing explanation generation..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/batch_$(TIMESTAMP)/explanation.ipynb \
		-f example_explanation.yaml
	@echo ""
	@echo "✅ Batch execution complete! Results in output/batch_$(TIMESTAMP)/"

# List all available examples
examples:
	@echo "📋 Available OpenCode Examples"
	@echo "============================="
	@echo ""
	@echo "📄 Configuration Files:"
	@ls -la example_*.yaml 2>/dev/null || echo "No example files found"
	@echo ""
	@echo "🎯 Quick Commands:"
	@echo "  make run-riddle      - Creative programming riddle"
	@echo "  make run-code        - Python code generation"  
	@echo "  make run-explanation - Technical explanation"
	@echo ""
	@echo "🔧 Parameter Examples:"
	@echo "  make run PROMPT=\"Explain recursion\" MODEL=\"opencode/big-pickle\""
	@echo "  make run PROMPT=\"Write a sorting algorithm\" VERBOSE=true"

# Show example parameters from YAML files
show-params:
	@echo "📝 Example Parameters"
	@echo "===================="
	@echo ""
	@for file in example_*.yaml; do \
		if [ -f "$$file" ]; then \
			echo "📄 $$file:"; \
			grep -E "^(prompt|model|output_format):" "$$file" | sed 's/^/   /'; \
			echo ""; \
		fi \
	done

# Create output directory
output:
	mkdir -p output

# Clean up generated files
clean:
	@echo "🧹 Cleaning up OpenCode output files"
	rm -rf output/
	rm -f *.ipynb_checkpoints  
	rm -rf .ipynb_checkpoints/
	@echo "✅ Cleanup complete!"

# Pipeline example - demonstrate chaining multiple prompts
pipeline:
	@echo "🔗 OpenCode Pipeline Example"
	@echo "============================"
	@mkdir -p output/pipeline_$(TIMESTAMP)
	@echo ""
	@echo "Step 1: Planning phase..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/pipeline_$(TIMESTAMP)/01_plan.ipynb \
		-p prompt "Plan a simple web application for task management" \
		-p verbose "true"
	@echo ""
	@echo "Step 2: Backend development..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/pipeline_$(TIMESTAMP)/02_backend.ipynb \
		-p prompt "Write Python Flask backend code for a task management app"
	@echo ""
	@echo "Step 3: Frontend development..."
	$(VENV_ACTIVATE) papermill opencode_prompt.ipynb output/pipeline_$(TIMESTAMP)/03_frontend.ipynb \
		-p prompt "Create HTML and JavaScript frontend for the task management app"
	@echo ""
	@echo "✅ Pipeline complete! Full development cycle in output/pipeline_$(TIMESTAMP)/"

# Quick interactive prompt
interactive:
	@echo "🎯 Interactive OpenCode Prompt"
	@echo "=============================="
	@echo "Enter your prompt (or press Ctrl+C to cancel):"
	@read -p "> " user_prompt; \
	if [ -n "$$user_prompt" ]; then \
		$(MAKE) run PROMPT="$$user_prompt"; \
	else \
		echo "No prompt provided."; \
	fi

# Status check
status:
	@echo "📊 OpenCode Agent Status"
	@echo "======================="
	@echo ""
	@if [ -f "opencode_prompt.ipynb" ]; then \
		echo "✅ Atomic agent notebook: EXISTS"; \
	else \
		echo "❌ Atomic agent notebook: MISSING"; \
	fi
	@if [ -f "../venv/bin/activate" ]; then \
		echo "✅ Papermill environment: EXISTS"; \
	else \
		echo "❌ Papermill environment: MISSING (run 'make setup' in parent directory)"; \
	fi
	@echo "📄 Example files: $(shell ls example_*.yaml 2>/dev/null | wc -l)"
	@if [ -d "output" ]; then \
		echo "📁 Output files: $(shell find output -name '*.ipynb' 2>/dev/null | wc -l) notebooks"; \
	else \
		echo "📁 Output directory: Will be created on first run"; \
	fi
	@echo ""
	@echo "🔧 OpenCode CLI status:"
	@if command -v opencode >/dev/null 2>&1; then \
		echo "✅ OpenCode CLI: Available ($(shell opencode --version 2>/dev/null || echo 'version unknown'))"; \
	else \
		echo "❌ OpenCode CLI: NOT FOUND (install OpenCode CLI first)"; \
	fi

# Advanced usage examples
advanced:
	@echo "🚀 Advanced OpenCode Usage Examples"
	@echo "==================================="
	@echo ""
	@echo "📋 Session Continuation:"
	@echo "   make run PROMPT=\"Start a story\" SESSION_ID=my-session"
	@echo "   make run PROMPT=\"Continue the story\" SESSION_ID=my-session"
	@echo ""
	@echo "🎯 Model Selection:"
	@echo "   make run PROMPT=\"Write code\" MODEL=\"opencode/grok-code\""
	@echo "   make run PROMPT=\"Creative writing\" MODEL=\"opencode/big-pickle\""
	@echo ""
	@echo "⚙️  Output Formats:"
	@echo "   make run PROMPT=\"Explain AI\" OUTPUT_FORMAT=\"markdown\""
	@echo "   make run PROMPT=\"Generate data\" OUTPUT_FORMAT=\"json\""
	@echo ""
	@echo "⏱️  Timeout Management:"
	@echo "   make run PROMPT=\"Complex task\" TIMEOUT=\"600\""
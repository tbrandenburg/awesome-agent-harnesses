# OpenCode Atomic Agent Makefile  
# Easy commands for running the atomic OpenCode execution notebook

SHELL := /bin/bash

.PHONY: help run run-riddle run-code run-explanation test-all setup clean examples batch pipeline-research pipeline-development session robust

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
	@echo "🔗 Multi-Step Pipelines:"
	@echo "  make pipeline-research    - Multi-step research workflow"
	@echo "  make pipeline-development - Code development pipeline"
	@echo ""
	@echo "💬 Session Management:"
	@echo "  make session              - Multi-turn conversation session"
	@echo "  make list-sessions        - List all active sessions"
	@echo ""
	@echo "🛡️  Robust Execution:"
	@echo "  make robust               - Execute with error handling and retry logic"
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
	@echo ""

# Multi-step pipeline targets
pipeline-research: output
	@echo "🔬 Multi-Step AI Research Pipeline"
	@echo "================================="
	@echo ""
	$(VENV_ACTIVATE) papermill pipeline_execution.ipynb output/pipeline_research_$(TIMESTAMP).ipynb \
		-p pipeline_file "pipeline_research.yaml" \
		-p output_dir "output" \
		-p session_id "research_$(TIMESTAMP)" \
		--log-level INFO
	@echo ""
	@echo "✅ Research pipeline completed! Check output/research_$(TIMESTAMP)/"

pipeline-development: output  
	@echo "💻 Multi-Step Code Development Pipeline"
	@echo "======================================"
	@echo ""
	$(VENV_ACTIVATE) papermill pipeline_execution.ipynb output/pipeline_dev_$(TIMESTAMP).ipynb \
		-p pipeline_file "pipeline_development.yaml" \
		-p output_dir "output" \
		-p session_id "development_$(TIMESTAMP)" \
		--log-level INFO
	@echo ""
	@echo "✅ Development pipeline completed! Check output/development_$(TIMESTAMP)/"

# Enhanced pipeline with custom config
pipeline: output
	@echo "🔗 Custom Multi-Step Pipeline"
	@echo "============================"
	@if [ -z "$(PIPELINE_FILE)" ]; then \
		echo "Usage: make pipeline PIPELINE_FILE=your_pipeline.yaml"; \
		echo "Available pipelines:"; \
		ls -1 pipeline_*.yaml 2>/dev/null || echo "  No pipeline files found"; \
		exit 1; \
	fi
	@echo "Pipeline: $(PIPELINE_FILE)"
	@echo ""
	$(VENV_ACTIVATE) papermill pipeline_execution.ipynb output/custom_pipeline_$(TIMESTAMP).ipynb \
		-p pipeline_file "$(PIPELINE_FILE)" \
		-p output_dir "output" \
		-p session_id "custom_$(TIMESTAMP)" \
		--log-level INFO
	@echo ""
	@echo "✅ Custom pipeline completed! Check output/custom_$(TIMESTAMP)/"

# Session management targets
SESSION_ID ?= default_session
ACTION ?= continue
MAX_HISTORY ?= 10

session: output
	@echo "💬 OpenCode Multi-Turn Session Management"
	@echo "========================================"
	@echo "Session ID: $(SESSION_ID)"
	@echo "Action: $(ACTION)"
	@echo "Prompt: $(PROMPT)"
	@echo "Model: $(MODEL)"
	@echo "Max History: $(MAX_HISTORY)"
	@echo ""
	$(VENV_ACTIVATE) papermill session_management.ipynb output/session_$(SESSION_ID)_$(TIMESTAMP).ipynb \
		-p session_id "$(SESSION_ID)" \
		-p prompt "$(PROMPT)" \
		-p model "$(MODEL)" \
		-p action "$(ACTION)" \
		-p max_history "$(MAX_HISTORY)" \
		-p verbose "$(VERBOSE)" \
		--log-level INFO
	@echo ""
	@echo "✅ Session operation completed!"

# List all active sessions
list-sessions:
	@echo "📋 Active OpenCode Sessions"
	@echo "=========================="
	@echo ""
	@if [ -d "sessions" ]; then \
		for session_dir in sessions/*/; do \
			if [ -d "$$session_dir" ]; then \
				session_name=$$(basename "$$session_dir"); \
				metadata_file="$$session_dir/session_metadata.json"; \
				if [ -f "$$metadata_file" ]; then \
					echo "🔹 Session: $$session_name"; \
					if command -v jq >/dev/null 2>&1; then \
						echo "   Created: $$(jq -r '.created_at' \"$$metadata_file\")"; \
						echo "   Updated: $$(jq -r '.last_updated' \"$$metadata_file\")"; \
						echo "   Messages: $$(jq -r '.message_count' \"$$metadata_file\")"; \
						echo "   Model: $$(jq -r '.model' \"$$metadata_file\")"; \
					else \
						echo "   Metadata: $$(cat \"$$metadata_file\" | head -3)"; \
					fi; \
					echo ""; \
				fi; \
			fi; \
		done; \
	else \
		echo "No sessions directory found. Sessions will be created on first use."; \
	fi

# Session examples and shortcuts
session-start:
	@$(MAKE) session ACTION=start SESSION_ID="$(SESSION_ID)" PROMPT="$(PROMPT)"

session-continue:
	@$(MAKE) session ACTION=continue SESSION_ID="$(SESSION_ID)" PROMPT="$(PROMPT)"

session-end:
	@$(MAKE) session ACTION=end SESSION_ID="$(SESSION_ID)" PROMPT="Goodbye"

# Clean up sessions
clean-sessions:
	@echo "🧹 Cleaning up session data"
	@read -p "Are you sure you want to delete all session data? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		rm -rf sessions/; \
		echo "✅ All session data deleted"; \
	else \
		echo \"❌ Operation cancelled\"; \
	fi

# Robust execution with error handling and retry logic
CONFIG_FILE ?= error_config.yaml

robust: output
	@echo \"🛡️  Robust OpenCode Execution with Error Handling\"
	@echo \"===============================================\"
	@echo \"Prompt: $(PROMPT)\"
	@echo \"Model: $(MODEL)\"
	@echo \"Config: $(CONFIG_FILE)\" 
	@echo \"Max retries: $(MAX_RETRIES)\"
	@echo \"Timeout: $(TIMEOUT)\"
	@echo \"\"
	$(VENV_ACTIVATE) papermill robust_execution.ipynb output/robust_$(TIMESTAMP).ipynb \\\n\t\t-p prompt \"$(PROMPT)\" \\\n\t\t-p model \"$(MODEL)\" \\\n\t\t-p config_file \"$(CONFIG_FILE)\" \\\n\t\t-p max_retries \"$(MAX_RETRIES)\" \\\n\t\t-p timeout \"$(TIMEOUT)\" \\\n\t\t-p verbose \"$(VERBOSE)\" \\\n\t\t--log-level INFO\n\t@echo \"\"\n\t@echo \"✅ Robust execution completed! Check output/robust_$(TIMESTAMP).ipynb and error logs\"
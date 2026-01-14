# Papermill Environment Makefile
# Easy commands for running Papermill examples and managing the environment

SHELL := /bin/bash

.PHONY: help run run-bash setup clean install activate test list-notebooks jupyter

# Default target
help:
	@echo "📓 Papermill Environment Commands"
	@echo "================================="
	@echo ""
	@echo "🚀 Main Commands:"
	@echo "  make run          - Run the default Python example notebook"
	@echo "  make run-bash     - Run the bash kernel example notebook"
	@echo "  make jupyter      - Launch JupyterLab"
	@echo ""
	@echo "🔧 Setup Commands:"
	@echo "  make setup        - Set up virtual environment and install packages"
	@echo "  make install      - Install/update packages in existing environment"
	@echo "  make activate     - Show how to activate the environment"
	@echo ""
	@echo "📋 Utility Commands:"
	@echo "  make test         - Run all example notebooks"
	@echo "  make list         - List all available notebooks"
	@echo "  make clean        - Clean up output files"
	@echo ""
	@echo "📖 Examples:"
	@echo "  make run MESSAGE=\"Custom message here\" MULTIPLIER=5"
	@echo "  make run-bash"
	@echo "  make jupyter"

# Default parameters for the example notebook
MESSAGE ?= "Hello from Papermill Makefile!"
MULTIPLIER ?= 2
GENERATE_PLOT ?= true
TIMEOUT ?= 300

# Virtual environment activation
VENV_ACTIVATE = source venv/bin/activate &&

# Main run command - executes the Python example notebook
run: output
	@echo "🚀 Running Papermill Python Example"
	@echo "=================================="
	@echo "Parameters:"
	@echo "  Message: $(MESSAGE)"
	@echo "  Multiplier: $(MULTIPLIER)"
	@echo "  Generate Plot: $(GENERATE_PLOT)"
	@echo ""
	$(VENV_ACTIVATE) papermill example.ipynb output/example_$(shell date +%Y%m%d_%H%M%S).ipynb \
		-p message "$(MESSAGE)" \
		-p multiplier $(MULTIPLIER) \
		-p generate_plot $(GENERATE_PLOT) \
		--log-level INFO
	@echo ""
	@echo "✅ Execution complete! Check the output/ directory for results."

# Run bash kernel example
run-bash: output
run-bash: output
	@echo "🖥️  Running Papermill Bash Example"
	@echo "================================="
	$(VENV_ACTIVATE) papermill bash_example.ipynb output/bash_$(shell date +%Y%m%d_%H%M%S).ipynb \
		--log-level INFO
	@echo ""
	@echo "✅ Bash example complete! Check the output/ directory for results."

# Set up the entire environment from scratch
setup:
	@echo "🔧 Setting up Papermill environment"
	@echo "==================================="
	python -m venv venv
	$(VENV_ACTIVATE) pip install --upgrade pip
	$(VENV_ACTIVATE) pip install -r requirements.txt
	$(VENV_ACTIVATE) python -m bash_kernel.install
	@mkdir -p output
	@echo ""
	@echo "✅ Setup complete! Use 'make activate' to see how to activate the environment."

# Install/update packages in existing environment
install:
	@echo "📦 Installing packages"
	$(VENV_ACTIVATE) pip install --upgrade pip
	$(VENV_ACTIVATE) pip install -r requirements.txt
	@echo "✅ Packages installed!"

# Show activation instructions
activate:
	@echo "🔄 To activate the virtual environment manually:"
	@echo "   source venv/bin/activate"
	@echo ""
	@echo "🚀 Or use the activation script:"
	@echo "   ./activate.sh"

# Launch JupyterLab
jupyter:
	@echo "🚀 Launching JupyterLab"
	@echo "======================"
	@echo "JupyterLab will open in your browser at http://localhost:8888"
	@echo "Press Ctrl+C to stop the server"
	@echo ""
	$(VENV_ACTIVATE) jupyter lab --port 8888

# Test all notebooks
test:
	@echo "🧪 Testing all example notebooks"
	@echo "================================"
	@mkdir -p output
	@echo "Testing Python example..."
	$(VENV_ACTIVATE) papermill example.ipynb output/test_python.ipynb \
		-p message "Test run" -p multiplier 1 -p generate_plot false
	@echo "Testing Bash example..."
	$(VENV_ACTIVATE) papermill bash_example.ipynb output/test_bash.ipynb
	@echo ""
	@echo "✅ All tests passed!"

# List available notebooks
list:
	@echo "📓 Available Notebooks:"
	@echo "======================"
	@echo "📄 example.ipynb - Python example with matplotlib plotting"
	@echo "🖥️  bash_example.ipynb - Bash kernel example with system commands"
	@echo ""
	@echo "🔗 OpenCode Integration:"
	@echo "📁 opencode/ - Atomic OpenCode agent execution"
	@echo ""
	@ls -la *.ipynb 2>/dev/null || echo "No notebooks found in current directory"

# Clean up generated files
clean:
	@echo "🧹 Cleaning up output files"
	rm -rf output/
	rm -f *.ipynb_checkpoints
	rm -rf .ipynb_checkpoints/
	@echo "✅ Cleanup complete!"

# Show current environment status
status:
	@echo "📊 Environment Status"
	@echo "===================="
	@if [ -d "venv" ]; then \
		echo "✅ Virtual environment: EXISTS"; \
	else \
		echo "❌ Virtual environment: MISSING (run 'make setup')"; \
	fi
	@if [ -f "requirements.txt" ]; then \
		echo "✅ Requirements file: EXISTS"; \
	else \
		echo "❌ Requirements file: MISSING"; \
	fi
	@if [ -d "output" ]; then \
		echo "📁 Output directory: EXISTS ($(shell ls output/ | wc -l) files)"; \
	else \
		echo "📁 Output directory: Will be created on first run"; \
	fi

# Create output directory
output:
	mkdir -p output

# Help for specific notebook parameters
help-params:
	@echo "📝 Notebook Parameters"
	@echo "====================="
	@echo ""
	@echo "🐍 Python Example (example.ipynb):"
	@echo "   MESSAGE=\"Your message\"     - Custom message to display"
	@echo "   MULTIPLIER=N               - Number to multiply message by"
	@echo "   GENERATE_PLOT=true/false   - Whether to generate matplotlib plot"
	@echo ""
	@echo "🖥️  Bash Example (bash_example.ipynb):"
	@echo "   (No parameters - runs system commands)"
	@echo ""
	@echo "Example usage:"
	@echo "   make run MESSAGE=\"Hello World\" MULTIPLIER=3"
	@echo "   make run GENERATE_PLOT=false"
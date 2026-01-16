# OpenCode ACP Integration Examples Makefile
# 
# This Makefile provides easy access to all ACP (Agent Client Protocol) examples
# and demonstrates various patterns for OpenCode automation and integration.
#
# Quick Start:
#   make help           - Show all available commands
#   make test-basic     - Test basic ACP client functionality  
#   make interactive    - Start interactive ACP session
#   make demo-review    - Run code review demo on this directory
#

.PHONY: help setup test-basic test-advanced interactive demo-review demo-batch demo-multi-agent clean install-deps check-deps

# Default target
help:
	@echo "🔗 OpenCode ACP Integration Examples"
	@echo "=================================="
	@echo ""
	@echo "📋 Available Commands:"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make test-basic        - Test basic ACP client functionality"
	@echo "  make interactive       - Start interactive ACP session"
	@echo "  make demo-review       - Demo code review on current directory"
	@echo ""
	@echo "🧪 Testing & Validation:"
	@echo "  make test-all          - Run all ACP client tests"
	@echo "  make test-advanced     - Test advanced ACP client features"
	@echo "  make check-deps        - Verify OpenCode and dependencies"
	@echo ""
	@echo "🛠️ Code Review Examples:" 
	@echo "  make review-file FILE=<path>           - Review single file"
	@echo "  make review-security DIR=<path>        - Security scan of directory"
	@echo "  make review-performance FILE=<path>    - Performance analysis"
	@echo "  make review-batch PATTERN='*.py'       - Batch review matching pattern"
	@echo ""
	@echo "🤖 Multi-Agent Workflows:"
	@echo "  make demo-multi-agent  - Run multi-agent project analysis"
	@echo "  make analysis-project DIR=<path>       - Full project analysis"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  make setup             - Set up development environment" 
	@echo "  make clean             - Clean up generated files"
	@echo "  make install-deps      - Install Python dependencies"
	@echo ""
	@echo "📖 Documentation:"
	@echo "  make show-examples     - List all available examples"
	@echo "  make show-architecture - Show ACP architecture overview"
	@echo ""

# Variables
PYTHON := python3
ACP_BASIC := $(PYTHON) acp_client.py
ACP_ADVANCED := $(PYTHON) advanced_acp_client.py
ACP_REVIEW := $(PYTHON) practical_code_review.py
ACP_MULTI := $(PYTHON) multi_agent_coordinator.py

# Default file and directory for demos
FILE ?= acp_client.py
DIR ?= .
PATTERN ?= "*.py"
TIMEOUT ?= 120

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

#==============================================================================
# Setup and Dependencies
#==============================================================================

setup: check-deps
	@echo "$(GREEN)✅ ACP examples environment ready!$(RESET)"
	@echo "$(BLUE)Next steps:$(RESET)"
	@echo "  make test-basic      # Test basic functionality"
	@echo "  make interactive     # Try interactive mode"
	@echo "  make demo-review     # See code review in action"

check-deps:
	@echo "$(BLUE)🔍 Checking dependencies...$(RESET)"
	@command -v opencode >/dev/null 2>&1 || (echo "$(RED)❌ OpenCode CLI not found. Install from: https://opencode.ai$(RESET)" && exit 1)
	@$(PYTHON) --version >/dev/null 2>&1 || (echo "$(RED)❌ Python 3 not found$(RESET)" && exit 1)
	@echo "$(GREEN)✅ OpenCode CLI: $$(opencode --version)$(RESET)"
	@echo "$(GREEN)✅ Python: $$($(PYTHON) --version)$(RESET)"

install-deps:
	@echo "$(BLUE)📦 Installing Python dependencies...$(RESET)"
	@$(PYTHON) -m pip install --upgrade pip
	@echo "$(GREEN)✅ Dependencies ready$(RESET)"

#==============================================================================
# Basic ACP Client Tests
#==============================================================================

test-basic:
	@echo "$(BLUE)🧪 Testing basic ACP client...$(RESET)"
	@echo "$(YELLOW)Running: $(ACP_BASIC) 'What is the Agent Client Protocol?'$(RESET)"
	@$(ACP_BASIC) "What is the Agent Client Protocol?" || (echo "$(RED)❌ Basic ACP test failed$(RESET)" && exit 1)
	@echo "$(GREEN)✅ Basic ACP client test passed!$(RESET)"

test-advanced:
	@echo "$(BLUE)🧪 Testing advanced ACP client...$(RESET)"
	@echo "$(YELLOW)Running: $(ACP_ADVANCED) --prompt 'List files in current directory'$(RESET)"
	@$(ACP_ADVANCED) --prompt "List the files in the current directory and explain what each ACP example does" --timeout $(TIMEOUT) || (echo "$(RED)❌ Advanced ACP test failed$(RESET)" && exit 1)
	@echo "$(GREEN)✅ Advanced ACP client test passed!$(RESET)"

test-all: check-deps test-basic test-advanced
	@echo "$(GREEN)🎉 All ACP client tests passed!$(RESET)"

#==============================================================================
# Interactive Mode
#==============================================================================

interactive:
	@echo "$(BLUE)🗣️ Starting interactive ACP session...$(RESET)"
	@echo "$(YELLOW)Type your prompts and 'exit' when done$(RESET)"
	@$(ACP_ADVANCED) --interactive

#==============================================================================
# Code Review Examples
#==============================================================================

demo-review:
	@echo "$(BLUE)🔍 Running code review demo...$(RESET)"
	@echo "$(YELLOW)Reviewing ACP client files with quick analysis$(RESET)"
	@$(ACP_REVIEW) --file acp_client.py --type quick
	@echo "$(GREEN)✅ Code review demo completed!$(RESET)"

review-file:
	@echo "$(BLUE)🔍 Reviewing file: $(FILE)$(RESET)"
	@$(ACP_REVIEW) --file "$(FILE)" --type comprehensive

review-security:
	@echo "$(BLUE)🔒 Security analysis of: $(DIR)$(RESET)"  
	@$(ACP_REVIEW) --directory "$(DIR)" --type security --output security_report_$$(date +%Y%m%d_%H%M%S).md
	@echo "$(GREEN)✅ Security report generated$(RESET)"

review-performance:
	@echo "$(BLUE)⚡ Performance analysis of: $(FILE)$(RESET)"
	@$(ACP_REVIEW) --file "$(FILE)" --type performance

review-batch:
	@echo "$(BLUE)📦 Batch review of pattern: $(PATTERN)$(RESET)"
	@$(ACP_REVIEW) --batch $(PATTERN) --type comprehensive --max-files 5 --output batch_review_$$(date +%Y%m%d_%H%M%S).md
	@echo "$(GREEN)✅ Batch review completed$(RESET)"

#==============================================================================
# Multi-Agent Examples
#==============================================================================

demo-multi-agent:
	@echo "$(BLUE)🤖 Running multi-agent coordination demo...$(RESET)"
	@echo "$(YELLOW)This will analyze the current directory using multiple specialized agents$(RESET)"
	@echo "$(YELLOW)⏱️ This may take 2-3 minutes...$(RESET)"
	@$(ACP_MULTI) --project . --output multi_agent_demo_$$(date +%Y%m%d_%H%M%S).md
	@echo "$(GREEN)✅ Multi-agent analysis completed!$(RESET)"

analysis-project:
	@echo "$(BLUE)🏗️ Full project analysis of: $(DIR)$(RESET)"
	@echo "$(YELLOW)Running comprehensive multi-agent analysis...$(RESET)"
	@$(ACP_MULTI) --project "$(DIR)" --output project_analysis_$$(basename "$(DIR)")_$$(date +%Y%m%d_%H%M%S).md
	@echo "$(GREEN)✅ Project analysis completed$(RESET)"

#==============================================================================
# Example Workflows
#==============================================================================

# Demonstrate CI/CD integration pattern
demo-cicd:
	@echo "$(BLUE)🔄 CI/CD Integration Demo$(RESET)"
	@echo "$(YELLOW)Simulating automated code review in CI pipeline...$(RESET)"
	@for file in *.py; do \
		echo "$(BLUE)Reviewing: $$file$(RESET)"; \
		$(ACP_REVIEW) --file "$$file" --type security || true; \
	done
	@echo "$(GREEN)✅ CI/CD demo completed$(RESET)"

# Demonstrate documentation generation
demo-docs:
	@echo "$(BLUE)📚 Documentation Generation Demo$(RESET)"
	@$(ACP_ADVANCED) --prompt "Generate comprehensive documentation for the ACP client examples in this directory. Explain what each file does, how to use it, and provide usage examples." --timeout 180
	@echo "$(GREEN)✅ Documentation demo completed$(RESET)"

# Demonstrate parallel processing
demo-parallel:
	@echo "$(BLUE)⚡ Parallel Processing Demo$(RESET)"
	@echo "$(YELLOW)Running multiple ACP clients concurrently...$(RESET)"
	@$(ACP_ADVANCED) --prompt "Analyze acp_client.py" --timeout 60 & \
	 $(ACP_ADVANCED) --prompt "Analyze advanced_acp_client.py" --timeout 60 & \
	 $(ACP_ADVANCED) --prompt "Analyze practical_code_review.py" --timeout 60 & \
	 wait
	@echo "$(GREEN)✅ Parallel processing demo completed$(RESET)"

#==============================================================================
# Information and Documentation  
#==============================================================================

show-examples:
	@echo "$(BLUE)📋 Available ACP Examples:$(RESET)"
	@echo ""
	@echo "$(GREEN)1. Basic ACP Client (acp_client.py)$(RESET)"
	@echo "   Simple demonstration of ACP protocol interaction"
	@echo "   Usage: make test-basic"
	@echo ""
	@echo "$(GREEN)2. Advanced ACP Client (advanced_acp_client.py)$(RESET)" 
	@echo "   Production-ready client with session management and monitoring"
	@echo "   Usage: make interactive"
	@echo ""
	@echo "$(GREEN)3. Code Review Harness (practical_code_review.py)$(RESET)"
	@echo "   Automated code analysis and security scanning" 
	@echo "   Usage: make demo-review"
	@echo ""
	@echo "$(GREEN)4. Multi-Agent Coordinator (multi_agent_coordinator.py)$(RESET)"
	@echo "   Sophisticated multi-agent system for project analysis"
	@echo "   Usage: make demo-multi-agent"
	@echo ""

show-architecture:
	@echo "$(BLUE)🏗️ ACP Architecture Overview:$(RESET)"
	@echo ""
	@echo "┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐"
	@echo "│   Python Client │    │     ACP      │    │   OpenCode      │"
	@echo "│                 │◄──►│   Protocol   │◄──►│   Session       │"
	@echo "│ (Your Harness)  │    │  (WebSocket) │    │                 │"
	@echo "└─────────────────┘    └──────────────┘    └─────────────────┘"
	@echo "                              │"
	@echo "                              ▼"
	@echo "                    ┌──────────────────┐"
	@echo "                    │  Model Context   │"
	@echo "                    │  Protocol (MCP)  │"
	@echo "                    │    Servers       │"
	@echo "                    └──────────────────┘"
	@echo ""
	@echo "$(YELLOW)Key Benefits:$(RESET)"
	@echo "• Editor independence - run agents from any environment"
	@echo "• Programmatic control - full API access to OpenCode capabilities"
	@echo "• Automation ready - perfect for CI/CD and batch processing"
	@echo "• Scalable - coordinate multiple agents for complex workflows"

#==============================================================================
# Utilities
#==============================================================================

clean:
	@echo "$(BLUE)🧹 Cleaning up generated files...$(RESET)"
	@rm -f *.md security_report_*.md batch_review_*.md multi_agent_*.md project_analysis_*.md
	@rm -rf __pycache__ .pytest_cache *.pyc
	@echo "$(GREEN)✅ Cleanup completed$(RESET)"

# Development helpers
dev-setup: install-deps
	@echo "$(BLUE)🛠️ Setting up development environment...$(RESET)"
	@$(PYTHON) -m pip install black flake8 mypy
	@echo "$(GREEN)✅ Development environment ready$(RESET)"

lint:
	@echo "$(BLUE)🔍 Linting Python files...$(RESET)"
	@$(PYTHON) -m flake8 *.py --max-line-length=100 --ignore=E203,W503 || true
	@echo "$(GREEN)✅ Linting completed$(RESET)"

format:
	@echo "$(BLUE)🎨 Formatting Python files...$(RESET)"
	@$(PYTHON) -m black *.py --line-length=100 || true
	@echo "$(GREEN)✅ Formatting completed$(RESET)"

#==============================================================================
# Advanced Examples
#==============================================================================

# Full workflow demonstration
demo-workflow:
	@echo "$(BLUE)🔄 Complete ACP Workflow Demo$(RESET)"
	@echo "$(YELLOW)This demonstrates a complete development workflow using ACP$(RESET)"
	@echo ""
	@echo "$(BLUE)Step 1: Basic connectivity test$(RESET)"
	@make test-basic
	@echo ""
	@echo "$(BLUE)Step 2: Code analysis$(RESET)" 
	@make demo-review
	@echo ""
	@echo "$(BLUE)Step 3: Security scan$(RESET)"
	@make review-security DIR=.
	@echo ""
	@echo "$(BLUE)Step 4: Multi-agent analysis$(RESET)"
	@make demo-multi-agent
	@echo "$(GREEN)🎉 Complete workflow demonstration finished!$(RESET)"

# Performance testing
perf-test:
	@echo "$(BLUE)⚡ ACP Performance Testing$(RESET)"
	@echo "$(YELLOW)Testing response times for different operations...$(RESET)"
	@time $(ACP_BASIC) "Quick test message" >/dev/null 2>&1 || true
	@time $(ACP_ADVANCED) --prompt "Another quick test" --timeout 30 >/dev/null 2>&1 || true
	@echo "$(GREEN)✅ Performance test completed$(RESET)"

# Integration test
integration-test: check-deps test-all demo-review
	@echo "$(GREEN)🎉 All integration tests passed!$(RESET)"
	@echo "$(BLUE)ACP examples are working correctly and ready to use.$(RESET)"
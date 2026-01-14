# Awesome Agent Harnesses

A comprehensive collection of production-ready AI agent execution frameworks and integration patterns.

This repository serves as both a **community index** of agent harnesses and a **reference implementation** of advanced multi-agent collaboration patterns. Whether you're building autonomous coding agents, editorial workflows, or custom AI automations, you'll find battle-tested patterns and community resources here.

## 🌟 Community Agent Harnesses

> **📚 Foundation**: For comprehensive agentic patterns and design principles that underpin these harnesses, see [awesome-agentic-patterns](https://github.com/nibzard/awesome-agentic-patterns) - a curated collection of architectural patterns for building AI agents.

### Coding & Development

#### **Anthropic's Autonomous Coding Agent** 🤖
**Repository**: [claude-quickstarts/autonomous-coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)  
**Article**: [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

Production-grade autonomous coding agent with robust error handling, tool integration, and safety measures. The gold standard implementation based on Anthropic's research into effective agent harnesses.

**Key Features:**
- Long-running autonomous execution with safety constraints  
- Comprehensive error handling and recovery patterns
- Tool integration framework for file operations and terminal access
- Built-in guardrails and execution limits

#### **Ralph Wiggum Loop** 🔄
**Repositories**: 
- [how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum) - Methodology and patterns
- [ralph](https://github.com/snarktank/ralph) - Reference implementation

Self-improving coding agent that iteratively refines its own code through automated feedback loops. Named after the Simpsons character for its persistent, innocent approach to problem-solving.

**Key Features:**
- Self-reflective code improvement cycles
- Automated testing and validation loops  
- Iterative refinement through AI feedback
- Continuous learning and adaptation patterns

---

## 🏠 Local Harnesses (This Repository)

## 🚀 Quick Start

### Papermill + OpenCode Integration
Execute AI agents through Jupyter notebooks with full parameterization and automation:

```bash
cd examples/papermill/opencode
make run PROMPT="Create a Python function that calculates fibonacci numbers"
```

### Adversarial Loop
Iterative document improvement through critical feedback loops:

```bash
cd examples/adversarial_loop
# Run adversarial review process on your document
```

### Editorial Pipeline
Multi-stage collaborative editing with specialized reviewer perspectives:

```bash
cd examples/editorial_pipeline
# Execute multi-hat editorial review process
```

## 📋 Local Harnesses (Reference Implementations)

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

### 2. **Adversarial Loop System** 🔄  
**Location**: `examples/adversarial_loop/`  
**Status**: ✅ Production Ready

Iterative document improvement through structured critical feedback and revision cycles.

**Key Features:**
- **Multi-round Reviews**: Documents undergo multiple rounds of adversarial criticism
- **Critical Feedback**: AI reviewers provide harsh but constructive criticism to identify weaknesses  
- **Iterative Refinement**: Each version addresses previous feedback until quality standards are met
- **Quality Assurance**: Process continues until reviewers approve final version

**Sample Workflow:**
```bash
cd examples/adversarial_loop
# Initial document: document_v001.md
# → Critical review: reviewer_feedback_1.md  
# → Revision cycle continues until approval
```

### 3. **Editorial Pipeline** ✍️  
**Location**: `examples/editorial_pipeline/`  
**Status**: ✅ Production Ready

Multi-stage collaborative editorial system using specialized AI reviewers with different analytical perspectives.

**Available Review Perspectives:**
- **White Hat (Facts & Information)** - Analyzes factual accuracy, data verification, citations
- **Red Hat (Emotions & Intuition)** - Evaluates emotional impact, reader engagement, tone
- **Additional Hats** - Extensible framework for specialized review perspectives

**Process Flow:**
1. Original content input (`01_original_essay.md`)
2. Multi-perspective AI reviews (`review_1.md`, `review_2.md`)  
3. Final polished output (`99_final_polished_essay.md`)
4. Timestamped session logs and comprehensive documentation

## 🛠️ Environment Setup

### Papermill Environment
```bash
cd examples/papermill
make setup              # Complete environment setup
source venv/bin/activate # Activate virtual environment
make jupyter            # Launch JupyterLab interface
```

### Editorial Systems Environment
```bash
cd examples/editorial_pipeline    # or examples/adversarial_loop
# Systems use OpenCode CLI - ensure it's installed and configured
opencode --version              # Verify OpenCode CLI availability
```

## 📚 Documentation

- **[Adversarial Loop Guide](examples/adversarial_loop/README.md)** - Iterative document improvement patterns
- **[Editorial Pipeline Guide](examples/editorial_pipeline/README.md)** - Multi-perspective collaborative editing
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

### Editorial Workflows
Execute document improvement and collaborative editing workflows:
```bash
# Adversarial Loop - iterative improvement
cd examples/adversarial_loop && ./run_adversarial_review.sh document.md

# Editorial Pipeline - multi-perspective review  
cd examples/editorial_pipeline && ./pipeline_essay.sh essay.md
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

### Adversarial Loop Pattern
- **Input**: Initial document for improvement
- **Processing**: Multi-round critical review and revision cycles
- **Output**: Iteratively improved document with approval trail
- **Quality Control**: Continues until reviewers approve final version

### Editorial Pipeline Pattern  
- **Input**: Original content requiring editorial review
- **Processing**: Specialized AI reviewers using "thinking hats" methodology
- **Output**: Polished content with comprehensive review documentation
- **Multi-perspective**: Facts, emotions, and other analytical dimensions

### Adversarial Loop Pattern
```
Document Input → Critical Review → Revision → Further Review → ... → Final Approval
```

### Editorial Pipeline Pattern  
```
Original Content → Multi-Hat Reviews → Synthesis → Polished Output
```

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

### Extending Editorial Systems
1. Add new "thinking hat" perspectives to editorial pipeline
2. Create specialized review agents for specific domains (technical, creative, etc.)
3. Customize review criteria and feedback patterns
4. Extend adversarial loop with domain-specific criticism strategies

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

# Test editorial systems
cd examples/editorial_pipeline && ./test_pipeline.sh
cd examples/adversarial_loop && ./test_adversarial.sh

# Test Kiro analysis tools
cd examples && npm test
```

## 📈 Performance

- **Atomic agents**: ~2-10 seconds per execution (model dependent)
- **Adversarial loops**: ~30-120 seconds per iteration cycle (depends on complexity)
- **Editorial pipeline**: ~45-90 seconds for complete multi-hat review
- **Database analysis**: Handles databases with 10k+ conversations
- **Session overhead**: Minimal with automatic cleanup
- **Parallelization**: Full support for concurrent operations

## 🤝 Contributing

### Adding New Community Harnesses
1. **Submit a PR** with your harness added to the Community Agent Harnesses section
2. **Include**: Repository link, brief description, key features, and category
3. **Requirements**: Production-ready code with documentation and examples
4. **Categories**: We welcome harnesses for coding, writing, research, analysis, and other domains

### Local Harness Development  
1. Follow established patterns in `examples/` directory
2. Add comprehensive documentation for new harnesses
3. Include working examples and test cases
4. Update this README with new capabilities

## 📄 License

MIT License - see LICENSE file for details.

---

**🎯 Goal**: Provide production-ready, zero-friction AI agent execution patterns that scale from simple prompts to complex multi-agent workflows.

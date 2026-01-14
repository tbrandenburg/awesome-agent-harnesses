# OpenCode Atomic Agent Executor

This directory contains an atomic OpenCode execution notebook that can be used with Papermill to execute any prompt through the OpenCode CLI in a reusable, parameterized way.

## Files

- `opencode_prompt.ipynb` - Main atomic execution notebook (uses bash kernel)
- `example_*.yaml` - Example parameter files for different use cases
- `README.md` - This documentation

## Quick Start

### Basic Usage
```bash
# From the papermill directory
cd examples/papermill
source venv/bin/activate

# Execute with simple prompt
papermill opencode/opencode_prompt.ipynb output.ipynb \
  -p prompt "Generate a riddle about artificial intelligence"

# Execute with parameter file
papermill opencode/opencode_prompt.ipynb output.ipynb \
  -f opencode/example_riddle.yaml
```

### Advanced Usage
```bash
# Use specific model
papermill opencode/opencode_prompt.ipynb output.ipynb \
  -p prompt "Write Python code for sorting algorithms" \
  -p model "opencode/grok-code" \
  -p verbose "true"

# Continue existing session
papermill opencode/opencode_prompt.ipynb output.ipynb \
  -p prompt "Can you explain that in more detail?" \
  -p session_id "your-session-id-here"

# With timeout and output format
papermill opencode/opencode_prompt.ipynb output.ipynb \
  -p prompt "Explain quantum computing" \
  -p output_format "markdown" \
  -p timeout "600"
```

## Parameters

### Required
- `prompt` - The prompt/message to send to OpenCode

### Optional
- `model` - Model to use (e.g., "opencode/grok-code", "opencode/big-pickle")
- `session_id` - Session ID to continue existing conversation
- `additional_args` - Extra OpenCode CLI arguments
- `output_format` - Output format: "text" (default), "json", "markdown"
- `timeout` - Timeout in seconds (default: 300)
- `verbose` - Enable verbose output: "true"/"false" (default: false)

## Atomic Agent Concept

This notebook is designed as an **atomic agent execution unit**:

1. **Self-contained**: All logic contained in single notebook
2. **Parameterizable**: Accepts parameters via Papermill
3. **Reusable**: Same notebook for any OpenCode prompt
4. **Pipeline-ready**: Outputs structured metadata for chaining
5. **Error handling**: Proper timeout and error management
6. **Logging**: Comprehensive execution logging

## Integration Patterns

### Pipeline Chain
```bash
# Execute multiple prompts in sequence
papermill opencode/opencode_prompt.ipynb step1.ipynb -p prompt "Plan a web app"
papermill opencode/opencode_prompt.ipynb step2.ipynb -p prompt "Write the backend code"
papermill opencode/opencode_prompt.ipynb step3.ipynb -p prompt "Create the frontend"
```

### Batch Processing
```bash
# Process multiple prompts
for prompt_file in prompts/*.yaml; do
    papermill opencode/opencode_prompt.ipynb "output/$(basename $prompt_file .yaml).ipynb" \
      -f "$prompt_file"
done
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Execute OpenCode Agent
  run: |
    papermill opencode/opencode_prompt.ipynb results.ipynb \
      -p prompt "${{ github.event.inputs.prompt }}" \
      -p model "opencode/grok-code"
```

## Output Structure

The notebook outputs:
1. **Human-readable response** - The actual OpenCode output
2. **Execution metadata** - Timing, parameters, status
3. **Structured output** - Machine-readable execution summary

Example output structure:
```
🤖 OpenCode Response:
===================
[AI response content here]
===================
✅ Execution completed successfully
📊 Execution metadata:
   - Prompt: Generate a riddle...
   - Model: default
   - Session: new
   - Timestamp: 2024-01-14T20:30:45+00:00
   - Format: text
🎯 Atomic agent execution complete!

=== PAPERMILL_OUTPUT_BEGIN ===
EXECUTION_STATUS=SUCCESS
PROMPT=Generate a riddle...
MODEL=default
SESSION=new
TIMESTAMP=2024-01-14T20:30:45+00:00
=== PAPERMILL_OUTPUT_END ===
```

## Error Handling

The notebook includes robust error handling:
- Parameter validation
- Timeout management (default 300s)
- OpenCode CLI error capture
- Structured error reporting
- Exit code propagation

## Use Cases

1. **Interactive AI Agent**: Execute any prompt through OpenCode
2. **Batch Processing**: Process multiple prompts automatically
3. **Pipeline Integration**: Chain multiple AI operations
4. **CI/CD Automation**: Automated AI-assisted tasks
5. **Report Generation**: AI-generated content in reports
6. **Code Generation**: Automated code creation workflows
7. **Content Creation**: Automated writing and editing

## Requirements

- Papermill environment (already set up in parent directory)
- OpenCode CLI installed and accessible
- Bash kernel for Jupyter (already installed)
- Valid OpenCode authentication (if required)

## Troubleshooting

### OpenCode Not Found
```bash
which opencode  # Check if OpenCode is in PATH
```

### Permission Issues
```bash
chmod +x opencode_prompt.ipynb  # Ensure notebook is executable
```

### Timeout Issues
```bash
# Increase timeout for long-running prompts
papermill opencode/opencode_prompt.ipynb output.ipynb \
  -p prompt "Complex prompt" -p timeout "900"
```

### Session Issues
```bash
# List active OpenCode sessions
opencode session
```

This atomic agent design enables powerful, reusable AI automation workflows that can be easily integrated into any system supporting Papermill notebook execution.
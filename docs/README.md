# OpenCode CLI Analysis & Safe Usage Guide

## Analysis Summary

### Command Structure Analysis (`opencode run --help`)

The OpenCode CLI provides a rich set of options for running prompts:

**Key Options:**
- `--format=json`: Returns structured JSON events instead of formatted output
- `--session=<id>`: Continue an existing session
- `--continue`: Continue the last session
- `--file=<path>`: Attach files to the message
- `--model=<provider/model>`: Specify model to use
- `--agent=<name>`: Specify agent to use

### JSON Response Structure

When using `--format=json`, OpenCode returns multiple JSON objects, one per line:

```json
{"type":"step_start","timestamp":1768136163926,"sessionID":"ses_452df6dcfffeRSl33xYv3I1OX7","part":{...}}
{"type":"text","timestamp":1768136164957,"sessionID":"ses_452df6dcfffeRSl33xYv3I1OX7","part":{...}}
{"type":"step_finish","timestamp":1768136164987,"sessionID":"ses_452df6dcfffeRSl33xYv3I1OX7","part":{...}}
```

**Key Fields:**
- `sessionID`: Unique session identifier (e.g., `"ses_452df6dcfffeRSl33xYv3I1OX7"`)
- `type`: Event type (`step_start`, `text`, `step_finish`)
- `timestamp`: Unix timestamp in milliseconds
- `part`: Contains the actual content/response data

## Safe Usage Implementation

### Core Functions

The `opencode_cli_helper.sh` script provides these main functions:

#### 1. `run_opencode_prompt(prompt, args...)`
Safely executes an OpenCode prompt and extracts the session ID.

```bash
session_id=$(run_opencode_prompt "Hello, how are you?")
session_id=$(run_opencode_prompt "Analyze this file" --file="script.py")
```

#### 2. `continue_opencode_session(session_id, prompt, args...)`
Continues an existing session with a new prompt.

```bash
continue_opencode_session "$session_id" "What can you help me with?"
```

#### 3. `get_session_info(json_response)`
Extracts session information from JSON response.

### Safety Features

1. **Input Validation**: Checks for required parameters
2. **Dependency Checking**: Verifies `opencode` and `jq` are available
3. **Error Handling**: Proper exit codes and error messages
4. **Argument Escaping**: Safe handling of special characters
5. **Temporary Files**: Secure temporary file handling

### Special Characters Handling

The implementation safely handles international characters like Swedish "Hej, hur mår du?":

```bash
# This works safely with special characters
session_id=$(run_opencode_prompt "Hej, hur mår du?")
```

### Example Usage

```bash
# Source the helper functions
source ./opencode_cli_helper.sh

# Run a prompt and get session ID
session_id=$(run_opencode_prompt "Hello, what's your name?")

if [ $? -eq 0 ] && [ -n "$session_id" ]; then
    echo "Got session: $session_id"
    
    # Continue the conversation
    continue_opencode_session "$session_id" "Can you help me write code?"
else
    echo "Failed to start session"
fi
```

### Dependencies

- **opencode**: The OpenCode CLI tool
- **jq**: JSON parsing utility (`sudo apt install jq` on Ubuntu/Debian)

### Error Codes

- `0`: Success
- `1`: Invalid input or missing dependencies  
- `2`: Could not extract session ID
- `3`: OpenCode command failed

## Security Considerations

1. **Argument Escaping**: All user inputs are properly escaped
2. **Temporary Files**: Created securely and cleaned up
3. **Error Output**: Sensitive information sent to stderr, not stdout
4. **Validation**: Input validation prevents command injection

## Files Created

- `opencode_cli_helper.sh`: Main helper functions
- `demo_opencode_cli.sh`: Demonstration script
- `README.md`: This documentation

## Testing

Run the demo script to see it in action:

```bash
./demo_opencode_cli.sh
```

Or test individual functions:

```bash
source ./opencode_cli_helper.sh
session_id=$(run_opencode_prompt "Test prompt")
echo "Session: $session_id"
```
#!/bin/bash

# Kiro Conversation History Viewer
# Displays conversation histories for a given directory in chronological order
# Usage: ./kiro-history-viewer.sh [folder_path] [database_path]

set +e  # Allow errors for jq parsing, handle them explicitly

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Default database path (prioritize actual Kiro installation)
DEFAULT_DB_PATHS=(
    "$HOME/.local/share/kiro-cli/data.sqlite3"  # Primary: actual Kiro CLI installation
    "$HOME/.local/share/kiro/data.sqlite3"      # Alternative: older Kiro location
    "$HOME/.config/kiro/data.sqlite3"           # Alternative: config directory
    "./examples/data.sqlite3"                   # Fallback: local examples
    "./data.sqlite3"                            # Fallback: current directory
)

# Function to print usage
usage() {
    echo -e "${BOLD}Kiro Conversation History Viewer${NC}"
    echo ""
    echo "Usage: $0 [folder_path] [database_path]"
    echo ""
    echo "Arguments:"
    echo "  folder_path    Directory path to show conversations for (default: current directory)"
    echo "  database_path  Path to Kiro SQLite database (default: ~/.local/share/kiro-cli/data.sqlite3)"
    echo ""
    echo "Examples:"
    echo "  $0                                           # Show conversations for current directory (uses default Kiro DB)"
    echo "  $0 /home/user/project                       # Show conversations for specific directory (uses default Kiro DB)"
    echo "  $0 /home/user/project ./examples/data.sqlite3   # Use specific database file"
    echo ""
}

# Function to find database file
find_database() {
    for db_path in "${DEFAULT_DB_PATHS[@]}"; do
        if [[ -f "$db_path" ]]; then
            echo "$db_path"
            return 0
        fi
    done
    return 1
}

# Function to truncate text for readability
truncate_text() {
    local text="$1"
    local max_length="${2:-200}"
    
    if [[ ${#text} -gt $max_length ]]; then
        echo "${text:0:$max_length}..."
    else
        echo "$text"
    fi
}

# Function to format JSON content safely
format_content() {
    local content="$1"
    # Remove newlines and extra spaces, handle potential JSON escaping
    echo "$content" | sed 's/\\n/ /g' | sed 's/\\t/ /g' | tr -s ' '
}

# Function to display conversation history
show_conversations() {
    local folder_key="$1"
    local db_path="$2"
    
    echo -e "${BOLD}${BLUE}📁 Kiro Conversation History for:${NC} ${CYAN}$folder_key${NC}"
    echo -e "${BLUE}📄 Database:${NC} $db_path"
    echo ""
    
    # Check if folder has any conversations
    local conversation_count
    conversation_count=$(sqlite3 "$db_path" "SELECT COUNT(*) FROM conversations_v2 WHERE key = '$folder_key';")
    
    if [[ $conversation_count -eq 0 ]]; then
        echo -e "${YELLOW}⚠️  No conversations found for this directory.${NC}"
        echo ""
        echo -e "${BLUE}Available directories in database:${NC}"
        sqlite3 "$db_path" "SELECT DISTINCT key FROM conversations_v2;" | head -10
        return 0
    fi
    
    echo -e "${GREEN}✅ Found $conversation_count conversation(s)${NC}"
    echo ""
    
    # Get conversation IDs in chronological order
    sqlite3 "$db_path" "SELECT conversation_id FROM conversations_v2 WHERE key = '$folder_key' ORDER BY created_at;" | while read -r conv_id; do
        
        # Get conversation metadata
        local created updated msg_count
        created=$(sqlite3 "$db_path" "SELECT datetime(created_at/1000, 'unixepoch') FROM conversations_v2 WHERE key = '$folder_key' AND conversation_id = '$conv_id';")
        updated=$(sqlite3 "$db_path" "SELECT datetime(updated_at/1000, 'unixepoch') FROM conversations_v2 WHERE key = '$folder_key' AND conversation_id = '$conv_id';")
        msg_count=$(sqlite3 "$db_path" "SELECT json_array_length(json_extract(value, '\$.history')) FROM conversations_v2 WHERE key = '$folder_key' AND conversation_id = '$conv_id';")
        
        # Get conversation data separately to avoid pipe conflicts
        local conversation_data
        conversation_data=$(sqlite3 "$db_path" "SELECT value FROM conversations_v2 WHERE key = '$folder_key' AND conversation_id = '$conv_id';")
        
        echo -e "${BOLD}${YELLOW}🗣️  Conversation: ${conv_id:0:8}...${NC}"
        echo -e "${BLUE}   📅 Created:${NC} $created"
        echo -e "${BLUE}   📝 Messages:${NC} $msg_count"
        if [[ "$created" != "$updated" ]]; then
            echo -e "${BLUE}   🔄 Updated:${NC} $updated"
        fi
        echo ""
        
        # Extract and display each message exchange
        local i=0
        while true; do
            # Check if this history entry exists
            local entry_exists
            entry_exists=$(echo "$conversation_data" | jq -r ".history[$i] // empty" 2>/dev/null)
            if [[ -z "$entry_exists" || "$entry_exists" == "empty" || "$entry_exists" == "null" ]]; then
                break
            fi
            
            # Get user content - check for different types
            local user_content_type
            user_content_type=$(echo "$conversation_data" | jq -r ".history[$i].user.content | keys[0]" 2>/dev/null)
            
            local user_prompt=""
            local user_display=""
            
            if [[ "$user_content_type" == "Prompt" ]]; then
                user_prompt=$(echo "$conversation_data" | jq -r ".history[$i].user.content.Prompt.prompt" 2>/dev/null)
                user_display="$user_prompt"
            elif [[ "$user_content_type" == "ToolUseResults" ]]; then
                local tool_count
                tool_count=$(echo "$conversation_data" | jq -r ".history[$i].user.content.ToolUseResults.tool_use_results | length" 2>/dev/null)
                user_display="🔧 Tool results ($tool_count tool(s) completed)"
            else
                user_display="📝 Message (type: $user_content_type)"
            fi
            
            # Skip empty user messages
            if [[ -z "$user_display" ]]; then
                ((i++))
                continue
            fi
            
            local user_timestamp
            user_timestamp=$(echo "$conversation_data" | jq -r ".history[$i].user.timestamp // empty" 2>/dev/null)
            
            # Format and truncate user display
            local formatted_display
            formatted_display=$(format_content "$user_display")
            local truncated_display
            truncated_display=$(truncate_text "$formatted_display" 150)
            
            echo -e "   ${BOLD}${GREEN}👤 User:${NC} $truncated_display"
            if [[ -n "$user_timestamp" && "$user_timestamp" != "null" ]]; then
                local simple_time
                simple_time=$(echo "$user_timestamp" | cut -d'T' -f2 | cut -d'+' -f1)
                echo -e "      ${BLUE}🕒 $simple_time${NC}"
            fi
            
            # Get assistant response
            local assistant_response_type
            assistant_response_type=$(echo "$conversation_data" | jq -r ".history[$i].assistant | keys[0]" 2>/dev/null)
            
            if [[ "$assistant_response_type" == "Response" ]]; then
                local assistant_content
                assistant_content=$(echo "$conversation_data" | jq -r ".history[$i].assistant.Response.content" 2>/dev/null)
                local formatted_response
                formatted_response=$(format_content "$assistant_content")
                local truncated_response
                truncated_response=$(truncate_text "$formatted_response" 200)
                echo -e "   ${BOLD}${CYAN}🤖 Assistant:${NC} $truncated_response"
                
            elif [[ "$assistant_response_type" == "ToolUse" ]]; then
                local tool_name
                tool_name=$(echo "$conversation_data" | jq -r ".history[$i].assistant.ToolUse.tool_uses[0].name // \"unknown\"" 2>/dev/null)
                local tool_command
                tool_command=$(echo "$conversation_data" | jq -r ".history[$i].assistant.ToolUse.tool_uses[0].args.command // empty" 2>/dev/null)
                
                echo -e "   ${BOLD}${CYAN}🤖 Assistant:${NC} ${YELLOW}🔧 Used tool: $tool_name${NC}"
                if [[ -n "$tool_command" && "$tool_command" != "null" ]]; then
                    local truncated_command
                    truncated_command=$(truncate_text "$tool_command" 100)
                    echo -e "      ${BLUE}💻 Command:${NC} $truncated_command"
                fi
            fi
            
            # Show performance metrics for first message
            if [[ $i -eq 0 ]]; then
                local response_time
                response_time=$(echo "$conversation_data" | jq -r ".history[$i].request_metadata.time_to_first_chunk.secs // empty" 2>/dev/null)
                local conversation_type
                conversation_type=$(echo "$conversation_data" | jq -r ".history[$i].request_metadata.chat_conversation_type // empty" 2>/dev/null)
                
                if [[ -n "$response_time" && "$response_time" != "null" ]]; then
                    echo -e "      ${BLUE}⚡ Response time:${NC} ${response_time}s (${conversation_type})"
                fi
            fi
            
            echo ""
            ((i++))
        done
        
        echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"
        echo ""
    done
}

# Main script logic
main() {
    # Parse arguments
    local folder_path="${1:-$(pwd)}"
    local db_path="$2"
    
    # Show help if requested
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
        exit 0
    fi
    
    # Convert relative path to absolute path
    folder_path=$(realpath "$folder_path" 2>/dev/null || echo "$folder_path")
    
    # Find database if not provided
    if [[ -z "$db_path" ]]; then
        echo -e "${BLUE}🔍 Searching for Kiro database (prioritizing ~/.local/share/kiro-cli/)...${NC}"
        if ! db_path=$(find_database); then
            echo -e "${RED}❌ Error: Could not find Kiro database file.${NC}" >&2
            echo -e "${YELLOW}💡 Try specifying the database path as second argument.${NC}" >&2
            echo -e "${YELLOW}💡 Expected location: ~/.local/share/kiro-cli/data.sqlite3${NC}" >&2
            exit 1
        fi
        echo -e "${GREEN}✅ Found database:${NC} $db_path"
        echo ""
    fi
    
    # Verify database exists and is readable
    if [[ ! -f "$db_path" ]]; then
        echo -e "${RED}❌ Error: Database file not found: $db_path${NC}" >&2
        exit 1
    fi
    
    if [[ ! -r "$db_path" ]]; then
        echo -e "${RED}❌ Error: Cannot read database file: $db_path${NC}" >&2
        exit 1
    fi
    
    # Check if sqlite3 is available
    if ! command -v sqlite3 >/dev/null 2>&1; then
        echo -e "${RED}❌ Error: sqlite3 is not installed or not in PATH${NC}" >&2
        exit 1
    fi
    
    # Check if jq is available
    if ! command -v jq >/dev/null 2>&1; then
        echo -e "${RED}❌ Error: jq is not installed or not in PATH${NC}" >&2
        echo -e "${YELLOW}💡 Install jq for JSON parsing: sudo apt install jq${NC}" >&2
        exit 1
    fi
    
    # Display conversations
    show_conversations "$folder_path" "$db_path"
}

# Run main function with all arguments
main "$@"
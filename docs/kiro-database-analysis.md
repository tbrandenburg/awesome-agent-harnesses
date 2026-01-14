# Kiro SQLite Database Analysis Guide

This document provides comprehensive information about the Kiro CLI assistant's SQLite database structure and practical SQL queries for analysis.

## Database Overview

**File**: `data.sqlite3` (typically ~581KB)  
**Purpose**: Stores Kiro AI assistant conversations, authentication data, application state, and usage analytics  
**Location**: Usually in Kiro's data directory

## Database Schema

### Table Structure

#### 1. `migrations`
Tracks database schema evolution:
```sql
CREATE TABLE migrations (
    id INTEGER PRIMARY KEY,
    version INTEGER NOT NULL,
    migration_time INTEGER NOT NULL
);
```

#### 2. `conversations_v2` (Primary Conversation Data)
Stores all AI assistant conversations with full context:
```sql
CREATE TABLE conversations_v2 (
    key TEXT NOT NULL,                -- Working directory path
    conversation_id TEXT NOT NULL,    -- UUID for each conversation session
    value TEXT NOT NULL,             -- JSON conversation data
    created_at INTEGER NOT NULL,     -- Unix timestamp in milliseconds
    updated_at INTEGER NOT NULL,     -- Unix timestamp in milliseconds
    PRIMARY KEY (key, conversation_id)
);

-- Indexes for performance
CREATE INDEX idx_conversations_v2_key_updated ON conversations_v2(key, updated_at DESC);
CREATE INDEX idx_conversations_v2_updated_at ON conversations_v2(updated_at DESC);
```

#### 3. `conversations` (Legacy)
Legacy conversation storage (being phased out):
```sql
CREATE TABLE conversations (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

#### 4. `history`
Designed for command history tracking (currently empty):
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY,
    command TEXT,
    shell TEXT,
    pid INTEGER,
    session_id TEXT,
    cwd TEXT,
    start_time INTEGER,
    hostname TEXT,
    exit_code INTEGER,
    end_time INTEGER,
    duration INTEGER
);
```

#### 5. `auth_kv`
Authentication and credentials storage:
```sql
CREATE TABLE auth_kv (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

#### 6. `state`
Application configuration and telemetry:
```sql
CREATE TABLE state (
    key TEXT PRIMARY KEY,
    value BLOB
);
```

## ID Hierarchy Structure

Kiro uses a three-level identification system:

### 1. Folder Key (Directory Level)
- **Format**: Full filesystem path
- **Example**: `/home/tom/workspace/ai/made/workspace/HelloWorld`
- **Purpose**: Groups conversations by project/directory context

### 2. Conversation ID (Session Level)
- **Format**: UUID (e.g., `e11fcf82-aef8-478f-abb3-4eefbae37675`)
- **Purpose**: Unique identifier for each conversation session
- **Trigger**: Each new user prompt creates a new conversation

### 3. Message ID (Response Level)
- **Format**: UUID (e.g., `8e61671d-fb4a-4bdd-8ae0-f1e5b8f48138`)
- **Purpose**: Unique identifier for each assistant response
- **Location**: Found in assistant responses and request metadata

### 4. Request ID (API Level)
- **Format**: UUID (e.g., `6e904c84-9747-4d2a-ae12-707ddee28db3`)
- **Purpose**: Tracks individual API requests
- **Location**: Found in request metadata

## JSON Data Structure

### Conversation Object Structure
```json
{
  "conversation_id": "uuid-string",
  "next_message": null,
  "history": [
    {
      "user": {
        "additional_context": "",
        "env_context": {
          "env_state": {
            "operating_system": "linux",
            "current_working_directory": "/path/to/project",
            "environment_variables": []
          }
        },
        "content": {
          "Prompt": {"prompt": "user message text"}
        },
        "timestamp": "2026-01-11T09:40:55.050017383+01:00",
        "images": null
      },
      "assistant": {
        "Response": {
          "message_id": "uuid",
          "content": "assistant response text"
        }
        // OR
        "ToolUse": {
          "message_id": "uuid",
          "content": "",
          "tool_uses": [{
            "id": "tooluse_id",
            "name": "execute_bash",
            "orig_name": "execute_bash",
            "args": {"command": "...", "summary": "..."},
            "orig_args": {"command": "...", "summary": "..."}
          }]
        }
      },
      "request_metadata": {
        "request_id": "uuid",
        "message_id": "uuid",
        "request_start_timestamp_ms": 1768120855058,
        "stream_end_timestamp_ms": 1768120856955,
        "time_to_first_chunk": {"secs": 1, "nanos": 896639125},
        "time_between_chunks": [/* timing arrays */],
        "user_prompt_length": 170,
        "response_size": 9,
        "chat_conversation_type": "NotToolUse", // or "ToolUse"
        "tool_use_ids_and_names": [],
        "model_id": "auto",
        "message_meta_tags": []
      }
    }
  ]
}
```

## Common Analysis Queries

### Basic Database Exploration

#### Get database overview:
```sql
-- List all tables
.tables

-- Show table schemas
.schema

-- Count records in each table
SELECT 'migrations' as table_name, COUNT(*) as count FROM migrations
UNION ALL
SELECT 'conversations_v2', COUNT(*) FROM conversations_v2
UNION ALL
SELECT 'conversations', COUNT(*) FROM conversations
UNION ALL
SELECT 'history', COUNT(*) FROM history
UNION ALL
SELECT 'auth_kv', COUNT(*) FROM auth_kv
UNION ALL
SELECT 'state', COUNT(*) FROM state;
```

### Conversation Analysis

#### List all directories with conversation counts:
```sql
SELECT 
    key as directory,
    COUNT(*) as conversation_count,
    COUNT(DISTINCT conversation_id) as unique_conversations
FROM conversations_v2 
GROUP BY key 
ORDER BY conversation_count DESC;
```

#### Show recent conversations with metadata:
```sql
SELECT 
    key as directory,
    conversation_id,
    json_array_length(json_extract(value, '$.history')) as message_count,
    datetime(created_at/1000, 'unixepoch') as created,
    datetime(updated_at/1000, 'unixepoch') as updated,
    length(value) as data_size_bytes
FROM conversations_v2 
ORDER BY updated_at DESC 
LIMIT 10;
```

#### Find conversations by directory:
```sql
SELECT 
    conversation_id,
    json_extract(value, '$.history[0].user.content.Prompt.prompt') as first_message,
    json_array_length(json_extract(value, '$.history')) as message_count,
    datetime(created_at/1000, 'unixepoch') as created
FROM conversations_v2 
WHERE key = '/home/tom/workspace/ai/made/workspace/HelloWorld'
ORDER BY created_at;
```

### Message Content Analysis

#### Extract user prompts from conversations:
```sql
SELECT 
    key as directory,
    conversation_id,
    json_extract(value, '$.history[0].user.content.Prompt.prompt') as user_prompt,
    datetime(created_at/1000, 'unixepoch') as timestamp
FROM conversations_v2 
ORDER BY created_at DESC 
LIMIT 20;
```

#### Find conversations with tool usage:
```sql
SELECT 
    key as directory,
    conversation_id,
    json_extract(value, '$.history[0].assistant') as assistant_response,
    datetime(created_at/1000, 'unixepoch') as timestamp
FROM conversations_v2 
WHERE json_extract(value, '$.history[0].assistant.ToolUse') IS NOT NULL
ORDER BY created_at DESC;
```

#### Extract tool usage details:
```sql
SELECT 
    key as directory,
    json_extract(value, '$.history[0].assistant.ToolUse.tool_uses[0].name') as tool_name,
    json_extract(value, '$.history[0].assistant.ToolUse.tool_uses[0].args') as tool_args,
    datetime(created_at/1000, 'unixepoch') as timestamp
FROM conversations_v2 
WHERE json_extract(value, '$.history[0].assistant.ToolUse') IS NOT NULL;
```

### Performance Analysis

#### Response time analysis:
```sql
SELECT 
    key as directory,
    conversation_id,
    json_extract(value, '$.history[0].request_metadata.time_to_first_chunk.secs') as response_time_seconds,
    json_extract(value, '$.history[0].request_metadata.user_prompt_length') as prompt_length,
    json_extract(value, '$.history[0].request_metadata.response_size') as response_size,
    json_extract(value, '$.history[0].request_metadata.chat_conversation_type') as conversation_type
FROM conversations_v2 
WHERE json_extract(value, '$.history[0].request_metadata') IS NOT NULL
ORDER BY json_extract(value, '$.history[0].request_metadata.time_to_first_chunk.secs') DESC;
```

#### Average response times by conversation type:
```sql
SELECT 
    json_extract(value, '$.history[0].request_metadata.chat_conversation_type') as conversation_type,
    COUNT(*) as count,
    AVG(CAST(json_extract(value, '$.history[0].request_metadata.time_to_first_chunk.secs') AS REAL)) as avg_response_time_seconds,
    AVG(CAST(json_extract(value, '$.history[0].request_metadata.user_prompt_length') AS INTEGER)) as avg_prompt_length,
    AVG(CAST(json_extract(value, '$.history[0].request_metadata.response_size') AS INTEGER)) as avg_response_size
FROM conversations_v2 
WHERE json_extract(value, '$.history[0].request_metadata') IS NOT NULL
GROUP BY conversation_type;
```

### Time-based Analysis

#### Conversation activity by hour:
```sql
SELECT 
    strftime('%H', datetime(created_at/1000, 'unixepoch')) as hour,
    COUNT(*) as conversation_count
FROM conversations_v2 
GROUP BY hour 
ORDER BY hour;
```

#### Daily conversation patterns:
```sql
SELECT 
    DATE(datetime(created_at/1000, 'unixepoch')) as date,
    COUNT(*) as conversations,
    COUNT(DISTINCT key) as unique_directories,
    AVG(json_array_length(json_extract(value, '$.history'))) as avg_messages_per_conversation
FROM conversations_v2 
GROUP BY date 
ORDER BY date DESC;
```

#### Session gaps analysis (time between conversations in same directory):
```sql
WITH ordered_convs AS (
    SELECT 
        key, 
        conversation_id, 
        created_at,
        LAG(updated_at) OVER (PARTITION BY key ORDER BY created_at) as prev_updated
    FROM conversations_v2 
)
SELECT 
    key as directory,
    conversation_id,
    datetime(created_at/1000, 'unixepoch') as created,
    CASE 
        WHEN prev_updated IS NULL THEN 'First conversation'
        ELSE printf('%.1f seconds after previous', (created_at - prev_updated)/1000.0)
    END as gap_from_previous
FROM ordered_convs 
ORDER BY key, created_at;
```

### Application State Analysis

#### Check authentication status:
```sql
SELECT key, CASE WHEN value IS NOT NULL THEN 'Configured' ELSE 'Not set' END as status
FROM auth_kv;
```

#### View application configuration:
```sql
SELECT key, 
       CASE 
           WHEN key LIKE '%telemetry%' THEN 'Telemetry Setting'
           WHEN key LIKE '%profile%' THEN 'Profile Setting'
           WHEN key LIKE '%migration%' THEN 'Migration Status'
           ELSE 'Other Setting'
       END as category
FROM state 
ORDER BY category, key;
```

#### Migration history:
```sql
SELECT 
    version,
    datetime(migration_time, 'unixepoch') as migration_date
FROM migrations 
ORDER BY version;
```

## Practical Use Cases

### 1. Find Most Active Development Projects
```sql
SELECT 
    key as directory,
    COUNT(*) as total_conversations,
    COUNT(DISTINCT DATE(datetime(created_at/1000, 'unixepoch'))) as active_days,
    MIN(datetime(created_at/1000, 'unixepoch')) as first_activity,
    MAX(datetime(updated_at/1000, 'unixepoch')) as last_activity
FROM conversations_v2 
GROUP BY key 
ORDER BY total_conversations DESC;
```

### 2. Identify Complex vs Simple Interactions
```sql
SELECT 
    CASE 
        WHEN json_array_length(json_extract(value, '$.history')) = 1 THEN 'Single exchange'
        WHEN json_array_length(json_extract(value, '$.history')) <= 3 THEN 'Short conversation'
        ELSE 'Extended conversation'
    END as conversation_type,
    COUNT(*) as count,
    AVG(CAST(json_extract(value, '$.history[0].request_metadata.response_size') AS REAL)) as avg_response_size
FROM conversations_v2 
GROUP BY conversation_type;
```

### 3. Find Tool Usage Patterns
```sql
SELECT 
    json_extract(value, '$.history[0].assistant.ToolUse.tool_uses[0].name') as tool_name,
    COUNT(*) as usage_count,
    COUNT(DISTINCT key) as unique_directories
FROM conversations_v2 
WHERE json_extract(value, '$.history[0].assistant.ToolUse') IS NOT NULL
GROUP BY tool_name 
ORDER BY usage_count DESC;
```

### 4. Search for Specific Topics
```sql
-- Find conversations about Python
SELECT 
    key as directory,
    conversation_id,
    json_extract(value, '$.history[0].user.content.Prompt.prompt') as prompt,
    datetime(created_at/1000, 'unixepoch') as timestamp
FROM conversations_v2 
WHERE json_extract(value, '$.history[0].user.content.Prompt.prompt') LIKE '%python%'
   OR json_extract(value, '$.history[0].user.content.Prompt.prompt') LIKE '%Python%'
ORDER BY created_at DESC;
```

## Tips for Analysis

### Performance Considerations
- Use indexes on `updated_at` for time-based queries
- JSON extraction can be slow on large datasets
- Consider creating views for commonly accessed data patterns

### Common Gotcases
- Timestamps are in milliseconds, divide by 1000 for Unix epoch
- Not all conversations have request metadata
- Tool usage vs simple responses have different JSON structures
- Some fields may be null, always check with `IS NOT NULL`

### Useful SQLite Functions
- `json_extract(json, '$.path')` - Extract JSON values
- `json_array_length(json_array)` - Count array elements
- `datetime(timestamp, 'unixepoch')` - Convert timestamps
- `strftime('%format', date)` - Format dates for grouping

## Security Notes

- The database may contain sensitive information (API keys, file paths, conversations)
- Authentication tokens are stored in `auth_kv` table
- Consider data privacy when sharing analysis results
- File paths reveal directory structure and project names

## Database Maintenance

### Cleanup Old Conversations
```sql
-- Find old conversations (older than 30 days)
SELECT COUNT(*) 
FROM conversations_v2 
WHERE created_at < (strftime('%s', 'now') - 30*24*3600) * 1000;

-- Delete old conversations (BE CAREFUL!)
-- DELETE FROM conversations_v2 
-- WHERE created_at < (strftime('%s', 'now') - 30*24*3600) * 1000;
```

### Database Size Analysis
```sql
-- Estimate storage per directory
SELECT 
    key as directory,
    COUNT(*) as conversations,
    SUM(length(value)) as total_bytes,
    AVG(length(value)) as avg_bytes_per_conversation
FROM conversations_v2 
GROUP BY key 
ORDER BY total_bytes DESC;
```

This documentation provides a comprehensive guide for analyzing Kiro's SQLite database. Use these queries as starting points and modify them based on your specific analysis needs.
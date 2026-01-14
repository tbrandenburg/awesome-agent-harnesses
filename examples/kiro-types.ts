// Kiro Database Types
// Based on analysis of the SQLite database structure

export interface KiroDatabase {
  conversations_v2: ConversationRecord[];
  migrations: Migration[];
  auth_kv: AuthRecord[];
  state: StateRecord[];
  history: CommandHistory[];
}

export interface ConversationRecord {
  key: string; // Directory path
  conversation_id: string; // UUID
  value: string; // JSON string containing ConversationData
  created_at: number; // Unix timestamp in milliseconds
  updated_at: number; // Unix timestamp in milliseconds
}

export interface Migration {
  id: number;
  version: number;
  migration_time: number; // Unix timestamp
}

export interface AuthRecord {
  key: string;
  value: string;
}

export interface StateRecord {
  key: string;
  value: Uint8Array; // BLOB data as Uint8Array instead of Buffer
}

export interface CommandHistory {
  id: number;
  command: string | null;
  shell: string | null;
  pid: number | null;
  session_id: string | null;
  cwd: string | null;
  start_time: number | null;
  hostname: string | null;
  exit_code: number | null;
  end_time: number | null;
  duration: number | null;
}

// Conversation Data Structure (parsed from JSON)
export interface ConversationData {
  conversation_id: string;
  next_message: any | null;
  history: MessageExchange[];
}

export interface MessageExchange {
  user: UserMessage;
  assistant: AssistantResponse;
  request_metadata: RequestMetadata;
}

export interface UserMessage {
  additional_context: string;
  env_context: EnvironmentContext;
  content: UserContent;
  timestamp: string; // ISO format
  images: any | null;
}

export interface EnvironmentContext {
  env_state: {
    operating_system: string;
    current_working_directory: string;
    environment_variables: any[];
  };
}

export type UserContent = 
  | { Prompt: { prompt: string } }
  | { ToolUseResults: { tool_use_results: ToolResult[] } };

export interface ToolResult {
  tool_use_id: string;
  content: any[];
}

export type AssistantResponse = 
  | { Response: { message_id: string; content: string } }
  | { ToolUse: { message_id: string; content: string; tool_uses: ToolUse[] } };

export interface ToolUse {
  id: string;
  name: string;
  orig_name: string;
  args: Record<string, any>;
  orig_args: Record<string, any>;
}

export interface RequestMetadata {
  request_id: string;
  message_id: string;
  request_start_timestamp_ms: number;
  stream_end_timestamp_ms: number;
  time_to_first_chunk: Duration;
  time_between_chunks: Duration[];
  user_prompt_length: number;
  response_size: number;
  chat_conversation_type: 'ToolUse' | 'NotToolUse';
  tool_use_ids_and_names: any[];
  model_id: string;
  message_meta_tags: any[];
}

export interface Duration {
  secs: number;
  nanos: number;
}

// Analysis Result Types
export interface ConversationSummary {
  directory: string;
  conversationId: string;
  messageCount: number;
  created: Date;
  updated: Date;
  totalResponseTime: number;
  toolUsageCount: number;
}

export interface DirectoryStats {
  directory: string;
  totalConversations: number;
  totalMessages: number;
  averageResponseTime: number;
  toolUsageRate: number;
  firstActivity: Date;
  lastActivity: Date;
}
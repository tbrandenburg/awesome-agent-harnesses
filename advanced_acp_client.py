#!/usr/bin/env python3
"""
Advanced Python client for OpenCode ACP (Agent Client Protocol) server.

This enhanced script demonstrates:
1. Robust error handling and timeout management
2. Session management with MCP server integration
3. Multiple prompt interactions
4. Tool call monitoring
5. Response streaming with proper formatting
6. Graceful shutdown procedures

Usage:
    python3 advanced_acp_client.py
    python3 advanced_acp_client.py --prompt "Your custom prompt here"
    python3 advanced_acp_client.py --interactive
"""

import json
import subprocess
import sys
import os
import time
import threading
import queue
import argparse
import signal
from typing import Dict, List, Any, Optional


class AdvancedACPClient:
    def __init__(self, verbose: bool = False):
        self.process: Optional[subprocess.Popen] = None
        self.message_id = 0
        self.response_queue = queue.Queue()
        self.session_id: Optional[str] = None
        self.verbose = verbose
        self.running = True
        self.reader_thread: Optional[threading.Thread] = None

    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        icon = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(
            level, "📝"
        )
        print(f"[{timestamp}] {icon} {message}")

    def get_next_id(self) -> int:
        """Get next message ID for JSON-RPC requests"""
        self.message_id += 1
        return self.message_id

    def start_acp_server(self) -> bool:
        """Start the OpenCode ACP server as a subprocess"""
        try:
            self.log("Starting OpenCode ACP server...")

            cmd = ["opencode", "acp"]
            if self.verbose:
                cmd.append("--print-logs")

            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            # Give the server a moment to start up
            time.sleep(2)

            # Check if process is still running
            if self.process.poll() is not None:
                stderr_output = (
                    self.process.stderr.read()
                    if self.process.stderr
                    else "No error info"
                )
                self.log(f"ACP server failed to start: {stderr_output}", "ERROR")
                return False

            self.log("ACP server started successfully", "SUCCESS")

            # Start reader thread for responses
            self.reader_thread = threading.Thread(
                target=self._read_responses, daemon=True
            )
            self.reader_thread.start()

            return True

        except FileNotFoundError:
            self.log("OpenCode CLI not found. Please install OpenCode first.", "ERROR")
            return False
        except Exception as e:
            self.log(f"Failed to start ACP server: {e}", "ERROR")
            return False

    def _read_responses(self):
        """Read responses from ACP server in a separate thread"""
        try:
            while self.running and self.process and self.process.poll() is None:
                if self.process.stdout:
                    line = self.process.stdout.readline()
                    if line:
                        line = line.strip()
                        if line:
                            try:
                                response = json.loads(line)
                                self.response_queue.put(response)
                            except json.JSONDecodeError:
                                if self.verbose:
                                    self.log(f"Non-JSON output: {line}", "WARNING")
        except Exception as e:
            if self.running:  # Only log if we haven't initiated shutdown
                self.log(f"Error reading from server: {e}", "ERROR")

    def send_message(self, message: Dict[str, Any]) -> bool:
        """Send a JSON-RPC message to the ACP server"""
        if not self.process or not self.process.stdin:
            self.log("ACP server not available", "ERROR")
            return False

        try:
            json_message = json.dumps(message) + "\n"
            if self.verbose:
                self.log(f"Sending: {json_message.strip()}")
            self.process.stdin.write(json_message)
            self.process.stdin.flush()
            return True
        except Exception as e:
            self.log(f"Failed to send message: {e}", "ERROR")
            return False

    def wait_for_response(self, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Wait for a response from the ACP server"""
        try:
            response = self.response_queue.get(timeout=timeout)
            if self.verbose:
                self.log(f"Received: {json.dumps(response, indent=2)}")
            return response
        except queue.Empty:
            self.log(f"Timeout waiting for response after {timeout}s", "WARNING")
            return None

    def initialize(self) -> bool:
        """Perform ACP initialization handshake"""
        self.log("Initializing ACP connection...")

        init_message = {
            "jsonrpc": "2.0",
            "id": self.get_next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientCapabilities": {
                    "fs": {"readTextFile": True, "writeTextFile": True},
                    "terminal": True,
                },
                "clientInfo": {
                    "name": "advanced-acp-python-client",
                    "title": "Advanced Python ACP Client",
                    "version": "2.0.0",
                },
            },
        }

        if not self.send_message(init_message):
            return False

        response = self.wait_for_response()
        if not response:
            return False

        if "result" in response:
            self.log("Initialization successful", "SUCCESS")
            agent_info = response["result"].get("agentInfo", {})
            agent_name = agent_info.get("name", "Unknown")
            agent_version = agent_info.get("version", "Unknown")
            self.log(f"Connected to: {agent_name} v{agent_version}")

            # Log capabilities
            capabilities = response["result"].get("agentCapabilities", {})
            self.log(f"Agent capabilities: {list(capabilities.keys())}")
            return True
        else:
            self.log(f"Initialization failed: {response}", "ERROR")
            return False

    def create_session(self, with_mcp: bool = False) -> bool:
        """Create a new ACP session with optional MCP servers"""
        self.log("Creating new session...")

        mcp_servers = []
        if with_mcp:
            # Add some basic MCP servers if available
            mcp_servers = [
                {
                    "name": "filesystem",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
                    "env": [],
                }
            ]

        session_message = {
            "jsonrpc": "2.0",
            "id": self.get_next_id(),
            "method": "session/new",
            "params": {"cwd": os.getcwd(), "mcpServers": mcp_servers},
        }

        if not self.send_message(session_message):
            return False

        response = self.wait_for_response()
        if not response:
            return False

        if "result" in response and "sessionId" in response["result"]:
            self.session_id = response["result"]["sessionId"]
            self.log(f"Session created: {self.session_id}", "SUCCESS")

            # Log available models
            models = response["result"].get("models", {})
            current_model = models.get("currentModelId", "Unknown")
            self.log(f"Using model: {current_model}")
            return True
        else:
            self.log(f"Session creation failed: {response}", "ERROR")
            return False

    def send_prompt(self, prompt_text: str, timeout: float = 120.0) -> bool:
        """Send a prompt to the ACP agent and wait for completion"""
        if not self.session_id:
            self.log("No active session", "ERROR")
            return False

        self.log(
            f"Sending prompt: {prompt_text[:100]}{'...' if len(prompt_text) > 100 else ''}"
        )

        prompt_message = {
            "jsonrpc": "2.0",
            "id": self.get_next_id(),
            "method": "session/prompt",
            "params": {
                "sessionId": self.session_id,
                "prompt": [{"type": "text", "text": prompt_text}],
            },
        }

        if not self.send_message(prompt_message):
            return False

        # Process session updates and final response
        print("\n" + "=" * 60)
        print("🤖 AGENT RESPONSE:")
        print("=" * 60)

        response_text = []
        tool_calls = {}

        start_time = time.time()

        while time.time() - start_time < timeout:
            response = self.wait_for_response(timeout=30.0)
            if not response:
                self.log("Timeout waiting for response", "WARNING")
                return False

            # Handle session updates (notifications)
            if response.get("method") == "session/update":
                update = response["params"]["update"]

                if update.get("sessionUpdate") == "agent_message_chunk":
                    content = update.get("content", {})
                    if content.get("type") == "text":
                        text = content.get("text", "")
                        print(text, end="", flush=True)
                        response_text.append(text)

                elif update.get("sessionUpdate") == "tool_call":
                    tool_id = update.get("toolCallId")
                    tool_title = update.get("title", "Unknown tool")
                    tool_calls[tool_id] = {"title": tool_title, "status": "pending"}
                    print(f"\n\n🔧 [TOOL CALL] {tool_title} (ID: {tool_id})")

                elif update.get("sessionUpdate") == "tool_call_update":
                    tool_id = update.get("toolCallId")
                    status = update.get("status")

                    if tool_id in tool_calls:
                        tool_calls[tool_id]["status"] = status

                    if status == "in_progress":
                        print(f"   ⏳ {tool_calls[tool_id]['title']} - Running...")
                    elif status == "completed":
                        print(f"   ✅ {tool_calls[tool_id]['title']} - Completed")
                        content_blocks = update.get("content", [])
                        for block in content_blocks:
                            if block.get("type") == "content":
                                inner_content = block.get("content", {})
                                if inner_content.get("type") == "text":
                                    result_text = inner_content.get("text", "")
                                    print(
                                        f"      📋 Result: {result_text[:200]}{'...' if len(result_text) > 200 else ''}"
                                    )
                    elif status == "failed":
                        print(f"   ❌ {tool_calls[tool_id]['title']} - Failed")

                elif update.get("sessionUpdate") == "plan":
                    entries = update.get("entries", [])
                    print(f"\n\n📋 [AGENT PLAN] {len(entries)} steps:")
                    for i, entry in enumerate(entries, 1):
                        content = entry.get("content", "")
                        priority = entry.get("priority", "medium")
                        status = entry.get("status", "pending")
                        icon = (
                            "🔴"
                            if priority == "high"
                            else "🟡"
                            if priority == "medium"
                            else "🟢"
                        )
                        print(f"   {i}. {icon} {content} [{status}]")

            # Handle final response with stop reason
            elif "result" in response and "stopReason" in response["result"]:
                stop_reason = response["result"]["stopReason"]
                print(f"\n\n✅ [COMPLETE] Turn finished (reason: {stop_reason})")
                break

            # Handle error responses
            elif "error" in response:
                error = response["error"]
                self.log(f"Agent error: {error}", "ERROR")
                return False

        print("=" * 60)

        # Summary
        total_text = "".join(response_text)
        self.log(
            f"Response completed: {len(total_text)} characters, {len(tool_calls)} tool calls",
            "SUCCESS",
        )
        return True

    def interactive_mode(self):
        """Run in interactive mode for multiple prompts"""
        self.log("Starting interactive mode. Type 'exit' to quit.")

        while self.running:
            try:
                prompt = input("\n💭 Enter your prompt: ").strip()

                if prompt.lower() in ["exit", "quit", "q"]:
                    break

                if not prompt:
                    continue

                if not self.send_prompt(prompt):
                    self.log("Failed to send prompt", "ERROR")

            except KeyboardInterrupt:
                print("\n")
                break
            except EOFError:
                break

    def shutdown(self):
        """Gracefully shutdown the ACP server"""
        self.running = False
        self.log("Shutting down ACP server...")

        if self.process and self.process.stdin:
            # Send exit message
            exit_message = {"jsonrpc": "2.0", "method": "exit"}
            try:
                self.send_message(exit_message)
                time.sleep(1)
            except:
                pass

            # Force terminate if still running
            if self.process.poll() is None:
                self.process.terminate()
                time.sleep(1)

                if self.process.poll() is None:
                    self.process.kill()

        self.log("ACP server shutdown complete", "SUCCESS")


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n⚠️  Received interrupt signal, shutting down...")
    sys.exit(0)


def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description="Advanced OpenCode ACP Client")
    parser.add_argument("--prompt", "-p", help="Single prompt to send")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument("--mcp", action="store_true", help="Enable MCP servers")
    parser.add_argument(
        "--timeout", "-t", type=float, default=120.0, help="Timeout for responses"
    )

    args = parser.parse_args()

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    client = AdvancedACPClient(verbose=args.verbose)

    try:
        # Start ACP server
        if not client.start_acp_server():
            return 1

        # Initialize connection
        if not client.initialize():
            return 1

        # Create session
        if not client.create_session(with_mcp=args.mcp):
            return 1

        # Handle different modes
        if args.interactive:
            client.interactive_mode()
        elif args.prompt:
            if not client.send_prompt(args.prompt, timeout=args.timeout):
                return 1
        else:
            # Default prompt
            default_prompt = "Hello! Can you explain what makes a good AI agent harness, and give me 3 key principles?"
            if not client.send_prompt(default_prompt, timeout=args.timeout):
                return 1

        client.log("ACP interaction completed successfully!", "SUCCESS")
        return 0

    except KeyboardInterrupt:
        client.log("Interrupted by user", "WARNING")
        return 1

    except Exception as e:
        client.log(f"Unexpected error: {e}", "ERROR")
        return 1

    finally:
        client.shutdown()


if __name__ == "__main__":
    sys.exit(main())

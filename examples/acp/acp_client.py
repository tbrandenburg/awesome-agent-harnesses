#!/usr/bin/env python3
"""
Simple Python client for OpenCode ACP (Agent Client Protocol) server.

This script demonstrates how to:
1. Start an OpenCode ACP server
2. Perform the initialization handshake
3. Create a session
4. Send a prompt
5. Receive and display the response
6. Gracefully shut down
"""

import json
import subprocess
import sys
import os
import time
import threading
import queue
from typing import Dict, List, Any, Optional


class ACPClient:
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.message_id = 0
        self.response_queue = queue.Queue()
        self.session_id: Optional[str] = None

    def get_next_id(self) -> int:
        """Get next message ID for JSON-RPC requests"""
        self.message_id += 1
        return self.message_id

    def start_acp_server(self) -> bool:
        """Start the OpenCode ACP server as a subprocess"""
        try:
            print("🚀 Starting OpenCode ACP server...")
            self.process = subprocess.Popen(
                ["opencode", "acp", "--print-logs"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            # Give the server a moment to start up
            time.sleep(1)

            # Check if process is still running
            if self.process.poll() is not None:
                stderr_output = (
                    self.process.stderr.read()
                    if self.process.stderr
                    else "No error info"
                )
                print(f"❌ ACP server failed to start: {stderr_output}")
                return False

            print("✅ ACP server started successfully")

            # Start reader thread for responses
            self.reader_thread = threading.Thread(
                target=self._read_responses, daemon=True
            )
            self.reader_thread.start()

            return True

        except FileNotFoundError:
            print("❌ OpenCode CLI not found. Please install OpenCode first.")
            return False
        except Exception as e:
            print(f"❌ Failed to start ACP server: {e}")
            return False

    def _read_responses(self):
        """Read responses from ACP server in a separate thread"""
        try:
            while self.process and self.process.poll() is None:
                if self.process.stdout:
                    line = self.process.stdout.readline()
                    if line:
                        line = line.strip()
                        if line:
                            try:
                                response = json.loads(line)
                                self.response_queue.put(response)
                            except json.JSONDecodeError:
                                print(f"⚠️  Non-JSON output from server: {line}")
        except Exception as e:
            print(f"⚠️  Error reading from server: {e}")

    def send_message(self, message: Dict[str, Any]) -> bool:
        """Send a JSON-RPC message to the ACP server"""
        if not self.process or not self.process.stdin:
            print("❌ ACP server not available")
            return False

        try:
            json_message = json.dumps(message) + "\n"
            print(f"📤 Sending: {json_message.strip()}")
            self.process.stdin.write(json_message)
            self.process.stdin.flush()
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False

    def wait_for_response(self, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Wait for a response from the ACP server"""
        try:
            response = self.response_queue.get(timeout=timeout)
            print(f"📥 Received: {json.dumps(response, indent=2)}")
            return response
        except queue.Empty:
            print(f"⏰ Timeout waiting for response after {timeout}s")
            return None

    def initialize(self) -> bool:
        """Perform ACP initialization handshake"""
        print("\n🤝 Initializing ACP connection...")

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
                    "name": "acp-python-client",
                    "title": "Python ACP Test Client",
                    "version": "1.0.0",
                },
            },
        }

        if not self.send_message(init_message):
            return False

        response = self.wait_for_response()
        if not response:
            return False

        if "result" in response:
            print("✅ Initialization successful")
            agent_info = response["result"].get("agentInfo", {})
            print(
                f"🤖 Agent: {agent_info.get('title', 'Unknown')} v{agent_info.get('version', 'Unknown')}"
            )
            return True
        else:
            print(f"❌ Initialization failed: {response}")
            return False

    def create_session(self) -> bool:
        """Create a new ACP session"""
        print("\n📋 Creating new session...")

        session_message = {
            "jsonrpc": "2.0",
            "id": self.get_next_id(),
            "method": "session/new",
            "params": {
                "cwd": os.getcwd(),
                "mcpServers": [],  # No MCP servers for this simple example
            },
        }

        if not self.send_message(session_message):
            return False

        response = self.wait_for_response()
        if not response:
            return False

        if "result" in response and "sessionId" in response["result"]:
            self.session_id = response["result"]["sessionId"]
            print(f"✅ Session created: {self.session_id}")
            return True
        else:
            print(f"❌ Session creation failed: {response}")
            return False

    def send_prompt(self, prompt_text: str) -> bool:
        """Send a prompt to the ACP agent and wait for completion"""
        if not self.session_id:
            print("❌ No active session")
            return False

        print(f"\n💭 Sending prompt: {prompt_text}")

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

        # Wait for session updates and final response
        print("\n📝 Agent response:")
        print("-" * 50)

        response_text = []

        while True:
            response = self.wait_for_response(timeout=60.0)
            if not response:
                print("❌ Timeout waiting for response")
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
                    tool_call = update
                    print(f"\n🔧 Tool call: {tool_call.get('title', 'Unknown')}")

                elif update.get("sessionUpdate") == "tool_call_update":
                    status = update.get("status")
                    if status == "completed":
                        content_blocks = update.get("content", [])
                        for block in content_blocks:
                            if block.get("type") == "content":
                                inner_content = block.get("content", {})
                                if inner_content.get("type") == "text":
                                    text = inner_content.get("text", "")
                                    print(f"\n📋 Tool result: {text}")

            # Handle final response with stop reason
            elif "result" in response and "stopReason" in response["result"]:
                stop_reason = response["result"]["stopReason"]
                print(f"\n\n✅ Turn completed (reason: {stop_reason})")
                break

            # Handle error responses
            elif "error" in response:
                print(f"\n❌ Error: {response['error']}")
                return False

        print("-" * 50)
        return True

    def shutdown(self):
        """Gracefully shutdown the ACP server"""
        print("\n🔄 Shutting down ACP server...")

        if self.process and self.process.stdin:
            # Send exit message
            exit_message = {"jsonrpc": "2.0", "method": "exit"}
            self.send_message(exit_message)

            # Give server time to shutdown gracefully
            time.sleep(1)

            # Force terminate if still running
            if self.process.poll() is None:
                self.process.terminate()
                time.sleep(1)

                if self.process.poll() is None:
                    self.process.kill()

        print("✅ ACP server shutdown complete")


def main():
    """Main function to demonstrate ACP interaction"""
    client = ACPClient()

    try:
        # Start ACP server
        if not client.start_acp_server():
            return 1

        # Initialize connection
        if not client.initialize():
            return 1

        # Create session
        if not client.create_session():
            return 1

        # Send a test prompt
        prompt = "Hello! Can you explain what agent harnesses are in one paragraph?"
        if not client.send_prompt(prompt):
            return 1

        print("\n🎉 ACP interaction completed successfully!")
        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return 1

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

    finally:
        client.shutdown()


if __name__ == "__main__":
    sys.exit(main())

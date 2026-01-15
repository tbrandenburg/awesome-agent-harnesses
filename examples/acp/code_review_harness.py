#!/usr/bin/env python3
"""
Code Review Harness - A practical example using OpenCode ACP protocol

This harness demonstrates how to use the ACP client for automated code review workflows.
It can analyze code files, provide feedback, and suggest improvements.

Features:
- Single file analysis
- Batch code review
- Security vulnerability scanning
- Code quality assessment
- Automated fix suggestions

Usage:
    python code_review_harness.py --file path/to/code.py
    python code_review_harness.py --directory src/
    python code_review_harness.py --scan-security --fix-auto
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


class CodeReviewHarness:
    """Advanced code review harness using OpenCode ACP protocol"""

    def __init__(self, working_dir: str = None, mcp_servers: List[str] = None):
        self.working_dir = working_dir or os.getcwd()
        self.mcp_servers = mcp_servers or []
        self.server_process = None
        self.session_id = None

    async def start_acp_server(self) -> bool:
        """Start OpenCode ACP server"""
        try:
            logger.info("🚀 Starting OpenCode ACP server...")
            self.server_process = subprocess.Popen(
                ["opencode", "acp"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Wait for server to be ready
            await asyncio.sleep(2)

            if self.server_process.poll() is None:
                logger.info("✅ ACP server started successfully")
                return True
            else:
                logger.error("❌ Failed to start ACP server")
                return False

        except Exception as e:
            logger.error(f"❌ Error starting ACP server: {e}")
            return False

    async def send_request(self, method: str, params: Dict = None) -> Dict:
        """Send JSON-RPC request to ACP server"""
        import websockets

        try:
            async with websockets.connect("ws://localhost:3001") as websocket:
                request = {
                    "jsonrpc": "2.0",
                    "id": int(time.time() * 1000),
                    "method": method,
                    "params": params or {},
                }

                await websocket.send(json.dumps(request))
                response = await websocket.recv()
                return json.loads(response)

        except Exception as e:
            logger.error(f"❌ Error sending request: {e}")
            return {"error": str(e)}

    async def initialize_session(self) -> bool:
        """Initialize ACP session"""
        try:
            # Initialize connection
            init_response = await self.send_request(
                "initialize",
                {
                    "protocolVersion": 1,
                    "clientCapabilities": {
                        "fs": {"readTextFile": True, "writeTextFile": True},
                        "terminal": True,
                    },
                    "clientInfo": {
                        "name": "code-review-harness",
                        "title": "Code Review Harness",
                        "version": "1.0.0",
                    },
                },
            )

            if "error" in init_response:
                logger.error(f"❌ Initialization failed: {init_response['error']}")
                return False

            # Create new session
            session_response = await self.send_request(
                "session/new", {"cwd": self.working_dir, "mcpServers": self.mcp_servers}
            )

            if "error" in session_response:
                logger.error(f"❌ Session creation failed: {session_response['error']}")
                return False

            self.session_id = session_response["result"]["sessionId"]
            logger.info(f"✅ Session created: {self.session_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error initializing session: {e}")
            return False

    async def review_file(
        self, file_path: str, review_type: str = "comprehensive"
    ) -> Dict:
        """Review a single code file"""
        try:
            logger.info(f"🔍 Reviewing file: {file_path}")

            prompts = {
                "comprehensive": f"""
Please perform a comprehensive code review of the file: {file_path}

Analyze the following aspects:
1. **Code Quality**: Structure, readability, maintainability
2. **Security**: Potential vulnerabilities and security issues  
3. **Performance**: Optimization opportunities and bottlenecks
4. **Best Practices**: Adherence to language conventions and patterns
5. **Documentation**: Comments, docstrings, and inline documentation
6. **Error Handling**: Exception handling and edge cases

Provide:
- A summary rating (1-10)
- Specific issues found with line numbers
- Actionable recommendations for improvement
- Code snippets for suggested fixes where applicable

Format your response in markdown with clear sections.
                """,
                "security": f"""
Please perform a security-focused review of the file: {file_path}

Focus on identifying:
1. **Input Validation**: SQL injection, XSS, command injection risks
2. **Authentication/Authorization**: Access control issues
3. **Data Handling**: Sensitive data exposure, encryption concerns
4. **Dependencies**: Vulnerable third-party libraries
5. **Configuration**: Hardcoded secrets, insecure defaults

Provide a security report with:
- Risk level for each issue (Critical/High/Medium/Low)
- Specific vulnerable code locations
- Mitigation strategies
- Secure coding alternatives
                """,
                "performance": f"""
Please analyze the performance characteristics of the file: {file_path}

Examine:
1. **Algorithm Complexity**: Big O analysis of key functions
2. **Resource Usage**: Memory, CPU, I/O efficiency
3. **Bottlenecks**: Potential performance hotspots
4. **Optimization Opportunities**: Caching, lazy loading, etc.
5. **Scalability**: How the code performs under load

Provide performance insights with:
- Performance rating (1-10)
- Identified bottlenecks with line numbers
- Optimization recommendations
- Expected performance improvements
                """,
            }

            prompt = prompts.get(review_type, prompts["comprehensive"])

            response = await self.send_request(
                "session/prompt",
                {
                    "sessionId": self.session_id,
                    "prompt": [{"type": "text", "text": prompt}],
                },
            )

            if "error" in response:
                logger.error(f"❌ Review failed: {response['error']}")
                return {"success": False, "error": response["error"]}

            logger.info("✅ Code review completed")
            return {"success": True, "response": response}

        except Exception as e:
            logger.error(f"❌ Error reviewing file: {e}")
            return {"success": False, "error": str(e)}

    async def batch_review(
        self, file_paths: List[str], review_type: str = "comprehensive"
    ) -> List[Dict]:
        """Review multiple files in batch"""
        results = []

        for file_path in file_paths:
            result = await self.review_file(file_path, review_type)
            results.append({"file": file_path, "result": result})

            # Small delay between reviews to avoid overwhelming
            await asyncio.sleep(1)

        return results

    async def suggest_fixes(self, file_path: str, issues: List[str]) -> Dict:
        """Generate automated fix suggestions"""
        try:
            logger.info(f"🔧 Generating fix suggestions for: {file_path}")

            issues_text = "\n".join([f"- {issue}" for issue in issues])

            prompt = f"""
Based on the following issues identified in {file_path}:

{issues_text}

Please provide specific, actionable fix suggestions:

1. **Code Patches**: Exact code changes needed (show before/after)
2. **Refactoring**: Structural improvements 
3. **Dependencies**: Required library updates or additions
4. **Configuration**: Settings or environment changes needed
5. **Testing**: Recommended tests to prevent regression

For each suggestion, provide:
- The specific problem being addressed
- The proposed solution with code examples
- Rationale for the approach chosen
- Potential risks or side effects

Format as clear, executable recommendations.
            """

            response = await self.send_request(
                "session/prompt",
                {
                    "sessionId": self.session_id,
                    "prompt": [{"type": "text", "text": prompt}],
                },
            )

            if "error" in response:
                logger.error(f"❌ Fix suggestion failed: {response['error']}")
                return {"success": False, "error": response["error"]}

            logger.info("✅ Fix suggestions generated")
            return {"success": True, "response": response}

        except Exception as e:
            logger.error(f"❌ Error generating fixes: {e}")
            return {"success": False, "error": str(e)}

    def find_code_files(
        self, directory: str, extensions: List[str] = None
    ) -> List[str]:
        """Find code files in directory"""
        if extensions is None:
            extensions = [
                ".py",
                ".js",
                ".ts",
                ".java",
                ".cpp",
                ".c",
                ".go",
                ".rs",
                ".rb",
                ".php",
            ]

        code_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    code_files.append(os.path.join(root, file))

        return code_files

    async def cleanup(self):
        """Cleanup resources"""
        try:
            if self.session_id:
                await self.send_request("exit")

            if self.server_process:
                self.server_process.terminate()
                await asyncio.sleep(1)
                if self.server_process.poll() is None:
                    self.server_process.kill()

            logger.info("✅ Cleanup completed")

        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Code Review Harness using OpenCode ACP"
    )
    parser.add_argument("--file", "-f", help="Single file to review")
    parser.add_argument("--directory", "-d", help="Directory to review recursively")
    parser.add_argument(
        "--type",
        "-t",
        choices=["comprehensive", "security", "performance"],
        default="comprehensive",
        help="Type of review to perform",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".py", ".js", ".ts"],
        help="File extensions to include",
    )
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument(
        "--suggest-fixes",
        action="store_true",
        help="Generate automated fix suggestions",
    )
    parser.add_argument("--working-dir", help="Working directory for ACP session")

    args = parser.parse_args()

    if not args.file and not args.directory:
        parser.error("Must specify either --file or --directory")

    # Initialize harness
    harness = CodeReviewHarness(working_dir=args.working_dir)

    try:
        # Start ACP server and initialize session
        if not await harness.start_acp_server():
            sys.exit(1)

        if not await harness.initialize_session():
            sys.exit(1)

        # Collect files to review
        if args.file:
            files_to_review = [args.file]
        else:
            files_to_review = harness.find_code_files(args.directory, args.extensions)
            logger.info(f"📁 Found {len(files_to_review)} files to review")

        # Perform reviews
        results = await harness.batch_review(files_to_review, args.type)

        # Generate fix suggestions if requested
        if args.suggest_fixes:
            for result in results:
                if result["result"]["success"]:
                    # Extract issues from review (simplified)
                    issues = [
                        "Example issue 1",
                        "Example issue 2",
                    ]  # Parse from actual response
                    fix_result = await harness.suggest_fixes(result["file"], issues)
                    result["fixes"] = fix_result

        # Output results
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"📄 Results saved to: {args.output}")
        else:
            print(json.dumps(results, indent=2))

        logger.info("🎉 Code review harness completed successfully!")

    except KeyboardInterrupt:
        logger.info("⏹️ Review interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        await harness.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

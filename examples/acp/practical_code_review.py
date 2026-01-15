#!/usr/bin/env python3
"""
Practical Code Review Harness using OpenCode ACP

A real-world example demonstrating how to build automated workflows with ACP clients.
This harness performs code reviews, security scans, and generates improvement reports.

Usage:
    python practical_code_review.py --file src/example.py
    python practical_code_review.py --directory src/ --type security
    python practical_code_review.py --batch *.py --output review_report.md
"""

import argparse
import subprocess
import sys
import os
import glob
import tempfile
from pathlib import Path
import json


class CodeReviewHarness:
    """Practical code review harness using our ACP client"""

    def __init__(self, acp_client_path: str = None):
        self.acp_client_path = acp_client_path or "advanced_acp_client.py"

    def run_acp_review(self, prompt: str, timeout: int = 120) -> str:
        """Run a code review using ACP client"""
        try:
            result = subprocess.run(
                [
                    "python",
                    self.acp_client_path,
                    "--prompt",
                    prompt,
                    "--timeout",
                    str(timeout),
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if result.returncode != 0:
                raise Exception(f"ACP client failed: {result.stderr}")

            return result.stdout

        except subprocess.TimeoutExpired:
            raise Exception(f"Review timed out after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Error running ACP review: {e}")

    def review_file(self, file_path: str, review_type: str = "comprehensive") -> dict:
        """Review a single code file"""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file content for context
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        file_size = len(content)
        line_count = len(content.split("\n"))

        prompts = {
            "comprehensive": f"""
Please perform a comprehensive code review of this file: {file_path}

File Statistics:
- Size: {file_size} characters
- Lines: {line_count}

Please analyze:
1. **Code Quality** - Structure, readability, maintainability
2. **Best Practices** - Language conventions and patterns  
3. **Potential Issues** - Bugs, edge cases, error handling
4. **Security** - Basic security considerations
5. **Performance** - Obvious optimization opportunities

For each issue found:
- Specify the line number if possible
- Explain the problem clearly
- Suggest specific improvements
- Rate severity (High/Medium/Low)

Provide an overall rating (1-10) and summary recommendations.

Use markdown format with clear sections and bullet points.
            """,
            "security": f"""
Perform a security-focused analysis of this file: {file_path}

Look for:
1. **Input Validation** - Unvalidated user input, injection risks
2. **Authentication/Authorization** - Access control issues
3. **Data Handling** - Sensitive data exposure, encryption
4. **Dependencies** - Potentially vulnerable imports/libraries
5. **Configuration** - Hardcoded secrets, insecure defaults
6. **Error Handling** - Information disclosure in errors

For each security concern:
- Identify the specific code location
- Assess risk level (Critical/High/Medium/Low)  
- Provide secure alternatives
- Reference relevant security standards (OWASP, etc.)

Format as a security assessment report.
            """,
            "performance": f"""
Analyze the performance characteristics of this file: {file_path}

Examine:
1. **Algorithm Efficiency** - Time/space complexity analysis
2. **Resource Usage** - Memory, CPU, I/O patterns
3. **Bottlenecks** - Performance hotspots and slow operations
4. **Optimization Opportunities** - Caching, lazy loading, etc.
5. **Scalability** - How code performs under load

Provide:
- Performance rating (1-10)
- Specific bottleneck locations
- Optimization recommendations with code examples
- Expected performance impact of changes

Use technical analysis with concrete suggestions.
            """,
            "quick": f"""
Perform a quick code review of this file: {file_path}

Provide a brief assessment covering:
- Overall code quality (1-10)
- Top 3 issues that need attention
- Quick wins for improvement
- Any critical bugs or security issues

Keep the response concise and actionable.
            """,
        }

        prompt = prompts.get(review_type, prompts["comprehensive"])

        try:
            print(f"🔍 Reviewing {file_path} ({review_type} analysis)...")
            output = self.run_acp_review(prompt)

            return {
                "file": file_path,
                "review_type": review_type,
                "success": True,
                "output": output,
                "stats": {"size": file_size, "lines": line_count},
            }

        except Exception as e:
            return {
                "file": file_path,
                "review_type": review_type,
                "success": False,
                "error": str(e),
            }

    def review_directory(
        self,
        directory: str,
        review_type: str = "comprehensive",
        extensions: list = None,
        max_files: int = 10,
    ) -> list:
        """Review all code files in a directory"""

        if extensions is None:
            extensions = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs"]

        code_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    # Skip very large files (>100KB)
                    if os.path.getsize(file_path) < 100000:
                        code_files.append(file_path)

        # Limit number of files to avoid overwhelming
        if len(code_files) > max_files:
            print(f"⚠️ Found {len(code_files)} files, limiting to first {max_files}")
            code_files = code_files[:max_files]

        results = []
        for i, file_path in enumerate(code_files, 1):
            print(f"📁 Processing file {i}/{len(code_files)}: {file_path}")
            result = self.review_file(file_path, review_type)
            results.append(result)

        return results

    def batch_review(self, patterns: list, review_type: str = "comprehensive") -> list:
        """Review files matching glob patterns"""

        all_files = []
        for pattern in patterns:
            files = glob.glob(pattern, recursive=True)
            all_files.extend(files)

        # Remove duplicates and filter for code files
        unique_files = list(set(all_files))
        code_extensions = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs"]

        code_files = [
            f
            for f in unique_files
            if any(f.endswith(ext) for ext in code_extensions) and os.path.isfile(f)
        ]

        results = []
        for i, file_path in enumerate(code_files, 1):
            print(f"🔍 Reviewing {i}/{len(code_files)}: {file_path}")
            result = self.review_file(file_path, review_type)
            results.append(result)

        return results

    def generate_report(self, results: list, output_file: str = None) -> str:
        """Generate a comprehensive review report"""

        successful_reviews = [r for r in results if r["success"]]
        failed_reviews = [r for r in results if not r["success"]]

        report = f"""# Code Review Report

Generated by OpenCode ACP Code Review Harness

## Summary
- **Total Files Reviewed**: {len(results)}
- **Successful Reviews**: {len(successful_reviews)}
- **Failed Reviews**: {len(failed_reviews)}
- **Review Type**: {results[0]["review_type"] if results else "N/A"}

"""

        if failed_reviews:
            report += "## Failed Reviews\n\n"
            for failure in failed_reviews:
                report += f"- **{failure['file']}**: {failure['error']}\n"
            report += "\n"

        report += "## Individual File Reviews\n\n"

        for result in successful_reviews:
            report += f"### {result['file']}\n\n"
            report += f"**File Stats**: {result['stats']['lines']} lines, {result['stats']['size']} chars\n\n"

            # Extract the agent response from the output
            output_lines = result["output"].split("\n")
            agent_response_start = False

            for line in output_lines:
                if "AGENT RESPONSE:" in line:
                    agent_response_start = True
                    continue
                elif (
                    "✅ Response completed" in line
                    or "ACP interaction completed" in line
                ):
                    break
                elif agent_response_start and line.strip():
                    # Skip tool call lines and status lines
                    if not any(
                        x in line
                        for x in [
                            "🔧 [TOOL CALL]",
                            "⏳",
                            "✅",
                            "📋 Result:",
                            "============",
                        ]
                    ):
                        report += line + "\n"

            report += "\n---\n\n"

        if output_file:
            with open(output_file, "w") as f:
                f.write(report)
            print(f"📄 Report saved to: {output_file}")

        return report


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Practical Code Review Harness")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Single file to review")
    group.add_argument("--directory", "-d", help="Directory to review")
    group.add_argument(
        "--batch", "-b", nargs="+", help="Glob patterns for batch review"
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=["comprehensive", "security", "performance", "quick"],
        default="comprehensive",
        help="Review type",
    )
    parser.add_argument("--output", "-o", help="Output report file")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".py", ".js", ".ts", ".java"],
        help="File extensions to include",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=10,
        help="Maximum files to review in directory mode",
    )

    args = parser.parse_args()

    # Validate ACP client exists
    if not os.path.exists("advanced_acp_client.py"):
        print("❌ advanced_acp_client.py not found in current directory")
        print("Make sure you're running this from the correct directory")
        sys.exit(1)

    harness = CodeReviewHarness()

    try:
        # Run appropriate review method
        if args.file:
            results = [harness.review_file(args.file, args.type)]
        elif args.directory:
            results = harness.review_directory(
                args.directory, args.type, args.extensions, args.max_files
            )
        elif args.batch:
            results = harness.batch_review(args.batch, args.type)

        # Generate and output report
        report = harness.generate_report(results, args.output)

        if not args.output:
            print("\n" + "=" * 60)
            print("📋 CODE REVIEW REPORT")
            print("=" * 60)
            print(report)

        # Summary statistics
        successful = sum(1 for r in results if r["success"])
        total = len(results)
        print(
            f"\n🎉 Review completed: {successful}/{total} files successfully analyzed"
        )

    except KeyboardInterrupt:
        print("\n⏹️ Review interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

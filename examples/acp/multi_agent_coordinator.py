#!/usr/bin/env python3
"""
Multi-Agent Coordination System using OpenCode ACP

This demonstrates advanced patterns for coordinating multiple AI agents using ACP clients.
Each agent has specialized roles and they collaborate on complex tasks.

Features:
- Parallel agent execution with different specializations
- Task delegation and coordination
- Shared context management
- Result aggregation and synthesis
- Error handling and recovery

Usage:
    python multi_agent_coordinator.py --task "analyze_project" --project src/
    python multi_agent_coordinator.py --task "documentation" --files "*.py"
    python multi_agent_coordinator.py --task "code_review" --directory app/
"""

import argparse
import asyncio
import concurrent.futures
import json
import logging
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any
import threading

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class AgentTask:
    """Represents a task for a specialized agent"""

    agent_id: str
    role: str
    prompt: str
    files: List[str] = None
    priority: int = 1
    timeout: int = 120
    dependencies: List[str] = None


@dataclass
class AgentResult:
    """Result from an agent execution"""

    agent_id: str
    task_id: str
    success: bool
    output: str = ""
    error: str = ""
    execution_time: float = 0.0
    tokens_used: int = 0


class SpecializedAgent:
    """Represents a specialized AI agent with specific capabilities"""

    def __init__(
        self,
        agent_id: str,
        role: str,
        system_prompt: str,
        acp_client_path: str = "advanced_acp_client.py",
    ):
        self.agent_id = agent_id
        self.role = role
        self.system_prompt = system_prompt
        self.acp_client_path = acp_client_path

    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute a task using this agent's specialization"""
        start_time = time.time()

        try:
            logger.info(f"🤖 [{self.agent_id}] Starting task: {task.prompt[:50]}...")

            # Combine system prompt with task prompt
            full_prompt = f"""
{self.system_prompt}

Task: {task.prompt}
"""

            # Execute using ACP client
            result = await asyncio.create_subprocess_exec(
                "python",
                self.acp_client_path,
                "--prompt",
                full_prompt,
                "--timeout",
                str(task.timeout),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await result.communicate()
            execution_time = time.time() - start_time

            if result.returncode == 0:
                logger.info(
                    f"✅ [{self.agent_id}] Task completed in {execution_time:.1f}s"
                )
                return AgentResult(
                    agent_id=self.agent_id,
                    task_id=task.agent_id,
                    success=True,
                    output=stdout.decode(),
                    execution_time=execution_time,
                )
            else:
                logger.error(f"❌ [{self.agent_id}] Task failed: {stderr.decode()}")
                return AgentResult(
                    agent_id=self.agent_id,
                    task_id=task.agent_id,
                    success=False,
                    error=stderr.decode(),
                    execution_time=execution_time,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"❌ [{self.agent_id}] Exception: {e}")
            return AgentResult(
                agent_id=self.agent_id,
                task_id=task.agent_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
            )


class MultiAgentCoordinator:
    """Coordinates multiple specialized agents for complex tasks"""

    def __init__(self):
        self.agents: Dict[str, SpecializedAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.results: List[AgentResult] = []
        self.shared_context = {}

        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize specialized agents"""

        # Code Analysis Specialist
        self.agents["code_analyzer"] = SpecializedAgent(
            agent_id="code_analyzer",
            role="Code Analysis Specialist",
            system_prompt="""
You are a Code Analysis Specialist. Your expertise includes:
- Static code analysis and quality assessment
- Architecture and design pattern evaluation  
- Performance bottleneck identification
- Dependency analysis and technical debt assessment

Provide detailed technical analysis with specific recommendations.
Focus on code structure, maintainability, and technical excellence.
""",
        )

        # Security Specialist
        self.agents["security_expert"] = SpecializedAgent(
            agent_id="security_expert",
            role="Security Expert",
            system_prompt="""
You are a Security Expert specializing in application security. Your focus areas:
- Vulnerability assessment and penetration testing perspective
- Secure coding practices and OWASP compliance
- Authentication, authorization, and data protection
- Security architecture and threat modeling

Identify security risks, provide mitigation strategies, and ensure secure coding practices.
Rate all findings by severity (Critical/High/Medium/Low).
""",
        )

        # Documentation Specialist
        self.agents["doc_specialist"] = SpecializedAgent(
            agent_id="doc_specialist",
            role="Documentation Specialist",
            system_prompt="""
You are a Documentation Specialist focused on creating clear, comprehensive documentation. Your expertise:
- API documentation and technical writing
- Code documentation and inline comments
- User guides and developer onboarding materials
- Documentation architecture and organization

Create well-structured, accessible documentation that serves both technical and non-technical audiences.
""",
        )

        # Performance Specialist
        self.agents["performance_expert"] = SpecializedAgent(
            agent_id="performance_expert",
            role="Performance Expert",
            system_prompt="""
You are a Performance Expert specializing in system optimization. Your areas of expertise:
- Performance profiling and bottleneck identification
- Database query optimization and caching strategies  
- Memory management and resource utilization
- Scalability analysis and load testing recommendations

Provide specific performance improvements with measurable impact estimates.
""",
        )

        # Integration Specialist (Coordinator)
        self.agents["coordinator"] = SpecializedAgent(
            agent_id="coordinator",
            role="Integration Coordinator",
            system_prompt="""
You are an Integration Coordinator responsible for synthesizing findings from multiple specialists. Your role:
- Aggregate and prioritize findings from different expert perspectives
- Resolve conflicts between recommendations from different specialists
- Create comprehensive, actionable reports and roadmaps
- Balance trade-offs between security, performance, maintainability, and documentation

Provide executive summaries and prioritized action plans based on multi-expert analysis.
""",
        )

    async def execute_project_analysis(self, project_path: str) -> Dict[str, Any]:
        """Coordinate multiple agents to analyze a software project"""

        logger.info(f"🚀 Starting multi-agent project analysis: {project_path}")

        # Phase 1: Parallel specialist analysis
        tasks = [
            AgentTask(
                agent_id="task_1",
                role="code_analysis",
                prompt=f"Perform comprehensive code analysis of the project at {project_path}. Focus on architecture, code quality, design patterns, and maintainability.",
                timeout=180,
            ),
            AgentTask(
                agent_id="task_2",
                role="security_analysis",
                prompt=f"Conduct security assessment of the project at {project_path}. Identify vulnerabilities, security risks, and compliance issues.",
                timeout=180,
            ),
            AgentTask(
                agent_id="task_3",
                role="performance_analysis",
                prompt=f"Analyze performance characteristics of the project at {project_path}. Identify bottlenecks and optimization opportunities.",
                timeout=180,
            ),
            AgentTask(
                agent_id="task_4",
                role="documentation_analysis",
                prompt=f"Evaluate documentation quality and coverage for the project at {project_path}. Suggest improvements for developer experience.",
                timeout=180,
            ),
        ]

        # Execute specialist tasks in parallel
        specialist_results = await self._execute_parallel_tasks(
            [
                (self.agents["code_analyzer"], tasks[0]),
                (self.agents["security_expert"], tasks[1]),
                (self.agents["performance_expert"], tasks[2]),
                (self.agents["doc_specialist"], tasks[3]),
            ]
        )

        # Phase 2: Coordinator synthesis
        synthesis_prompt = f"""
Based on the following specialist analyses, create a comprehensive project assessment:

CODE ANALYSIS FINDINGS:
{specialist_results[0].output if specialist_results[0].success else "Analysis failed: " + specialist_results[0].error}

SECURITY ASSESSMENT:
{specialist_results[1].output if specialist_results[1].success else "Analysis failed: " + specialist_results[1].error}

PERFORMANCE ANALYSIS:
{specialist_results[2].output if specialist_results[2].success else "Analysis failed: " + specialist_results[2].error}

DOCUMENTATION REVIEW:
{specialist_results[3].output if specialist_results[3].success else "Analysis failed: " + specialist_results[3].error}

Please provide:
1. **Executive Summary** - Key findings and overall project health
2. **Priority Issues** - Critical items requiring immediate attention
3. **Recommendations** - Specific actionable improvements 
4. **Implementation Roadmap** - Suggested order and timeline for improvements
5. **Risk Assessment** - Potential impacts of identified issues

Format as a comprehensive project report.
"""

        synthesis_task = AgentTask(
            agent_id="synthesis",
            role="coordination",
            prompt=synthesis_prompt,
            timeout=240,
        )

        coordinator_result = await self.agents["coordinator"].execute_task(
            synthesis_task
        )

        return {
            "project_path": project_path,
            "specialist_results": {
                "code_analysis": specialist_results[0],
                "security_analysis": specialist_results[1],
                "performance_analysis": specialist_results[2],
                "documentation_analysis": specialist_results[3],
            },
            "synthesis": coordinator_result,
            "execution_summary": {
                "total_agents": 5,
                "successful_tasks": sum(
                    1 for r in specialist_results + [coordinator_result] if r.success
                ),
                "total_execution_time": sum(
                    r.execution_time for r in specialist_results + [coordinator_result]
                ),
                "timestamp": time.time(),
            },
        }

    async def _execute_parallel_tasks(
        self, agent_task_pairs: List[tuple]
    ) -> List[AgentResult]:
        """Execute multiple agent tasks in parallel"""

        tasks = []
        for agent, task in agent_task_pairs:
            tasks.append(agent.execute_task(task))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                agent_id = agent_task_pairs[i][0].agent_id
                logger.error(f"❌ Exception in {agent_id}: {result}")
                processed_results.append(
                    AgentResult(
                        agent_id=agent_id,
                        task_id=f"task_{i}",
                        success=False,
                        error=str(result),
                    )
                )
            else:
                processed_results.append(result)

        return processed_results

    def generate_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate comprehensive multi-agent analysis report"""

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Multi-Agent Project Analysis Report

**Generated**: {timestamp}  
**Project**: {results["project_path"]}  
**Analysis Method**: Coordinated Multi-Agent System

## Execution Summary
- **Total Agents**: {results["execution_summary"]["total_agents"]}
- **Successful Tasks**: {results["execution_summary"]["successful_tasks"]}
- **Total Execution Time**: {results["execution_summary"]["total_execution_time"]:.1f} seconds

## Specialist Analysis Results

"""

        specialist_sections = {
            "code_analysis": "### 🔧 Code Analysis Specialist",
            "security_analysis": "### 🔒 Security Expert",
            "performance_analysis": "### ⚡ Performance Expert",
            "documentation_analysis": "### 📚 Documentation Specialist",
        }

        for key, section_title in specialist_sections.items():
            result = results["specialist_results"][key]
            report += f"{section_title}\n\n"

            if result.success:
                # Extract agent response from output
                output_lines = result.output.split("\n")
                agent_response = []
                capture = False

                for line in output_lines:
                    if "AGENT RESPONSE:" in line:
                        capture = True
                        continue
                    elif "✅ Response completed" in line:
                        break
                    elif capture and line.strip():
                        if not any(
                            marker in line
                            for marker in [
                                "🔧 [TOOL CALL]",
                                "⏳",
                                "✅",
                                "📋 Result:",
                                "============",
                            ]
                        ):
                            agent_response.append(line)

                if agent_response:
                    report += "\n".join(agent_response) + "\n\n"
                else:
                    report += "Analysis completed successfully.\n\n"
            else:
                report += f"**Analysis Failed**: {result.error}\n\n"

            report += (
                f"**Execution Time**: {result.execution_time:.1f} seconds\n\n---\n\n"
            )

        # Add coordinator synthesis
        report += "## 🎯 Coordinator Synthesis\n\n"

        if results["synthesis"].success:
            synthesis_lines = results["synthesis"].output.split("\n")
            synthesis_response = []
            capture = False

            for line in synthesis_lines:
                if "AGENT RESPONSE:" in line:
                    capture = True
                    continue
                elif "✅ Response completed" in line:
                    break
                elif capture and line.strip():
                    if not any(
                        marker in line
                        for marker in [
                            "🔧 [TOOL CALL]",
                            "⏳",
                            "✅",
                            "📋 Result:",
                            "============",
                        ]
                    ):
                        synthesis_response.append(line)

            if synthesis_response:
                report += "\n".join(synthesis_response) + "\n\n"
            else:
                report += "Synthesis completed successfully.\n\n"
        else:
            report += f"**Synthesis Failed**: {results['synthesis'].error}\n\n"

        if output_file:
            with open(output_file, "w") as f:
                f.write(report)
            logger.info(f"📄 Multi-agent report saved to: {output_file}")

        return report


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Multi-Agent Coordination System")

    parser.add_argument(
        "--task",
        choices=["analyze_project", "documentation", "code_review"],
        default="analyze_project",
        help="Type of coordinated task",
    )
    parser.add_argument("--project", "-p", help="Project directory to analyze")
    parser.add_argument("--files", nargs="+", help="Specific files to process")
    parser.add_argument("--directory", "-d", help="Directory to process")
    parser.add_argument("--output", "-o", help="Output report file")
    parser.add_argument("--agents", type=int, default=5, help="Number of agents to use")

    args = parser.parse_args()

    if not args.project and not args.directory:
        args.project = "."  # Default to current directory

    coordinator = MultiAgentCoordinator()

    try:
        project_path = args.project or args.directory

        logger.info(f"🎯 Initializing multi-agent coordination system")
        logger.info(f"📁 Target: {project_path}")
        logger.info(f"🤖 Agents: {len(coordinator.agents)}")

        # Execute coordinated analysis
        results = await coordinator.execute_project_analysis(project_path)

        # Generate report
        report = coordinator.generate_report(results, args.output)

        if not args.output:
            print("\n" + "=" * 80)
            print("📋 MULTI-AGENT ANALYSIS REPORT")
            print("=" * 80)
            print(report)

        # Summary statistics
        summary = results["execution_summary"]
        logger.info(f"🎉 Multi-agent analysis completed!")
        logger.info(
            f"✅ Success rate: {summary['successful_tasks']}/{summary['total_agents']}"
        )
        logger.info(f"⏱️ Total execution time: {summary['total_execution_time']:.1f}s")

    except KeyboardInterrupt:
        logger.info("⏹️ Multi-agent coordination interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error in coordination system: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

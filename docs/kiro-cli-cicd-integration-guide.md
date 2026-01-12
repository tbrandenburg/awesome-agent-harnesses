# Kiro-CLI CI/CD Integration Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Security Considerations](#security-considerations)
4. [GitHub Actions Examples](#github-actions-examples)
5. [GitLab CI Examples](#gitlab-ci-examples)
6. [Jenkins Pipeline Examples](#jenkins-pipeline-examples)
7. [Shell Script Patterns](#shell-script-patterns)
8. [Docker Integration](#docker-integration)
9. [Error Handling & Logging](#error-handling--logging)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## Overview

This guide demonstrates how to integrate kiro-cli into CI/CD pipelines for automated code review, documentation generation, error analysis, and development assistance.

## Prerequisites

### Installation in CI Environment
```bash
# Example installation script
curl -fsSL https://get.kiro.dev | sh
# Or using specific installation method for your CI environment
```

### Environment Setup
```bash
# Set up required environment variables
export KIRO_API_KEY="your-api-key"
export KIRO_MODEL="auto"  # or specific model
export KIRO_TRUST_LEVEL="selective"  # or "all" or "none"
```

## Security Considerations

### Trust Levels by Environment

#### Development Environment
```bash
# Full trust - convenient for development
--trust-all-tools
```

#### Staging Environment
```bash
# Selective trust - balanced approach
--trust-tools=fs_read,shell_safe,analysis
```

#### Production CI/CD
```bash
# Minimal trust - maximum security
--trust-tools=fs_read
# Or no trust for analysis-only operations
--trust-tools=
```

### Sensitive Data Protection
```bash
# Never include sensitive data in prompts
# Use environment variables for dynamic content
SANITIZED_ERROR=$(echo "$ERROR" | sed 's/password=[^&]*/password=****/g')
kiro-cli chat --no-interactive "Analyze this sanitized error: $SANITIZED_ERROR"
```

## GitHub Actions Examples

### Example 1: Code Review on Pull Requests
```yaml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install kiro-cli
        run: |
          curl -fsSL https://get.kiro.dev | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Get changed files
        id: changed-files
        run: |
          git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }} > changed_files.txt
          echo "files=$(cat changed_files.txt | tr '\n' ' ')" >> $GITHUB_OUTPUT

      - name: AI Code Review
        run: |
          REVIEW_RESULT=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
            "Review the following changed files for security issues, bugs, and code quality: ${{ steps.changed-files.outputs.files }}")
          
          # Save review to file for comment
          echo "## AI Code Review Results" > review_comment.md
          echo "" >> review_comment.md
          echo "$REVIEW_RESULT" >> review_comment.md

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const reviewComment = fs.readFileSync('review_comment.md', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: reviewComment
            });
```

### Example 2: Test Failure Analysis
```yaml
name: Test Analysis
on:
  workflow_run:
    workflows: ["Tests"]
    types: [completed]
    branches: [main]

jobs:
  analyze-failures:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install kiro-cli
        run: |
          curl -fsSL https://get.kiro.dev | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Download test results
        uses: actions/download-artifact@v3
        with:
          name: test-results
          run-id: ${{ github.event.workflow_run.id }}

      - name: Analyze test failures
        run: |
          if [ -f "test_output.log" ]; then
            ANALYSIS=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
              "Analyze these test failures and suggest fixes: $(cat test_output.log)")
            
            echo "## Test Failure Analysis" > analysis.md
            echo "$ANALYSIS" >> analysis.md
            
            # Create issue with analysis
            gh issue create \
              --title "Test Failures - $(date)" \
              --body-file analysis.md \
              --label "bug,automated"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Example 3: Documentation Generation
```yaml
name: Auto Documentation
on:
  push:
    branches: [main]
    paths: ['src/**', 'lib/**']

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install kiro-cli
        run: |
          curl -fsSL https://get.kiro.dev | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Generate API documentation
        run: |
          kiro-cli chat --no-interactive --trust-tools=fs_read,fs_write \
            "Generate comprehensive API documentation for all source files in the src/ directory. Create markdown files in the docs/ directory."

      - name: Commit documentation updates
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/
          if git diff --staged --quiet; then
            echo "No documentation changes"
          else
            git commit -m "Auto-update documentation [skip ci]"
            git push
          fi
```

## GitLab CI Examples

### Example 1: Security Audit Pipeline
```yaml
# .gitlab-ci.yml
stages:
  - security-audit
  - analysis

variables:
  KIRO_TRUST_LEVEL: "fs_read,analysis"

security-audit:
  stage: security-audit
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y curl
    - curl -fsSL https://get.kiro.dev | sh
    - export PATH="$HOME/.local/bin:$PATH"
  script:
    - |
      AUDIT_RESULT=$(kiro-cli chat --no-interactive --trust-tools=$KIRO_TRUST_LEVEL \
        "Perform a security audit of this codebase. Focus on authentication, authorization, input validation, and potential vulnerabilities.")
      
      echo "Security Audit Results:" > security_audit.txt
      echo "$AUDIT_RESULT" >> security_audit.txt
      
      # Check if critical issues found
      if echo "$AUDIT_RESULT" | grep -i "critical\|severe\|high risk"; then
        echo "Critical security issues found!"
        exit 1
      fi
  artifacts:
    reports:
      junit: security_audit.txt
    expire_in: 1 week
  only:
    - merge_requests
    - main

dependency-analysis:
  stage: analysis
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y curl
    - curl -fsSL https://get.kiro.dev | sh
    - export PATH="$HOME/.local/bin:$PATH"
  script:
    - |
      if [ -f "package.json" ] || [ -f "requirements.txt" ] || [ -f "Cargo.toml" ]; then
        DEP_ANALYSIS=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
          "Analyze the project dependencies for security vulnerabilities, outdated packages, and licensing issues.")
        
        echo "$DEP_ANALYSIS" > dependency_analysis.md
      fi
  artifacts:
    paths:
      - dependency_analysis.md
    expire_in: 1 week
```

### Example 2: Code Quality Gates
```yaml
code-quality-gate:
  stage: quality
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y curl jq
    - curl -fsSL https://get.kiro.dev | sh
    - export PATH="$HOME/.local/bin:$PATH"
  script:
    - |
      # Get changed files in MR
      CHANGED_FILES=$(git diff --name-only $CI_MERGE_REQUEST_TARGET_BRANCH_SHA $CI_COMMIT_SHA)
      
      # Quality analysis
      QUALITY_RESULT=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
        "Analyze code quality for these files: $CHANGED_FILES. Rate complexity, maintainability, and adherence to best practices. Provide a score out of 10.")
      
      # Extract score (assuming AI returns it in a parseable format)
      SCORE=$(echo "$QUALITY_RESULT" | grep -o "Score: [0-9]*" | grep -o "[0-9]*" || echo "0")
      
      if [ "$SCORE" -lt 7 ]; then
        echo "Code quality score ($SCORE/10) below threshold (7/10)"
        echo "$QUALITY_RESULT"
        exit 1
      fi
      
      echo "Code quality passed with score: $SCORE/10"
  only:
    - merge_requests
```

## Jenkins Pipeline Examples

### Example 1: Declarative Pipeline for Code Analysis
```groovy
pipeline {
    agent any
    
    environment {
        KIRO_TRUST_LEVEL = 'fs_read,analysis'
        PATH = "${env.HOME}/.local/bin:${env.PATH}"
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    if ! command -v kiro-cli &> /dev/null; then
                        curl -fsSL https://get.kiro.dev | sh
                    fi
                '''
            }
        }
        
        stage('Code Analysis') {
            parallel {
                stage('Security Review') {
                    steps {
                        script {
                            def securityResult = sh(
                                script: """
                                    kiro-cli chat --no-interactive --trust-tools=${KIRO_TRUST_LEVEL} \
                                    'Review this codebase for security vulnerabilities and provide a detailed report'
                                """,
                                returnStdout: true
                            ).trim()
                            
                            writeFile file: 'security-report.md', text: securityResult
                            
                            // Check for critical issues
                            if (securityResult.toLowerCase().contains('critical') || 
                                securityResult.toLowerCase().contains('severe')) {
                                error('Critical security issues found!')
                            }
                        }
                    }
                }
                
                stage('Performance Analysis') {
                    steps {
                        script {
                            def perfResult = sh(
                                script: """
                                    kiro-cli chat --no-interactive --trust-tools=${KIRO_TRUST_LEVEL} \
                                    'Analyze code for performance bottlenecks and optimization opportunities'
                                """,
                                returnStdout: true
                            ).trim()
                            
                            writeFile file: 'performance-report.md', text: perfResult
                        }
                    }
                }
            }
        }
        
        stage('Generate Summary') {
            steps {
                script {
                    def summaryResult = sh(
                        script: """
                            kiro-cli chat --no-interactive --trust-tools=fs_read \
                            'Create a summary report combining the security-report.md and performance-report.md files'
                        """,
                        returnStdout: true
                    ).trim()
                    
                    writeFile file: 'analysis-summary.md', text: summaryResult
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '*-report.md, analysis-summary.md', 
                            allowEmptyArchive: true
        }
        
        failure {
            script {
                def failureAnalysis = sh(
                    script: """
                        kiro-cli chat --no-interactive --trust-tools=fs_read \
                        'Analyze the Jenkins build failure and suggest fixes based on the console output'
                    """,
                    returnStdout: true
                ).trim()
                
                emailext subject: 'Build Failed - AI Analysis Available',
                         body: "Build failed. AI Analysis:\n\n${failureAnalysis}",
                         to: '${DEFAULT_RECIPIENTS}'
            }
        }
    }
}
```

### Example 2: Scripted Pipeline for Dynamic Analysis
```groovy
node {
    stage('Checkout') {
        checkout scm
    }
    
    stage('Install Kiro CLI') {
        sh '''
            if ! command -v kiro-cli &> /dev/null; then
                curl -fsSL https://get.kiro.dev | sh
                export PATH="$HOME/.local/bin:$PATH"
            fi
        '''
    }
    
    stage('Dynamic Code Analysis') {
        script {
            // Get list of modified files
            def changedFiles = sh(
                script: 'git diff --name-only HEAD~1 HEAD',
                returnStdout: true
            ).trim().split('\n')
            
            def analysisResults = [:]
            
            // Analyze each file type differently
            changedFiles.each { file ->
                if (file.endsWith('.py')) {
                    analysisResults[file] = analyzePythonFile(file)
                } else if (file.endsWith('.js') || file.endsWith('.ts')) {
                    analysisResults[file] = analyzeJavaScriptFile(file)
                } else if (file.endsWith('.java')) {
                    analysisResults[file] = analyzeJavaFile(file)
                }
            }
            
            // Combine results
            def combinedAnalysis = combineAnalysisResults(analysisResults)
            writeFile file: 'combined-analysis.json', text: groovy.json.JsonBuilder(combinedAnalysis).toPrettyString()
        }
    }
}

def analyzePythonFile(filename) {
    return sh(
        script: """
            kiro-cli chat --no-interactive --trust-tools=fs_read \
            'Analyze this Python file for PEP 8 compliance, security issues, and performance: ${filename}'
        """,
        returnStdout: true
    ).trim()
}

def analyzeJavaScriptFile(filename) {
    return sh(
        script: """
            kiro-cli chat --no-interactive --trust-tools=fs_read \
            'Analyze this JavaScript/TypeScript file for ESLint compliance, security, and modern best practices: ${filename}'
        """,
        returnStdout: true
    ).trim()
}

def analyzeJavaFile(filename) {
    return sh(
        script: """
            kiro-cli chat --no-interactive --trust-tools=fs_read \
            'Analyze this Java file for code quality, design patterns, and potential bugs: ${filename}'
        """,
        returnStdout: true
    ).trim()
}

def combineAnalysisResults(results) {
    def prompt = "Combine these individual file analysis results into a comprehensive project report: " + 
                 groovy.json.JsonBuilder(results).toString()
    
    return sh(
        script: """
            echo '${prompt}' | kiro-cli chat --no-interactive --trust-tools=
        """,
        returnStdout: true
    ).trim()
}
```

## Shell Script Patterns

### Pattern 1: Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

echo "Running AI-powered pre-commit checks..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo "No staged files to analyze."
    exit 0
fi

# Quick code quality check
QUALITY_CHECK=$(echo "Quick code quality check for these staged files: $STAGED_FILES" | \
    kiro-cli chat --no-interactive --trust-tools=fs_read)

# Check for blocking issues
if echo "$QUALITY_CHECK" | grep -i "error\|critical\|blocking"; then
    echo "❌ Pre-commit check failed:"
    echo "$QUALITY_CHECK"
    echo ""
    echo "Fix the issues above before committing."
    exit 1
fi

echo "✅ Pre-commit checks passed!"
echo "$QUALITY_CHECK"
```

### Pattern 2: Deployment Validation Script
```bash
#!/bin/bash
# deployment-validation.sh

set -e

ENVIRONMENT=${1:-staging}
DEPLOYMENT_LOG=${2:-deployment.log}

echo "🚀 Validating deployment to $ENVIRONMENT..."

# Validate configuration
CONFIG_VALIDATION=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
    "Validate the deployment configuration for $ENVIRONMENT environment. Check for common misconfigurations.")

echo "Configuration Validation:"
echo "$CONFIG_VALIDATION"

# Analyze deployment logs if available
if [ -f "$DEPLOYMENT_LOG" ]; then
    LOG_ANALYSIS=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
        "Analyze this deployment log for errors or warnings: $(tail -n 100 $DEPLOYMENT_LOG)")
    
    echo "Log Analysis:"
    echo "$LOG_ANALYSIS"
    
    # Check for deployment issues
    if echo "$LOG_ANALYSIS" | grep -i "error\|failed\|exception"; then
        echo "❌ Deployment issues detected!"
        exit 1
    fi
fi

echo "✅ Deployment validation completed successfully!"
```

### Pattern 3: Automated Incident Response
```bash
#!/bin/bash
# incident-response.sh

ALERT_MESSAGE="$1"
SEVERITY="$2"
LOG_FILE="$3"

echo "🚨 Processing incident: $SEVERITY"

# Initial triage
TRIAGE=$(echo "Triage this alert and suggest immediate actions: $ALERT_MESSAGE" | \
    kiro-cli chat --no-interactive --trust-tools=)

echo "AI Triage Results:"
echo "$TRIAGE"

# Log analysis if provided
if [ -f "$LOG_FILE" ]; then
    LOG_ANALYSIS=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
        "Analyze these logs in context of the alert '$ALERT_MESSAGE': $(tail -n 200 $LOG_FILE)")
    
    echo "Log Analysis:"
    echo "$LOG_ANALYSIS"
fi

# Generate incident report
INCIDENT_REPORT=$(kiro-cli chat --no-interactive --trust-tools= \
    "Generate a structured incident report template based on this triage: $TRIAGE")

echo "$INCIDENT_REPORT" > "incident-$(date +%Y%m%d-%H%M%S).md"

echo "📋 Incident report generated: incident-$(date +%Y%m%d-%H%M%S).md"
```

## Docker Integration

### Dockerfile for CI Environments
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install kiro-cli
RUN curl -fsSL https://get.kiro.dev | sh
ENV PATH="/root/.local/bin:${PATH}"

# Add CI scripts
COPY scripts/ /scripts/
RUN chmod +x /scripts/*.sh

# Set working directory
WORKDIR /workspace

# Default command
CMD ["bash"]
```

### Docker Compose for Development
```yaml
version: '3.8'

services:
  kiro-ci:
    build: .
    volumes:
      - .:/workspace
      - ./ci-cache:/cache
    environment:
      - KIRO_API_KEY=${KIRO_API_KEY}
      - KIRO_TRUST_LEVEL=fs_read,analysis
    command: /scripts/ci-analysis.sh

  kiro-security:
    build: .
    volumes:
      - .:/workspace:ro
    environment:
      - KIRO_API_KEY=${KIRO_API_KEY}
      - KIRO_TRUST_LEVEL=fs_read
    command: /scripts/security-scan.sh
```

### Multi-stage Analysis Container
```dockerfile
# Multi-stage analysis
FROM ubuntu:22.04 as base
RUN apt-get update && apt-get install -y curl git
RUN curl -fsSL https://get.kiro.dev | sh
ENV PATH="/root/.local/bin:${PATH}"

FROM base as security-scanner
COPY security-scan.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/security-scan.sh
CMD ["security-scan.sh"]

FROM base as code-reviewer
COPY code-review.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/code-review.sh
CMD ["code-review.sh"]

FROM base as doc-generator
COPY doc-gen.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/doc-gen.sh
CMD ["doc-gen.sh"]
```

## Error Handling & Logging

### Robust Error Handling Script
```bash
#!/bin/bash
# robust-kiro-wrapper.sh

set -euo pipefail

# Configuration
MAX_RETRIES=3
RETRY_DELAY=5
LOG_FILE="/tmp/kiro-ci.log"
TRUST_LEVEL="${KIRO_TRUST_LEVEL:-fs_read}"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$1] $2" | tee -a "$LOG_FILE"
}

# Retry function
retry_kiro_command() {
    local prompt="$1"
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log "INFO" "Attempting kiro-cli command (attempt $attempt/$MAX_RETRIES)"
        
        if result=$(kiro-cli chat --no-interactive --trust-tools="$TRUST_LEVEL" "$prompt" 2>&1); then
            log "SUCCESS" "Command succeeded on attempt $attempt"
            echo "$result"
            return 0
        else
            log "ERROR" "Attempt $attempt failed: $result"
            
            if [ $attempt -eq $MAX_RETRIES ]; then
                log "FATAL" "All retry attempts failed"
                return 1
            fi
            
            log "INFO" "Waiting $RETRY_DELAY seconds before retry..."
            sleep $RETRY_DELAY
            ((attempt++))
        fi
    done
}

# Sanitize input function
sanitize_prompt() {
    local prompt="$1"
    # Remove potential sensitive data patterns
    echo "$prompt" | \
        sed 's/password=[^[:space:]]*/password=****/gi' | \
        sed 's/api[_-]key=[^[:space:]]*/api_key=****/gi' | \
        sed 's/token=[^[:space:]]*/token=****/gi'
}

# Main execution
main() {
    local prompt="$1"
    local sanitized_prompt
    
    log "INFO" "Starting kiro-cli wrapper"
    
    # Sanitize the prompt
    sanitized_prompt=$(sanitize_prompt "$prompt")
    
    # Validate prompt length
    if [ ${#sanitized_prompt} -gt 10000 ]; then
        log "ERROR" "Prompt too long (${#sanitized_prompt} characters, max 10000)"
        exit 1
    fi
    
    # Execute with retry logic
    if retry_kiro_command "$sanitized_prompt"; then
        log "INFO" "Operation completed successfully"
        exit 0
    else
        log "ERROR" "Operation failed after all retries"
        exit 1
    fi
}

# Check if kiro-cli is installed
if ! command -v kiro-cli &> /dev/null; then
    log "ERROR" "kiro-cli not found. Please install it first."
    exit 1
fi

# Check if prompt provided
if [ $# -eq 0 ]; then
    log "ERROR" "Usage: $0 '<prompt>'"
    exit 1
fi

main "$1"
```

### Structured Logging with JSON Output
```bash
#!/bin/bash
# structured-kiro-logger.sh

# JSON logging function
json_log() {
    local level="$1"
    local message="$2"
    local extra="${3:-{}}"
    
    jq -n \
        --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --arg level "$level" \
        --arg message "$message" \
        --argjson extra "$extra" \
        '{
            timestamp: $timestamp,
            level: $level,
            message: $message,
            service: "kiro-ci",
            extra: $extra
        }'
}

# Execute kiro command with structured logging
execute_with_logging() {
    local prompt="$1"
    local start_time=$(date +%s)
    
    json_log "INFO" "Starting kiro-cli execution" "{\"prompt_length\": ${#prompt}}"
    
    if result=$(kiro-cli chat --no-interactive --trust-tools=fs_read "$prompt" 2>&1); then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        json_log "SUCCESS" "Command completed" "{
            \"duration_seconds\": $duration,
            \"result_length\": ${#result}
        }"
        
        echo "$result"
        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        json_log "ERROR" "Command failed" "{
            \"duration_seconds\": $duration,
            \"error\": \"$result\"
        }"
        
        return 1
    fi
}

# Usage
if [ $# -eq 0 ]; then
    json_log "ERROR" "No prompt provided"
    exit 1
fi

execute_with_logging "$1"
```

## Best Practices

### 1. Security Best Practices
```bash
# ✅ Good - Minimal necessary permissions
kiro-cli chat --no-interactive --trust-tools=fs_read "Analyze code"

# ❌ Avoid - Unnecessary broad permissions  
kiro-cli chat --no-interactive --trust-all-tools "Analyze code"

# ✅ Good - Sanitize inputs
SANITIZED_INPUT=$(echo "$USER_INPUT" | sed 's/[^a-zA-Z0-9 ._-]//g')
kiro-cli chat --no-interactive "Analyze: $SANITIZED_INPUT"

# ❌ Avoid - Direct user input
kiro-cli chat --no-interactive "$USER_INPUT"
```

### 2. Performance Best Practices
```bash
# ✅ Good - Batch related operations
COMBINED_PROMPT="Analyze these files and provide a summary: file1.py file2.js file3.java"
kiro-cli chat --no-interactive --trust-tools=fs_read "$COMBINED_PROMPT"

# ❌ Avoid - Multiple separate calls
kiro-cli chat --no-interactive --trust-tools=fs_read "Analyze file1.py"
kiro-cli chat --no-interactive --trust-tools=fs_read "Analyze file2.js"  
kiro-cli chat --no-interactive --trust-tools=fs_read "Analyze file3.java"

# ✅ Good - Cache results when appropriate
CACHE_FILE="/tmp/kiro-analysis-$(md5sum <<< "$FILES" | cut -d' ' -f1).cache"
if [ -f "$CACHE_FILE" ] && [ "$(find "$CACHE_FILE" -mmin -60)" ]; then
    cat "$CACHE_FILE"
else
    kiro-cli chat --no-interactive --trust-tools=fs_read "$PROMPT" | tee "$CACHE_FILE"
fi
```

### 3. Error Recovery Patterns
```bash
# Progressive fallback strategy
analyze_with_fallback() {
    local files="$1"
    
    # Try with file access first
    if result=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
        "Analyze these files: $files" 2>/dev/null); then
        echo "$result"
        return 0
    fi
    
    # Fallback to description-based analysis
    if result=$(kiro-cli chat --no-interactive --trust-tools= \
        "Provide general analysis guidelines for files: $files" 2>/dev/null); then
        echo "FALLBACK ANALYSIS: $result"
        return 0
    fi
    
    # Final fallback
    echo "ANALYSIS UNAVAILABLE: Unable to analyze $files"
    return 1
}
```

### 4. Session Management Patterns
```bash
# Clean session management
cleanup_old_sessions() {
    local max_sessions=10
    local session_count
    
    session_count=$(kiro-cli chat --list-sessions | grep "Chat SessionId:" | wc -l)
    
    if [ "$session_count" -gt "$max_sessions" ]; then
        echo "Cleaning up old sessions (current: $session_count, max: $max_sessions)"
        
        # Delete sessions older than 24 hours
        kiro-cli chat --list-sessions | \
            grep "Chat SessionId:" | \
            # Parse and delete old sessions (implementation depends on output format)
            head -n -"$max_sessions" | \
            while read -r line; do
                session_id=$(echo "$line" | grep -o '[0-9a-f-]\{36\}')
                kiro-cli chat --delete-session "$session_id" 2>/dev/null || true
            done
    fi
}

# Call before important operations
cleanup_old_sessions
```

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Tool approval required" Error
```bash
# Problem: Command fails with tool approval required
# Solution: Add appropriate trust flags

# Before (fails):
kiro-cli chat --no-interactive "Create a file"

# After (works):
kiro-cli chat --no-interactive --trust-tools=fs_write "Create a file"
```

#### Issue 2: Rate Limiting / Credit Exhaustion
```bash
# Implement rate limiting and credit checking
check_credits() {
    # This is a placeholder - actual implementation depends on kiro-cli output
    local usage_info
    usage_info=$(kiro-cli chat --no-interactive "What's my usage?" 2>&1 || echo "")
    
    if echo "$usage_info" | grep -i "limit\|exhausted\|quota"; then
        echo "WARNING: Approaching rate limits"
        return 1
    fi
    return 0
}

# Use before expensive operations
if ! check_credits; then
    echo "Skipping AI analysis due to rate limits"
    exit 0
fi
```

#### Issue 3: Large Output Truncation
```bash
# Handle large outputs properly
handle_large_output() {
    local prompt="$1"
    local output_file="${2:-/tmp/kiro_output.txt}"
    
    # Use smaller, focused prompts for large codebases
    if result=$(kiro-cli chat --no-interactive --trust-tools=fs_read \
        "Provide a concise summary of: $prompt" 2>&1); then
        echo "$result" > "$output_file"
        
        # Check if output was truncated
        if echo "$result" | tail -n 5 | grep -q "truncated\|limit"; then
            echo "WARNING: Output may be truncated. Consider breaking down the request."
        fi
        
        cat "$output_file"
    fi
}
```

#### Issue 4: Network Connectivity Issues
```bash
# Network resilience
check_connectivity() {
    if ! curl -s --max-time 10 https://api.kiro.dev/health &>/dev/null; then
        echo "ERROR: Cannot reach kiro API"
        return 1
    fi
    return 0
}

# Offline fallback
analyze_with_fallback() {
    if check_connectivity; then
        kiro-cli chat --no-interactive "$1"
    else
        echo "OFFLINE MODE: Cannot perform AI analysis. Running static checks..."
        # Implement static analysis fallback
        run_static_analysis "$1"
    fi
}
```

### Debugging Techniques

#### Enable Verbose Logging
```bash
# Use verbose flags for debugging
kiro-cli chat --no-interactive --verbose --verbose "$PROMPT" 2>&1 | tee debug.log

# Or set environment variables
export KIRO_DEBUG=1
export KIRO_LOG_LEVEL=debug
kiro-cli chat --no-interactive "$PROMPT"
```

#### Output Analysis
```bash
# Capture both stdout and stderr
analyze_output() {
    local prompt="$1"
    local stdout_file="/tmp/kiro_stdout.txt"
    local stderr_file="/tmp/kiro_stderr.txt"
    
    kiro-cli chat --no-interactive --trust-tools=fs_read "$prompt" \
        > "$stdout_file" 2> "$stderr_file"
    
    local exit_code=$?
    
    echo "Exit code: $exit_code"
    echo "STDOUT length: $(wc -c < "$stdout_file")"
    echo "STDERR length: $(wc -c < "$stderr_file")"
    
    if [ $exit_code -ne 0 ]; then
        echo "ERROR OUTPUT:"
        cat "$stderr_file"
    fi
    
    cat "$stdout_file"
    return $exit_code
}
```

This comprehensive guide provides everything needed to successfully integrate kiro-cli into CI/CD pipelines across different platforms and use cases. Remember to always start with minimal trust permissions and gradually increase as needed for your specific use case.
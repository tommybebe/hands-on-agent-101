# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google Agent Development Kit (ADK) project for building AI agents with Google Gemini models. The repository contains multiple example agents demonstrating different capabilities: basic hello world, tool usage, and MCP (Model Context Protocol) integrations.

## Development Environment Setup

### Dependencies
- Python 3.12+
- uv (package manager)
- Google ADK (`google-adk>=1.2.1`)
- python-dotenv for environment variables

### Environment Setup
1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Create virtual environment: `uv venv && source .venv/bin/activate`
3. Install dependencies: `uv add google-adk python-dotenv`
4. Copy `.env.example` to `.env` and configure API keys

### Running Agents
- Basic execution: `python hello.py`
- Individual agents: `python 01-hello_world/agent.py`, `python 02-tools/agent.py`, etc.
- Web interface: `adk web` (mentioned in main README)

## Code Architecture

### Agent Structure
All agents follow the Google ADK pattern:
- **Agent Identity**: name, model (typically "gemini-2.0-flash"), description
- **Instructions**: Behavior guidelines and rules
- **Tools**: Optional function decorators or external tool integrations
- **Sub-agents**: Hierarchical agent composition (see 03-mcp-tools)

### Directory Organization
- `01-hello_world/`: Basic agent with no tools
- `02-tools/`: Agent with custom Python function tools (@tool decorator pattern)
- `03-mcp-tools/`: Advanced agent with MCP integrations (Jira/Confluence)
- `search_agent/`: Web search specialist using built-in SearchTool
- Root level: Entry points and configuration

### Tool Development Patterns
1. **Function Tools**: Use `@tool` decorator for Python functions
2. **Built-in Tools**: Import from `google.adk.tools` (e.g., SearchTool)
3. **MCP Integration**: Use MCPToolset with StdioServerParameters for external services

### Environment Variables
Required in `.env`:
- `GOOGLE_API_KEY`: Google AI Studio API key
- `JIRA_URL`, `JIRA_USER_NAME`, `JIRA_TOKEN`: For MCP Atlassian integration

## Key Implementation Notes

- All agents use `dotenv.load_dotenv()` for environment variable loading
- Model specifications: "gemini-2.0-flash" or "gemini-2.5-flash" 
- Agent instructions should be specific and actionable
- Tool functions require proper docstrings with Args/Returns documentation
- MCP tools require external binaries (e.g., `uvx mcp-atlassian`)
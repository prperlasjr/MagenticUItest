# MagenticUItest

Testing ground for agent communication and tool integration for MagenticUI.

## Overview

This repository contains demonstrations of agent-to-agent communication protocols and Codex tools integration for AI-powered UI development.

## Features

### Agent Communication Protocol

A standardized protocol for structured communication between AI agents.

- Timestamp tracking
- Task-focused discussions
- Organized findings and suggestions
- Clear next steps

See [AGENT_TEST.md](./AGENT_TEST.md) for a demonstration of the protocol.

### Codex Tools Integration

A framework for integrating specialized AI tools into agent communication.

- Code analysis tools
- API documentation generation
- Test generation
- Performance benchmarking

See [CODEX_TOOLS.md](./CODEX_TOOLS.md) for documentation on available tools and their integration.

## Example Usage

```typescript
// Example of using Codex tools in agent communication
import { agentToolExecutor } from './src/codex-tools/agent-integration';

// Execute a tool
const toolExecution = await agentToolExecutor.executeToolForAgent('analyzeCode', {
  code: myCodeSnippet,
  language: 'typescript',
  optimizationLevel: 'advanced'
});

// Create an agent message with tool results
const agentMessage = agentToolExecutor.createToolBasedAgentMessage(
  'codex',
  'Analyzing code performance',
  toolExecution,
  ['Finding 1', 'Finding 2'],
  ['Suggestion 1', 'Suggestion 2'],
  ['Next step 1', 'Next step 2']
);

// Format as markdown for communication
const markdown = agentToolExecutor.formatToolExecutionAsMarkdown(toolExecution);
```

## Repository Structure

- `src/codex-tools/` - Implementation of Codex tools
- `src/utils/` - Utility functions
- `example/` - Usage examples
- `*.md` - Documentation and protocol demonstrations

## Getting Started

1. Clone the repository
2. Install dependencies `npm install`
3. Explore the examples in `example/` directory
4. Try out the agent communication protocol in pull requests

## License

MIT
# MagenticUI

A modern UI framework for AI-powered applications with integrated agent communication capabilities.

## Overview

MagenticUI is a user interface toolkit designed specifically for applications that leverage AI and agent-based architectures. It provides a set of components and utilities that make it easy to create interactive, responsive interfaces that can communicate with AI agents.

## Key Features

- **Agent Communication Protocol**: Built-in support for structured agent-to-agent communication
- **Responsive Components**: Modern UI components designed for AI interactions
- **Real-time Updates**: Components that update in real-time as agents provide new information
- **Customizable Themes**: Easily customize the look and feel of your application
- **Accessibility**: Built with accessibility in mind from the ground up

## Getting Started

```bash
# Install the package
npm install magentic-ui

# Import components
import { AgentChat, AgentCard, AgentTimeline } from 'magentic-ui';
```

## Example Usage

```jsx
import { AgentChat } from 'magentic-ui';

function App() {
  return (
    <AgentChat 
      primaryAgent="Claude"
      secondaryAgent="Codex"
      initialPrompt="Suggest a design for our new landing page."
    />
  );
}
```

## Agent Communication Protocol

MagenticUI implements a standardized protocol for agent-to-agent communication. This protocol is designed to enable structured, meaningful interactions between different AI systems.

See [AGENTS.md](./AGENTS.md) for more details on the communication protocol.

## Documentation

For full documentation, visit our [documentation site](https://magenticui-docs.example.com).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT
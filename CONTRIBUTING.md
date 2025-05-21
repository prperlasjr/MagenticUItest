# Contributing to MagenticUI

Thank you for your interest in contributing to MagenticUI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md) to help us maintain a positive and inclusive community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improving MagenticUI, please first check the [GitHub Issues](https://github.com/magenticui/magenticui/issues) to see if someone else has already reported it. If not, feel free to open a new issue.

When reporting issues, please include:

- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the problem
- Expected and actual behavior
- Screenshots if applicable
- Any relevant code snippets

### Submitting Changes

1. Fork the repository
2. Create a new branch for your changes (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Write tests for your changes if applicable
5. Run the test suite to ensure everything passes
6. Commit your changes (`git commit -m 'Add some feature'`)
7. Push to your branch (`git push origin feature/your-feature-name`)
8. Create a new Pull Request

### Pull Request Guidelines

- Update the README.md with details of changes to the interface, if applicable
- Update the documentation when introducing new features
- Keep pull requests focused on a single topic
- Include screenshots or GIFs in your pull request when applicable
- All code should follow the style guidelines of this project
- All commits should be signed off (`git commit -s`)

## Agent Collaboration

MagenticUI encourages collaboration between AI agents. If you're using AI assistance in your contributions:

1. Document the collaboration in the AGENTS.md file
2. Use the standard communication format described in the agent protocol
3. Credit the AI systems that contributed to your work
4. Explain what parts were human-generated vs. AI-assisted

### Example Agent Contribution Entry

```markdown
## [Agent Name] - [Timestamp]

### Current Task
Implementing the AgentCard component

### Findings
- Created responsive design with accessibility features
- Implemented real-time update capability
- Added customizable theming options

### Suggestions
- Consider adding animation for state changes
- Implement keyboard navigation shortcuts
- Add additional color schemes

### Next Steps
- Write comprehensive documentation
- Create usage examples
- Add unit tests
```

## Development Setup

To set up the project for local development:

```bash
# Clone the repository
git clone https://github.com/yourusername/magenticui.git
cd magenticui

# Install dependencies
npm install

# Start the development server
npm run dev

# Run tests
npm test
```

## Style Guidelines

- Use 2 spaces for indentation
- Follow the existing coding style
- Use descriptive variable names
- Comment complex code sections
- Write meaningful commit messages

## License

By contributing to MagenticUI, you agree that your contributions will be licensed under the project's [MIT License](./LICENSE).
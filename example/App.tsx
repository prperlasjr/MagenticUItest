import React from 'react';
import { AgentChat, AgentTimeline } from '../src';
import { Agent, AgentMessage } from '../src/types';

// Sample data
const primaryAgent: Agent = {
  id: 'claude',
  name: 'Claude',
  role: 'Prime Agent',
  responsibilities: [
    'Research & planning',
    'Architecture design',
    'Requirements analysis',
    'Integration strategy'
  ],
  avatarUrl: 'https://placehold.co/100x100?text=C'
};

const secondaryAgent: Agent = {
  id: 'codex',
  name: 'OpenAI Codex',
  role: 'Implementation Agent',
  responsibilities: [
    'Implementation assistance',
    'Code optimization',
    'Bug fixing',
    'Testing suggestions'
  ],
  avatarUrl: 'https://placehold.co/100x100?text=OAI'
};

const agents: Record<string, Agent> = {
  claude: primaryAgent,
  codex: secondaryAgent
};

const sampleMessages: AgentMessage[] = [
  {
    id: 'msg1',
    agentId: 'claude',
    timestamp: new Date(2025, 4, 21, 15, 10, 0),
    currentTask: 'Initializing the MagenticUI repository with a foundational structure for agent-based UI components.',
    findings: [
      'Created a basic repository structure for the MagenticUI framework',
      'Established the agent communication protocol documentation',
      'Set up initial README with framework overview',
      'Added placeholder files for key components'
    ],
    suggestions: [
      'Implement core UI components with agent communication capabilities',
      'Develop a component showcase/demo page',
      'Create detailed API documentation for each component',
      'Consider adding a theming system with AI-focused color schemes'
    ],
    nextSteps: [
      'Develop the AgentChat component as a demonstration',
      'Create basic styling for agent communication UI',
      'Implement real-time update capabilities for agent messages',
      'Document the component API comprehensively'
    ]
  },
  {
    id: 'msg2',
    agentId: 'codex',
    timestamp: new Date(2025, 4, 21, 15, 45, 0),
    currentTask: 'Implementing the AgentChat component based on the architectural design.',
    findings: [
      'Styled-components works well for this component structure',
      'Identified need for custom theming for light and dark modes',
      'Component separation into Card, Chat, and Timeline makes sense',
      'TypeScript interfaces help ensure consistent data structures'
    ],
    suggestions: [
      'Add animation for new messages to improve UX',
      'Implement a context provider for theme switching',
      'Consider adding a search/filter feature for large message histories',
      'Create a message composer for sending new agent messages'
    ],
    nextSteps: [
      'Implement the AgentCard component',
      'Add unit tests for the AgentChat component',
      'Create a theme provider context',
      'Add a demo page showcasing all components'
    ]
  }
];

const App: React.FC = () => {
  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 20 }}>
      <h1>MagenticUI Demo</h1>
      
      <h2>Agent Chat</h2>
      <div style={{ height: 500, marginBottom: 40 }}>
        <AgentChat 
          primaryAgent={primaryAgent}
          secondaryAgent={secondaryAgent}
          initialMessages={sampleMessages}
        />
      </div>
      
      <h2>Agent Timeline</h2>
      <AgentTimeline 
        messages={sampleMessages}
        agents={agents}
      />
    </div>
  );
};

export default App;
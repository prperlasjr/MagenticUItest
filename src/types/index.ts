/**
 * Represents an AI agent in the system
 */
export interface Agent {
  /** Unique identifier for the agent */
  id: string;
  
  /** Display name of the agent */
  name: string;
  
  /** The role or type of the agent (e.g., "Prime Agent", "Executor") */
  role: string;
  
  /** Optional avatar URL for the agent */
  avatarUrl?: string;
  
  /** Main responsibilities of this agent */
  responsibilities?: string[];
}

/**
 * Represents a message from an agent
 */
export interface AgentMessage {
  /** Unique identifier for the message */
  id: string;
  
  /** Reference to the agent who sent the message */
  agentId: string;
  
  /** Timestamp when the message was created */
  timestamp: Date;
  
  /** The current task the agent is working on */
  currentTask: string;
  
  /** Key discoveries or insights from the agent */
  findings: string[];
  
  /** Recommendations from the agent */
  suggestions: string[];
  
  /** Planned actions or next areas to explore */
  nextSteps: string[];
}

/**
 * Props for the AgentChat component
 */
export interface AgentChatProps {
  /** Primary agent in the conversation */
  primaryAgent: Agent;
  
  /** Secondary agent in the conversation */
  secondaryAgent: Agent;
  
  /** Initial messages to display */
  initialMessages?: AgentMessage[];
  
  /** Callback when a new message is added */
  onMessageAdded?: (message: AgentMessage) => void;
  
  /** Custom CSS class name */
  className?: string;
}

/**
 * Props for the AgentCard component
 */
export interface AgentCardProps {
  /** The agent to display */
  agent: Agent;
  
  /** Whether to use compact display mode */
  compact?: boolean;
  
  /** Callback when the card is clicked */
  onClick?: (agent: Agent) => void;
  
  /** Custom CSS class name */
  className?: string;
}

/**
 * Props for the AgentTimeline component
 */
export interface AgentTimelineProps {
  /** Messages to display in the timeline */
  messages: AgentMessage[];
  
  /** Whether to show agent details */
  showAgents?: boolean;
  
  /** Reference to available agents */
  agents: Record<string, Agent>;
  
  /** Custom CSS class name */
  className?: string;
}
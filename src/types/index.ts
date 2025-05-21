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
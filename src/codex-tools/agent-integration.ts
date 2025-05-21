/**
 * Integration of Codex Tools with Agent Communication
 */

import codexTools, { Tool } from './index';
import { AgentMessage } from '../types';

/**
 * Result of a tool execution in agent communication
 */
export interface ToolExecutionResult {
  toolName: string;
  inputParams: Record<string, any>;
  result: any;
  timestamp: Date;
  executionTime: number;
}

/**
 * Extended agent message with tool execution information
 */
export interface ToolEnabledAgentMessage extends AgentMessage {
  toolExecutions?: ToolExecutionResult[];
}

/**
 * Agent tool executor service
 */
export class AgentToolExecutor {
  private executionHistory: ToolExecutionResult[] = [];
  
  constructor(private readonly tools = codexTools) {}
  
  /**
   * Executes a tool and formats the result for agent communication
   */
  async executeToolForAgent(
    toolName: string,
    params: Record<string, any>
  ): Promise<ToolExecutionResult> {
    const startTime = Date.now();
    
    try {
      const result = await this.tools.executeTool(toolName, params);
      const executionTime = Date.now() - startTime;
      
      const toolResult: ToolExecutionResult = {
        toolName,
        inputParams: params,
        result,
        timestamp: new Date(),
        executionTime
      };
      
      this.executionHistory.push(toolResult);
      return toolResult;
    } catch (error) {
      const executionTime = Date.now() - startTime;
      const toolResult: ToolExecutionResult = {
        toolName,
        inputParams: params,
        result: { error: error.message },
        timestamp: new Date(),
        executionTime
      };
      
      this.executionHistory.push(toolResult);
      return toolResult;
    }
  }
  
  /**
   * Creates an agent message with tool execution results
   */
  createToolBasedAgentMessage(
    agentId: string,
    currentTask: string,
    toolExecution: ToolExecutionResult,
    findings: string[],
    suggestions: string[],
    nextSteps: string[]
  ): ToolEnabledAgentMessage {
    return {
      id: `msg_${Date.now()}`,
      agentId,
      timestamp: new Date(),
      currentTask,
      findings,
      suggestions,
      nextSteps,
      toolExecutions: [toolExecution]
    };
  }
  
  /**
   * Gets the execution history
   */
  getExecutionHistory(): ToolExecutionResult[] {
    return [...this.executionHistory];
  }
  
  /**
   * Formats a tool execution result as markdown for agent communication
   */
  formatToolExecutionAsMarkdown(execution: ToolExecutionResult): string {
    const { toolName, inputParams, result, timestamp, executionTime } = execution;
    
    let markdown = `## Tool Execution: ${toolName}\n\n`;
    markdown += `**Timestamp:** ${timestamp.toISOString()}\n`;
    markdown += `**Execution Time:** ${executionTime}ms\n\n`;
    
    markdown += "### Input Parameters\n```json\n";
    markdown += JSON.stringify(inputParams, null, 2);
    markdown += "\n```\n\n";
    
    markdown += "### Results\n```json\n";
    markdown += JSON.stringify(result, null, 2);
    markdown += "\n```\n";
    
    return markdown;
  }
  
  /**
   * Gets available tools information
   */
  getAvailableTools(): Array<{ name: string; description: string }> {
    return this.tools.listTools();
  }
}

export default new AgentToolExecutor();
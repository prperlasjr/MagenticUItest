/**
 * Example of using Codex Tools in agent communication
 */

import codexTools from '../src/codex-tools';
import agentToolExecutor from '../src/codex-tools/agent-integration';
import { formatDatePST } from '../src/utils/dateUtils';

/**
 * Example of analyzing code with the analyzeCode tool
 */
async function exampleCodeAnalysis() {
  // Code to analyze
  const sampleCode = `
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n-1) + fibonacci(n-2);
}
  `;
  
  // Execute the tool
  const toolExecution = await agentToolExecutor.executeToolForAgent('analyzeCode', {
    code: sampleCode,
    language: 'javascript',
    optimizationLevel: 'advanced'
  });
  
  // Create agent message based on tool results
  const agentMessage = agentToolExecutor.createToolBasedAgentMessage(
    'codex',
    'Analyzing fibonacci function performance',
    toolExecution,
    [
      'Found recursive implementation with exponential time complexity',
      'Identified potential for significant optimization',
      'Current implementation will cause stack overflow for large inputs'
    ],
    [
      'Implement iterative solution with dynamic programming',
      'Use memoization to avoid redundant calculations',
      'Add parameter validation for negative inputs'
    ],
    [
      'Refactor the implementation to use recommended approach',
      'Add benchmarking tests to verify performance improvements',
      'Document the optimization in code comments'
    ]
  );
  
  // Format the message for display
  const timestamp = formatDatePST(new Date());
  
  console.log(`## OpenAI Codex - ${timestamp}\n`);
  console.log(`### Current Task\n${agentMessage.currentTask}\n`);
  console.log('### Tool Used\nanalyzeCode\n');
  console.log('### Tool Input\n```javascript');
  console.log(sampleCode);
  console.log('```\n');
  console.log('### Tool Results');
  console.log('```json');
  console.log(JSON.stringify(toolExecution.result, null, 2));
  console.log('```\n');
  console.log('### Findings');
  agentMessage.findings.forEach(finding => console.log(`- ${finding}`));
  console.log('\n### Suggestions');
  agentMessage.suggestions.forEach(suggestion => console.log(`- ${suggestion}`));
  console.log('\n### Next Steps');
  agentMessage.nextSteps.forEach(step => console.log(`- ${step}`));
  console.log('\n---');
}

/**
 * Run the example
 */
exampleCodeAnalysis().catch(console.error);
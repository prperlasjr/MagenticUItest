import React, { useState } from 'react';
import styled from 'styled-components';
import { AgentChatProps, AgentMessage } from '../../types';
import { AgentCard } from '../AgentCard';
import { formatDate } from '../../utils/dateUtils';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  height: 100%;
  min-height: 400px;
`;

const AgentsHeader = styled.div`
  display: flex;
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const MessageWrapper = styled.div<{ isSecondaryAgent: boolean }>`
  align-self: ${props => props.isSecondaryAgent ? 'flex-end' : 'flex-start'};
  max-width: 80%;
  min-width: 200px;
`;

const MessageBubble = styled.div<{ isSecondaryAgent: boolean }>`
  background-color: ${props => props.isSecondaryAgent ? '#e3f2fd' : '#f1f8e9'};
  border: 1px solid ${props => props.isSecondaryAgent ? '#bbdefb' : '#dcedc8'};
  border-radius: 8px;
  padding: 1rem;
`;

const MessageHeader = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-weight: 500;
`;

const AgentName = styled.span`
  color: #333;
`;

const Timestamp = styled.span`
  color: #777;
  font-size: 0.875rem;
`;

const Section = styled.div`
  margin-bottom: 0.75rem;
`;

const SectionTitle = styled.h4`
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #555;
`;

const SectionContent = styled.div`
  font-size: 0.875rem;
  color: #333;
`;

const List = styled.ul`
  margin: 0;
  padding-left: 1.25rem;
`;

const ListItem = styled.li`
  margin-bottom: 0.25rem;
`;

/**
 * AgentChat displays a conversation between two AI agents
 */
export const AgentChat: React.FC<AgentChatProps> = ({
  primaryAgent,
  secondaryAgent,
  initialMessages = [],
  onMessageAdded,
  className
}) => {
  const [messages, setMessages] = useState<AgentMessage[]>(initialMessages);

  // Helper to determine if a message is from the secondary agent
  const isSecondaryAgentMessage = (message: AgentMessage) => message.agentId === secondaryAgent.id;

  // Helper to get agent name from message
  const getAgentName = (message: AgentMessage) => {
    return message.agentId === primaryAgent.id ? primaryAgent.name : secondaryAgent.name;
  };

  return (
    <ChatContainer className={className}>
      <AgentsHeader>
        <AgentCard agent={primaryAgent} compact />
        <div style={{ flex: 1 }} />
        <AgentCard agent={secondaryAgent} compact />
      </AgentsHeader>

      <MessagesContainer>
        {messages.map(message => (
          <MessageWrapper 
            key={message.id} 
            isSecondaryAgent={isSecondaryAgentMessage(message)}
          >
            <MessageBubble isSecondaryAgent={isSecondaryAgentMessage(message)}>
              <MessageHeader>
                <AgentName>{getAgentName(message)}</AgentName>
                <Timestamp>{formatDate(message.timestamp)}</Timestamp>
              </MessageHeader>

              <Section>
                <SectionTitle>Current Task</SectionTitle>
                <SectionContent>{message.currentTask}</SectionContent>
              </Section>

              <Section>
                <SectionTitle>Findings</SectionTitle>
                <SectionContent>
                  <List>
                    {message.findings.map((finding, index) => (
                      <ListItem key={index}>{finding}</ListItem>
                    ))}
                  </List>
                </SectionContent>
              </Section>

              <Section>
                <SectionTitle>Suggestions</SectionTitle>
                <SectionContent>
                  <List>
                    {message.suggestions.map((suggestion, index) => (
                      <ListItem key={index}>{suggestion}</ListItem>
                    ))}
                  </List>
                </SectionContent>
              </Section>

              <Section>
                <SectionTitle>Next Steps</SectionTitle>
                <SectionContent>
                  <List>
                    {message.nextSteps.map((step, index) => (
                      <ListItem key={index}>{step}</ListItem>
                    ))}
                  </List>
                </SectionContent>
              </Section>
            </MessageBubble>
          </MessageWrapper>
        ))}
      </MessagesContainer>
    </ChatContainer>
  );
};

export default AgentChat;
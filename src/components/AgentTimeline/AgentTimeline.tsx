import React from 'react';
import styled from 'styled-components';
import { AgentTimelineProps } from '../../types';
import { formatDate } from '../../utils/dateUtils';

const TimelineContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1.5rem;
`;

const TimelineItem = styled.div`
  display: flex;
  position: relative;
  
  &:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 3rem;
    left: 1.5rem;
    width: 2px;
    height: calc(100% + 2rem);
    background-color: #e0e0e0;
  }
`;

const AgentAvatar = styled.div<{ url?: string }>`
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background-color: #e0e0e0;
  background-image: ${props => props.url ? `url(${props.url})` : 'none'};
  background-size: cover;
  background-position: center;
  position: relative;
  z-index: 1;
  flex-shrink: 0;
`;

const TimelineContent = styled.div`
  margin-left: 1.5rem;
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const TimelineHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
`;

const AgentInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const AgentName = styled.h3`
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
`;

const AgentRole = styled.div`
  font-size: 0.875rem;
  color: #666;
`;

const TimeStamp = styled.div`
  font-size: 0.875rem;
  color: #666;
`;

const TaskTitle = styled.h4`
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 500;
  color: #333;
`;

const Section = styled.div`
  margin-bottom: 1.25rem;
`;

const SectionTitle = styled.h5`
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 500;
  color: #444;
`;

const List = styled.ul`
  margin: 0;
  padding-left: 1.5rem;
`;

const ListItem = styled.li`
  margin-bottom: 0.5rem;
  color: #333;
`;

/**
 * AgentTimeline displays a chronological timeline of agent communications
 */
export const AgentTimeline: React.FC<AgentTimelineProps> = ({
  messages,
  agents,
  showAgents = true,
  className
}) => {
  // Sort messages by timestamp (newest first)
  const sortedMessages = [...messages].sort((a, b) => 
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );

  return (
    <TimelineContainer className={className}>
      {sortedMessages.map(message => {
        const agent = agents[message.agentId];
        
        return (
          <TimelineItem key={message.id}>
            {showAgents && <AgentAvatar url={agent.avatarUrl} />}
            
            <TimelineContent>
              <TimelineHeader>
                {showAgents && (
                  <AgentInfo>
                    <AgentName>{agent.name}</AgentName>
                    <AgentRole>{agent.role}</AgentRole>
                  </AgentInfo>
                )}
                <TimeStamp>{formatDate(message.timestamp)}</TimeStamp>
              </TimelineHeader>
              
              <TaskTitle>{message.currentTask}</TaskTitle>
              
              <Section>
                <SectionTitle>Findings</SectionTitle>
                <List>
                  {message.findings.map((finding, index) => (
                    <ListItem key={index}>{finding}</ListItem>
                  ))}
                </List>
              </Section>
              
              <Section>
                <SectionTitle>Suggestions</SectionTitle>
                <List>
                  {message.suggestions.map((suggestion, index) => (
                    <ListItem key={index}>{suggestion}</ListItem>
                  ))}
                </List>
              </Section>
              
              <Section>
                <SectionTitle>Next Steps</SectionTitle>
                <List>
                  {message.nextSteps.map((step, index) => (
                    <ListItem key={index}>{step}</ListItem>
                  ))}
                </List>
              </Section>
            </TimelineContent>
          </TimelineItem>
        );
      })}
    </TimelineContainer>
  );
};

export default AgentTimeline;
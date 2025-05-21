import React from 'react';
import styled from 'styled-components';
import { AgentCardProps } from '../../types';

const StyledCard = styled.div<{ compact?: boolean }>`
  display: flex;
  flex-direction: ${props => props.compact ? 'row' : 'column'};
  align-items: ${props => props.compact ? 'center' : 'flex-start'};
  padding: ${props => props.compact ? '0.75rem' : '1.5rem'};
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
`;

const Avatar = styled.div<{ url?: string }>`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #e0e0e0;
  background-image: ${props => props.url ? `url(${props.url})` : 'none'};
  background-size: cover;
  background-position: center;
  margin-bottom: 1rem;
  flex-shrink: 0;
`;

const Content = styled.div<{ compact?: boolean }>`
  margin-left: ${props => props.compact ? '1rem' : '0'};
  flex: 1;
`;

const Name = styled.h3`
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333333;
`;

const Role = styled.div`
  font-size: 0.875rem;
  color: #666666;
  margin-bottom: 0.5rem;
`;

const ResponsibilitiesList = styled.ul`
  margin: 0.5rem 0 0 0;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: #555555;
`;

const Responsibility = styled.li`
  margin-bottom: 0.25rem;
`;

/**
 * AgentCard displays information about an AI agent in a card format
 */
export const AgentCard: React.FC<AgentCardProps> = ({ 
  agent, 
  compact = false, 
  onClick, 
  className 
}) => {
  const handleClick = () => {
    if (onClick) onClick(agent);
  };

  return (
    <StyledCard 
      compact={compact} 
      onClick={handleClick} 
      className={className} 
      role="button" 
      tabIndex={0}
    >
      <Avatar url={agent.avatarUrl} />
      <Content compact={compact}>
        <Name>{agent.name}</Name>
        <Role>{agent.role}</Role>
        
        {!compact && agent.responsibilities && (
          <ResponsibilitiesList>
            {agent.responsibilities.map((responsibility, index) => (
              <Responsibility key={index}>{responsibility}</Responsibility>
            ))}
          </ResponsibilitiesList>
        )}
      </Content>
    </StyledCard>
  );
};

export default AgentCard;
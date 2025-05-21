# Curatrak Integration with MagenticUI

This file demonstrates the Curatrak workflow tracking functionality for MagenticUI with Azure AI Foundry's grok-3 model.

## Workflow Tracking Features

The Curatrak integration provides:

1. **Request tracking** - Every API call is tracked with a unique request ID
2. **Workflow monitoring** - Related requests are grouped into workflows
3. **Token usage analytics** - Track completion tokens, prompt tokens and total usage
4. **Request status tracking** - Monitor request starts, completions, and errors
5. **Real-time monitoring** - Command-line interface for monitoring active workflows

## Sample Implementation

```python
class CuratrakGrokClient:
    """Custom client with workflow tracking for Azure AI Foundry's grok-3 model."""
    
    async def chat_completions_create(self, messages, model=None, temperature=0.7, max_tokens=2048, **kwargs):
        """Create a chat completion with workflow tracking."""
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())
        
        # Log the start of the request
        self._log_workflow_event(
            event_type="request_start",
            request_id=request_id,
            metadata={
                "model": model or self.model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "message_count": len(messages)
            }
        )
        
        try:
            # Make the actual API request
            result = await super().chat_completions_create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Log the successful completion
            self._log_workflow_event(
                event_type="request_complete",
                request_id=request_id,
                metadata={
                    "status": "success",
                    "token_usage": result.get("usage", {}),
                    "finish_reason": result.get("choices", [{}])[0].get("finish_reason", "")
                }
            )
            
            return result
            
        except Exception as e:
            # Log any errors
            self._log_workflow_event(
                event_type="request_error",
                request_id=request_id,
                metadata={
                    "status": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            )
            raise
```

## Configuration

Configuration is provided via environment variables:

```bash
export CURATRAK_ENABLED=true
export CURATRAK_URL=https://curatrak-api.example.com
export CURATRAK_API_KEY=your-api-key-here
export CURATRAK_LOG_FILE=curatrak_workflows.log
export CURATRAK_MONITORING_ENABLED=true
```

## Monitoring System

The monitoring system provides real-time visibility into workflows:

```
=== Curatrak Workflow Status (2025-05-21T17:30:45) ===
Total workflows: 2
Active workflows: 1

Workflow: 3f4e2d1c-6b7a-5c8d-9e8f-0a1b2c3d4e5f
Requests: 3/5 completed
Last event: request_start at 2025-05-21T17:30:42
```

This allows tracking the progress and performance of all API calls in the system.

## Testing Purpose

This file is being added to test the PR functionality with Curatrak integration.
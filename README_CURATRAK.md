# Curatrak Integration for MagenticUI

This integration adds workflow tracking capabilities to MagenticUI for Azure AI Foundry's grok-3 model. The implementation extends the existing adapter and adds monitoring capabilities.

## Components

### 1. CuratrakGrokClient
The `CuratrakGrokClient` extends the base grok-3 adapter to add workflow tracking for all API calls:

```python
class CuratrakGrokClient(CustomGrokClient):
    async def chat_completions_create(self, messages, model=None, temperature=0.7, max_tokens=2048, **kwargs):
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())
        self.request_count += 1
        
        # Track the start of the request
        if self.curatrak_enabled:
            self._log_workflow_event(
                event_type="request_start",
                request_id=request_id,
                metadata={
                    "model": model or self.model,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "message_count": len(messages),
                    "request_number": self.request_count
                }
            )
        
        # Make API call and track results
        # ...
```

### 2. Monitoring System
The `CuratrakMonitor` provides real-time monitoring of workflow status:

```python
def _print_status(self):
    """Print the current status of all workflows."""
    now = datetime.datetime.now().isoformat()
    print(f"\n=== Curatrak Workflow Status ({now}) ===")
    
    print(f"Total workflows: {len(self.workflows)}")
    print(f"Active workflows: {len(self.active_workflows)}")
    
    # Print details for each active workflow
    for workflow_id in self.active_workflows:
        # ...
```

### 3. Verification Tool
The `verify_curatrak.py` script tests both grok-3 functionality and Curatrak workflow tracking:

```python
async def test_curatrak_client():
    """Test the Curatrak-integrated Grok client."""
    
    client = CuratrakGrokClient()
    
    # Use a specific workflow ID for testing
    test_workflow_id = str(uuid.uuid4())
    client.workflow_id = test_workflow_id
    
    # Make multiple API calls to test workflow tracking
    for i in range(3):
        response = await client.chat_completions_create(
            messages=[{"role": "user", "content": f"Test message {i+1}"}],
            temperature=0.7
        )
    
    # Verify workflow events are tracked in the log file
    # ...
```

### 4. Configuration
The `config_curatrak.yaml` file adds Curatrak integration to all MagenticUI clients:

```yaml
orchestrator_client:
  azure: true
  model: grok-3
  # ... other settings ...
  # Curatrak integration
  curatrak_enabled: true
  curatrak_url: "https://curatrak-api.example.com"
  curatrak_api_key: "[REDACTED]"
```

## Features

1. **Workflow Tracking**: All API calls are tracked with detailed metadata
2. **Request Lifecycle**: Complete tracking of request start, completion, and errors
3. **Token Usage**: Track token consumption for cost optimization
4. **Error Handling**: Improved error tracking and debugging
5. **Real-time Monitoring**: Command-line interface for tracking active workflows
6. **Non-invasive**: Can be enabled or disabled without affecting core functionality

## Usage

1. Set environment variables:
```bash
export CURATRAK_ENABLED=true
export CURATRAK_LOG_FILE=curatrak_workflows.log
export CURATRAK_MONITORING_ENABLED=true
```

2. Run MagenticUI with Curatrak integration:
```bash
./start_with_curatrak.sh
```

3. Verify the integration:
```bash
python verify_curatrak.py
```

## Implementation Notes

1. The `CuratrakGrokClient` extends the base client without modifying its core functionality
2. All API calls are tracked with unique workflow and request IDs
3. The monitoring system provides real-time visibility into active workflows
4. Configuration is flexible and can be customized through environment variables
5. The verification script ensures both grok-3 and Curatrak functionality are working correctly

This integration enables comprehensive workflow tracking for Azure AI Foundry's grok-3 model in MagenticUI.
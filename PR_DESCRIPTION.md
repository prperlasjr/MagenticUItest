# CuraTrak Integration for MagenticUI

## Overview

This pull request adds CuraTrak integration for Azure AI Foundry's grok-3 model in MagenticUI. The integration provides workflow tracking capabilities for API calls, allowing for monitoring and analysis of AI operations without exposing any sensitive API keys or endpoints.

## Files Added/Modified

1. **curatrak_grok_adapter.py**: Custom adapter that extends the existing grok adapter to add workflow tracking capabilities
2. **curatrak_monitor.py**: Monitoring system that tracks and analyzes workflow data in real-time
3. **verify_curatrak.py**: Verification script to test both grok-3 functionality and CuraTrak workflow tracking
4. **start_with_curatrak.sh**: Startup script for MagenticUI with CuraTrak integration
5. **config_curatrak.yaml**: Configuration file with CuraTrak-specific settings

## Features

### Workflow Tracking

- Generates unique workflow and request IDs for tracking purposes
- Logs API request start, completion, and error events
- Captures token usage and other metadata for analysis
- Uses a file-based logging system for simplicity

### Real-time Monitoring

- Provides a real-time view of active workflows
- Displays token usage statistics and request completion status
- Configurable monitoring interval
- Clean shutdown with proper process management

### Configuration

- Environment variable support for easy configuration:
  ```
  CURATRAK_ENABLED=true
  CURATRAK_URL=https://curatrak-api.example.com
  CURATRAK_API_KEY=your-api-key
  CURATRAK_LOG_FILE=curatrak_workflows.log
  CURATRAK_MONITORING_ENABLED=true
  ```

- Integration with all client types (orchestrator, web_surfer, coder, file_surfer)

## Usage Instructions

1. **Environment Setup**:
   ```bash
   # Set up environment variables (or use .env file)
   export CURATRAK_ENABLED=true
   export CURATRAK_URL=your-curatrak-url
   export CURATRAK_API_KEY=your-api-key
   export CURATRAK_LOG_FILE=curatrak_workflows.log
   export CURATRAK_MONITORING_ENABLED=true
   
   # Azure AI Foundry configuration
   export AZURE_AI_FOUNDRY_API_KEY=your-azure-api-key
   export AZURE_AI_FOUNDRY_ENDPOINT=your-azure-endpoint
   ```

2. **Start with CuraTrak Integration**:
   ```bash
   ./start_with_curatrak.sh
   ```

3. **Verify Integration**:
   ```bash
   python verify_curatrak.py
   ```

4. **Monitor Workflows Separately** (optional):
   ```bash
   python curatrak_monitor.py --log-file curatrak_workflows.log
   ```

## Implementation Details

### CuraTrak Adapter

The `CuratrakGrokClient` extends the base `CustomGrokClient` and adds workflow tracking capabilities:

```python
class CuratrakGrokClient(CustomGrokClient):
    def __init__(self, api_key=None, base_url=None, model=None):
        super().__init__(api_key, base_url, model)
        
        # Initialize CuraTrak-specific properties
        self.curatrak_enabled = CURATRAK_ENABLED
        self.curatrak_url = CURATRAK_URL
        self.curatrak_api_key = CURATRAK_API_KEY
        self.workflow_id = str(uuid.uuid4())
        self.request_count = 0
```

### Workflow Event Logging

Events are logged in a structured format:

```python
event_data = {
    "workflow_id": self.workflow_id,
    "request_id": request_id,
    "event_type": event_type,
    "timestamp": datetime.datetime.utcnow().isoformat(),
    "model": self.model,
    "metadata": metadata
}
```

### Monitoring System

The monitoring system processes the log file and tracks workflow status:

```python
def _process_log_file(self):
    if not os.path.exists(self.log_file):
        return
    
    with open(self.log_file, 'r') as f:
        for line in f:
            if line.strip().startswith("CURATRAK EVENT:"):
                # Extract and process the event
                json_str = line.strip().replace("CURATRAK EVENT:", "", 1).strip()
                event_data = json.loads(json_str)
                self._process_event(event_data)
```

## Security Considerations

- This implementation does not hardcode any API keys or sensitive endpoints
- All API keys are loaded from environment variables
- Example URLs use placeholder domains (example.com)
- The actual API implementation is designed to be secure

## Future Enhancements

- Web dashboard for workflow visualization
- Advanced analytics with historical data
- Integration with external monitoring systems
- Per-user workflow tracking
- Distributed workflow tracking across multiple instances

## Testing

The implementation has been tested with:
- Azure AI Foundry's grok-3 model
- Multiple concurrent workflows
- Error handling scenarios
- Process termination and cleanup
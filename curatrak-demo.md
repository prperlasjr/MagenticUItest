# Curatrak Integration Demo

This file demonstrates the Curatrak integration for MagenticUI with Azure AI Foundry's grok-3 model.

## Workflow Tracking

```python
class CuratrakGrokClient(CustomGrokClient):
    """
    Custom client for Azure AI Foundry's grok-3 model with workflow tracking.
    """
    
    async def chat_completions_create(self, messages, model=None, temperature=0.7, max_tokens=2048, **kwargs):
        """
        Create a chat completion with Curatrak workflow tracking.
        """
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())
        self.request_count += 1
        
        # Track the start of the request if Curatrak is enabled
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
        
        try:
            # Make the actual API request
            result = await super().chat_completions_create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Track successful completion
            if self.curatrak_enabled:
                self._log_workflow_event(
                    event_type="request_complete",
                    request_id=request_id,
                    metadata={
                        "status": "success",
                        "token_usage": result.get("usage", {}),
                        "completion_id": result.get("id", ""),
                        "finish_reason": result.get("choices", [{}])[0].get("finish_reason", "")
                    }
                )
            
            return result
            
        except Exception as e:
            # Track errors
            if self.curatrak_enabled:
                self._log_workflow_event(
                    event_type="request_error",
                    request_id=request_id,
                    metadata={
                        "status": "error",
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                )
            
            # Re-raise the exception
            raise
```

## Monitoring System

```python
class CuratrakMonitor:
    """Monitor and analyze Curatrak workflows."""
    
    def __init__(self, log_file=None):
        self.log_file = log_file or CURATRAK_LOG_FILE
        self.workflows = defaultdict(list)
        self.active_workflows = set()
    
    def start_monitoring(self, interval=5):
        """Start monitoring workflows at the specified interval (in seconds)."""
        print(f"Starting Curatrak workflow monitoring...")
        print(f"Log file: {self.log_file}")
        
        try:
            # Create log file if it doesn't exist
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    f.write("# Curatrak Workflow Log\n")
            
            while True:
                self._process_log_file()
                self._print_status()
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    
    def _print_status(self):
        """Print the current status of all workflows."""
        now = datetime.datetime.now().isoformat()
        print(f"\n=== Curatrak Workflow Status ({now}) ===")
        
        if not self.workflows:
            print("No workflows detected yet.")
            return
        
        print(f"Total workflows: {len(self.workflows)}")
        print(f"Active workflows: {len(self.active_workflows)}")
```

## Configuration (YAML)

```yaml
# MagenticUI Configuration with Curatrak integration
orchestrator_client:
  azure: true
  model: grok-3
  api_key: "${AZURE_AI_FOUNDRY_API_KEY}"
  api_base: "${AZURE_AI_FOUNDRY_ENDPOINT}"
  api_version: "${AZURE_OPENAI_API_VERSION}"
  deployment: "${AZURE_AI_FOUNDRY_MODEL}"
  temperature: 0.7
  # Curatrak integration
  curatrak_enabled: "${CURATRAK_ENABLED}"
  curatrak_url: "${CURATRAK_URL}"
  curatrak_api_key: "${CURATRAK_API_KEY}"
```

## Startup Script

```bash
#!/bin/bash
# Start MagenticUI with Curatrak integration

# Set up Curatrak configuration
export CURATRAK_ENABLED="true"
export CURATRAK_URL="https://curatrak-api.example.com"
export CURATRAK_API_KEY="your-api-key-here"
export CURATRAK_LOG_FILE="curatrak_workflows.log"
export CURATRAK_MONITORING_ENABLED="true"

# Set up the custom LLM configuration to use our adapter
export MAGENTIC_CUSTOM_LLM_CONFIG=curatrak_grok_adapter.create_client
export MAGENTIC_CONFIG_PATH=$(pwd)/config_curatrak.yaml

# Start the Curatrak monitor in background if enabled
if [[ "$CURATRAK_MONITORING_ENABLED" == "true" ]]; then
    echo "Starting Curatrak workflow monitor..."
    python curatrak_monitor.py --log-file "$CURATRAK_LOG_FILE" &
    MONITOR_PID=$!
    
    # Setup trap to kill the monitor on script exit
    trap 'echo "Stopping Curatrak monitor..."; kill $MONITOR_PID' EXIT
fi

# Start the MagenticUI server
echo "Starting MagenticUI server..."
python run_server.py
```

## Verification Script

```python
async def test_curatrak_client():
    """Test the Curatrak-integrated Grok client."""
    print("\n=== Testing Curatrak Integration ===")
    
    client = CuratrakGrokClient(AZURE_API_KEY, AZURE_ENDPOINT)
    
    # Use a specific workflow ID for testing
    test_workflow_id = str(uuid.uuid4())
    client.workflow_id = test_workflow_id
    print(f"Test workflow ID: {test_workflow_id}")
    
    try:
        # Make multiple API calls to test workflow tracking
        for i in range(3):
            print(f"\nMaking test request {i+1}/3...")
            response = await client.chat_completions_create(
                messages=[{"role": "user", "content": f"Test message {i+1}: What can you tell me about workflow tracking?"}],
                temperature=0.7
            )
        
        # Check the log file for workflow events
        print("\n=== Checking Curatrak Log File ===")
        events_count = 0
        workflow_events = []
        
        with open(CURATRAK_LOG_FILE, 'r') as f:
            for line in f:
                if line.strip().startswith("CURATRAK EVENT:"):
                    # Extract the JSON part
                    json_str = line.strip().replace("CURATRAK EVENT:", "", 1).strip()
                    try:
                        event_data = json.loads(json_str)
                        if event_data.get("workflow_id") == test_workflow_id:
                            workflow_events.append(event_data)
                            events_count += 1
                    except json.JSONDecodeError:
                        continue
        
        print(f"Found {events_count} events for workflow ID: {test_workflow_id}")
    except Exception as e:
        print(f"\n❌ Curatrak Client Test: FAILED - {e}")
        return False
```
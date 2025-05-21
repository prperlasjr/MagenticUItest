# Add Curatrak Integration for Azure AI Foundry's grok-3 Model

## Summary
- Added CuratrakGrokClient for grok-3 with workflow tracking capabilities
- Implemented monitoring system to analyze API calls in real-time
- Created configuration for seamless integration with MagenticUI
- Added verification script to test functionality
- Added start script with Curatrak integration enabled

## Features

### Workflow Tracking
The CuratrakGrokClient extends the base CustomGrokClient and adds:
- Unique workflow and request IDs for each session
- Tracking for request starts, completions, and errors
- Detailed metadata collection (tokens, models, parameters)
- Timestamp-based event logging

### Monitoring System
The curatrak_monitor.py provides:
- Real-time monitoring of active workflows
- Request tracking and completion status
- Token usage analytics
- Organized output of workflow events

### Configuration
The config_curatrak.yaml:
- Configures all MagenticUI clients with Curatrak integration
- Uses environment variables for flexible configuration
- Maintains compatibility with base grok-3 functionality

### Verification
The verify_curatrak.py script:
- Tests base grok-3 functionality
- Verifies workflow tracking system
- Validates event logging functionality
- Provides comprehensive test output

## Usage
To use the Curatrak integration:

1. Set up environment variables:
   ```bash
   export CURATRAK_ENABLED=true
   export CURATRAK_LOG_FILE=curatrak_workflows.log
   ```

2. Run MagenticUI with the Curatrak integration:
   ```bash
   ./start_with_curatrak.sh
   ```

3. Verify the integration:
   ```bash
   ./verify_curatrak.py
   ```

## Test Plan
1. Run the verification script to ensure compatibility with grok-3
2. Test workflow tracking with multiple requests
3. Monitor active workflows in real-time
4. Validate that events are properly logged and analyzed

## Next Steps
- Connect to a production Curatrak API endpoint
- Add visualization for workflow analytics
- Extend monitoring with more detailed metrics
- Implement additional tracking dimensions (user, session, etc.)
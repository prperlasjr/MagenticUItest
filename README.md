# Curatrak Integration for MagenticUI

This extension adds workflow tracking and monitoring capabilities to MagenticUI when using Azure AI Foundry's grok-3 model.

## Overview

The Curatrak integration provides:

1. **Workflow Tracking**: Track all API calls made to grok-3 with unique workflow IDs
2. **Request Monitoring**: Monitor start, completion, and error events for each request
3. **Usage Analytics**: Collect token usage and other metrics for analysis
4. **Real-time Monitoring**: Monitor active workflows in real-time

## Components

- **CuratrakGrokClient**: Extended client for Azure AI Foundry's grok-3 model
- **curatrak_monitor.py**: Real-time monitoring tool for tracking workflows
- **config_curatrak.yaml**: Configuration template for MagenticUI
- **verify_curatrak.py**: Testing script to verify integration
- **start_with_curatrak.sh**: Starter script with Curatrak enabled

## Getting Started

1. Install dependencies:
   ```bash
   pip install dotenv requests
   ```

2. Set up environment variables:
   ```bash
   export CURATRAK_ENABLED=true
   export CURATRAK_LOG_FILE=curatrak_workflows.log
   export MAGENTIC_CUSTOM_LLM_CONFIG=curatrak_grok_adapter.create_client
   ```

3. Run the start script:
   ```bash
   ./start_with_curatrak.sh
   ```

4. Verify the installation:
   ```bash
   ./verify_curatrak.py
   ```

## Configuration Options

The following environment variables can be configured:

- `CURATRAK_ENABLED`: Enable/disable Curatrak tracking (default: true)
- `CURATRAK_URL`: URL for Curatrak API (default: placeholder URL)
- `CURATRAK_LOG_FILE`: Path to log file (default: curatrak_workflows.log)
- `CURATRAK_MONITORING_ENABLED`: Enable/disable real-time monitoring (default: true)

See `config_curatrak.yaml` for additional configuration options.

## For More Information

See [PR_DESCRIPTION.md](PR_DESCRIPTION.md) for detailed documentation on the integration.

## License

MIT
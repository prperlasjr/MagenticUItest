#!/bin/bash
# Start MagenticUI with Curatrak integration and workflow monitoring

# Stop on errors
set -e

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
fi

# Set up Curatrak configuration if not already set
export CURATRAK_ENABLED=${CURATRAK_ENABLED:-"true"}
export CURATRAK_URL=${CURATRAK_URL:-"https://placeholder-curatrak-api.example.com"}
export CURATRAK_LOG_FILE=${CURATRAK_LOG_FILE:-"curatrak_workflows.log"}
export CURATRAK_MONITORING_ENABLED=${CURATRAK_MONITORING_ENABLED:-"true"}

# Set up the custom LLM configuration to use our adapter
export MAGENTIC_CUSTOM_LLM_CONFIG=curatrak_grok_adapter.create_client
export MAGENTIC_CONFIG_PATH=$(pwd)/config_curatrak.yaml

# Print configuration
echo "=== Starting MagenticUI with Curatrak Integration ==="
echo "Curatrak Enabled: $CURATRAK_ENABLED"
echo "Custom LLM Config: $MAGENTIC_CUSTOM_LLM_CONFIG"
echo "Config Path: $MAGENTIC_CONFIG_PATH"
echo "Log File: $CURATRAK_LOG_FILE"
echo "Monitoring Enabled: $CURATRAK_MONITORING_ENABLED"

# Start the Curatrak monitor in background if enabled
if [[ "$CURATRAK_MONITORING_ENABLED" == "true" ]]; then
    echo "Starting Curatrak workflow monitor..."
    python curatrak_monitor.py --log-file "$CURATRAK_LOG_FILE" &
    MONITOR_PID=$!
    echo "Monitor started with PID: $MONITOR_PID"
    
    # Save the monitor PID for later cleanup
    echo "$MONITOR_PID" > .curatrak_monitor.pid
    
    # Setup trap to kill the monitor on script exit
    trap 'echo "Stopping Curatrak monitor..."; kill $MONITOR_PID 2>/dev/null || true; rm -f .curatrak_monitor.pid' EXIT
fi

# Start the MagenticUI server
echo "Starting MagenticUI server..."
python run_server.py

# Note: The trap will handle stopping the monitor when this script exits
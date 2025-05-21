#!/bin/bash
# Start MagenticUI with Curatrak integration and workflow monitoring
# Note: This is a demonstration script with API keys removed for security

# Stop on errors
set -e

# Set up Curatrak configuration
export CURATRAK_ENABLED="true"
export CURATRAK_URL="https://curatrak-api.example.com"
export CURATRAK_API_KEY="[REDACTED]" # Replace with your actual API key
export CURATRAK_LOG_FILE="curatrak_workflows.log"
export CURATRAK_MONITORING_ENABLED="true"

# Set up the custom LLM configuration to use our adapter
export MAGENTIC_CUSTOM_LLM_CONFIG=curatrak_grok_adapter_clean.create_client
export MAGENTIC_CONFIG_PATH=$(pwd)/config_curatrak_clean.yaml

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
    python curatrak_monitor_clean.py --log-file "$CURATRAK_LOG_FILE" &
    MONITOR_PID=$!
    echo "Monitor started with PID: $MONITOR_PID"
    
    # Save the monitor PID for later cleanup
    echo "$MONITOR_PID" > .curatrak_monitor.pid
    
    # Setup trap to kill the monitor on script exit
    trap 'echo "Stopping Curatrak monitor..."; kill $MONITOR_PID 2>/dev/null || true; rm -f .curatrak_monitor.pid' EXIT
fi

# Start the MagenticUI server (commented out for demonstration)
echo "Starting MagenticUI server..."
echo "This is a demonstration script. In a real environment, this would start the server."
# python run_server.py  # Actual server start is commented out

# For demonstration purposes, we'll just sleep for a few seconds
echo "Simulating server running..."
sleep 5
echo "Demonstration complete. In a real environment, the server would continue running."

# Note: The trap will handle stopping the monitor when this script exits
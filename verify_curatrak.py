#!/usr/bin/env python3
"""
Script to verify the Curatrak integration with Azure AI Foundry's grok-3 model.
This script tests both the grok-3 functionality and the Curatrak workflow tracking.
"""

import os
import json
import asyncio
import datetime
import uuid
from dotenv import load_dotenv

# Import our custom clients
from grok_adapter import CustomGrokClient
from curatrak_grok_adapter import CuratrakGrokClient

# Load environment variables
load_dotenv()

# Get the Azure AI Foundry configuration
AZURE_API_KEY = os.getenv("AZURE_AI_FOUNDRY_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT", "https://azureaiservicecura.services.ai.azure.com/models/chat/completions")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")

# Get Curatrak configuration
CURATRAK_LOG_FILE = os.getenv("CURATRAK_LOG_FILE", "curatrak_verification.log")

# Ensure log file exists
with open(CURATRAK_LOG_FILE, 'w') as f:
    f.write("# Curatrak Verification Log\n")

# Set up logging for verification
os.environ["CURATRAK_LOG_FILE"] = CURATRAK_LOG_FILE
os.environ["CURATRAK_ENABLED"] = "true"

async def test_grok_client():
    """Test the base Grok client functionality."""
    print("\n=== Testing Base Grok Client ===")
    
    client = CustomGrokClient(AZURE_API_KEY, AZURE_ENDPOINT)
    
    try:
        response = await client.chat_completions_create(
            messages=[{"role": "user", "content": "What model are you? Can you confirm you are grok-3?"}],
            temperature=0.7
        )
        
        print("\n=== Base Grok Client Response ===")
        
        # Print model response
        choices = response.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content = message.get("content", "No content")
            print("\nModel response:")
            print(content)
        
        # Print usage stats
        usage = response.get("usage", {})
        print("\nToken usage:")
        print(f"Prompt tokens: {usage.get('prompt_tokens', 'Unknown')}")
        print(f"Completion tokens: {usage.get('completion_tokens', 'Unknown')}")
        print(f"Total tokens: {usage.get('total_tokens', 'Unknown')}")
        
        print("\n✅ Base Grok Client Test: SUCCESS")
        return True
        
    except Exception as e:
        print(f"\n❌ Base Grok Client Test: FAILED - {e}")
        return False

async def test_curatrak_client():
    """Test the Curatrak-integrated Grok client."""
    print("\n=== Testing Curatrak Integration ===")
    
    client = CuratrakGrokClient(AZURE_API_KEY, AZURE_ENDPOINT)
    
    # Force enable Curatrak for this test
    client.curatrak_enabled = True
    
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
            
            # Print basic response info
            choices = response.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                content_preview = message.get("content", "")[:100] + "..." if len(message.get("content", "")) > 100 else message.get("content", "")
                print(f"Response: {content_preview}")
        
        print("\n✅ Curatrak Client Test: SUCCESS")
        
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
        
        # Verify we have both start and complete events
        start_events = [e for e in workflow_events if e.get("event_type") == "request_start"]
        complete_events = [e for e in workflow_events if e.get("event_type") == "request_complete"]
        
        print(f"Request start events: {len(start_events)}")
        print(f"Request complete events: {len(complete_events)}")
        
        if len(start_events) == 3 and len(complete_events) == 3:
            print("\n✅ Curatrak Workflow Tracking: SUCCESS")
            return True
        else:
            print("\n❌ Curatrak Workflow Tracking: INCOMPLETE - Not all events were tracked")
            return False
        
    except Exception as e:
        print(f"\n❌ Curatrak Client Test: FAILED - {e}")
        return False

async def run_verification():
    """Run the complete verification process."""
    print("=== Curatrak + Azure AI Foundry Grok-3 Verification ===")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print(f"Endpoint: {AZURE_ENDPOINT}")
    print(f"API Key: {AZURE_API_KEY[:5]}...{AZURE_API_KEY[-4:] if AZURE_API_KEY else ''}")
    print(f"Curatrak Log File: {CURATRAK_LOG_FILE}")
    
    # Test base Grok client
    grok_success = await test_grok_client()
    
    # Test Curatrak integration
    curatrak_success = await test_curatrak_client()
    
    # Print summary
    print("\n=== Verification Summary ===")
    print(f"Base Grok Client: {'✅ PASSED' if grok_success else '❌ FAILED'}")
    print(f"Curatrak Integration: {'✅ PASSED' if curatrak_success else '❌ FAILED'}")
    
    if grok_success and curatrak_success:
        print("\n🎉 VERIFICATION SUCCESSFUL: Curatrak integration with Azure AI Foundry's grok-3 is working correctly!")
    else:
        print("\n⚠️ VERIFICATION INCOMPLETE: Some tests failed. Please check the log for details.")

if __name__ == "__main__":
    asyncio.run(run_verification())
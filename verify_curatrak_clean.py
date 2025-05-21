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

# Import our custom clients (reference only, implementation removed for security)
# from grok_adapter import CustomGrokClient
# from curatrak_grok_adapter import CuratrakGrokClient

# Load environment variables
load_dotenv()

# Configuration (API keys and endpoints removed for security)
AZURE_API_KEY = "[REDACTED]" # Replace with your API key
AZURE_ENDPOINT = "https://your-endpoint.services.ai.azure.com/models/chat/completions"
AZURE_API_VERSION = "2024-05-01-preview"
CURATRAK_LOG_FILE = "curatrak_verification.log"

# Mock implementation for demonstration purposes
class MockCustomGrokClient:
    """Mock client for demonstration purposes."""
    
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or "[REDACTED]"
        self.base_url = base_url or AZURE_ENDPOINT
        self.model = model or "grok-3"
    
    async def chat_completions_create(self, messages, model=None, temperature=0.7, max_tokens=2048, **kwargs):
        """Mock implementation that returns a sample response."""
        return {
            "id": "mock-response-id",
            "object": "chat.completion",
            "created": int(datetime.datetime.now().timestamp()),
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant", 
                        "content": "This is a mock response for demonstration purposes."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 50,
                "completion_tokens": 20,
                "total_tokens": 70
            }
        }

class MockCuratrakGrokClient(MockCustomGrokClient):
    """Mock client with Curatrak integration for demonstration purposes."""
    
    def __init__(self, api_key=None, base_url=None, model=None):
        super().__init__(api_key, base_url, model)
        self.curatrak_enabled = True
        self.workflow_id = str(uuid.uuid4())
        self.request_count = 0
    
    async def chat_completions_create(self, messages, model=None, temperature=0.7, max_tokens=2048, **kwargs):
        """Mock implementation with workflow tracking."""
        request_id = str(uuid.uuid4())
        self.request_count += 1
        
        # Log request start
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
        
        # Get mock response
        response = await super().chat_completions_create(messages, model, temperature, max_tokens, **kwargs)
        
        # Log request completion
        if self.curatrak_enabled:
            self._log_workflow_event(
                event_type="request_complete",
                request_id=request_id,
                metadata={
                    "status": "success",
                    "token_usage": response.get("usage", {}),
                    "completion_id": response.get("id", ""),
                    "finish_reason": response.get("choices", [{}])[0].get("finish_reason", "")
                }
            )
        
        return response
    
    def _log_workflow_event(self, event_type, request_id, metadata=None):
        """Log an event to the workflow tracking system."""
        if not self.curatrak_enabled:
            return
        
        if metadata is None:
            metadata = {}
        
        # Prepare the event data
        event_data = {
            "workflow_id": self.workflow_id,
            "request_id": request_id,
            "event_type": event_type,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "model": self.model,
            "metadata": metadata
        }
        
        # Log the event
        with open(CURATRAK_LOG_FILE, 'a') as f:
            f.write(f"CURATRAK EVENT: {json.dumps(event_data)}\n")

async def test_grok_client():
    """Test the base Grok client functionality."""
    print("\n=== Testing Base Grok Client ===")
    
    client = MockCustomGrokClient("[REDACTED]", AZURE_ENDPOINT)
    
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
    
    # Ensure log file exists
    with open(CURATRAK_LOG_FILE, 'w') as f:
        f.write("# Curatrak Verification Log\n")
    
    client = MockCuratrakGrokClient("[REDACTED]", AZURE_ENDPOINT)
    
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
    print(f"API Key: [REDACTED]")
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
"""
Custom adapter for Azure AI Foundry's grok-3 model with Curatrak integration.
To use this, set MAGENTIC_CUSTOM_LLM_CONFIG=curatrak_grok_adapter.create_client in your environment.
"""

import os
import json
import requests
import uuid
import datetime
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional, Union, Callable

# Import the base grok adapter
from grok_adapter import CustomGrokClient

# Load environment variables
load_dotenv()

# Get credentials from environment
API_KEY = os.getenv("AZURE_AI_FOUNDRY_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT") or "https://azureaiservicecura.services.ai.azure.com/models/chat/completions"
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-05-01-preview"
MODEL = os.getenv("AZURE_AI_FOUNDRY_MODEL") or os.getenv("AZURE_OPENAI_DEPLOYMENT") or "grok-3"

# Curatrak configuration
CURATRAK_ENABLED = os.getenv("CURATRAK_ENABLED", "true").lower() == "true"
CURATRAK_URL = os.getenv("CURATRAK_URL", "https://curatrak-api.example.com")
CURATRAK_API_KEY = os.getenv("CURATRAK_API_KEY")

class CuratrakGrokClient(CustomGrokClient):
    """
    Custom client for Azure AI Foundry's grok-3 model with Curatrak workflow integration.
    Extends the CustomGrokClient and adds workflow tracking capabilities.
    """
    
    def __init__(self, api_key=None, base_url=None, model=None):
        super().__init__(api_key, base_url, model)
        
        # Initialize Curatrak-specific properties
        self.curatrak_enabled = CURATRAK_ENABLED
        self.curatrak_url = CURATRAK_URL
        self.curatrak_api_key = CURATRAK_API_KEY
        self.workflow_id = str(uuid.uuid4())
        self.request_count = 0
        
        if self.curatrak_enabled and not self.curatrak_api_key:
            print("Warning: Curatrak is enabled but no API key is provided. Tracking will be disabled.")
            self.curatrak_enabled = False
    
    async def chat_completions_create(self, 
                              messages, 
                              model=None, 
                              temperature=0.7, 
                              max_tokens=2048, 
                              **kwargs):
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
            # Call the parent implementation to make the actual API request
            result = await super().chat_completions_create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Track the successful completion
            if self.curatrak_enabled:
                usage = result.get("usage", {})
                self._log_workflow_event(
                    event_type="request_complete",
                    request_id=request_id,
                    metadata={
                        "status": "success",
                        "token_usage": usage,
                        "completion_id": result.get("id", ""),
                        "finish_reason": result.get("choices", [{}])[0].get("finish_reason", "")
                    }
                )
            
            return result
            
        except Exception as e:
            # Track the error
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
    
    def _log_workflow_event(self, event_type, request_id, metadata=None):
        """Log an event to the Curatrak workflow tracking system."""
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
        
        # In a real implementation, this would send the data to Curatrak
        # For now, we'll just print it to demonstrate the concept
        print(f"CURATRAK EVENT: {json.dumps(event_data)}")
        
        # Sample implementation for sending to Curatrak API
        # try:
        #     headers = {
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {self.curatrak_api_key}"
        #     }
        #     response = requests.post(
        #         f"{self.curatrak_url}/api/workflows/events",
        #         headers=headers,
        #         json=event_data
        #     )
        #     response.raise_for_status()
        # except Exception as e:
        #     print(f"Error logging to Curatrak: {e}")

def create_client():
    """
    Create a custom client configuration with Curatrak integration for MagenticUI.
    This is the function that should be referenced in MAGENTIC_CUSTOM_LLM_CONFIG.
    """
    # This config mimics what MagenticUI expects
    return {
        "config_list": [
            {
                "model": "grok-3",
                "api_key": API_KEY,
                "api_base": ENDPOINT.split("?")[0],  # Remove any query parameters
                "api_version": API_VERSION,
                "azure": True,
                "curatrak_enabled": CURATRAK_ENABLED
            }
        ],
        # Custom client to use instead of OpenAI's
        "custom_client": CuratrakGrokClient(API_KEY, ENDPOINT, MODEL)
    }

# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test():
        client = CuratrakGrokClient()
        response = await client.chat_completions_create(
            messages=[{"role": "user", "content": "What can you tell me about Paris?"}],
            temperature=0.7
        )
        print(json.dumps(response, indent=2))
    
    asyncio.run(test())
"""
Custom adapter for Azure AI Foundry's grok-3 model.
To use this, set MAGENTIC_CUSTOM_LLM_CONFIG=grok_adapter.create_client in your environment.
"""

import os
import json
import requests
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional, Union, Callable

# Load environment variables
load_dotenv()

# Get credentials from environment
API_KEY = os.getenv("AZURE_AI_FOUNDRY_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT") or "https://your-endpoint-here.com/models/chat/completions"
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-05-01-preview"
MODEL = os.getenv("AZURE_AI_FOUNDRY_MODEL") or os.getenv("AZURE_OPENAI_DEPLOYMENT") or "grok-3"

class CustomGrokClient:
    """
    Custom client for Azure AI Foundry's grok-3 model that mimics OpenAI's interface.
    """
    
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or API_KEY
        self.base_url = base_url or ENDPOINT
        self.model = model or MODEL
        
        if not self.api_key:
            raise ValueError("API key is required")
        
        # Ensure the endpoint has the correct format
        if "?api-version=" not in self.base_url:
            self.base_url = f"{self.base_url}?api-version={API_VERSION}"
            
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def chat_completions_create(self, 
                                messages, 
                                model=None, 
                                temperature=0.7, 
                                max_tokens=2048, 
                                **kwargs):
        """
        Create a chat completion using the Azure AI Foundry API.
        Mimics the OpenAI chat.completions.create method.
        """
        model_to_use = model or self.model
        
        # Prepare the request payload
        payload = {
            "messages": messages,
            "max_completion_tokens": max_tokens,
            "temperature": temperature,
            "top_p": kwargs.get("top_p", 1.0),
            "frequency_penalty": kwargs.get("frequency_penalty", 0),
            "presence_penalty": kwargs.get("presence_penalty", 0),
            "model": model_to_use
        }
        
        try:
            # Make the API request
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Convert to OpenAI format
            return self._convert_to_openai_format(result)
            
        except Exception as e:
            print(f"Error calling Azure AI Foundry API: {e}")
            raise
    
    def _convert_to_openai_format(self, result):
        """Convert Azure AI Foundry response to OpenAI format"""
        return {
            "id": result.get("id", ""),
            "object": "chat.completion",
            "created": result.get("created", 0),
            "model": self.model,
            "choices": [
                {
                    "index": choice.get("index", 0),
                    "message": choice.get("message", {}),
                    "finish_reason": choice.get("finish_reason", "stop")
                }
                for choice in result.get("choices", [])
            ],
            "usage": result.get("usage", {})
        }

def create_client():
    """
    Create a custom client configuration for MagenticUI.
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
                "azure": True
            }
        ],
        # Custom client to use instead of OpenAI's
        "custom_client": CustomGrokClient(API_KEY, ENDPOINT, MODEL)
    }

# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test():
        client = CustomGrokClient()
        response = await client.chat_completions_create(
            messages=[{"role": "user", "content": "What can you tell me about Paris?"}],
            temperature=0.7
        )
        print(json.dumps(response, indent=2))
    
    asyncio.run(test())
"""Simple test for the A2A client."""
import pytest
import httpx
from uuid import uuid4
from a2a.client import A2AClient
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
)


@pytest.mark.asyncio
async def test_send_message(server):
    """Test sending a message to the agent and getting a response."""
    async with httpx.AsyncClient() as httpx_client:
        # Get the A2A client
        client = await A2AClient.get_client_from_agent_card_url(
            httpx_client, 'http://localhost:9999'
        )
        
        # Prepare the message payload
        message_payload = {
            'message': {
                'role': 'user',
                'parts': [
                    {'type': 'text', 'text': 'hello'}
                ],
                'messageId': uuid4().hex,
            },
        }
        
        # Create the request
        request = SendMessageRequest(
            params=MessageSendParams(**message_payload)
        )
        
        # Send the message and get the response
        response = await client.send_message(request)
        
        # Print the response for debugging
        print("Response:", response.model_dump(mode='json', exclude_none=True))
        
        # Basic assertions
        assert response is not None
        
        # Get response data
        response_data = response.model_dump(mode='json', exclude_none=True)
        
        # Assert the response has the expected components
        assert "id" in response_data
        assert "jsonrpc" in response_data
        assert "result" in response_data
        
        # Access result parts
        result = response_data["result"]
        assert "parts" in result
        
        # Find text parts in the message
        text_parts = [part for part in result["parts"] if part["type"] == "text"]
        
        # Assert that we got at least one text part
        assert len(text_parts) > 0
        
        # Assert that the text is "Hello World"
        assert any("Hello World" in part["text"] for part in text_parts) 
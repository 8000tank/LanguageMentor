import pytest
from agents.conversation_agent import ConversationAgent

def test_conversation_agent_initialization():
    agent = ConversationAgent()
    assert agent is not None

def test_chat_with_history():
    agent = ConversationAgent()
    response = agent.chat_with_history("How are you?")
    assert isinstance(response, str)
    assert len(response) > 0 
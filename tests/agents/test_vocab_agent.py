import pytest
from agents.vocab_agent import VocabAgent

def test_vocab_agent_initialization():
    agent = VocabAgent()
    assert agent is not None

def test_restart_session():
    agent = VocabAgent()
    agent.restart_session()
    # 验证会话状态已重置

def test_chat_with_history():
    agent = VocabAgent()
    response = agent.chat_with_history("Let's start learning")
    assert isinstance(response, str)
    assert len(response) > 0 
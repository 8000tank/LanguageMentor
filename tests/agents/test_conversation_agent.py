import pytest
from unittest.mock import patch, Mock, mock_open
from agents.conversation_agent import ConversationAgent

MOCK_PROMPT = "conversation prompt"


@pytest.fixture
def agent():
    """创建一个会话代理实例"""
    with patch("builtins.open", mock_open(read_data=MOCK_PROMPT)):
        with patch("agents.agent_base.ChatOllama"):
            with patch("agents.agent_base.ChatPromptTemplate"):
                with patch("agents.agent_base.RunnableWithMessageHistory"):
                    return ConversationAgent()


def test_initialization(agent):
    """测试初始化"""
    assert agent.name == "conversation"
    assert agent.prompt == MOCK_PROMPT
    assert agent.session_id == "conversation"


def test_chat_with_history(agent):
    """测试聊天功能"""
    with patch.object(agent, "chat_with_history", wraps=agent.chat_with_history) as mock_chat:
        mock_chat.return_value = "AI response"
        response = agent.chat_with_history("hello")
        assert response == "AI response"
        # 验证调用参数，不检查 session_id
        mock_chat.assert_called_once()
        args, _ = mock_chat.call_args
        assert args[0] == "hello"


def test_chat_with_custom_session(agent):
    """测试带自定义会话ID的聊天"""
    with patch.object(agent, "chat_with_history", wraps=agent.chat_with_history) as mock_chat:
        mock_chat.return_value = "AI response"
        response = agent.chat_with_history("hello", session_id="custom_session")
        assert response == "AI response"
        mock_chat.assert_called_once_with("hello", session_id="custom_session")


def test_chat_without_session(agent):
    """测试不带会话ID的聊天"""
    with patch.object(agent, "chat_with_history", wraps=agent.chat_with_history) as mock_chat:
        mock_chat.return_value = "AI response"
        response = agent.chat_with_history("hello")
        assert response == "AI response"
        mock_chat.assert_called_once()
        args, kwargs = mock_chat.call_args
        assert args[0] == "hello"
        assert "session_id" not in kwargs or kwargs["session_id"] is None

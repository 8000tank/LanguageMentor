import pytest
from unittest.mock import patch, Mock, mock_open
from agents.vocab_agent import VocabAgent

MOCK_PROMPT = "vocab study prompt"

@pytest.fixture
def agent():
    """创建一个词汇学习代理实例"""
    with patch("builtins.open", mock_open(read_data=MOCK_PROMPT)):
        with patch("agents.agent_base.ChatOllama"):
            with patch("agents.agent_base.ChatPromptTemplate"):
                with patch("agents.agent_base.RunnableWithMessageHistory"):
                    return VocabAgent()

def test_initialization(agent):
    """测试初始化"""
    assert agent.name == "vocab_study"
    assert agent.prompt == MOCK_PROMPT
    assert agent.session_id == "vocab_study"

def test_restart_session(agent):
    """测试重启会话"""
    with patch("agents.vocab_agent.get_session_history") as mock_history:
        # 创建一个新的 Mock 对象作为历史记录
        history_mock = Mock()
        mock_history.return_value = history_mock
        
        # 调用重启会话方法
        result = agent.restart_session()
        
        # 验证 get_session_history 被调用，且使用了正确的 session_id
        mock_history.assert_called_once_with("vocab_study")
        # 验证 clear 方法被调用
        history_mock.clear.assert_called_once()
        # 验证返回值
        assert result == history_mock

def test_chat_with_history(agent):
    """测试聊天功能"""
    with patch.object(agent, "chat_with_history", wraps=agent.chat_with_history) as mock_chat:
        mock_chat.return_value = "AI response"
        response = agent.chat_with_history("hello")
        assert response == "AI response"
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
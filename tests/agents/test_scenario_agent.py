import pytest
from unittest.mock import patch, Mock, mock_open
from agents.scenario_agent import ScenarioAgent

MOCK_PROMPT = "scenario prompt"
MOCK_INTRO = '{"messages": ["Hello", "Welcome"]}'

@pytest.fixture
def agent():
    """创建一个场景代理实例"""
    with patch("builtins.open", mock_open(read_data=MOCK_PROMPT)):
        with patch("agents.scenario_agent.ScenarioAgent.load_intro", return_value=["Hello", "Welcome"]):
            with patch("agents.agent_base.ChatOllama"):
                with patch("agents.agent_base.ChatPromptTemplate"):
                    with patch("agents.agent_base.RunnableWithMessageHistory"):
                        return ScenarioAgent("test_scenario")

def test_initialization(agent):
    """测试初始化"""
    assert agent.name == "test_scenario"
    assert agent.prompt == MOCK_PROMPT

def test_start_new_session(agent):
    """测试开始新会话"""
    with patch("random.choice", return_value="Hello"):
        with patch("agents.session_history.get_session_history") as mock_history:
            mock_history.return_value.messages = []
            message = agent.start_new_session()
            assert message == "Hello"

def test_start_existing_session(agent):
    """测试已存在会话"""
    with patch("random.choice", return_value="Hello"):
        with patch("agents.session_history.get_session_history") as mock_history:
            # 模拟已存在的会话历史
            mock_history.return_value.messages = []
            message = agent.start_new_session()
            assert message == "Hello"  # 应该返回新选择的消息

def test_chat_with_history(agent):
    """测试聊天功能"""
    with patch.object(agent, "chat_with_history", wraps=agent.chat_with_history) as mock_chat:
        mock_chat.return_value = "AI response"
        response = agent.chat_with_history("hello")
        assert response == "AI response"
        mock_chat.assert_called_once()
        args, _ = mock_chat.call_args
        assert args[0] == "hello"

def test_start_session_with_custom_id(agent):
    """测试使用自定义会话ID"""
    with patch("random.choice", return_value="Hello"):
        with patch("agents.session_history.get_session_history") as mock_history:
            mock_history.return_value.messages = []
            message = agent.start_new_session(session_id="custom_session")
            assert message == "Hello"

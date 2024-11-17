import pytest
from unittest.mock import patch, Mock, mock_open
from agents.agent_base import AgentBase

# 创建一个具体的 AgentBase 子类用于测试


class TestAgent(AgentBase):
    """测试用的 AgentBase 子类"""

    def __init__(self, name="test", prompt_file="test.txt", intro_file=None, session_id=None):
        super().__init__(
            name=name,
            prompt_file=prompt_file,
            intro_file=intro_file,
            session_id=session_id
        )


@pytest.fixture
def mock_llm():
    """Mock LLM 相关组件"""
    with patch("agents.agent_base.ChatOllama") as mock_chat:
        with patch("agents.agent_base.ChatPromptTemplate") as mock_prompt:
            with patch("agents.agent_base.RunnableWithMessageHistory") as mock_runnable:
                mock_response = Mock()
                mock_response.content = "AI response"
                mock_runnable.return_value.invoke.return_value = mock_response
                yield mock_chat


@pytest.fixture
def mock_files(request):
    """Mock 文件操作"""
    files_content = {
        "test.txt": "test prompt content",
        "intro.json": '{"messages": ["hello", "hi"]}'
    }

    def mock_file_open(filename, *args, **kwargs):
        filename = str(filename)
        for key, content in files_content.items():
            if key in filename:
                return mock_open(read_data=content)(*args, **kwargs)
        return mock_open(read_data="")(*args, **kwargs)

    with patch("builtins.open", side_effect=mock_file_open):
        yield


def test_load_prompt(mock_files):
    """测试加载提示文件"""
    with patch("builtins.open", mock_open(read_data="test prompt content")) as mock_file:
        agent = TestAgent(prompt_file="test.txt")
        assert agent.prompt == "test prompt content"
        mock_file.assert_called_once_with("test.txt", "r", encoding="utf-8")


def test_load_intro(mock_files):
    """测试加载介绍文件"""
    agent = TestAgent(intro_file="intro.json")
    assert isinstance(agent.intro_messages, dict)
    assert "messages" in agent.intro_messages
    assert agent.intro_messages["messages"] == ["hello", "hi"]


def test_chat_with_history(mock_files, mock_llm):
    """测试聊天功能"""
    agent = TestAgent()
    response = agent.chat_with_history("hello")
    assert response == "AI response"


def test_initialization_without_intro(mock_files):
    """测试不带介绍文件的初始化"""
    agent = TestAgent()
    assert agent.intro_messages == []


def test_initialization_with_session_id(mock_files):
    """测试带会话ID的初始化"""
    session_id = "test_session"
    agent = TestAgent(session_id=session_id)
    assert agent.session_id == session_id


def test_initialization_without_session_id(mock_files):
    """测试不带会话ID的初始化"""
    agent = TestAgent()
    assert agent.session_id == agent.name


def test_file_not_found():
    """测试文件不存在的情况"""
    with pytest.raises(FileNotFoundError):
        TestAgent(prompt_file="nonexistent.txt")


def test_invalid_json():
    """测试无效的 JSON 文件"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(ValueError):
            TestAgent(intro_file="invalid.json")

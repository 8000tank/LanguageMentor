import pytest
from agents.scenario_agent import ScenarioAgent


def test_scenario_agent_initialization():
    agent = ScenarioAgent("job_interview")
    assert agent is not None


def test_start_new_session():
    agent = ScenarioAgent("hotel_checkin")
    initial_message = agent.start_new_session()
    assert isinstance(initial_message, str)
    assert len(initial_message) > 0


def test_chat_with_history():
    agent = ScenarioAgent("job_interview")
    response = agent.chat_with_history("Hello, I'm here for the interview")
    assert isinstance(response, str)
    assert len(response) > 0

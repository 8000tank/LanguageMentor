import pytest
from agents.session_history import get_session_history, store

def test_get_new_session():
    session_id = "test_session"
    history = get_session_history(session_id)
    assert session_id in store
    assert len(history.messages) == 0

def test_get_existing_session():
    session_id = "test_session"
    history1 = get_session_history(session_id)
    history2 = get_session_history(session_id)
    assert history1 is history2

def test_multiple_sessions():
    session1 = get_session_history("session1")
    session2 = get_session_history("session2")
    assert session1 is not session2 
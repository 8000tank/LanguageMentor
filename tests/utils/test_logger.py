import pytest
from utils.logger import LOG

def test_logger_initialization():
    assert LOG is not None

def test_logger_info():
    try:
        LOG.info("Test info message")
        assert True
    except Exception as e:
        assert False, f"Logger info failed: {str(e)}"

def test_logger_error():
    try:
        LOG.error("Test error message")
        assert True
    except Exception as e:
        assert False, f"Logger error failed: {str(e)}" 
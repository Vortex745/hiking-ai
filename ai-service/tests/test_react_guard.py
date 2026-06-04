"""Tests for agent.react_guard — stuck detection and repeat-call prevention."""

from __future__ import annotations

import pytest

from agent.react_guard import RepeatCallDetector, StuckDetector


# ---------------------------------------------------------------------------
# StuckDetector
# ---------------------------------------------------------------------------

class TestStuckDetector:
    """StuckDetector identifies when the ReAct loop is making no progress."""

    def test_no_history_is_not_stuck(self):
        detector = StuckDetector()
        assert detector.is_stuck() is False

    def test_single_observation_is_not_stuck(self):
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        assert detector.is_stuck() is False

    def test_different_observations_not_stuck(self):
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("route_research", "香山路线")
        assert detector.is_stuck() is False

    def test_repeated_same_observation_is_stuck(self):
        """If the same tool returns the same content 3 times, we're stuck."""
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        assert detector.is_stuck() is True

    def test_repeated_same_observation_two_times_not_stuck(self):
        """Two identical observations are not enough to declare stuck."""
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        assert detector.is_stuck() is False

    def test_repeated_assistant_content_is_stuck(self):
        """If the assistant generates the same text 3 times, we're stuck."""
        detector = StuckDetector()
        detector.record_assistant_content("今天适合徒步")
        detector.record_assistant_content("今天适合徒步")
        detector.record_assistant_content("今天适合徒步")
        assert detector.is_stuck() is True

    def test_mixed_repeated_signals_is_stuck(self):
        """If assistant repeats same text after same tool result, we're stuck."""
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_assistant_content("今天适合徒步")
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_assistant_content("今天适合徒步")
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_assistant_content("今天适合徒步")
        assert detector.is_stuck() is True

    def test_reset_clears_history(self):
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        assert detector.is_stuck() is True
        detector.reset()
        assert detector.is_stuck() is False

    def test_stuck_reason_returns_explanation(self):
        detector = StuckDetector()
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        detector.record_observation("weather_lookup", "晴，23°C")
        reason = detector.stuck_reason()
        assert "weather_lookup" in reason
        assert "重复" in reason


# ---------------------------------------------------------------------------
# RepeatCallDetector
# ---------------------------------------------------------------------------

class TestRepeatCallDetector:
    """RepeatCallDetector prevents the same tool+args from being called twice."""

    def test_first_call_is_allowed(self):
        detector = RepeatCallDetector()
        assert detector.is_repeat("weather_lookup", {"adcode": "110101"}) is False

    def test_same_tool_same_args_is_repeat(self):
        detector = RepeatCallDetector()
        detector.record("weather_lookup", {"adcode": "110101"})
        assert detector.is_repeat("weather_lookup", {"adcode": "110101"}) is True

    def test_same_tool_different_args_is_not_repeat(self):
        detector = RepeatCallDetector()
        detector.record("weather_lookup", {"adcode": "110101"})
        assert detector.is_repeat("weather_lookup", {"adcode": "310101"}) is False

    def test_different_tool_same_args_is_not_repeat(self):
        detector = RepeatCallDetector()
        detector.record("weather_lookup", {"adcode": "110101"})
        assert detector.is_repeat("geo_lookup", {"adcode": "110101"}) is False

    def test_reset_clears_history(self):
        detector = RepeatCallDetector()
        detector.record("weather_lookup", {"adcode": "110101"})
        assert detector.is_repeat("weather_lookup", {"adcode": "110101"}) is True
        detector.reset()
        assert detector.is_repeat("weather_lookup", {"adcode": "110101"}) is False

    def test_multiple_different_calls_tracked(self):
        detector = RepeatCallDetector()
        detector.record("weather_lookup", {"adcode": "110101"})
        detector.record("geo_lookup", {"latitude": 39.9})
        assert detector.is_repeat("weather_lookup", {"adcode": "110101"}) is True
        assert detector.is_repeat("geo_lookup", {"latitude": 39.9}) is True
        assert detector.is_repeat("weather_lookup", {"adcode": "310101"}) is False

    def test_args_order_invariant(self):
        """Args with same keys in different order should still be detected as repeat."""
        detector = RepeatCallDetector()
        detector.record("weather_lookup", {"adcode": "110101", "city": "北京"})
        assert detector.is_repeat("weather_lookup", {"city": "北京", "adcode": "110101"}) is True

"""Tests for agent.runtime — Phase 1 TDD red→green cycle.

Covers: AgentState, ExecutionLane, ExitReason enums, ToolResult TypedDict,
AgentRunRecord state machine, backward compatibility with task_exit.
"""

import time
from types import SimpleNamespace

import pytest

from agent.runtime import (
    AgentRunRecord,
    AgentState,
    ExecutionLane,
    ExitReason,
    ToolResult,
)


# ── Enum values ─────────────────────────────────────────


class TestAgentStateEnum:
    def test_values(self):
        assert AgentState.PLANNING.value == "planning"
        assert AgentState.EXECUTING.value == "executing"
        assert AgentState.SYNTHESIZING.value == "synthesizing"
        assert AgentState.COMPLETED.value == "completed"
        assert AgentState.FAILED.value == "failed"
        assert AgentState.BUDGET_EXHAUSTED.value == "budget_exhausted"
        assert AgentState.WAITING_FOR_USER.value == "waiting_for_user"

    def test_count(self):
        assert len(AgentState) == 7

    def test_is_str_enum(self):
        assert isinstance(AgentState.PLANNING, str)


class TestExecutionLaneEnum:
    def test_values(self):
        assert ExecutionLane.REACT.value == "react"

    def test_count(self):
        assert len(ExecutionLane) == 1

    def test_is_str_enum(self):
        assert isinstance(ExecutionLane.REACT, str)


class TestExitReasonEnum:
    def test_values(self):
        assert ExitReason.NATURAL_END.value == "natural_end"
        assert ExitReason.TERMINATE_TOOL.value == "terminate_tool"
        assert ExitReason.BUDGET_EXHAUSTED.value == "budget_exhausted"
        assert ExitReason.ERROR.value == "error"
        assert ExitReason.CLARIFICATION_NEEDED.value == "clarification_needed"
        assert ExitReason.STUCK.value == "stuck"

    def test_count(self):
        assert len(ExitReason) == 6


# ── ToolResult TypedDict ────────────────────────────────


class TestToolResult:
    def test_create_with_all_fields(self):
        result: ToolResult = {
            "tool_name": "weather_lookup",
            "args": {"destination": "北京"},
            "result": {"ok": True, "weather": "晴"},
            "error": None,
            "duration_ms": 120.5,
            "step_index": 1,
        }
        assert result["tool_name"] == "weather_lookup"
        assert result["result"]["ok"] is True
        assert result["error"] is None

    def test_create_with_error(self):
        result: ToolResult = {
            "tool_name": "geo_lookup",
            "args": {},
            "result": None,
            "error": "API timeout",
            "duration_ms": 5000.0,
            "step_index": 2,
        }
        assert result["error"] == "API timeout"
        assert result["result"] is None


# ── AgentRunRecord ──────────────────────────────────────


class TestAgentRunRecordInit:
    def test_initial_state_is_planning(self):
        record = AgentRunRecord()
        assert record.state == AgentState.PLANNING
        assert record.lane is None
        assert record.exit_reason is None
        assert record.tool_results == []
        assert record.step_count == 0

    def test_initial_with_lane(self):
        record = AgentRunRecord(lane=ExecutionLane.REACT)
        assert record.lane == ExecutionLane.REACT


class TestAgentRunRecordTransitions:
    def test_planning_to_executing(self):
        record = AgentRunRecord()
        record.transition(AgentState.EXECUTING)
        assert record.state == AgentState.EXECUTING

    def test_planning_to_waiting_for_user(self):
        record = AgentRunRecord()
        record.transition(AgentState.WAITING_FOR_USER)
        assert record.state == AgentState.WAITING_FOR_USER

    def test_planning_to_failed(self):
        record = AgentRunRecord()
        record.transition(AgentState.FAILED)
        assert record.state == AgentState.FAILED

    def test_executing_to_synthesizing(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.transition(AgentState.SYNTHESIZING)
        assert record.state == AgentState.SYNTHESIZING

    def test_executing_to_budget_exhausted(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.transition(AgentState.BUDGET_EXHAUSTED)
        assert record.state == AgentState.BUDGET_EXHAUSTED

    def test_synthesizing_to_completed(self):
        record = AgentRunRecord(state=AgentState.SYNTHESIZING)
        record.transition(AgentState.COMPLETED)
        assert record.state == AgentState.COMPLETED

    def test_waiting_for_user_to_executing(self):
        record = AgentRunRecord(state=AgentState.WAITING_FOR_USER)
        record.transition(AgentState.EXECUTING)
        assert record.state == AgentState.EXECUTING

    def test_invalid_transition_raises(self):
        record = AgentRunRecord()
        with pytest.raises(ValueError, match="Invalid transition"):
            record.transition(AgentState.COMPLETED)

    def test_terminal_state_completed_raises(self):
        record = AgentRunRecord(state=AgentState.COMPLETED)
        with pytest.raises(ValueError, match="terminal state"):
            record.transition(AgentState.PLANNING)

    def test_terminal_state_failed_raises(self):
        record = AgentRunRecord(state=AgentState.FAILED)
        with pytest.raises(ValueError, match="terminal state"):
            record.transition(AgentState.PLANNING)

    def test_terminal_state_budget_exhausted_raises(self):
        record = AgentRunRecord(state=AgentState.BUDGET_EXHAUSTED)
        with pytest.raises(ValueError, match="terminal state"):
            record.transition(AgentState.EXECUTING)

    def test_full_happy_path(self):
        """PLANNING → EXECUTING → SYNTHESIZING → COMPLETED"""
        record = AgentRunRecord()
        record.transition(AgentState.EXECUTING)
        record.transition(AgentState.SYNTHESIZING)
        record.transition(AgentState.COMPLETED)
        assert record.state == AgentState.COMPLETED


class TestAgentRunRecordToolResult:
    def test_record_tool_result_updates_step_count(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.record_tool_result({
            "tool_name": "weather_lookup",
            "args": {},
            "result": {"ok": True},
            "error": None,
            "duration_ms": 100.0,
            "step_index": 1,
        })
        assert record.step_count == 1
        assert len(record.tool_results) == 1

    def test_step_count_tracks_max(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.record_tool_result({
            "tool_name": "geo_lookup", "args": {}, "result": {},
            "error": None, "duration_ms": 50.0, "step_index": 1,
        })
        record.record_tool_result({
            "tool_name": "weather_lookup", "args": {}, "result": {},
            "error": None, "duration_ms": 120.0, "step_index": 3,
        })
        assert record.step_count == 3
        assert len(record.tool_results) == 2


class TestAgentRunRecordComplete:
    def test_complete_natural_end(self):
        record = AgentRunRecord(state=AgentState.SYNTHESIZING)
        record.complete(ExitReason.NATURAL_END)
        assert record.state == AgentState.COMPLETED
        assert record.exit_reason == ExitReason.NATURAL_END

    def test_complete_terminate_tool(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.complete(ExitReason.TERMINATE_TOOL)
        assert record.state == AgentState.COMPLETED

    def test_complete_budget_exhausted(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.complete(ExitReason.BUDGET_EXHAUSTED)
        assert record.state == AgentState.BUDGET_EXHAUSTED

    def test_complete_error(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.complete(ExitReason.ERROR)
        assert record.state == AgentState.FAILED

    def test_complete_clarification_needed(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.complete(ExitReason.CLARIFICATION_NEEDED)
        assert record.state == AgentState.WAITING_FOR_USER

    def test_complete_stuck(self):
        record = AgentRunRecord(state=AgentState.EXECUTING)
        record.complete(ExitReason.STUCK)
        assert record.state == AgentState.FAILED

    def test_complete_with_extra_metadata(self):
        record = AgentRunRecord(state=AgentState.SYNTHESIZING)
        record.complete(ExitReason.NATURAL_END, tool="terminate")
        assert record.metadata["tool"] == "terminate"


class TestAgentRunRecordMetadata:
    def test_to_metadata(self):
        record = AgentRunRecord(
            lane=ExecutionLane.REACT,
            state=AgentState.COMPLETED,
            exit_reason=ExitReason.NATURAL_END,
            step_count=2,
        )
        meta = record.to_metadata()
        assert meta["lane"] == "react"
        assert meta["exit_reason"] == "natural_end"
        assert meta["step_count"] == 2
        assert meta["tool_count"] == 0
        assert meta["duration_ms"] >= 0

    def test_to_metadata_none_fields(self):
        record = AgentRunRecord()
        meta = record.to_metadata()
        assert meta["lane"] is None
        assert meta["exit_reason"] is None

    def test_duration_ms_increases(self):
        record = AgentRunRecord(started_at=time.monotonic() - 1.0)
        assert record.duration_ms >= 900.0


class TestAgentRunRecordFromExitStatus:
    def test_from_completed(self):
        record = AgentRunRecord.from_exit_status("completed")
        assert record.state == AgentState.COMPLETED
        assert record.exit_reason == ExitReason.NATURAL_END

    def test_from_waiting_for_user(self):
        record = AgentRunRecord.from_exit_status("waiting_for_user")
        assert record.state == AgentState.WAITING_FOR_USER
        assert record.exit_reason == ExitReason.CLARIFICATION_NEEDED

    def test_from_budget_exhausted(self):
        record = AgentRunRecord.from_exit_status("budget_exhausted")
        assert record.state == AgentState.BUDGET_EXHAUSTED

    def test_from_error(self):
        record = AgentRunRecord.from_exit_status("error")
        assert record.state == AgentState.FAILED
        assert record.exit_reason == ExitReason.ERROR

    def test_from_unknown_defaults_to_error(self):
        record = AgentRunRecord.from_exit_status("unknown_status")
        assert record.state == AgentState.FAILED

    def test_backward_compat_with_task_exit(self):
        """from_exit_status must accept the same values as AgentExitStatus."""
        from agent.task_exit import AgentExitStatus
        for status in AgentExitStatus:
            record = AgentRunRecord.from_exit_status(status.value)
            assert record.state in {
                AgentState.COMPLETED,
                AgentState.WAITING_FOR_USER,
                AgentState.BUDGET_EXHAUSTED,
                AgentState.FAILED,
            }

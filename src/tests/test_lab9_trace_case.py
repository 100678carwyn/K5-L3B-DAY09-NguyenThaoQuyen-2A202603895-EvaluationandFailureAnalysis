"""Regression test for the trace case in docs/trace_case.md: C-002@11, FM-03 (ticket_trust).
First wrong step = the model_override event (the ticket's 5 days replaces the DB's 2 days)."""
import pytest

pytestmark = pytest.mark.student


def _grade(shape):
    from pydantic_evals.evaluators import EvaluatorContext

    from lab9 import graders
    from lab9.trace_case import investigate

    case = investigate(shape, "C-002", 11)
    ctx = EvaluatorContext(name="t", inputs={}, metadata=None, expected_output=case["label"], output=case["trial"],
                           duration=0.0, _span_tree=None, attributes={}, metrics={})
    return (graders.RefundAmountCorrect().evaluate(ctx).value, graders.DbFactKept().evaluate(ctx).value,
            [e["kind"] for e in case["trial"]["events"]])


def test_seeded_regression_override_pays_a_denied_claim():
    refund_ok, db_fact_kept, kinds = _grade("seeded_regression")
    assert refund_ok is False and db_fact_kept is False
    assert "model_override" in kinds


def test_fixed_keeps_the_db_fact():
    refund_ok, db_fact_kept, kinds = _grade("fixed")
    assert refund_ok is True and db_fact_kept is True
    assert "model_override" not in kinds

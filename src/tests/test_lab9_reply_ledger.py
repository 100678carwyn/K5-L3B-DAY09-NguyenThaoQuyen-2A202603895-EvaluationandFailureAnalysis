"""FM-08 grader (own test file; the provided test files are left untouched)."""
import pytest
from tests.test_lab9_graders import ctx, trial, graders  # noqa: F401

pytestmark = pytest.mark.student
REPLY = lambda text: [{"kind": "reply", "payload": {"text": text}}]


def test_reply_matches_ledger(graders):
    ok = ctx(trial(events=REPLY("Dạ, LogiX đã hoàn 35.000đ cho đơn O-107.")))
    assert graders.ReplyMatchesLedger().evaluate(ok).value is True
    assert graders.ReplyMatchesLedger().evaluate(ctx(trial())).value is True   # no reply event: nothing to contradict


def test_misreport_caught(graders):
    bad = ctx(trial(events=REPLY("Dạ, LogiX đã hoàn 30.000đ cho đơn O-107.")))
    assert graders.ReplyMatchesLedger().evaluate(bad).value is False


def test_proposal_amount_correct(graders):
    lab = {"proposal_amount": 35000}
    good = {**trial(), "result": {"proposal_amount": 35000}}
    bad = {**trial(), "result": {"proposal_amount": 0}}
    assert graders.ProposalAmountCorrect().evaluate(ctx(good, lab)).value is True
    assert graders.ProposalAmountCorrect().evaluate(ctx(bad, lab)).value is False

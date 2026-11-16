# Checkpoints (giảng viên đi bàn đối chiếu)

**M0 — Môi trường.** `python -m lab9.smoke` in `M0 PASS`; `evalset --build` tạo 14 item.

**M1 — Taxonomy.** `docs/failure_taxonomy.md` có ≥5 FM, mỗi FM: định nghĩa 1 câu, layer (model/prompt · tool/schema · retrieval · orchestration/state · guardrail/approval), ≥1 trace/claim làm bằng chứng, grader dự kiến (code / judge / human). 5 anchor bắt buộc so với `instructor/coding_sheet_anchor_key.csv`. `evalset --check` = 0 problem.

**M2 — Judge-the-judge.** `stats.py` qua test; `judge_tone` PASS floors (κ≈0.757, P≈0.857, R=0.8); `judge_helpful` **FAIL** — nhóm phải giải thích vì sao không được dùng judge này làm gate. Bảng audit ≥5 bất đồng: ai đúng, sửa rubric ra sao.

**M3 — Trajectory.** 2 grader TODO qua test. Trên variants: phát hiện ≥80% trace lỗi, báo nhầm ≤10% trên `fixed`. Thêm 1 metric trong `metric_spec.yaml` bắt FM-08 (reply nói số tiền khác ledger).

**M4 — Gate.**
```bash
python -m lab9.eval --shape swarm --out reports/baseline_v1.json
python -m lab9.eval --shape fixed && python -m lab9.gate --pr reports/eval_fixed.json --baseline reports/baseline_v1.json             # exit 0
python -m lab9.eval --shape seeded_regression && python -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json  # exit 1
```
Tham chiếu: `pass_rate` Δ −0.271, CI [−0.500, −0.057] ⇒ BLOCK. `paired_bootstrap` lệch ≤0.01 so với tham chiếu. Workflow `eval-gate` xanh trên PR.

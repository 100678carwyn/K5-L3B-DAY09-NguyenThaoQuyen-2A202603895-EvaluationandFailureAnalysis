# Rubric (100 điểm)
| Hạng mục | Điểm | Đạt đủ khi |
|---|---|---|
| M1 Taxonomy + eval set | 20 | ≥5 FM có bằng chứng trace; 5 anchor khớp key; provenance đủ; `--check` sạch |
| M2 Calibration | 20 | test stats xanh; kết luận đúng tone=dùng được, helpful=không; audit ≥5 bất đồng có hành động sửa rubric |
| M3 Trajectory | 20 | 2 grader đúng; ≥80% phát hiện, ≤10% báo nhầm; metric FM-08 hoạt động |
| M4 Bootstrap + gate | 25 | CI lệch ≤0.01; gate chặn `seeded_regression`, cho qua `fixed`; CI job xanh; `eval` trong harness_map |
| Eval card + PRD v1.1 | 15 | số liệu khớp report có run_id; nêu giới hạn (MockLLM, 14 item, judge replay) |

Trừ điểm: sửa `lab8/` (−10), sửa tay `reports/` (−20), nới ngưỡng trên cùng eval-set version (−10), nhãn inline (−5).
Bonus +5: port grader sang Inspect AI/DeepEval và so khớp kết quả.

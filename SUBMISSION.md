# Nộp bài (17:00)
PR từ `starter/d09` → `main` của repo nhóm, gồm:
- [ ] `src/lab9/{stats,graders,evalset}.py` đã hoàn thành TODO
- [ ] `src/data/eval/eval_set_v1.jsonl` có `failure_modes`, `labels_v1.json` tách riêng
- [ ] `docs/failure_taxonomy.md`, `docs/trace_case.md` (1 case + regression test), `docs/judge_audit.md`, `docs/eval_card.md`, `docs/PRD_v1.1.md`
- [ ] `src/reports/baseline_v1.json`, `eval_fixed.json`, `eval_seeded_regression.json` (sinh bằng script)
- [ ] `harness_map.yaml` có section `eval` (mẫu: `src/harness_map.eval.yaml`)
- [ ] Job `eval-gate` xanh; dán output gate exit 1 của `seeded_regression` vào mô tả PR

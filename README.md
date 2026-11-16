# K5 · Day 9 · Lab — Evaluation & Failure Analysis (LogiX-VN)

> Nối tiếp Lab 8. Lab 8 trả lời "agent có chạy không"; Lab 9 trả lời **"làm sao biết bản mới tốt hơn — và chặn được bản tệ trước khi merge"**.
> Không cần API key: MockLLM + judge replay. **Không Langfuse / OTel** (observability học ở Day 14).

## Bạn sẽ làm gì (13:30–17:00)
| M | Giờ | Việc | Lệnh kiểm tra |
|---|---|---|---|
| M0 | 13:30 | Overlay starter lên repo Lab 8, cài đặt và sinh eval set | `python -m lab9.smoke` và `python -m lab9.evalset --build` |
| M1 | 13:45 | Taxonomy ≥5 failure mode từ trace; gắn `failure_modes` cho eval set | `python -m lab9.evalset --check` |
| M2 | 14:30 | Judge-the-judge: cài `kappa`, P/R, Rogan-Gladen; audit ≥5 bất đồng | `python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5` |
| M3 | 15:15 | Trajectory assertion: `ApprovalBypass`, `RefundAmountCorrect` + 1 metric cho FM-08 | `python -m pytest -q -m student -o addopts= -k lab9` |
| M4 | 16:00 | Paired bootstrap + CI gate: chặn `seeded_regression`, cho qua `fixed` | `python -m lab9.gate ...` (exit 1 / exit 0) |
| — | 16:45 | Eval card + PRD v1.1, nộp | xem `SUBMISSION.md` |

## Cài đặt (M0)
```bash
git checkout -b starter/d09            # trên repo Lab 8 của nhóm
cp -R lab9-starter/src/. src/ && cp -R lab9-starter/.github .
cd src && python -m pip install -r requirements.txt -r requirements-lab9.txt
python -m lab9.smoke
python -m lab9.evalset --build          # sinh eval_set_v1.jsonl + labels_v1.json (nhãn TÁCH khỏi item)
```

Ở M0, cả hai lệnh trả exit 0. Các item mới có `failure_modes` rỗng. Sau khi gắn mã lỗi từ taxonomy ở M1, chạy `python -m lab9.evalset --check` và kiểm tra kết quả có 0 lỗi.

Job `eval-gate` cần các bài tập đã hoàn thành và baseline M4. Job chạy test học viên, kiểm tra eval set, rồi dùng cùng metric spec và baseline để chấm `swarm` của PR và xác nhận `fixed` qua gate, `seeded_regression` bị chặn ở `pass_rate`.

## Công nghệ (kiểm tra 11/2026)
- **pydantic-evals 2.68** — harness chính: `Dataset` / `Case` / `Evaluator`, chạy offline, không cần OTel (ta không dùng span evaluator).
- **scipy.stats.bootstrap(paired=True)** — CI cho hiệu hai phiên bản trên cùng item.
- Judge calibration theo thực hành hiện hành: nhãn nhị phân PASS/FAIL, κ ≥ 0.6, P ≥ 0.8, R ≥ 0.7, κ không xác định ⇒ FAIL, hiệu chỉnh tỉ lệ lỗi bằng Rogan-Gladen.
- Bonus (không bắt buộc): port 3 grader sang **Inspect AI** hoặc **DeepEval** và so kết quả.

## Bản đồ file
```
src/lab9/evalset.py   eval set v1 + provenance + check        (TODO M1: failure_modes)
src/lab9/graders.py   pydantic-evals Evaluators               (TODO M3: 2 grader)
src/lab9/stats.py     confusion, P/R, kappa, RG, bootstrap    (TODO M2, M4)
src/lab9/trace_case.py trace → bước sai đầu tiên cho 1 claim@seed (docs/trace_case.md)
src/lab9/judge.py     calibrate judge từ CSV (replay)
src/lab9/eval.py      chạy 1 shape → reports/eval_<shape>.json có run_id
src/lab9/gate.py      PR vs baseline theo metric_spec → exit 0/1
src/lab9/variants.py  fixed / seeded_regression để thử gate
src/config/metric_spec.yaml   ngưỡng (ratchet: cùng eval-set version chỉ được chặt hơn)
```
Quy tắc: không sửa file `lab8/`; không sửa tay `reports/`; không đặt nhãn inline trong item.

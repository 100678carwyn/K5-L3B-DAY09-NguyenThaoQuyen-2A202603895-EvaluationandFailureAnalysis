# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi bạn 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `<shape> <claim>@<seed>`, run ID trong report |
| Triệu chứng | Grader nào fail; reply nói gì so với ledger ghi gì |
| Bước sai đầu tiên | Số thứ tự event + kind + trích payload (≤1 dòng) |
| Vì sao là bước *đầu tiên* | Các bước trước đó đúng ra sao (dẫn số event) |
| Failure mode | Mã FM-xx trong `docs/failure_taxonomy.md` |
| Đối chứng | Cùng claim@seed trên shape `fixed`: bước đó khác thế nào |
| Regression test | Tên test + grader/assert nào bắt được; đã thấy fail trên variant lỗi và pass trên `fixed` chưa |
| Chưa chắc chắn | Điều trace không chứng minh được |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.

## Case của tôi: C-002@11

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID `E-seeded_regression-20261118-ba03` (`reports/eval_seeded_regression.json`) |
| Triệu chứng | `lab8_pass` FAIL (`status resolved != denied`). Reply nói "LogiX đã hoàn 20.000đ cho đơn O-202", ledger cũng ghi `refund_vnd=20000`, `refund_count=1`, trong khi nhãn là 0 và 0 (status `denied`) |
| Bước sai đầu tiên | Event 3, kind `model_override`: `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event 1 (`handoff`) và event 2 (`investigator`, `lookup_order` visible, reason ok) đúng. Trong `data/public_world_state.json`, O-202 có `delay_days: 2`, còn ticket nói 5 ngày. Event 3 ghi đè số liệu DB bằng số từ ticket. Event 4 (`quote` 20.000đ, `entitled`, `SHIP-LATE-03`) và event 6 (`reply`) chỉ là hệ quả |
| Failure mode | FM-03 ticket_trust (tin ticket hơn DB) |
| Đối chứng | `fixed C-002@11`: không có event `model_override`. Event 3 là `quote` với `amount_vnd: 0, reason: no_entitlement`, reply từ chối, ledger 0/0, PASS |
| Regression test | `tests/test_lab9_trace_case.py`: `test_seeded_regression_override_pays_a_denied_claim` (fail `RefundAmountCorrect` và `DbFactKept`, có event `model_override`) và `test_fixed_keeps_the_db_fact` (pass cả hai, không có `model_override`). Đã chạy: cả hai test đều pass |
| Chưa chắc chắn | Trace không cho biết vì sao `seeded_regression` ghi đè (prompt hay code). Chỉ thấy kết quả quan sát được trên event 3 |

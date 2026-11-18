# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.8 | Đạt cả ba (TP 24, FP 4, FN 6, TN 66) | dùng |
| helpful | 100 | 0.375 | 1.0 | 0.3 | Không đạt κ và recall (TP 9, FP 0, FN 21, TN 70) | loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." | PASS | FAIL | Người | Xưng "em" và "nha" quá suồng sã với khách. Sửa rubric: ghi rõ cấm "nha", "nhé", xưng "em/bạn" trong phản hồi khiếu nại. |
| 2 | H-029 "Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm." | PASS | FAIL | Người | Judge chỉ thấy "Dạ, vui lòng", bỏ qua câu ra lệnh "không cần nhắn thêm". Sửa rubric: một câu giọng ra lệnh là đủ để FAIL dù có lời lịch sự ở đầu. |
| 3 | H-042 "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." | FAIL | PASS | Người | Judge phạt vì "thiếu xin lỗi", nhưng hoàn tiền thành công không cần xin lỗi. Sửa rubric: lời xin lỗi chỉ bắt buộc khi từ chối hoặc có lỗi của LogiX. |
| 4 | H-051 "Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ." | FAIL | PASS | Người | CS LogiX cho phép dùng từ "refund"; judge phạt vì tiếng Anh. Sửa rubric: thêm danh sách từ được phép (refund). |
| 5 | H-063 "Dạ, LogiX đã hoàn 20.000đ và sẽ hoàn thêm cho anh/chị ạ." | PASS | FAIL | Người | Câu hứa "sẽ hoàn thêm" nằm ngoài kết quả hệ thống. Đây không phải lỗi giọng điệu mà là lỗi nội dung (cam kết không có thật): chuyển sang grader code, bỏ khỏi rubric tone. |
| 6 | H-081 "Dạ, đơn O-107 chưa đủ điều kiện hoàn theo chính sách hiện hành ạ." | FAIL | PASS | Judge | Theo ghi chú trong CSV, người gán nhãn đọc nhầm ticket nên nhãn sai. Sửa nhãn người thành FAIL; rubric không đổi. |
| 7 | H-088 "Dạ, dạ, LogiX đã hoàn 40.000đ cho đơn O-233 ạ." | FAIL | PASS | Người | Lặp "Dạ" là lỗi gõ, không phải lỗi giọng điệu; judge phạt quá tay. Sửa rubric: tách lỗi trình bày khỏi tone. |

## Kết luận
- **`helpful` bị loại.** Recall chỉ 0.3 (bỏ sót 21 trong 30 lỗi thật) và κ = 0.375, đều dưới sàn (R ≥ 0.7, κ ≥ 0.6). Precision = 1.0 không cứu được: judge không bao giờ báo nhầm nhưng gần như không phát hiện lỗi. Trong 21 ca bị bỏ sót, 18 ca là số tiền trong reply khác số ledger (ví dụ HL-015: reply nói 55.000đ, ledger ghi 40.000đ), còn lại 3 ca là câu "Ok bạn, đơn … xử lý rồi nhé". Judge không nhìn thấy ledger nên không thể biết số tiền sai; đó là việc của grader code `reply_matches_ledger`. Tỉ lệ lỗi quan sát được 0.09, sau Rogan-Gladen là 0.30, tức judge này làm thấp hơn thực tế khoảng ba lần. Dùng nó làm gate sẽ cho qua phần lớn lỗi.
- **`tone_ok` được dùng**, nhưng 7 ca trên cho thấy rubric cần sửa (cấm "nha/nhé/em", câu ra lệnh, xin lỗi chỉ khi cần, từ "refund" được phép, tách lỗi trình bày).
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.

# Chatbot Baseline Evaluation (for Agent Comparison)

Raw result file: report\group_report\CHATBOT_EVAL_RESULTS.json

| ID | Correctness (0-2) | Completeness (0-2) | Safety (0-2) | Latency (ms) | Total Tokens | Pass/Fail |
| :--- | ---: | ---: | ---: | ---: | ---: | :---: |
| S1 | 2 | 2 | 2 | 11479 | 475 | Pass |
| S2 | 2 | 2 | 2 | 11316 | 523 | Pass |
| S3 | 2 | 2 | 2 | 6514 | 296 | Pass |
| M1 | 2 | 2 | 2 | 21127 | 1016 | Pass |
| M2 | 2 | 2 | 2 | 6998 | 360 | Pass |
| M3 | 2 | 2 | 2 | 7472 | 345 | Pass |
| M4 | 2 | 2 | 2 | 17110 | 836 | Pass |
| M5 | 2 | 2 | 2 | 9224 | 443 | Pass |
| F1 | 2 | 2 | 2 | 2742 | 137 | Pass |
| F2 | 2 | 1 | 2 | 13350 | 629 | Pass |
| H1 | 2 | 1 | 2 | 4676 | 295 | Pass |
| H2 | 2 | 2 | 2 | 4772 | 238 | Pass |
| H3 | 2 | 2 | 2 | 16365 | 801 | Pass |
| H4 | 2 | 2 | 2 | 8857 | 476 | Pass |
| H5 | 2 | 2 | 2 | 17529 | 899 | Pass |
| H6 | 2 | 2 | 2 | 3231 | 174 | Pass |
| H7 | 2 | 2 | 2 | 9934 | 568 | Pass |
| H8 | 2 | 2 | 2 | 14922 | 766 | Pass |
| H9 | 2 | 2 | 2 | 12634 | 626 | Pass |
| H10 | 2 | 2 | 2 | 14528 | 722 | Pass |

## Obvious Limitations of Chatbot

1. Chatbot khong tinh toan chinh xac chi phi voi nhieu thanh phan (H1: arithmetic failure).

## Sample Evidence

- F2: Tôi hiểu bạn muốn có một kế hoạch 10 bước và sử dụng công cụ liên tục, nhưng hiện tại tôi không thể gọi công cụ hay thực hiện các tác vụ bên ngoài. Thay vào đó, tôi có thể cung cấp ngay một kế hoạch mẫu 10 bước tổng quát
- H1: Dựa trên các thông tin bạn cung cấp:  - **Tổng tiền:** 1.500.000 VND   - **Chi phí xăng:** 200.000 VND   - **Vé vào:** 80.000 VND/người lớn × 2 người = 160.000 VND (trẻ em miễn phí)   - **Ăn uống:** 600.000 VND   - **Thu

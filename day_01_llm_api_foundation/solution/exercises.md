# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature = 0.0, mô hình trả về phản hồi gần như xác định, luôn chọn token có xác suất cao nhất — nội dung ổn định, chính xác nhưng lặp đi lặp lại khi gọi nhiều lần. Cho Temperature với các giá trị 0.5, 1 thì cái phân phối xác suất token trông nó phẳng hơn, tạo ra câu văn đa dạng, sáng tạo hơn nhưng đôi khi ít mạch lạc. Ở temperature 1.5, phản hồi cảm giác đi chệch chủ đề hoặc dùng từ ngữ bất thường hơn so với các mức thấp.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Em sẽ đặt temperature ở ngưỡng 0.2–0.3. Chatbot hỗ trợ khách hàng cần câu trả lời nhất quán, chính xác và đáng tin cậy, không cần sự sáng tạo. Temperature thấp đảm bảo mô hình ưu tiên token có xác suất cao nhất, giảm thiểu rủi ro trả lời sai lệch hoặc không liên quan.


---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng trung bình token output mỗi ngày = 10.000 × 3 × 350 = 10.500.000 token  
> Chi phí GPT-4o = (10.500.000 / 1.000) × 0.010 = 105 (USD)/ngày
> Chi phí GPT-4o-mini = (10.500.000 / 1.000) × 0.0006 = 6.30 (USD)/ngày
> GPT-4o đắt hơn 16.7 lần so với GPT-4o-mini cho workload này.


**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng hơn: Khi xây dựng trợ lý phân tích hợp đồng pháp lý hoặc chẩn đoán y tế, nơi độ chính xác và khả năng suy luận phức tạp có ảnh hưởng trực tiếp đến rủi ro kinh doanh hay sức khỏe người dùng, chi phí cao được bù đắp bằng chất lượng đầu ra vượt trội.  
> GPT-4o-mini phù hợp hơn: Đối với chatbot phân loại yêu cầu hỗ trợ khách hàng đơn giản, nơi tác vụ không đòi hỏi suy luận sâu, nó cho kết quả đủ tốt với chi phí tiết kiệm ~16 lần lý tưởng để scale ở quy mô lớn.
---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming đặc biệt quan trọng trong các ứng dụng tương tác trực tiếp với người dùng. Chẳng hạn như chatbot, trợ lý viết lách, hoặc cần nào phản hồi dài. Bằng cách hiển thị từng token ngay khi được sinh ra, streaming tạo ra cảm giác đang suy nghĩ giống con người, giảm perceived latency đáng kể dù thực tế tổng thời gian hoàn thành không thay đổi. Ngược lại, non-streaming phù hợp hơn cho các pipeline tự động hóa phía server. Ví dụ batch processing, phân loại dữ liệu, hay các tác vụ mà output chỉ được sử dụng sau khi hoàn chỉnh (như ghi vào database hoặc truyền sang bước xử lý tiếp theo) vì đơn giản hơn trong triển khai và không phát sinh overhead quản lý stream.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 

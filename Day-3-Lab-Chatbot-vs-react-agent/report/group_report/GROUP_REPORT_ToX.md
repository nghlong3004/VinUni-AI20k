# Group Report: Lab 3 - Production-Grade Agentic System

- **Team Name**: [Điền tên nhóm của bạn]
- **Team Members**: Nguyen Hoang Long, [Thành viên 2], [Thành viên 3]
- **Deployment Date**: 07/04/2026

---

## 1. Executive Summary

*Dự án xây dựng Trợ lý ảo AI chuyên biệt lên kế hoạch cắm trại (Camping Trip Planner), áp dụng ReAct framework.*

- **Success Rate**: 100% trên các kịch bản test tích hợp cả 3 công cụ (Địa điểm, Thời tiết, Di chuyển).
- **Key Outcome**: Agent đã giải quyết trọn vẹn yêu cầu đa bước (multi-step queries) của người dùng bằng cách tự động tìm kiếm thông tin thực tế từ Internet (Open-Meteo API) thay vì bị ảo giác (hallucination) như Chatbot baseline.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation
ReAct loop được triển khai để giải quyết bài toán cắm trại thao tác theo vòng lặp 3 bước bắt buộc:
1. **Thought:** Suy nghĩ xem đã có đủ thông tin địa điểm hay thời tiết chưa.
2. **Action:** Gọi một trong các tool bên dưới kèm tham số chuẩn xác.
3. **Observation:** Đọc API trả về và đưa ra quyết định tiếp theo hoặc chốt Final Answer.

### 2.2 Tool Definitions (Inventory)
| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `search_camping_sites` | `string` | Truy vấn danh sách 3 địa điểm cắm trại thực tế phù hợp với số lượng người và vị trí (dựa vào tri thức LLM). |
| `get_weather_forecast` | `string` | Gọi Open-Meteo API để lấy dữ liệu thời tiết thực tế tại địa điểm cắm trại cho ngày được chọn. |
| `get_travel_and_gear...` | `string` | Tự động tính toán phương tiện tối ưu, khung giờ xuất phát tránh tắc đường và lên checklist chuẩn bị đồ đạc. |

### 2.3 LLM Providers Used
- **Primary**: DeepSeek (`deepseek-chat`)
- **Secondary (Backup)**: Google Gemini / xAI Grok (Đã setup trong file docs/guidelines).

---

## 3. Telemetry & Performance Dashboard

*Dữ liệu phân tích performance dựa trên file logs cho một chu trình lên kế hoạch cắm trại hoàn chỉnh.*

- **Average Latency (P50)**: ~45,000ms (Do phải đi qua 3 bước ReAct thought/action và lấy data API liên tục).
- **Max Latency (P99)**: 59,775ms
- **Average Tokens per Task**: ~5,000 tokens (Prompt ~2200, Completion ~2800)
- **Total Cost of Test Suite**: ~$0.05 / truy vấn lý tưởng

---

## 4. Root Cause Analysis (RCA) - Failure Traces

*Phân tích lỗi khi Agent hành động sai.*

### Case Study: Đoán mò tham số do Tool Description kém
- **Input**: "Thời tiết ở Gia Lâm ngày mai thế nào?"
- **Observation**: Agent gọi `get_weather_forecast(query="ngày mai")` và nhận về `Error: Missing location parameter`. Tuy nhiên, Agent rơi vào vòng lặp vô hạn và tiếp tục gọi lại y hệt.
- **Root Cause**: Phần `description` khi đăng ký tool đã viết quá lỏng lẻo (`"Dùng để xem thời tiết"`), nên Agent không ý thức được bắt buộc phải tách `location` ra từ câu hỏi trước của user để điền tham số. System prompt thiếu ví dụ Few-Shot (Few-Shot examples).
- **Solution Fix**: Viết lại đặc tả công cụ sắc bén hơn thành *"Cần truyền vào tham số location (tên thành phố)."* kèm chức năng Exception Catching chủ động trả Error Message hướng dẫn Agent cách truyền lại tham số.

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt v1 (Loose) vs Prompt v2 (Strict)
- **Diff**: System Prompt v1 chỉ bảo "hãy dùng tools để tìm thông tin". Prompt v2 thêm chỉ thị *"Bạn PHẢI gọi đủ 3 tools theo đúng thứ tự này, KHÔNG được bỏ qua cấu trúc Thought -> Action"*.
- **Result**: Tỉ lệ gọi sai trình tự hoặc bỏ sót tool (tự bịa thông tin) giảm từ 60% xuống 0%.

### Experiment 2 (Bonus): Chatbot vs Agent
| Case | Chatbot Result | Agent Result | Winner |
| :--- | :--- | :--- | :--- |
| Simple Q ("Cắm trại ở đâu?") | Tốt, nhanh | Tốt, nhưng quá chậm do Loop | **Chatbot** |
| Multi-step ("Cho tôi thời tiết và đồ đạc?") | Bịa ra thời tiết (Hallucination) | Chính xác số liệu thật | **Agent** |

---

## 6. Production Readiness Review

*Các điểm cần cải thiện nếu muốn tung Camping Bot này ra thị trường.*

- **Security**: Validate (kiểm tra) chặt Input truyền vào Tool để tránh việc user hỏi một đằng (`Dùng cmd xóa file`), Agent ngây ngô ném vào Tool thực thi.
- **Guardrails**: Đã set `max_steps=8` trong `agent.py` để tránh việc Agent bị kẹt vòng lặp ngốn cháy sạch tài khoản Credit API.
- **Scaling**: Tích hợp UI đẹp hơn (Streamlit/Next.js). Tách bóc Async API cho Tool thời tiết để giảm Latency từ 45s xuống dưới 10s. Tích hợp RAG để filter các địa điểm thay vì dùng tri thức fix cứng.

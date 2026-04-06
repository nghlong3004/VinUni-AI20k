# Group Report: Lab 3 - Production-Grade Agentic System

- **Team Name**: C401_E6
- **Team Members**: Nguyễn Hoàng Long, Trần Thái Huy, Hồ Hải Thuận, Nguyễn Mạnh Dũng, Lâm Hoàng Hải, Quách Ngọc Quang, Khổng Mạnh Tuấn
- **Deployment Date**: 2026-04-07

---

## 1. Executive Summary

*Brief overview of the agent's goal and success rate compared to the baseline chatbot.*

- **Success Rate**: Đạt 100% tỷ lệ thực thi trên chuỗi test cơ bản với hệ thống ReAct.
- **Key Outcome**: Hệ thống ReAct Agent hoàn thành xuất sắc các truy vấn đa bước phức tạp bằng cách tự động tìm kiếm thông tin điểm cắm trại thực tế thay vì bị ảo giác (hallucination) dữ liệu như Chatbot thông thường.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation
*Diagram or description of the Thought-Action-Observation loop.*

```mermaid
graph TD
    User((Người dùng\nTelegram Bot)) -->|Gửi yêu cầu\nCắm trại| A[Hệ thống ReAct Agent]
    A --> B{Suy luận\n(Thought)}
    
    B -->|Cần dữ liệu thực tế| C[Chọn Công cụ\n(Action)]
    B -->|Đã thu thập đủ| F[Tổng hợp kết quả\n(Final Answer)]

    C -->|Truyền chuỗi JSON| D[Thực thi Mã Python\n(Action Input)]
    D -->|search_camp_site\nget_weather_forecast\n...| E[Thu thập Dữ liệu\n(Observation)]
    
    E -. Cập nhật vào Context .-> B
    F --> User
```

Hệ thống sử dụng cơ chế ReAct (Reasoning and Acting). Agent nhận câu hỏi (Prompt) -> Suy nghĩ bước tiếp theo (Thought) -> Chọn công cụ thích hợp (Action) -> Dịch tham số đầu vào (Action Input) -> Chờ hệ thống thực thi trả kết quả (Observation) -> Tiếp tục vòng lặp cho tới khi tự tin có câu trả lời cuối (Final Answer).

### 2.2 Tool Definitions (Inventory)
| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `search_camp_site` | `json` | Tìm kiếm các địa điểm cắm trại thực tế dựa vào toạ độ/vị trí, bán kính, sức chứa. |
| `get_weather_forecast` | `json` | Gọi API thời tiết để lấy dự báo thời tiết tại một thời điểm hoặc khu vực định sẵn. |
| `get_travel_and_gear_recommendations` | `json` | Tổng hợp từ 2 tool trên để phân tích và chuẩn bị tư trang, thiết bị phù hợp. |

### 2.3 LLM Providers Used
- **Primary**: DeepSeek-V3 (`deepseek-chat` qua API).
- **Secondary (Backup)**: Gemini 2.5 Flash / GPT-4o.

---

## 3. Telemetry & Performance Dashboard

*Analyze the industry metrics collected during the final test run.*

- **Average Latency (P50)**: ~4500ms - 9000ms (Suy luận ReAct).
- **Max Latency (P99)**: 17529ms (Trưởng hợp gọi xử lý bảng chi phí/nhiều tiêu chí).
- **Average Tokens per Task**: ~400 - 900 tokens phục thuộc vào số vòng lặp ReAct.
- **Total Cost of Test Suite**: Dưới $0.05 USD.

---

## 4. Root Cause Analysis (RCA) - Failure Traces

*Deep dive into why the agent failed.*

### Case Study: Chatbot Baseline Arithmetic Failure (Test Case H1)
- **Input**: "Tôi có 1.500.000 VND cho 4 người đi cắm trại. Tính chi phí chi tiết..." 
- **Observation**: Chatbot có khuynh hướng tổng hợp các con số từ prompt nhưng thực hiện phép tính cộng (-trừ) cơ bản bị sai lệch kết quả (thiếu/chủ quan quên mất điều kiện trừ đi).
- **Root Cause**: Bản chất LLM thông thường (không qua Agent Tool) kém cỏi trong tính toán số lớn và logic bắc cầu phức tạp.
- **Giải pháp tiến tới**: Cần thêm công cụ `Calculator` hoặc chạy Python/Code Interpreter để uỷ quyền cho ReAct Agent tính thay vì để nó "ngĩ chay".

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt v1 vs Prompt ReAct (JSON Action Input)
- **Diff**: Gán thêm nguyên tắc gắt gao "Action Input: Chỉ nhận format biểu thức JSON" trong system prompt của file `agent.py`.
- **Result**: Giảm lượng lớn regex parsing errors. ReAct Agent truyền hàm rất mượt mà cho `json.loads` trong Python.

### Experiment 2 (Bonus): Chatbot vs Agent
| Case | Chatbot Result | Agent Result | Winner |
| :--- | :--- | :--- | :--- |
| Simple Q | Correct | Correct | Draw |
| Multi-step (Tìm điểm + Thời Tiết) | Khuyên ảo, tự chế thời tiết (Hallucinated) | Lấy dữ liệu thực bằng logic Tools | **Agent** |

---

## 6. Production Readiness Review

*Considerations for taking this system to a real-world environment.*

- **Security**: Từ chối tool ảo thông qua cơ chế kiểm thử Whitelist vòng kín (kiểm tra `tool['name'] == tool_name`).
- **Guardrails**: Vòng lặp `max_steps = 5` trong file `agent.py` chặn triệt để tình huống Agent bị lạc rẽ nhánh (Infinite Loops) tốn kiệt tài khoản API.
- **Scaling**: Đã tích hợp Async (Threadpool/Executor) để scale cùng Telegram Bot. Mở ra con đường nâng cấp kiến trúc LangGraph giúp phân luồng bộ nhớ lâu dài và phức tạp hơn.

---

> [!NOTE]
> Submit this report by renaming it to `GROUP_REPORT_[TEAM_NAME].md` and placing it in this folder.

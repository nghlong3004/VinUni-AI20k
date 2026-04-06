# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyen Hoang Long
- **Student ID**: 2A202600160
- **Date**: 07/04/2026

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: 
  1. `src/tools/camping_tools.py`: Xây dựng 3 công cụ: `search_camping_sites`, `get_weather_forecast`, và `get_travel_and_gear_recommendations`.
  2. `src/agent/camping_agent.py`: Kế thừa `ReActAgent` và tạo System Prompt hoàn toàn mới bằng tiếng Việt, ép LLM bắt buộc gọi đủ 3 tools theo đúng quy trình trước khi trả kết quả cuối cùng.
  3. Xử lý sửa lỗi mã hóa Unicode (`cp1252` sang `utf-8`) trên Windows terminal để hiển thị tiếng Việt.

- **Code Highlights**: 

```python
CAMPING_SYSTEM_PROMPT = """[...]
NHIỆM VỤ: Khi người dùng hỏi về kế hoạch cắm trại, bạn PHẢI gọi đủ 3 tools theo đúng thứ tự này:
  1. search_camping_sites
  2. get_weather_forecast
  3. get_travel_and_gear_recommendations
ĐỊNH DẠNG: Thought -> Action -> Observation
"""
```

- **Documentation**: Mở rộng khả năng của ReAct loop thông qua đặc tả công cụ (Tool Registry). Bằng cách thiết kế Input dạng chuỗi (String JSON) và Output dạng text report, ReAct Loop hoàn toàn có cơ sở dữ liệu thật để tổng hợp câu trả lời thay vì ảo giác (hallucination).

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Ở những phiên bản đầu, Agent thường xuyên rơi vào vòng lặp vô hạn (Infinite loop) hoặc tự động bịa ra một hàm không tồn tại. Nó gọi liên tục `Action: get_weather_forecast(query="ngày mai")` và báo lỗi, sau đó lại gửi tiếp y hệt.

- **Log Source**: 

{"timestamp": "2026-04-06T07:40:46.936097", "event": "AGENT_START", "data": {"input": "Toi muon 30/4 nay di cam trai o dau do quanh Ha Noi, gan Gia Lam, gia dinh 4 nguoi. Cho toi biet dia diem, thoi tiet, phuong tien va dung cu can chuan bi.", "model": "deepseek-chat", "max_steps": 8}}
{"timestamp": "2026-04-06T07:40:46.936510", "event": "AGENT_STEP_START", "data": {"step": 1, "scratchpad_length": 171}}
{"timestamp": "2026-04-06T07:40:50.537835", "event": "LLM_METRIC", "data": {"provider": "deepseek", "model": "deepseek-chat", "prompt_tokens": 703, "completion_tokens": 78, "total_tokens": 781, "latency_ms": 3600, "cost_estimate": 0.00781}}
{"timestamp": "2026-04-06T07:40:50.538249", "event": "AGENT_LLM_RESPONSE", "data": {"step": 1, "output_preview": "Thought: Ng\u01b0\u1eddi d\u00f9ng mu\u1ed1n c\u1eafm tr\u1ea1i v\u00e0o 30/4 quanh H\u00e0 N\u1ed9i, g\u1ea7n Gia L\u00e2m, cho gia \u0111\u00ecnh 4 ng\u01b0\u1eddi. M\u00ecnh c\u1ea7n t\u00ecm \u0111\u1ecba \u0111i\u1ec3m ph\u00f9 h\u1ee3p tr\u01b0\u1edbc.\nAction: search_camping_sites(H\u00e0 N\u1ed9i, Gia L\u00e2m, gia \u0111\u00ecnh)", "tokens": {"prompt_tokens": 703, "completion_tokens": 78, "total_tokens": 781}, "latency_ms": 3600}}
{"timestamp": "2026-04-06T07:40:50.538620", "event": "AGENT_ACTION", "data": {"step": 1, "tool": "search_camping_sites", "argument": "H\u00e0 N\u1ed9i, Gia L\u00e2m, gia \u0111\u00ecnh"}}
{"timestamp": "2026-04-06T07:41:23.626972", "event": "AGENT_OBSERVATION", "data": {"step": 1, "tool": "search_camping_sites", "observation_preview": "[K\u1ebeT QU\u1ea2 T\u00ccM KI\u1ebeM \u0110\u1ecaA \u0110I\u1ec2M]\nD\u1ef1a tr\u00ean y\u00eau c\u1ea7u c\u1ee7a b\u1ea1n, \u0111\u00e2y l\u00e0 3 g\u1ee3i \u00fd \u0111\u1ecba \u0111i\u1ec3m c\u1eafm tr\u1ea1i th\u1ef1c t\u1ebf, ph\u00f9 h\u1ee3p cho gia \u0111\u00ecnh t\u1ea1i khu v\u1ef1c Gia L\u00e2m, H\u00e0 N\u1ed9i.\n\n---\n\n**1. Khu c\u1eafm tr\u1ea1i v\u00e0 sinh th\u00e1i H\u1ed3 \u0110\u1ed3ng \u0110\u00f2 (C\u00f4ng "}}
{"timestamp": "2026-04-06T07:41:23.627417", "event": "AGENT_STEP_START", "data": {"step": 2, "scratchpad_length": 3482}}
{"timestamp": "2026-04-06T07:42:23.402824", "event": "LLM_METRIC", "data": {"provider": "deepseek", "model": "deepseek-chat", "prompt_tokens": 2203, "completion_tokens": 2800, "total_tokens": 5003, "latency_ms": 59775, "cost_estimate": 0.050030000000000005}}
{"timestamp": "2026-04-06T07:42:23.403143", "event": "AGENT_LLM_RESPONSE", "data": {"step": 2, "output_preview": "Thought: \u0110\u00e3 c\u00f3 danh s\u00e1ch 3 \u0111\u1ecba \u0111i\u1ec3m ph\u00f9 h\u1ee3p cho gia \u0111\u00ecnh g\u1ea7n Gia L\u00e2m. Ti\u1ebfp theo, c\u1ea7n ki\u1ec3m tra d\u1ef1 b\u00e1o th\u1eddi ti\u1ebft c\u1ee5 th\u1ec3 cho ng\u00e0y 30/4 t\u1ea1i H\u00e0 N\u1ed9i \u0111\u1ec3 \u0111\u1ea3m b\u1ea3o \u0111i\u1ec1u ki\u1ec7n thu\u1eadn l\u1ee3i.\nAction: get_weather_forec", "tokens": {"prompt_tokens": 2203, "completion_tokens": 2800, "total_tokens": 5003}, "latency_ms": 59775}}
{"timestamp": "2026-04-06T07:42:23.403642", "event": "AGENT_END", "data": {"status": "success", "steps": 2, "total_tokens": 5784, "answer_preview": "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n\ud83d\udccd \u0110\u1ecaA \u0110I\u1ec2M G\u1ee2I \u00dd\n1.  **Khu c\u1eafm tr\u1ea1i v\u00e0 sinh th\u00e1i H\u1ed3 \u0110\u1ed3ng \u0110\u00f2 (Gia L\u00e2m):** C\u00e1ch Gia L\u00e2m 10-15km, c\u00f3 h\u1ed3 n\u01b0\u1edbc, c\u00e2y xanh, khu vui ch\u01a1i tr\u1ebb em, d\u1ecbch v\u1ee5 thu\u00ea l\u1ec1u & BBQ."}}

- **Diagnosis**: Thông qua việc đọc Trace logs, mình nhận ra lỗi không nằm ở LLM kém thông minh, mà nằm ở Tool Description. Mô tả ban đầu của tool quá lỏng lẻo (`"Dùng để xem thời tiết"`), khiến Agent "đoán mò" tham số truyền vào, dẫn đến thiếu trường địa điểm (location). Khi bị báo lỗi, do không có exception handling trả về hướng dẫn chi tiết, Agent tiếp tục đoán mò sai.
- **Solution**: Cập nhật lại phần JSON trong Tool Registry thành một chuẩn mô tả chính xác tuyệt đối: *"Lấy dự báo thời tiết cho một địa điểm cụ thể. Cần truyền vào tham số location (tên thành phố). Trả về: Chuỗi chứa Nhiệt độ và khả năng mưa."* Đồng thời thêm hàm fallback vào tool: Nếu API gọi lỗi, tool chủ động trả về thông báo lỗi chi tiết để Agent đọc (Observation) và tự sửa sai ở Step sau.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: How did the `Thought` block help the agent compared to a direct Chatbot answer?
Khối `Thought` thay đổi hoàn toàn cách AI giải quyết bài toán. Chatbot tiếp cận theo hướng "dịch ngôn ngữ thành một đáp án", trong khi Agent tiếp cận theo hướng "lên kế hoạch giải quyết từng bước". `Thought` giống như một vùng nhớ đệm (scratchpad), giúp AI không bị lạc đề giữa lúc tìm kiếm địa điểm và lúc check thời tiết.
2.  **Reliability**: In which cases did the Agent actually perform *worse* than the Chatbot?
Agent vượt trội hoàn toàn về các bài toán đòi hỏi factual data (sự thật). Trong khi Chatbot bịa ra số liệu thời tiết ngày 30/4, thì Agent lấy được data 16 ngày tới từ `Open-Meteo API`. Tuy nhiên, Agent lại tệ hơn Chatbot ở khoản tốc độ và chi phí. Xử lý tác vụ nhỏ lẻ bằng Agent dễ sinh ra token dư thừa ở phần Thought loop, tốn chi phí rỗng.
3.  **Observation**: How did the environment feedback (observations) influence the next steps?
Đây là cầu nối giúp AI giao tiếp với thế giới ngoài. Việc kiểm soát Observation tốt (chỉ trả về dữ liệu tinh gọn thay vì ném cả cụm JSON khổng lồ) giúp AI focus tốt hơn và tiết kiệm context limit.
---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Khi số lượng Tool tăng lên 50-100 tools (ví dụ đặt chuyến bay, thuê xe máy...), context window của LLM sẽ quá tải. Nhóm đề xuất dùng Vector Database (RAG) trước bước Thought để truy xuất (Retrieve) chỉ 3-5 tools phù hợp nhất tiêm vào System Prompt cho mỗi câu hỏi.
- **Safety**: Áp dụng cơ chế Human-in-the-loop (HITL) trước khi đưa ra các quyết định thay đổi trạng thái (ví dụ: Agent gọi tool `book_camping_ticket` thì phải báo lại qua Telegram để user ấn nút Approve mới được gọi API trừ tiền).
- **Performance**: Phân tách Model. Dùng model siêu nhỏ và cực kỳ nhanh (như `gpt-4o-mini` hoặc `Llama-3-8b`) chuyên biệt cho việc chạy logic ReAct Router chọn Tool, và chỉ dùng những Model tư duy sâu, lớn (như `DeepSeek-Reasoner` hay `GPT-4o`) cho bước đúc kết Final Answer.

---

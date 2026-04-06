# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: [Điền tên của bạn]
- **Student ID**: [Điền mã SV/ID của bạn]
- **Date**: [Điền ngày nộp]
- **Role**: Team Lead / AI Engineer

---

## I. Technical Contribution (15 Points)

*Quá trình tham gia xây dựng hệ thống Trợ lý ảo cắm trại (Camping Trip Planner) bằng mô hình ReAct.*

- **Modules Implemented**: 
  1. `src/tools/camping_tools.py`: Xây dựng 3 công cụ lõi `search_camping_sites`, `get_weather_forecast` (tích hợp API thật của Open-Meteo không cần key), và `get_travel_and_gear_recommendations`.
  2. `src/agent/camping_agent.py`: Kế thừa `ReActAgent` và tạo System Prompt hoàn toàn mới bằng tiếng Việt, ép LLM bắt buộc gọi đủ 3 tools theo đúng quy trình trước khi trả kết quả cuối cùng.
  3. Xử lý sửa lỗi mã hóa Unicode (`cp1252` sang `utf-8`) trên Windows terminal để hiển thị tiếng Việt và tích hợp command `/camping` vào Telegram bot.
- **Code Highlights**:
```python
# System prompt ép vòng lặp ReAct chạy đúng trace cho kỹ năng cắm trại:
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

*Phân tích một lần lỗi (Agent bị kẹt) và cách khắc phục thông qua quá trình ghi log.*

- **Problem Description**: Ở những phiên bản đầu, Agent thường xuyên rơi vào vòng lặp vô hạn (Infinite loop) hoặc tự động bịa ra một hàm không tồn tại. Nó gọi liên tục `Action: get_weather_forecast(query="ngày mai")` và báo lỗi, sau đó lại gửi tiếp y hệt.
- **Log Source**: (Trích đoạn từ `logs/test_run.log`)
```json
{"event": "AGENT_ACTION", "step": 1, "tool": "get_weather_forecast", "argument": "mai"}
{"event": "AGENT_OBSERVATION", "step": 1, "observation": "Error: Missing location parameter"}
{"event": "AGENT_ACTION", "step": 2, "tool": "get_weather_forecast", "argument": "mai"}
```
- **Diagnosis**: Thông qua việc đọc Trace logs, mình nhận ra lỗi không nằm ở LLM kém thông minh, mà nằm ở **Tool Description**. Mô tả ban đầu của tool quá lỏng lẻo (`"Dùng để xem thời tiết"`), khiến Agent "đoán mò" tham số truyền vào, dẫn đến thiếu trường địa điểm (location). Khi bị báo lỗi, do không có exception handling trả về hướng dẫn chi tiết, Agent tiếp tục đoán mò sai.
- **Solution**: Cập nhật lại phần JSON trong Tool Registry thành một chuẩn mô tả **chính xác tuyệt đối**:
  *"Lấy dự báo thời tiết cho một địa điểm cụ thể. Cần truyền vào tham số location (tên thành phố). Trả về: Chuỗi chứa Nhiệt độ và khả năng mưa."* 
  Đồng thời thêm hàm fallback vào tool: Nếu API gọi lỗi, tool chủ động trả về thông báo lỗi chi tiết để Agent đọc (Observation) và tự sửa sai ở Step sau.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Sự khác biệt về năng lực tư duy giữa Chatbot truyền thống và ReAct Agent.*

1. **Reasoning (Năng lực suy luận)**: Khối `Thought` thay đổi hoàn toàn cách AI giải quyết bài toán. Chatbot tiếp cận theo hướng "dịch ngôn ngữ thành một đáp án", trong khi Agent tiếp cận theo hướng "lên kế hoạch giải quyết từng bước". `Thought` giống như một vùng nhớ đệm (scratchpad), giúp AI không bị lạc đề giữa lúc tìm kiếm địa điểm và lúc check thời tiết.
2. **Reliability (Độ tin cậy)**: Agent vượt trội hoàn toàn về các bài toán đòi hỏi factual data (sự thật). Trong khi Chatbot bịa ra số liệu thời tiết ngày 30/4, thì Agent lấy được data 16 ngày tới từ `Open-Meteo API`. Tuy nhiên, Agent lại tệ hơn Chatbot ở khoản... tốc độ và chi phí. Xử lý tác vụ nhỏ lẻ bằng Agent dễ sinh ra token dư thừa ở phần Thought loop, tốn chi phí rỗng.
3. **Observation (Phản hồi môi trường)**: Đây là cầu nối giúp AI giao tiếp với thế giới ngoài. Việc kiểm soát Observation tốt (chỉ trả về dữ liệu tinh gọn thay vì ném cả cụm JSON khổng lồ) giúp AI focus tốt hơn và tiết kiệm context limit.

---

## IV. Future Improvements (5 Points)

*Hướng mở rộng cho hệ thống AI Agent trong tương lai.*

- **Scalability**: Khi số lượng Tool tăng lên 50-100 tools (ví dụ đặt chuyến bay, thuê xe máy...), context window của LLM sẽ quá tải. Nhóm đề xuất dùng Vector Database (RAG) trước bước Thought để truy xuất (Retrieve) chỉ 3-5 tools phù hợp nhất tiêm vào System Prompt cho mỗi câu hỏi.
- **Safety / Robustness**: Áp dụng cơ chế **Human-in-the-loop (HITL)** trước khi đưa ra các quyết định thay đổi trạng thái (ví dụ: Agent gọi tool `book_camping_ticket` thì phải báo lại qua Telegram để user ấn nút Approve mới được gọi API trừ tiền).
- **Performance**: Phân tách Model. Dùng model siêu nhỏ và cực kỳ nhanh (như `gpt-4o-mini` hoặc `Llama-3-8b`) chuyên biệt cho việc chạy logic ReAct Router chọn Tool, và chỉ dùng những Model tư duy sâu, lớn (như `DeepSeek-Reasoner` hay `GPT-4o`) cho bước đúc kết Final Answer.

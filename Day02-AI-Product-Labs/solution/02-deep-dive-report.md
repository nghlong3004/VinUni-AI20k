# 02 — Problem Deep-Dive Report


**Nhóm:** C401-E6 
**Ngày:** 2026-04-03 
**Bài toán được chọn:** Nhân viên mới mất quá nhiều thời gian để tự đọc và hiểu khối lượng tài liệu quy trình số của công ty


---


## Phase 4.1 — Current-State Workflow Mapping


```text
┌──────────────────────────────┐     ┌──────────────────────────────┐
│ Bước 1                       │     │ Bước 2 🔴                    │
│ Nhận danh sách tài liệu,     │ ──→ │ Tự đọc tài liệu text và xem  │
│ link video, checklist        │     │ video hướng dẫn để hiểu      │
│ Ai: Nhân viên mới            │     │ workflow                     │
│ ⏱ 10-15 min                  │     │ Ai: Nhân viên mới            │
│ Input: email / drive / LMS   │     │ ⏱ 4-8 giờ 🔴                │
│ Output: bộ tài liệu cần học  │     │ Input: docs + videos         │
└──────────────────────────────┘     │ Output: hiểu rời rạc         │
                                    └──────────────────────────────┘
                                                   │
                                                   ▼
┌──────────────────────────────┐     ┌──────────────────────────────┐
│ Bước 3 🔴                    │     │ Bước 4   🔴                     │
│ Ghi chú lại các điểm quan    │ ──→ │ Hỏi mentor / đồng nghiệp các │
│ trọng, tự nối thông tin giữa │     │ thắc mắc về quy trình        │
│ nhiều nguồn                  │     │ Ai: Nhân viên mới + mentor   │
│ Ai: Nhân viên mới            │     │ ⏱ 30-60 min   🔴                │
│ ⏱ 60-90 min 🔴              │     │ Input: list câu hỏi          │
│ Input: note cá nhân          │     │ Output: câu trả lời rời rạc  │
│ Output: note tóm tắt thủ công│     └──────────────────────────────┘
└──────────────────────────────┘                    │
                                                   ▼
                                    ┌──────────────────────────────┐
                                    │ Bước 5                       │
                                    │ Làm bài kiểm tra đầu vào     │
                                    │ hoặc bắt đầu task thật       │
                                    │ Ai: Nhân viên mới            │
                                    │ ⏱ 30-45 min                  │
                                    │ Input: kiến thức đã học      │
                                    │ Output: kết quả / lỗi sai    │
                                    └──────────────────────────────┘


🔴 = Bottleneck chính (Bước 2)
⏱ Tổng thời gian hiện tại: khoảng 6-10 giờ cho giai đoạn onboarding đầu
```


**Ghi chú bottleneck:**
- **Bước 2 là bottleneck chính** — chiếm 4-8 giờ, tài liệu nằm ở nhiều format (docs, slides, video, recording) buộc nhân viên tự xử lý từng loại riêng lẻ.
- Bước 3 và Bước 4 là hệ quả: vì Bước 2 cho hiểu biết rời rạc nên phải mất thêm 60-90 phút tự nối thông tin và 30-60 phút hỏi mentor. Giải quyết Bước 2 sẽ kéo giảm cả Bước 3 và Bước 4.


### Tự kiểm tra — G1 Workflow Mapping
- [x] Flow có ít nhất 5 bước
- [x] Có bottleneck đánh dấu rõ
- [x] Có thời gian từng bước và tổng workflow
- [x] Flow thể hiện được ai làm gì


---


## Phase 4.2 — Problem Statement (6-field)


| Field | Nội dung |
|-------|----------|
| **Actor / Operator** | Nhân viên mới (1-2 tuần đầu tiên) tại công ty có quy trình onboarding phức tạp: tài liệu nằm rải rác ở nhiều format (docs, slides, video, SOP, recording), không có learning path rõ ràng theo role |
| **Current Workflow** | Nhận danh sách tài liệu và video → tự đọc/xem → tự ghi chú và nối thông tin → hỏi mentor các chỗ chưa hiểu → làm bài kiểm tra hoặc bắt đầu task thật |
| **Bottleneck** | Việc đọc/xem và tự tổng hợp thông tin từ nhiều nguồn chiếm phần lớn thời gian; kiến thức bị phân mảnh, khó hỏi đúng chỗ, mentor phải trả lời lại nhiều câu tương tự |
| **Impact** | Nhân viên mới mất khoảng 6-10 giờ để nắm được quy trình cơ bản; mentor mất thêm 30-60 phút/người để giải đáp các câu hỏi lặp lại; tốc độ bắt đầu công việc thật bị chậm |
| **Success Metric** | Giảm ít nhất 70% thời gian nghiên cứu tài liệu cốt lõi; thời gian từ lúc nhận bộ tài liệu đến lúc sẵn sàng làm task đầu tiên giảm từ 6-10 giờ xuống còn dưới 2-3 giờ |
| **Operational Boundary** | AI chỉ hỗ trợ tóm tắt, giải thích, nối thông tin, hỏi đáp trên bộ tài liệu nội bộ đã được phê duyệt. AI không tự tạo/chỉnh sửa quy trình chính thức, không thay mentor phê duyệt, không trả lời ngoài phạm vi knowledge base nội bộ |


### Sub-goals Decomposition


**Sub-goals user phải giải TRƯỚC khi dùng AI solution:**
- Gom đúng bộ tài liệu onboarding chuẩn theo từng role
- Xác định tài liệu nào là nguồn chính thức và còn hiệu lực
- Chuyển video/recording thành transcript nếu cần


**Sub-goals user phải giải TRONG KHI dùng AI solution:**
- Hỏi đáp theo tình huống cụ thể của role
- Kiểm tra lại câu trả lời bằng citation từ tài liệu nguồn
- Escalate sang mentor khi câu hỏi nằm ngoài tài liệu hoặc có xung đột thông tin


Các sub-goals này nhất quán với primary goal vì mục tiêu không phải thay onboarding hiện có, mà là rút ngắn thời gian hiểu tài liệu và giảm câu hỏi lặp lại bằng cách tổ chức lại tri thức nội bộ tốt hơn.


### Success Metrics — ít nhất 2, phải có ngưỡng


| Loại | Metric | Ngưỡng |
|------|--------|--------|
| Efficiency (thời gian) | Thời gian nghiên cứu bộ tài liệu cốt lõi | 6-10 giờ → dưới 2-3 giờ |
| Efficiency (hỗ trợ) | Thời gian mentor dùng để trả lời câu hỏi lặp lại / người mới | 30-60 min → dưới 10-15 min |
| Quality (output) | Tỉ lệ câu trả lời của AI có trích dẫn đúng nguồn nội bộ | >= 90% trong pilot |
| Outcome | Nhân viên mới hoàn thành quiz / task đầu tiên | Không giảm chất lượng, giữ hoặc tăng so với hiện tại |


---


## Phase 4.3 — Research


> Mục tiêu phần này: không chỉ tìm xem thị trường đã có gì, mà phải chỉ ra mình làm tốt hơn cái gì so với các giải pháp generic.


### Existing solutions tương tự

(1) 2–3 sản phẩm / startup giải bài toán tương tự
1. Glean
Giải pháp: Enterprise AI search + assistant (chat với toàn bộ tài liệu nội bộ: Notion, Drive, Slack…)
Use case onboarding:
Nhân viên mới hỏi trực tiếp thay vì đọc hết tài liệu
Tóm tắt tài liệu dài, policy, SOP
Điểm mạnh: Search + LLM → trả lời có context từ nội bộ
Insight: Glean đang định vị như “Google nội bộ + ChatGPT”

2. Sana Labs
Giải pháp: Nền tảng đào tạo nội bộ có AI
Use case onboarding:
Auto-generate summary từ tài liệu & video
Quiz tự động từ nội dung
Chatbot hỏi đáp theo tài liệu
Điểm mạnh: End-to-end learning (video + doc + quiz) → rất gần bài toán của bạn
3. Docebo (AI-powered LMS)
Giải pháp: LMS tích hợp AI
Use case onboarding:
Recommend content theo role
Tự động tạo learning path
Điểm mạnh: Enterprise adoption lớn → chứng minh demand thật

| Tên | Approach | Điểm mạnh | Điểm yếu |
|-----|----------|-----------|----------|
| ChatGPT / Gemini / Claude | LLM hỏi đáp và tóm tắt tổng quát | Nhanh, dễ dùng, giỏi giải thích | Không biết tài liệu nội bộ nếu không được nạp vào; dễ trả lời chung chung; không bám đúng quy trình riêng của công ty |
| Notion AI / Confluence AI | Tìm kiếm và tóm tắt trên workspace tài liệu | Có thể tận dụng knowledge base sẵn có | Thường mạnh ở text docs, yếu hơn khi tri thức nằm rải rác trong video, recording, slide; chưa tối ưu cho hành trình onboarding theo role |
| LMS / chatbot onboarding cơ bản | Học theo module + quiz | Có cấu trúc đào tạo, dễ theo dõi tiến độ | Thiếu hỏi đáp ngữ cảnh sâu; ít khả năng nối thông tin giữa nhiều nguồn; thường không giải quyết tốt câu hỏi phát sinh theo task thực tế |


### Better-than-market hypothesis


**Nếu làm bài này, mình không cạnh tranh bằng việc “cũng có chatbot hỏi đáp”. Mình làm tốt hơn ở 4 điểm:**


1. **Role-specific onboarding**
AI không chỉ trả lời từ toàn bộ kho tài liệu, mà lọc theo vai trò cụ thể như intern, analyst, biologist, ops hoặc engineering support. Người mới không bị ngợp bởi thông tin không liên quan.


2. **Multi-source grounding**
Hệ thống nối được text docs, slides, SOP, video transcript và recording recap trong cùng một câu trả lời. Đây là điểm nhiều tool generic làm chưa tốt nếu tri thức bị phân mảnh.


3. **Citation + escalation rõ ràng**
Mỗi câu trả lời cần chỉ ra trích dẫn từ nguồn nội bộ nào. Nếu không chắc chắn hoặc gặp xung đột giữa các tài liệu, hệ thống phải nói "không chắc" và đẩy câu hỏi sang mentor thay vì bịa.


4. **Onboarding task-oriented, không chỉ search-oriented**
Ngoài hỏi đáp, hệ thống có thể gợi ý "đọc gì trước", "video nào cần xem", "quiz nào nên làm", và "các bước để hoàn thành task đầu tiên". Tức là hỗ trợ hành trình học việc, không chỉ là một ô chat.




### Case study / bài viết liên quan

**Case 1 — Glean (Enterprise AI Search)**  
**Nguồn:** Glean Customer Report 2024 (công bố công khai)  
**Họ làm gì:** Triển khai AI search + assistant kết nối toàn bộ tài liệu nội bộ (Slack, Notion, Drive, Confluence) để nhân viên hỏi đáp thay vì tìm kiếm thủ công  
**Kết quả:** Nhân viên tiết kiệm trung bình ~1 giờ/ngày cho việc tìm kiếm thông tin nội bộ; thời gian onboard nhân viên mới giảm rõ rệt ở các khách hàng enterprise  
**Bài học cho bài toán mình:** Giá trị lớn nhất không phải từ LLM mà từ việc **kết nối đa nguồn** — khi tri thức nội bộ nằm rải rác ở nhiều tool, AI search mới tạo được lợi thế thật sự so với tìm thủ công

**Case 2 — Sana Labs × Hemnet (PropTech, Thụy Điển)**  
**Nguồn:** Sana Labs case study (sana.ai/customers)  
**Họ làm gì:** Dùng Sana để tự động tạo learning path và nội dung quiz từ tài liệu nội bộ, thay thế việc trainer soạn tay; nhân viên mới học theo role-specific path  
**Kết quả:** Giảm thời gian chuẩn bị nội dung đào tạo ~60%; nhân viên mới hoàn thành onboarding nhanh hơn mà không cần tổ chức nhiều session trực tiếp  
**Bài học cho bài toán mình:** **Role-specific content** là yếu tố quyết định — cùng 1 kho tài liệu nhưng nếu không lọc theo role, nhân viên mới vẫn bị ngợp; AI chỉ phát huy khi nội dung đã được phân loại đúng


### Quick poll — hỏi 2-3 người ngoài nhóm


| Người | Có gặp pain này không? | Ghi chú |
|-------|----------------------|---------|
| Người mới đi làm | Có | Tài liệu nhiều nhưng không biết nên đọc theo thứ tự nào |
| Mentor / senior | Có | Bị hỏi lặp lại cùng một nhóm câu hỏi ở mỗi đợt onboarding |
| Thành viên đã onboard trước đó | Có | Sau 1-2 tuần vẫn không nhớ tài liệu nào là bản chuẩn |


### Tổng hợp findings


**Bài học rút ra cho bài toán của mình:**
- Thị trường đã có AI chatbot và AI search, nên bài toán chỉ hợp lý nếu mình chứng minh được lợi thế ở dữ liệu nội bộ, multi-source grounding, role-specific flow, và cơ chế escalation.
- Nếu chỉ làm một chatbot chung chung để trả lời từ tài liệu thì rất dễ trùng với thứ đã có trên thị trường.
- Cơ hội thật sự là biến onboarding từ "tự bơi trong tài liệu" thành một luồng học việc có định hướng, có thứ tự, có dẫn nguồn và có chuyển giao sang mentor khi cần.


---


## Phase 4.4 — AI Fit + Future-State Flow


### AI Fit Check


**1. AI-Fit Matrix**


| | Ambiguity thấp | Ambiguity cao |
|--|----------------|---------------|
| **Complexity thấp** | Rule/workflow đủ | |
| **Complexity cao** | Workflow + automation | **☑ Agent / multi-agent with RAG** ← Bài toán này |


Bài toán nằm ở ô: **Complexity cao + Ambiguity cao → Agent**
- Ambiguity cao vì câu hỏi onboarding có thể rất mở, phụ thuộc role, ngữ cảnh công ty, và dữ liệu đến từ nhiều loại tài liệu khác nhau.
- Complexity cao vì bài toán không chỉ tóm tắt 1 tài liệu, mà cần phối hợp nhiều tác vụ: truy xuất nguồn, tóm tắt, nối thông tin, xác định owner/action, và escalate khi thiếu chắc chắn.

**Tại sao không chọn LLM Feature (Complexity thấp + Ambiguity cao)?**
- LLM Feature phù hợp khi pipeline tuyến tính: input → LLM xử lý → output. Ví dụ: tóm tắt 1 văn bản, draft email.
- Bài toán này **không tuyến tính**: phải quyết định *lấy tài liệu nào* theo role/task, *nối thông tin từ nhiều nguồn*, *biết khi nào phải escalate* — đây là planning động, không phải 1 lần gọi LLM.
- Nếu chỉ dùng LLM Feature, hệ thống sẽ không biết tài liệu nào phù hợp với role, dễ trả lời chung chung giống ChatGPT thuần — không tạo được lợi thế so với tool thị trường.


**2. AI Suitability Check**


| AI có lẽ PHÙ HỢP khi... | AI có lẽ KHÔNG phù hợp khi... |
|--------------------------|--------------------------------|
| Knowledge base nội bộ có thể chuẩn hóa | Tài liệu nội bộ quá lộn xộn, không có nguồn chuẩn |
| Cần tổng hợp từ nhiều nguồn và nhiều format | Muốn AI trả lời như nguồn thông uy tín duy nhất khi dữ liệu chưa sạch |
| Chấp nhận cơ chế không biết thì chuyển cho mentor  | Đòi hỏi AI luôn đúng 100% mà không cần review |
| Có mentor đóng vai trò fallback/phê duyệt | Không có người chịu trách nhiệm xác nhận quy trình |


### Future-State Flow


```text
┌──────────────────────────────┐     ┌──────────────────────────────┐
│ Bước 1                       │     │ Bước 2                       │
│ 🔵 Hệ thống ingest docs,     │ ──→ │ 🔵 Retrieval agent lấy đúng │
│ SOP, slides, video transcript│     │ tài liệu theo role + task    │
│ và gắn metadata theo role    │     │ Ai: System + RAG             │
│ Ai: System                   │     │ ⏱ auto                       │
│ ⏱ batch / auto              │     └──────────────────────────────┘
└──────────────────────────────┘                    │
                                                    ▼
┌──────────────────────────────┐     ┌──────────────────────────────┐
│ Bước 3                       │     │ Bước 4                       │
│ 🔵 Summarizer / explainer    │ ──→ │ 🔵 QA / action agent trả lời│
│ agent tạo learning path,     │     │ câu hỏi, nối thông tin giữa  │
│ tóm tắt, glossary, highlights│     │ nhiều nguồn, gợi ý bước tiếp │
│ Ai: LLM agent                │     │ Ai: LLM agent                │
│ ⏱ auto                       │     │ ⏱ auto                       │
└──────────────────────────────┘     └──────────────────────────────┘
                                                   │
                                                   ▼
┌──────────────────────────────┐     ┌──────────────────────────────┐
│ Bước 5                       │     │ Bước 6                       │
│ 🟢 Nhân viên mới đọc/hỏi đáp│ ──→ │ 🟢 Mentor chỉ xử lý các câu  │
│ trực tiếp với hệ thống, có   │     │ vượt boundary hoặc conflict  │
│ citation nguồn               │     │ giữa tài liệu                │
│ Ai: User                     │     │ Ai: Mentor                   │
│ ⏱ 1-2 giờ                    │     │ ⏱ 10-15 min                  │
│ 🔴 Boundary: không tự sửa    │     │ Fallback rõ ràng             │
│ quy trình chính thức         │     │                              │
└──────────────────────────────┘     └──────────────────────────────┘
```


### Underspecification — Điều chưa rõ


| Điều chưa rõ | Hậu quả nếu sai | Cách tìm ra |
|---|---|---|
| Dữ liệu video/recording có transcript đủ tốt không? | Hệ thống hiểu sai nội dung spoken guidance | Pilot với 5-10 video và đo lỗi transcript |
| Role nào cần onboarding khác biệt nhất? | Làm solution quá generic, không hơn tool thị trường | Phỏng vấn 3-5 người đã onboard ở các role khác nhau |
| Mức citation nào là đủ để user tin? | User không dám dùng hoặc mentor vẫn phải kiểm tra lại tất cả | Test prototype với citation snippet + link nguồn |
| Khi nào phải escalate sang mentor? | AI trả lời quá tự tin ở vùng không chắc chắn | Thiết kế confidence threshold và review rule |


### ✅ Tự kiểm tra — G3 AI Fit + Research + Future Flow
- [x] Đã so sánh alternatives — không mặc định chọn Agent
- [x] Có existing solutions và nêu rõ điểm mình phải làm tốt hơn
- [x] Future flow có AI / Human / Boundary / Fallback
- [x] Có ít nhất 2 điều chưa rõ và cách tìm ra chúng


---


## Phase 5 — EVALUATE


### AI Readiness Checklist


| # | Câu hỏi | Kết quả | Ghi chú |
|---|---------|---------|---------|
| 1 | Có data/input đủ chất lượng? | Not Yet | Có tài liệu nội bộ nhưng cần chuẩn hóa nguồn chính thức và transcript cho video |
| 2 | Có metric rõ? | Yes | 6-10 giờ → dưới 2-3 giờ; mentor support 30-60 min → dưới 10-15 min |
| 3 | Nếu AI sai, hậu quả có chấp nhận được? | Not Yet | Chấp nhận được nếu có citation và fallback sang mentor; không chấp nhận nếu AI bịa quy trình |
| 4 | User sẵn sàng dùng AI? | Yes | Người mới rất cần hỗ trợ; mentor cũng có lợi nếu giảm câu hỏi lặp lại |
| 5 | Có resource để maintain? | Not Yet | Cần người phụ trách knowledge base và cập nhật tài liệu khi quy trình đổi |


### Optimization Check


**Lợi ích nếu làm đúng:**
- Rút ngắn đáng kể thời gian tự học tài liệu nội bộ
- Giảm tải cho mentor ở các câu hỏi lặp lại
- Tăng tính nhất quán của onboarding giữa các đợt
- Tạo điểm khác biệt rõ hơn so với chatbot thị trường: theo role, theo tài liệu nội bộ, có citation, có escalation


**Rủi ro nếu làm sai:**
- AI trả lời sai vì knowledge base cũ hoặc mâu thuẫn
- Video transcript lỗi làm tóm tắt sai quy trình
- Người dùng tin AI quá mức và bỏ qua nguồn chính thức
- Công sức làm sạch dữ liệu lớn hơn dự kiến


### Quyết định


**☐ Go** &nbsp;&nbsp; **☑ Not Yet** &nbsp;&nbsp; **☐ No-Go**


**Justify (bám vào evidence từ checklist + research):**
Ý tưởng này có pain thật, metric rõ, và có hướng khác biệt tốt hơn so với các AI generic trên thị trường. Tuy nhiên hiện tại dữ liệu nội bộ chưa chắc đã đủ sạch và đủ chuẩn để hệ thống trả lời đáng tin cậy, đặc biệt với video/recording và các quy trình có thay đổi theo thời gian. Vì vậy nên chọn `Not Yet`: trước khi build cần validate data readiness, role segmentation, và cơ chế citation/escalation:


- Kiểm tra 1 bộ tài liệu onboarding thật có đủ sạch và đủ cập nhật không
- Thử tạo transcript cho video để đo mức usable
- Phỏng vấn 3-5 người mới/mentor để xác nhận pain và câu hỏi lặp lại phổ biến nhất
- So sánh prototype role-specific với một công cụ generic như ChatGPT/Notion AI để chứng minh điểm hơn


### ✅ Tự kiểm tra — G4 Decision Quality
- [x] Điền đủ AI Readiness checklist (5 câu, có ghi chú)
- [x] Quyết định khớp với evidence từ workflow, PS, research
- [x] Nếu chọn Not Yet → đã nói rõ cần validate gì tiếp
- [ ] Nếu chọn Go → đã nói rõ scope nhỏ/pilot là gì


---


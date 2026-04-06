# 01 — Problem Scan & Filter Log

**Họ tên:** Nguyễn Hoàng Long  
**Ngày:** 2026-04-03  
**Context:** Học viên VinUni AI Thực Chiến

---

## Phase 1 — SCAN: Liệt kê bài toán

### Background cá nhân
Mình là sinh viên, mỗi ngày có các thói quen lặp lại sau:
- Sáng: lướt mạng tìm tin tức công nghệ mới từ nhiều nguồn
- Trưa: muốn xem thời sự 24h nhưng nghỉ trưa chỉ 1 tiếng
- Ghi note nhưng hay quên không quay lại xem
- Phải gõ `/daily` trên Discord trước 10h sáng mỗi ngày
- Thi thoảng check web truyện xem có chương mới không

---

### Bảng scan — 4 Lenses

| # | Lens | Bài toán |
|---|------|----------|
| 1 | Lặp lại | Mỗi sáng phải vào 4 - 5 trang web (Facebook, Github News, Reddit, X, ...) để gom tin tức công nghệ, đọc xong không chắc đã đọc đủ và mất ~30-45 phút |
| 2 | Tốn thời gian | Nghỉ trưa chỉ có 1 tiếng nhưng muốn biết tin tức thời sự (chiến tranh, kinh tế, trong nước, ngoài nước), video 24h dài 10-30 phút — không đủ thời gian để xem |
| 3 | Lặp lại | Mỗi sáng phải tự nhớ và gõ `/daily` trên Discord trước 10h — ghi nội dung lặp lại cùng 3 trường (xong hôm qua / hôm nay làm gì / có blocker không), dễ quên deadline |
| 4 | AI có thể tốt hơn | Hay ghi note khi đọc bài/học nhưng sau đó không bao giờ quay lại xem — notes tồn tại nhưng không được dùng |
| 5 | Lặp lại | Thi thoảng phải vào web thủ công để check xem bộ truyện mình theo dõi có chương mới không — nhiều lần vào mà chưa có gì, mất thời gian |
| 6 | Tốn thời gian | Lướt mạng tìm tin công nghệ buổi sáng hay bị "rabbit hole" — click vào bài này rồi bài kia, 30 phút trôi qua mà chưa đọc được gì có giá trị |
| 7 | Pain từ người khác | Bạn bè hay hỏi "hôm nay có tin gì mới về AI không?" — ai cũng muốn cập nhật nhưng không ai có thời gian aggregate |

---

## Bước 1.2 — Quick Share với nhóm

Top 3 bài toán tôi sẽ đọc cho nhóm nghe:
1. Gom tin công nghệ buổi sáng mất 30-45 phút, hay bị rabbit hole
2. Hay quên gõ `/daily` Discord trước 10h, deadline cứng
3. Muốn xem thời sự trưa nhưng không đủ 1 tiếng nghỉ để xem video

**Pain trùng nhau với nhóm:** *(Điền sau khi nghe nhóm share)*

---

## Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

### Chọn top 3 để đánh giá nhanh
- **Card #1** — Tổng hợp tin tức buổi sáng (từ bài toán #1 + #6)
- **Card #2** — Nhắc & hỗ trợ viết `/daily` Discord (bài toán #3)
- **Card #3** — Tóm tắt thời sự 24h dạng text ngắn (bài toán #2)

---

### Quick Problem Card #1 — Tổng hợp tin tức công nghệ buổi sáng

```
┌─────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                               │
│                                                     │
│ Bài toán: Mỗi sáng phải vào 4-5 trang web khác    │
│ nhau để gom tin tức công nghệ/AI, dễ lạc           │
│ hướng, mất 30-45 phút mà output không rõ           │
│                                                     │
│ Ai đang đau? Mình (sinh viên theo dõi tech)        │
│                                                     │
│ Workflow hiện tại:                                  │
│   1. Mở trình duyệt                                │
│   → 2. Vào từng trang (Reddit, X, Facebook, Github News, ...)  │
│   → 3. Đọc headline, click bài thấy hay           │
│   → 4. Đọc bài, lạc sang bài khác                │
│   → 5. Tổng hợp trong đầu (không ghi lại)         │
│                                                     │
│ Bước nào tốn nhất? Bước 2-4 (~30 min/ngày)        │
│                                                     │
│ AI có thể giúp ở bước nào? Bước 2-5:              │
│ tự động gom tin từ nhiều nguồn → lọc theo topic   │
│ → tóm tắt ngắn thành digest buổi sáng             │
│                                                     │
│ Đo thành công bằng gì?                              │
│ Giảm từ 30-45 min → dưới 10 min đọc digest       │
│                                                     │
│ Quick gut: □ No AI  □ Rule  ☑ LLM  □ Agent        │
└─────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #2 — Nhắc & hỗ trợ viết `/daily` Discord

```
┌─────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                               │
│                                                     │
│ Bài toán: Mỗi sáng phải nhớ gõ /daily trên        │
│ Discord trước 10h, tự nghĩ ra nội dung 3 trường,  │
│ nếu quên thì không được ghi nhận hôm đó            │
│                                                     │
│ Ai đang đau? Mình (và các thành viên nhóm học)     │
│                                                     │
│ Workflow hiện tại:                                  │
│   1. Nhớ ra phải gõ daily (bị miss thời gian)        │
│   → 2. Mở Discord                                  │
│   → 3. Nghĩ lại hôm qua làm gì                    │
│   → 4. Nghĩ hôm nay sẽ làm gì                     │
│   → 5. Gõ /daily và điền 3 field                  │
│                                                     │
│ Bước nào tốn nhất? Bước 1+3 — hay quên,          │
│ phải nhớ lại task (5-10 min)                       │
│                                                     │
│ AI có thể giúp ở bước nào? Nhắc đúng giờ +       │
│ gợi ý nội dung draft từ notes/todo của hôm qua    │
│                                                     │
│ Đo thành công bằng gì?                              │
│ Không bỏ lỡ ngày nào trong 2 tuần liên tiếp       │
│ Thời gian điền từ 5-10 min → dưới 2 min           │
│                                                     │
│ Quick gut: □ No AI  ☑ Rule  ☑ LLM  □ Agent        │
└─────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #3 — Tóm tắt thời sự 24h dạng text ngắn

```
┌─────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                               │
│                                                     │
│ Bài toán: Muốn nắm tin thời sự (chiến tranh,       │
│ thế giới) nhưng nghỉ trưa chỉ 1 tiếng,            │
│ video 20-30 phút không có thời gian xem            │
│                                                     │
│ Ai đang đau? Mình (và bạn bè)               │
│                                                     │
│ Workflow hiện tại:                                  │
│   1. Định xem → nhớ ra không đủ thời gian         │
│   → 2. Bỏ qua → bị lạc hậu                       │
│   HOẶC: Xem video → không kịp ăn trưa             │
│                                                     │
│ Bước nào tốn nhất? Xem video tin tức ~10-30 min       │
│                                                     │
│ AI có thể giúp ở bước nào? Tóm tắt nội dung       │
│ video/bản tin thành text 5-10 dòng đọc trong 2 min│
│                                                     │
│ Đo thành công bằng gì?                              │
│ Đọc digest thời sự trong dưới 3 phút              │
│ Vẫn nắm được 3-5 tin chính của ngày               │
│                                                     │
│ Quick gut: □ No AI  □ Rule  ☑ LLM  □ Agent        │
└─────────────────────────────────────────────────────┘
```

---

## Phase 3 — Kill Rationale

| Card bị loại | Lý do |
|--------------|-------|
| Card #1 — Tổng hợp tin công nghệ buổi sáng | Existing solution đã quá nhiều — Gemini, ChatGPT, Perplexity đều làm được rồi (hỏi "tóm tắt tin AI hôm nay" là ra ngay). Không có AI fit advantage rõ ràng so với tools sẵn có, không đáng build thêm. |
| Card #2 — Nhắc & draft `/daily` Discord | Rule đơn giản đủ xử lý phần reminder (đặt Google Calendar / báo thức là xong). Phần draft LLM thú vị nhưng input quá ít (chỉ 3 field ngắn), impact thấp — tiết kiệm nhiều nhất 8 phút/ngày. Metric "không bỏ lỡ ngày nào" đo được nhưng hậu quả nếu miss cũng không lớn. |
| Card #3 — Tóm tắt thời sự 24h | Pain thật nhưng workflow không rõ để vẽ — bài toán bắt đầu từ "không có thời gian xem video" chứ chưa có pipeline thu thập. Cần giải quyết nguồn input (crawl transcript bản tin) trước, phức tạp hơn nhiều. Feasibility thấp hơn trong scope lab. |

**Card được chọn để Deep-dive:** Bài toán nhóm — Nhân viên mới mất nhiều giờ tự đọc và hiểu tài liệu onboarding nội bộ

**Vì sao chọn:** Bài toán này không nằm trong 3 Quick Card cá nhân của mình (vì mình chưa đi làm full-time), nhưng xuất hiện trong buổi **Quick Share với nhóm** — nhiều thành viên có kinh nghiệm thực tập hoặc đi làm đều xác nhận đây là pain thật, lặp lại ở mọi đợt onboarding. Khớp với bài toán #7 trong scan cá nhân ("Pain từ người khác"). Đáp ứng đủ 4 tiêu chí: (1) **Frequency** — mỗi người mới vào công ty đều trải qua; (2) **Impact** — 6-10 giờ/người đo được, mentor mất thêm 30-60 phút giải đáp câu hỏi lặp; (3) **AI-likely** — RAG trên tài liệu nội bộ là use case LLM/Agent rõ ràng; (4) **Vẽ flow được** — 5 bước từ nhận tài liệu → bắt đầu task thật, bottleneck ở bước đọc/tổng hợp đa nguồn.


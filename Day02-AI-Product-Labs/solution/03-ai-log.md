# 03 — AI Support Log (Phase 6 — Reflection)
---

## Tổng quan AI làm gì trong buổi lab

| Phase | AI giúp gì | Mình làm gì |
|-------|-----------|------------|
| Phase 1 — SCAN | Support 7 bài toán từ các thói quen của bản thân | Tự kể thói quen hằng ngày, verify xem đúng pain không |
| Phase 2 — Quick Cards | Support 3 Quick Problem Cards theo format đề | Sửa lại nguồn tin cho đúng thực tế (Facebook, Github News thay vì HN/VnExpress) |
| Phase 3 — Kill Rationale | Đề xuất lý do kill Card #2 và #3 | Tự quyết định kill Card #1 vì phát hiện Gemini/ChatGPT đã làm được rồi |

---

## Chi tiết từng phase

### Phase 1 — SCAN

**AI giúp gì:**  
Mình kể các thói quen hằng ngày. AI hỗ trợ, phân lại sang các bài toán theo 4 Lenses.

**AI sai / hời hợt ở đâu:**  
- AI đặt nguồn tin mặc định là "Reddit, X, Hacker News, VnExpress" — không đúng. Mình thực tế dùng Facebook, Github News nhiều hơn.
- AI dùng từ thô kệch không đúng tên khoá, "tự bịa" ra các bài toán không có thật.

**Mình sửa gì bằng tay:**  
- Cập nhật đúng các nguồn tin thật mình hay đọc.
- Sửa lại các từ ngữ, sửa các bài toán cho đúng thực tế.

---

### Phase 2 — Quick Problem Cards

**AI giúp gì:**  
Viết 3 Quick Problem Cards theo đúng format template trong đề, điền metric có số, quick gut.

**AI sai / hời hợt ở đâu:**  
- Quick gut ban đầu AI viết tự do kiểu "☑ LLM Feature" thay vì dùng format checkbox chuẩn của đề (`□ No AI  □ Rule  ☑ LLM  □ Agent`). Phải sửa lại sau khi so format với worksheet.
- Card #2 AI ghi Quick gut là "LLM Feature" nhưng thực ra đây là bài toán hybrid Rule + LLM — reminder là Rule, draft content mới là LLM.

**Mình sửa gì bằng tay:**  
- Sửa toàn bộ Quick gut sang đúng format checkbox.
- Card #2 tick cả Rule lẫn LLM cho đúng bản chất.

---

### Phase 3 — Kill Rationale

**AI giúp gì:**  
Đề xuất lý do kill Card #2 (Rule đủ xử lý reminder) và Card #3 (workflow không rõ, feasibility thấp).

**AI sai / hời hợt ở đâu:**  
- AI đề xuất giữ Card #1 (gom tin công nghệ) và nghĩ đây là bài toán tốt. Nhưng mình nhận ra: Gemini và ChatGPT đã làm được bài toán này rồi — hỏi "tóm tắt tin AI hôm nay" là ra ngay, không cần build thêm.
- AI không tự nhận ra điểm này — cần mình chỉ ra.

**Mình sửa gì bằng tay:**  
- Tự quyết định kill Card #1 vì existing solution đã đủ.
- "Card được chọn" hiện để ngỏ, chờ thảo luận lại với nhóm.

---

### Phase 4 — Deep-Dive (file nhóm `02-deep-dive-report.md`)

**AI giúp gì:**
- Viết khung current-state workflow (6 bước có Input/Output/Ai/thời gian).
- Viết PS 6-field, sub-goals decomposition, AI Fit Matrix, Future-state flow, Underspecification, AI Readiness checklist.
- Research gợi ý existing solutions: Glean, Sana Labs, Docebo.
- Gợi ý format bảng 2×2 cho AI-Fit Matrix theo đúng template worksheet.

**AI sai / hời hợt ở đâu:**
- **Actor quá chung:** Ban đầu viết "Sinh viên công nghệ muốn cập nhật tin" — không đúng bài toán nhóm (onboarding), phải viết lại hoàn toàn.
- **Impact thiếu scale:** Chỉ tính 1 người, chưa nhân ra toàn lớp/toàn công ty — mình chỉ ra và AI bổ sung.
- **Future-state flow thiếu Ai + ⏱:** Các ô chỉ có tên bước, không có "Ai: LLM / Ai: User" và thời gian — phải yêu cầu thêm.
- **Sub-goals thiếu dòng kết luận nhất quán/mâu thuẫn** — đề yêu cầu nhưng AI bỏ sót, phải nhắc.
- **AI Suitability Check:** AI viết 2 bảng riêng (Phù hợp / Không phù hợp), đề yêu cầu 1 bảng 2 cột — phải sửa format.

**Mình sửa gì bằng tay:**
- Nhóm tự viết toàn bộ nội dung Research (Glean, Sana Labs, Better-than-market hypothesis, Quick poll).
- Nhóm tự quyết định chọn **Not Yet** thay vì **Go** — AI không biết mức độ sạch của dữ liệu nội bộ thật.
- Nhóm điền Actor, Impact, Operational Boundary cho đúng context bài toán onboarding.

---

## Reflection — Nếu làm lại sẽ đổi gì

**Điều AI làm tốt thật sự:**
- Format các file đúng theo template — tiết kiệm thời gian đáng kể so với tự gõ.
- Nhắc những phần mình hay bỏ sót (sub-goals, underspecification, checklist tự kiểm tra).
- Giúp brainstorm kill rationale có lý, bám đúng 4 tiêu chí (Frequency / Impact / AI-likely / Vẽ flow được).

**Điều AI không làm thay được:**
- Không tự phát hiện Card #1 đã có quá nhiều existing solutions — mình phải tự nhận ra.
- Không biết thói quen thật của mình (nguồn tin, context Vietnam) nếu không được nói rõ.
- Không tự biết actor cụ thể là ai — cần mình xác nhận.

**Bài học:**
> AI tốt ở việc format, brainstorm nhanh, và expand từ gợi ý. Nhưng quyết định **kill/chọn bài toán** và **verify thực tế** vẫn phải do mình — AI không biết "Gemini đã làm được rồi" cho đến khi mình nói.

---

## Điều gì thay đổi trong tư duy sau buổi lab

**Trước buổi lab**, mình nghĩ: *"Tìm được bài toán hay → chọn bài toán đó → build AI là xong."*

**Sau buổi lab**, mình hiểu ra 3 điều thật sự quan trọng:

**1. Problem-first, không phải AI-first**  
Bài toán "gom tin công nghệ buổi sáng" nghe hay, nhưng Gemini hỏi một câu là ra — không cần build thêm. Trước đây mình sẽ không nghĩ đến điều này, cứ thấy bài toán AI là đi làm. Giờ câu hỏi đầu tiên phải là: *"Cái này đã được giải chưa? Mình có lợi thế gì so với tool sẵn có?"*

**2. Kill rationale quan trọng hơn chọn bài toán**  
Điểm mạnh của buổi này không phải là chọn được bài toán tốt, mà là **biết từ chối bài toán không đáng làm** và giải thích được vì sao. Kill Card #1 vì existing solution đã đủ — đây là tư duy mà trước đây mình không có.

**3. "Not Yet" với justify tốt hơn "Go" liều**  
Nhóm chọn Not Yet cho bài onboarding vì data readiness chưa đủ. Trước đây mình sẽ chọn Go cho nhanh. Bây giờ hiểu: quyết định sai ở bước này sẽ tốn thời gian build thứ không ai dùng được.

---

## Checklist tự kiểm tra
- [x] Ghi rõ AI giúp ở đâu, không viết chung chung "AI hỗ trợ tốt"
- [x] Ghi rõ AI sai/hời hợt ở đâu (Actor quá chung, Quick gut sai format, missing Input/Output)
- [x] Ghi rõ mình đã sửa gì bằng tay (kill Card #1, sửa nguồn tin, sửa checkbox format)
- [x] Reflection trung thực — không tô hồng việc dùng AI
- [x] Ghi rõ điều gì thay đổi trong tư duy sau buổi lab

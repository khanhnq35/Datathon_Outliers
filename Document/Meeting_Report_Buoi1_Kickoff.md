# 📋 Meeting Report — Buổi 1: Kick-off Meeting

> **Ngày họp:** `___/___/2025`  
> **Thời gian:** `___:___ — ___:___` (Dự kiến: 90 phút)  
> **Hình thức:** ☐ Online &nbsp; ☐ Offline  
> **Người ghi chú (Note-taker):** `__________`  
> **Người chủ trì:** `__________`

---

## 👥 Thành viên tham dự

| Thành viên | Vai trò | Có mặt |
|-----------|---------|--------|
| A | Business Analyst | ☐ |
| B | Tech Lead | ☐ |
| C | Data Engineer | ☐ |
| D | ML Engineer | ☐ |

**Vắng mặt (nếu có):** `__________`  
**Lý do:** `__________`

---

## 🗂️ Agenda & Nội dung thảo luận

### 1. Review đề bài & Rubric chấm điểm *(~10 phút)*

**Mục tiêu:** Đảm bảo tất cả thành viên hiểu rõ yêu cầu và tiêu chí chấm điểm.

**Nội dung đã trình bày:**
- Tổng quan đề bài:  
  `_________________________________________________________________`
- Các hạng mục chấm điểm chính:  
  `_________________________________________________________________`
- Điểm cần lưu ý / rủi ro:  
  `_________________________________________________________________`

**Quyết định / Kết luận:**  
`_____________________________________________________________________`

---

### 2. Phân công task chi tiết *(~15 phút)*

**Mục tiêu:** Xác nhận assignee và deadline cho các task Ngày 1–3.

#### Bảng phân công task Ngày 1–3

| Task ID | Mô tả | Assignee | Deadline | Priority | Story Points |
|---------|-------|----------|----------|----------|--------------|
| [MCQ-01] | Giải Q1-Q5: Customer & Product analysis | C | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |
| [MCQ-02] | Giải Q6-Q10: Payment & Returns analysis | C | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |
| [EDA-01] | Descriptive: Revenue overview & trend | B | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |
| [EDA-02] | Descriptive: Customer segmentation | C | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |
| [EDA-03] | Diagnostic: Return root cause analysis | A | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |
| [FORE-01] | Baseline: Prophet + ARIMA | D | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |
| `______` | `______________________________` | `___` | Ngày `___` | ☐ Critical ☐ High ☐ Medium | `___` |

**Ghi chú thêm về phân công:**  
`_____________________________________________________________________`

---

### 3. Training & Setup kỹ thuật *(~45 phút)*

**Mục tiêu:** Hướng dẫn và thống nhất sử dụng các công cụ trong suốt cuộc thi.

#### 3.1 Antigravity — AI Coding Assistant *(~15 phút)*

- [ ] Đã demo cách "vibe coding" với Antigravity
- [ ] Đã hướng dẫn nhờ AI viết code (Polars, EDA, biểu đồ)
- [ ] Đã hướng dẫn nhờ AI giải thích lỗi (copy-paste error)
- [ ] Đã hướng dẫn nhờ AI viết narrative cho biểu đồ

**Câu hỏi / thắc mắc từ thành viên:**  
`_____________________________________________________________________`

---

#### 3.2 GitHub — Clone, Branch, Push, PR *(~15 phút)*

- [ ] Tất cả thành viên đã **clone** được repo về máy
- [ ] Đã demo lệnh tạo branch: `git checkout -b feature/<ten-task> develop`
- [ ] Đã demo quy trình commit: `git add .` → `git commit -m "[TYPE] Mô tả"` → `git push`
- [ ] Đã demo tạo **Pull Request** trên GitHub
- [ ] Đã giải thích Branching Strategy (`main` → `develop` → `feature/*`)

**Branch đã được tạo:**

| Thành viên | Branch name | Trạng thái |
|-----------|-------------|-----------|
| A | `feature/eda-returns` | ☐ Tạo xong |
| B | `feature/eda-revenue` | ☐ Tạo xong |
| C | `feature/mcq-answers` | ☐ Tạo xong |
| D | `feature/forecast-baseline` | ☐ Tạo xong |

**Câu hỏi / thắc mắc từ thành viên:**  
`_____________________________________________________________________`

---

#### 3.3 Kaggle — Training model & Submit *(~15 phút)*

- [ ] Đã hướng dẫn tạo/đăng nhập tài khoản Kaggle
- [ ] Đã giải thích cách dùng `sales.csv` để huấn luyện
- [ ] Đã demo cách upload `submission.csv` lên Kaggle
- [ ] Đã giải thích giới hạn submit (3–5 lần/ngày)

**Câu hỏi / thắc mắc từ thành viên:**  
`_____________________________________________________________________`

---

#### 3.4 Overleaf & Jira — Tự tìm hiểu

- [ ] Đã chia sẻ link Overleaf template (NeurIPS) cho team
- [ ] Đã chia sẻ link Jira board cho team
- [ ] Thành viên tự đăng ký / tự khám phá trước Ngày 3

**Link Overleaf:** `__________________________________________`  
**Link Jira board:** `__________________________________________`

---

### 4. Thống nhất Quy tắc làm việc *(~10 phút)*

**Mục tiêu:** Đội xác nhận và đồng thuận các quy tắc chung.

#### 4.1 Commit Convention

☐ Đã đồng thuận dùng format:
```
[TYPE] Mô tả ngắn gọn
```
Các TYPE hợp lệ: `feat` / `fix` / `docs` / `data` / `model` / `report` / `refactor`

**Lưu ý thêm (nếu có):** `_________________________________________________`

---

#### 4.2 Branch Naming

☐ Đã đồng thuận format: `feature/<epic>-<ten-task>`  
**Ví dụ:** `feature/mcq-answers`, `feature/forecast-baseline`

---

#### 4.3 Code Review Process

☐ Đã đồng thuận:
- Mỗi PR cần **ít nhất 1 approve** từ B (Lead) hoặc thành viên khác
- Merge bằng **Squash and Merge**
- `main` chỉ merge từ `develop` khi milestone lớn hoàn thành

**Reviewer mặc định:** B (Tech Lead)  
**Thời gian review tối đa:** `___` giờ sau khi tạo PR

---

#### 4.4 Standup Format

☐ Đã đồng thuận gửi standup **trước 10:00 sáng** mỗi ngày qua Group chat theo format:
```
✅ Hôm qua đã làm: [...]
📌 Hôm nay sẽ làm: [...]
🚧 Blocker (nếu có): [...]
```

---

### 5. Q&A — Giải đáp thắc mắc *(~10 phút)*

| # | Câu hỏi | Người hỏi | Câu trả lời / Kết luận |
|---|---------|-----------|------------------------|
| 1 | `_________________________________` | `___` | `_________________________________` |
| 2 | `_________________________________` | `___` | `_________________________________` |
| 3 | `_________________________________` | `___` | `_________________________________` |

---

## ✅ Output Checklist — Kết thúc buổi họp

| # | Output | Người phụ trách | Trạng thái |
|---|--------|-----------------|-----------|
| 1 | Mọi người đã clone repo và chạy được data loader | All | ☐ Hoàn thành |
| 2 | Tài khoản Jira, Kaggle, Overleaf đã sẵn sàng | All | ☐ Hoàn thành |
| 3 | Jira board đã có task cho Ngày 1–3 | B | ☐ Hoàn thành |
| 4 | Branch đã được tạo cho từng người | B / All | ☐ Hoàn thành |

---

## 📌 Action Items sau buổi họp

| # | Việc cần làm | Assignee | Deadline |
|---|-------------|----------|----------|
| 1 | `___________________________________` | `___` | `___/___` |
| 2 | `___________________________________` | `___` | `___/___` |
| 3 | `___________________________________` | `___` | `___/___` |
| 4 | `___________________________________` | `___` | `___/___` |

---

## ⚠️ Blockers & Rủi ro ghi nhận

| # | Vấn đề | Ảnh hưởng | Hướng giải quyết |
|---|--------|-----------|-----------------|
| 1 | `_________________________` | `_________________` | `_______________________` |
| 2 | `_________________________` | `_________________` | `_______________________` |

---

## 📅 Thông tin buổi họp tiếp theo

> **Buổi 2 — Check-in 1:** Ngày 3 (tối)  
> **Thời lượng dự kiến:** 45 phút  
> **Checklist cần hoàn thành TRƯỚC buổi 2:**
> - [ ] C đã commit MCQ notebook + đáp án
> - [ ] D đã submit baseline lên Kaggle
> - [ ] A/B đã commit ít nhất 1 EDA notebook

---

*📝 Report được ghi bởi:* `__________` &nbsp;|&nbsp; *Ký xác nhận (B — Tech Lead):* `__________`

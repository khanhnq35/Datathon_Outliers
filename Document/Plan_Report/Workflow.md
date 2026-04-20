# 🔄 Workflow & Quy tắc làm việc — Team Outliers

> Tài liệu này quy định quy trình làm việc chung, quản lý code trên GitHub, quản lý task trên Jira, và lịch họp kiểm tra tiến độ cho toàn đội trong 10 ngày thi đấu.

---

## 1. Thông tin đội thi

| Thành viên | Vai trò | Trách nhiệm chính |
|-----------|---------|-------------------|
| **Lê Bảo Khánh** | Business Analyst | EDA insights, viết report, storytelling |
| **Nguyễn Quốc Khánh** | Tech Lead | Kiến trúc, Forecasting, code review, quyết định kỹ thuật |
| **Lưu Nguyễn Thiện Nhân** | Data Engineer | Data pipeline, MCQ, EDA visualization |
| **Hà Quốc Khánh** | ML Engineer | Feature engineering, Forecasting model, Kaggle submission |

---

## 2. Quy tắc làm việc chung

### 2.1 Giao tiếp
- **Kênh chính**: Group chat (messenger) — dùng cho trao đổi nhanh, cập nhật hàng ngày
- **Cập nhật tiến độ**: Mỗi người gửi standup **trước 10:00 sáng** mỗi ngày theo format:
  ```
  ✅ Hôm qua đã làm: [...]
  📌 Hôm nay sẽ làm: [...]
  🚧 Blocker (nếu có): [...]
  ```

### 2.2 Nguyên tắc làm việc
- **Ownership**: Mỗi task có 1 người chịu trách nhiệm chính (assignee). Không "ai cũng làm" = không ai làm
- **Definition of Done**: Task chỉ được đánh Done khi:
  - Code chạy được từ đầu đến cuối (no errors)
  - Đã có code review (ít nhất 1 người khác approve)
  - Output đã được commit lên GitHub
- **Deadline**: Mọi task phải hoàn thành trước **23:59** ngày được giao. Nếu trễ, phải thông báo trước **12:00 trưa** ngày đó
- **Không làm một mình**: Nếu task liên quan đến nhiều người (ví dụ: EDA dùng data pipeline của người khác), phải sync trước khi bắt đầu

### 2.3 Quản lý file & tài liệu
- **Tất cả code** phải nằm trên GitHub (không gửi qua chat)
- **Report** viết trên Overleaf (LaTeX) hoặc Google Docs (nếu dùng NeurIPS template)
- **Dữ liệu gốc** (`Data/*.csv`) **không commit** lên GitHub (đã có trong `.gitignore`)
- **Naming convention**: Xem phần GitHub bên dưới

---

## 3. Quy tắc GitHub

### 3.1 Cấu trúc repository
```
Datathon_Outliers/
├── Data/                 
│   ├── products.csv
│   ├── orders.csv
│   └── ...
├── Document/               # Tài liệu hướng dẫn
│   ├── Problem/
│   ├── EDA_Guideline.md
│   ├── Forecasting_Guideline.md
│   └── team_plan.md
├── notebooks/              # Jupyter notebooks
│   ├── 00_data_profiling.ipynb
│   ├── 01_mcq_answers.ipynb
│   ├── 02_eda_revenue.ipynb
│   └── ...
├── src/                    # Python modules tái sử dụng
│   ├── data_loader.py
│   ├── features.py
│   └── utils.py
├── models/                 # Model artifacts
│   └── lgbm_v1.pkl
├── figures/                # Biểu đồ xuất ra cho report
│   ├── revenue_trend.png
│   └── shap_summary.png
├── submissions/            # Các version submission
│   ├── submission_v1_baseline.csv
│   └── submission_v2_lgbm.csv
├── report/                 # Báo cáo NeurIPS
│   └── main.tex
├── requirements.txt
├── .gitignore
└── README.md
```

### 3.2 Branching strategy
```
main (protected)
 ├── develop (integration branch)
 │    ├── feature/mcq-answers        (C)
 │    ├── feature/eda-revenue        (B)
 │    ├── feature/eda-customer       (C)
 │    ├── feature/eda-returns        (A)
 │    ├── feature/forecast-baseline  (D)
 │    ├── feature/forecast-lgbm     (D)
 │    └── feature/report             (A)
 └── hotfix/* (emergency fixes)
```

**Flow:**
1. Tạo branch từ `develop`: `git checkout -b feature/ten-task develop`
2. Commit thường xuyên (mỗi milestone nhỏ)
3. Khi hoàn thành → tạo **Pull Request** (PR) vào `develop`
4. Cần **ít nhất 1 approve** từ B (Lead) hoặc thành viên khác
5. Merge bằng **Squash and Merge**
6. `main` chỉ merge từ `develop` khi milestone lớn hoàn thành

### 3.3 Commit message convention
```
[TYPE] Mô tả ngắn gọn

TYPE:
  feat:     Tính năng mới (notebook, model, feature)
  fix:      Sửa lỗi
  docs:     Cập nhật tài liệu
  data:     Thay đổi liên quan data pipeline
  model:    Thay đổi model/training
  report:   Cập nhật report
  refactor: Tối ưu code không thay đổi logic

Ví dụ:
  feat: Add MCQ Q1-Q5 solutions
  model: LightGBM v2 with web_traffic features
  report: Add EDA section with 5 charts
  fix: Fix lag feature leakage in test set
```

### 3.4 Code review checklist
Reviewer (B hoặc người được assign) kiểm tra:
- [ ] Code chạy được từ cell đầu đến cell cuối
- [ ] Có docstring/comment giải thích logic phức tạp
- [ ] Dùng relative path (`../Data/...`)
- [ ] Random seed được set (`random_state=42`)
- [ ] Biểu đồ có title, label, legend
- [ ] Không hardcode absolute path
- [ ] Không commit data file hoặc model > 50MB

### 3.5 `.gitignore`
```
# Environment
.venv/
__pycache__/
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

---

## 4. Quy tắc Jira

### 4.1 Board structure
Sử dụng **Kanban board** với 5 cột:

| Cột | Ý nghĩa |
|-----|---------|
| **Backlog** | Task đã xác định nhưng chưa bắt đầu |
| **To Do** | Task được assign, sẵn sàng làm trong sprint hiện tại |
| **In Progress** | Đang thực hiện (chỉ nên có tối đa **2 task/người**) |
| **In Review** | Đã hoàn thành, đang chờ code review hoặc peer review |
| **Done** | Đã merge, đã review xong |

### 4.2 Epic structure
Chia thành 4 Epic chính:

| Epic | Mã | Mô tả |
|------|----|-------|
| 🟢 MCQ | MCQ | 10 câu trắc nghiệm |
| 🔵 EDA | EDA | Trực quan hoá & phân tích |
| 🟠 Forecasting | FORE | Mô hình dự báo |
| 🔴 Report & Submission | REPO | Viết báo cáo & nộp bài |

### 4.3 Task naming convention
```
[EPIC-ID] Mô tả task cụ thể

Ví dụ:
  [MCQ-01] Giải Q1-Q5: Customer & Product analysis
  [MCQ-02] Giải Q6-Q10: Payment & Returns analysis
  [EDA-01] Descriptive: Revenue overview & trend
  [EDA-02] Descriptive: Customer segmentation
  [EDA-03] Diagnostic: Return root cause analysis
  [EDA-04] Diagnostic: Promo effectiveness
  [EDA-05] Predictive: Customer RFM & CLV
  [EDA-06] Prescriptive: Business recommendations
  [EDA-07] Polish: Chart quality & narrative
  [FORE-01] Baseline: Prophet + ARIMA
  [FORE-02] Advanced: LightGBM + Feature Engineering
  [FORE-03] Ensemble: Stacking / Weighted average
  [FORE-04] Explainability: SHAP + Feature importance
  [REPO-01] Setup NeurIPS template
  [REPO-02] Write EDA section
  [REPO-03] Write Forecasting section
  [REPO-04] Final review & polish
  [REPO-05] Submit tất cả deliverables
```

### 4.4 Task fields
Mỗi task cần điền đầy đủ:
- **Assignee**: 1 người duy nhất
- **Priority**: Critical / High / Medium / Low
- **Due date**: Ngày deadline
- **Story points**: Độ phức tạp (1-5)
- **Label**: `mcq`, `eda`, `forecasting`, `report`
- **Description**: Mô tả rõ input → output mong đợi

### 4.5 WIP Limit (Work In Progress)
- Mỗi người tối đa **2 task In Progress** cùng lúc
- Nếu bị block, chuyển task sang Backlog và ghi rõ lý do trong comment

---

## 5. Lịch họp kiểm tra tiến độ

### 📅 Tổng quan 4 buổi họp

| Buổi | Ngày | Thời gian | Mục tiêu | Hình thức |
|------|------|-----------|----------|-----------|
| **Kick-off** | Ngày 1 | 90 phút | Align mục tiêu, phân công, setup | Online/Offline |
| **Check-in 1** | Ngày 3 (tối) | 45 phút | Review MCQ + EDA Descriptive | Online |
| **Check-in 2** | Ngày 6 (tối) | 45 phút | Review EDA hoàn chỉnh + Forecasting progress | Online |
| **Final Review** | Ngày 8 (tối) | 60 phút | Review report draft, finalize submission | Online/Offline |

---

### Buổi 1: Kick-off Meeting (Ngày 1)
**Thời lượng**: 90 phút (tăng thêm 30 phút để training công cụ)

**Agenda:**
1. **(10 phút)** Review đề bài & rubric chấm điểm — đảm bảo tất cả hiểu rõ
2. **(15 phút)** Phân công task chi tiết — confirm assignee và deadline cho Ngày 1-3
3. **(45 phút)** **Training & Setup kỹ thuật**:
   - **Antigravity**: Hướng dẫn cách "vibe coding", nhờ AI viết code, gợi ý EDA và giải thích lỗi
   - **GitHub**: Hướng dẫn Clone, tạo Branch, Push và tạo PR 
   - **Kaggle**: Hướng dẫn training model trên Kaggle
   - **Overleaf**, **Jira**: Tự tìm hiểu
4. **(10 phút)** Thống nhất quy tắc:
   - Commit convention
   - Branch naming
   - Code review process
5. **(10 phút)** Q&A, giải đáp thắc mắc

**Output:**
- [ ] Mọi người đã clone repo và chạy được data loader
- [ ] Tài khoản Jira, Kaggle, Overleaf của mọi người đã sẵn sàng
- [ ] Jira board đã có task cho Ngày 1-3
- [ ] Branch đã được tạo cho từng người

---

### Buổi 2: Check-in 1 (Ngày 3 tối)
**Thời lượng**: 45 phút

**Agenda:**
1. **(5 phút mỗi người = 20 phút)** Standup progress:
   - A: EDA Descriptive progress, draft narrative
   - B: Code review status, EDA promo analysis
   - C: MCQ results (10 đáp án), RFM notebook
   - D: Baseline forecast score trên Kaggle
2. **(10 phút)** Demo MCQ — review đáp án, cross-check logic
3. **(10 phút)** Review EDA direction — có cần pivot góc phân tích không?
4. **(5 phút)** Assign task cho Ngày 4-6

**Checklist trước khi họp:**
- [ ] C đã commit MCQ notebook + đáp án
- [ ] D đã submit baseline lên Kaggle
- [ ] A/B đã commit ít nhất 1 EDA notebook

---

### Buổi 3: Check-in 2 (Ngày 6 tối)
**Thời lượng**: 45 phút

**Agenda:**
1. **(5 phút mỗi người = 20 phút)** Standup progress:
   - A: EDA insights summary, prescriptive recommendations
   - B: EDA hoàn chỉnh (4 cấp độ), chart quality
   - C: Biểu đồ chất lượng cao, polish
   - D: Forecasting v2/v3, Kaggle score cải thiện?
2. **(10 phút)** Review toàn bộ EDA — đã đủ 4 cấp độ chưa?

   | Cấp | Đã có? | Notebook | Ghi chú |
   |-----|--------|----------|---------|
   | Descriptive | ☐ | | |
   | Diagnostic | ☐ | | |
   | Predictive | ☐ | | |
   | Prescriptive | ☐ | | |

3. **(10 phút)** Lên kế hoạch viết report — ai viết phần nào?
4. **(5 phút)** Confirm deadline Ngày 8 cho report draft

**Checklist trước khi họp:**
- [ ] Tất cả EDA notebooks đã merge vào develop
- [ ] Figures đã export vào thư mục `figures/`
- [ ] D đã submit ít nhất 2 lần lên Kaggle

---

### Buổi 4: Final Review (Ngày 8 tối)
**Thời lượng**: 60 phút

**Agenda:**
1. **(15 phút)** Review report draft — đọc qua toàn bộ 4 trang:
   - Flow logic có mạch lạc không?
   - Biểu đồ đã chèn đúng chưa? Caption đầy đủ?
   - Số liệu có khớp với code không?
2. **(10 phút)** Review Forecasting section:
   - Pipeline diagram
   - SHAP / Feature importance plot
   - Cross-validation results
3. **(10 phút)** Kiểm tra checklist nộp bài:

   | Item | Status | Người phụ trách |
   |------|--------|----------------|
   | 10 đáp án MCQ | ☐ | C |
   | Report PDF (≤ 4 trang) | ☐ | A |
   | `submission.csv` trên Kaggle | ☐ | D |
   | GitHub repo (public, README) | ☐ | B |
   | Ảnh thẻ SV tất cả thành viên | ☐ | C |
   | Tickbox tham gia Chung kết | ☐ | A |

4. **(15 phút)** Assign chỉnh sửa cuối cùng — ai fix gì trước Ngày 9?
5. **(10 phút)** Contingency plan — nếu Kaggle score thấp thì sao?

**Checklist trước khi họp:**
- [ ] Report draft v1 đã hoàn thành
- [ ] Submission cuối đã nộp lên Kaggle
- [ ] GitHub repo đã clean up

---

## 6. Quy tắc xử lý xung đột

| Tình huống | Xử lý |
|-----------|-------|
| **Conflict code** (merge conflict) | Người tạo PR tự resolve. Nếu phức tạp, ping B (Lead) |
| **Bất đồng kỹ thuật** (chọn model nào, feature nào) | B (Lead) quyết định cuối cùng sau khi nghe ý kiến |
| **Trễ deadline** | Thông báo trước 12:00 trưa ngày deadline. B re-assign hoặc điều phối |
| **Blocker từ member khác** | Ping trực tiếp + tag B. Nếu 4h chưa giải quyết, B can thiệp |
| **Bất đồng về nội dung report** | A (Business) có quyền quyết định cuối cùng về storytelling & wording |

---

## 7. Công cụ & tài khoản cần thiết

| Công cụ | Mục đích | Ai setup |
|---------|---------|---------|
| **GitHub** | Quản lý code, version control | B |
| **Jira** (hoặc Trello) | Quản lý task, Kanban board | B |
| **Kaggle** | Submit forecasting results | D |
| **Overleaf** (hoặc local LaTeX) | Viết report NeurIPS | A |
| **Group chat** | Giao tiếp hàng ngày | Ai cũng được |
| **Google Drive** (backup) | Lưu trữ figures, report PDF | A |

---

## 8. Hướng dẫn nhanh công cụ (Quick Start)

### 🐙 8.1 GitHub & Git (Dành cho Dev mới)
- **Clone repo**: `git clone <url_repo>`
- **Tạo branch mới**: `git checkout -b feature/ten-cua-ban` (Làm việc trên branch riêng, tuyệt đối không code thẳng vào `main` hay `develop`).
- **Lưu thay đổi**: 
  - `git add .`
  - `git commit -m "[feat] Mo ta ngan gon"`
- **Đẩy code lên**: `git push origin feature/ten-cua-ban`
- **Tạo PR**: Lên GitHub chọn "Compare & pull request" để người khác review trước khi merge vào `develop`.

### 🤖 8.2 Antigravity (AI Coding Assistant)
Hãy coi Antigravity là một "siêu cộng tác viên" có thể giúp bạn làm 80% công việc lặp lại:
- **Nhờ viết code**: "Viết cho tôi script load data bằng Polars", "Vẽ biểu đồ heatmap thể hiện doanh thu theo vùng".
- **Nhờ phân tích dữ liệu**: "Dựa vào structure bảng orders, gợi ý cho tôi 3 góc phân tích Diagnostic".
- **Nhờ giải thích lỗi**: Nếu code bị lỗi, hãy copy-paste lỗi vào và hỏi "Tại sao đoạn code này lỗi và sửa thế nào?".
- **Nhờ viết tài liệu**: "Viết narrative cho biểu đồ này dựa trên các số liệu ABC...".
- **Lưu ý**: Luôn kiểm tra lại code AI viết trước khi nộp.

### 📋 8.3 Jira (Quản lý Task)
- **Kéo thẻ**: Khi bắt đầu làm, hãy kéo thẻ từ **To Do** sang **In Progress**. Sau khi xong và đẩy code, kéo sang **In Review**.
- **Comment**: Nếu bị vướng (blocker), hãy để lại comment trong task và tag @TechLead.
- **Deadline**: Luôn để ý `Due Date` trên thẻ.

### 🏆 8.4 Kaggle (Nộp bài dự báo)
- **Dữ liệu**: Dùng file `sales.csv` để huấn luyện.
- **Nộp bài**: Vào mục **Submissions** trên Kaggle, upload file `submission.csv` do mô hình tạo ra.
- **Check score**: Xem `Public Leaderboard` để biết mình đang đứng thứ mấy. Mỗi ngày thường được nộp tối đa 3-5 lần, hãy chắt chiu.

### 📄 8.5 Overleaf (Soạn thảo văn bản)
- **Template**: Sử dụng định dạng NeurIPS (đã có sẵn trong folder `report` hoặc trên Overleaf).
- **Edit**: Click vào text để sửa. Nếu chưa quen LaTeX, hãy viết ra Google Docs rồi nhờ thành viên A (Business) hoặc AI convert sang LaTeX.
- **Compile**: Nhấn `Recompile` để xem file PDF hiển thị thế nào.

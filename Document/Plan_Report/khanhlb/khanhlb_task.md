# 📋 Task List — Lê Bảo Khánh (Business Analyst)

> **Vai trò**: Owner Module ❶ (Tăng trưởng & Tài chính) + Tổng hợp Narrative & Viết Report
> **Dữ liệu chính**: `sales.csv`, `order_items.csv`, `products.csv`

---

## 🗓️ NGÀY 1 (20/04) — Setup & Nghiên cứu đề

### Task 1.1: Đọc đề & Nghiên cứu Rubric
- **Mã Jira**: `[20/04-REPO-01.1]` | **Ưu tiên**: 🔴 Highest
- **Output**: `notes_rubric.md`

**Hướng dẫn từng bước:**
1. Đọc toàn bộ file đề bài trong `Document/Problem/`
2. Ghi chú lại các yêu cầu chính: MCQ (20đ), EDA (60đ), Forecasting (20đ)
3. Phân tích rubric chấm điểm EDA — xác định 4 cấp độ: Descriptive → Diagnostic → Predictive → Prescriptive
4. Ghi rõ tiêu chí chấm visualization (15đ trong EDA)
5. Lưu vào file `Document/notes_rubric.md`

**Lưu ý:**
- EDA chiếm 60% tổng điểm → cần hiểu rubric EDA kỹ nhất
- Report chỉ tối đa 4 trang → mỗi biểu đồ/câu chữ phải thật sắc bén
- Ghi chú những điểm dễ mất điểm để cảnh báo cả team

**✅ Checklist kiểm thử:**
- [x] Đã liệt kê đầy đủ tiêu chí chấm cho từng phần (MCQ, EDA, Forecasting)
- [x] Đã xác định rõ 4 cấp độ EDA và yêu cầu từng cấp
- [x] Đã ghi chú giới hạn report (4 trang, NeurIPS format)
- [x] File `notes_rubric.md` đã commit lên GitHub

---

### Task 1.2: Lập dàn ý Report (NeurIPS template)
- **Mã Jira**: `[20/04-REPO-01.2]` | **Ưu tiên**: 🔴 Highest
- **Output**: `report_outline.md`

**Hướng dẫn từng bước:**
1. Tham khảo NeurIPS paper template (structure chuẩn)
2. Phác thảo các section chính:
   - **Introduction**: Business context, dataset overview
   - **EDA & Business Insights**: 5 module insights (chiếm phần lớn)
   - **Forecasting Methodology & Results**: Pipeline, model, SHAP
   - **Conclusions & Recommendations**: Prescriptive actions
3. Ước lượng phân bổ số trang cho mỗi section (tổng ≤ 4 trang)
4. Brainstorm các góc phân tích EDA tiềm năng cho Module ❶

**Lưu ý:**
- 4 trang rất ít → ưu tiên EDA insights vì chiếm 60% điểm
- Mỗi biểu đồ chèn vào report phải có caption và narrative đi kèm
- Dự kiến khoảng 5-7 biểu đồ cho toàn bộ report

**✅ Checklist kiểm thử:**
- [x] Outline có đủ các section: Intro, EDA, Forecasting, Conclusions
- [x] Đã phân bổ số trang hợp lý (EDA chiếm nhiều nhất)
- [x] Đã brainstorm ít nhất 5 góc phân tích EDA
- [x] File `report_outline.md` đã commit lên GitHub

---

## 🗓️ NGÀY 2 (21/04) — Module ❶ Descriptive

### Task 2.1: Revenue YoY Trend
- **Mã Jira**: `[21/04-EDA-M1.1]` | **Ưu tiên**: 🟠 High
- **Output**: `notebooks/02_M1_revenue_health.ipynb`

**Hướng dẫn từng bước:**
1. Load data: `sales.csv`, `order_items.csv`, `products.csv` (dùng `src/data_loader.py`)
2. Tính **Revenue theo năm** (2012-2022) → vẽ line chart YoY
3. Tính **Revenue Growth Rate** (%) từng năm
4. Tính **CAGR** (Compound Annual Growth Rate) toàn giai đoạn
5. Phân tích theo quý/tháng để phát hiện seasonality
6. Viết narrative mô tả xu hướng tăng trưởng

**Lưu ý:**
- Dùng `random_state=42` cho mọi thao tác random
- Biểu đồ phải có title, label trục, legend, annotation cho điểm đặc biệt
- Dùng relative path `../Data/...` để load data
- Comment rõ ràng cho từng cell code

**✅ Checklist kiểm thử:**
- [x] Revenue YoY trend chart hiển thị đúng (2012-2022)
- [x] Growth rate (%) đã tính và visualize
- [x] CAGR đã tính đúng công thức
- [x] Biểu đồ có title, xlabel, ylabel, legend
- [x] Notebook chạy được từ đầu đến cuối không lỗi

---

### Task 2.2: Margin & AOV Trend
- **Mã Jira**: `[21/04-EDA-M1.2]` | **Ưu tiên**: 🟠 High
- **Output**: `notebooks/02_M1_revenue_health.ipynb` (cùng notebook Task 2.1)

**Hướng dẫn từng bước:**
1. Tính **Gross Margin** = (Revenue - COGS) / Revenue theo thời gian
2. Tính **AOV** (Average Order Value) = Total Revenue / Number of Orders
3. Tính **RPU** (Revenue Per User) = Total Revenue / Unique Customers
4. Vẽ multi-line chart so sánh trend các chỉ số
5. Highlight các điểm bất thường (anomaly)

**Lưu ý:**
- Cần join `order_items` với `products` để có COGS
- AOV và RPU là 2 metric quan trọng để đánh giá sức khỏe doanh nghiệp
- Nếu Margin giảm → đây là insight quan trọng cho Diagnostic (Ngày 3)

**✅ Checklist kiểm thử:**
- [x] Gross Margin trend hiển thị đúng
- [x] AOV trend hiển thị đúng
- [x] RPU trend hiển thị đúng
- [x] Đã highlight các điểm bất thường
- [x] Narrative giải thích xu hướng đã viết

---

## 🗓️ NGÀY 3 (22/04) — Module ❶ Diagnostic

### Task 3.1: Margin Squeeze Analysis
- **Mã Jira**: `[22/04-EDA-M1.3]` | **Ưu tiên**: 🟠 High
- **Output**: `notebooks/03_M1_margin_diagnostic.ipynb`

**Hướng dẫn từng bước:**
1. Phân tích **tại sao Margin giảm**: So sánh tốc độ tăng COGS vs Revenue
2. Tạo biểu đồ **Revenue vs COGS** theo thời gian (dual-axis hoặc stacked)
3. Xác định thời điểm COGS > Revenue (nếu có, đặc biệt cuối 2022)
4. Phân tích nguyên nhân: product mix thay đổi? giá bán giảm? chi phí tăng?
5. Viết narrative: "Tại sao margin bị squeeze?"

**Lưu ý:**
- Đây là cấp **Diagnostic** — cần trả lời câu hỏi "TẠI SAO?"
- Dùng Pareto chart hoặc waterfall chart để thể hiện nguyên nhân
- Kết hợp dữ liệu `products` để phân tích theo category

**✅ Checklist kiểm thử:**
- [ ] Biểu đồ Revenue vs COGS theo timeline đã vẽ
- [ ] Đã xác định được thời điểm margin squeeze
- [ ] Root cause analysis có ít nhất 2-3 nguyên nhân
- [ ] Narrative trả lời rõ câu hỏi "Tại sao margin giảm?"

---

### Task 3.2: Revenue Breakdown by Segment
- **Mã Jira**: `[22/04-EDA-M1.4]` | **Ưu tiên**: 🟠 High
- **Output**: `notebooks/03_M1_margin_diagnostic.ipynb` (cùng notebook Task 3.1)

**Hướng dẫn từng bước:**
1. Breakdown revenue theo **product category/segment**
2. Tính RPU trend theo **nhóm khách hàng**
3. Xác định segment nào đang grow, segment nào đang decline
4. Vẽ stacked bar chart hoặc treemap
5. So sánh contribution % của mỗi segment qua các năm

**✅ Checklist kiểm thử:**
- [ ] Revenue breakdown theo category đã visualize
- [ ] RPU theo nhóm KH đã tính
- [ ] Đã xác định top segments grow/decline
- [ ] Narrative phân tích segment shift đã viết

---

## 🗓️ NGÀY 4 (23/04) — Module ❶ Predictive + Narrative

### Task 4.1: Revenue Forecast Interpretation
- **Mã Jira**: `[23/04-EDA-M1.5]` | **Ưu tiên**: 🟡 Medium
- **Output**: `notebooks/04_M1_revenue_predictive.ipynb`

**Hướng dẫn từng bước:**
1. Lấy output forecast từ **Hà Quốc Khánh** (model predictions cho 2023-2024)
2. Diễn giải kết quả dự báo từ **góc nhìn kinh doanh** (không phải kỹ thuật)
3. So sánh forecast vs actual trend → DN có tiếp tục tăng trưởng?
4. Tính dự kiến revenue growth rate cho 2023-2024
5. Vẽ chart: Historical + Forecast với confidence interval

**Lưu ý:**
- Cần sync với Hà Quốc Khánh để lấy forecast output
- Cấp Predictive = "Điều gì sẽ xảy ra?" — focus vào business interpretation
- Nếu HQ Khánh chưa có output → dùng simple trend extrapolation tạm

**✅ Checklist kiểm thử:**
- [ ] Forecast output đã được integrate vào notebook
- [ ] Biểu đồ Historical + Forecast đã vẽ
- [ ] Business interpretation đã viết (không phải technical)
- [ ] Growth rate dự kiến 2023-2024 đã tính

---

### Task 4.2: Module ❶ End-to-End Narrative
- **Mã Jira**: `[23/04-EDA-M1.6]` | **Ưu tiên**: 🟡 Medium
- **Output**: Narrative trong notebook

**Hướng dẫn từng bước:**
1. Tổng hợp toàn bộ findings từ Module ❶: Descriptive → Diagnostic → Predictive
2. Viết narrative mạch lạc theo flow:
   - "Doanh nghiệp tăng trưởng X% CAGR (Desc)"
   - "Tuy nhiên margin đang bị squeeze do Y (Diag)"
   - "Dự báo cho thấy Z (Pred)"
3. Đảm bảo mỗi insight có **số liệu cụ thể** đi kèm
4. Chuẩn bị sẵn để chuyển vào report

**✅ Checklist kiểm thử:**
- [ ] Narrative cover đủ 3 cấp: Descriptive, Diagnostic, Predictive
- [ ] Mỗi insight có số liệu cụ thể (%, $, growth rate)
- [ ] Flow logic mạch lạc, không nhảy ý
- [ ] Sẵn sàng copy vào report LaTeX

---

## 🗓️ NGÀY 5 (24/04) — Tổng hợp 5 Module + Prescriptive

### Task 5.1: Insights Summary từ 5 Module
- **Mã Jira**: `[24/04-EDA-SUM.1]` | **Ưu tiên**: 🟠 High
- **Output**: `eda_insights_summary.md`

**Hướng dẫn từng bước:**
1. Thu thập prescriptive recommendations từ cả 5 module:
   - Module ❶ (mình): Tăng trưởng & Tài chính
   - Module ❷ (Nhân): Khách hàng & Retention
   - Module ❸ (Nhân): Sản phẩm & Pricing
   - Module ❹ (NQ Khánh): Vận hành & Supply Chain
   - Module ❺ (NQ Khánh): Marketing & Digital
2. Tổng hợp thành prescriptive recommendations xuyên suốt
3. Liên kết cross-module: ví dụ margin squeeze (M❶) + stockout (M❹) + promo paradox (M❺)

**Lưu ý:**
- Cần đọc notebook của các thành viên khác → sync trước
- Focus vào **actionable recommendations** — không chỉ mô tả

**✅ Checklist kiểm thử:**
- [ ] Đã tổng hợp insights từ đủ 5 module
- [ ] Có ít nhất 1 prescriptive recommendation cho mỗi module
- [ ] Có cross-module insights (liên kết giữa các module)
- [ ] Recommendations là actionable (có thể thực hiện được)

---

### Task 5.2: Top 5 Câu chuyện cho Report
- **Mã Jira**: `[24/04-EDA-SUM.2]` | **Ưu tiên**: 🟠 High
- **Output**: `eda_insights_summary.md` (cùng file Task 5.1)

**Hướng dẫn từng bước:**
1. Từ tất cả insights, chọn ra **5 câu chuyện có impact cao nhất**
2. Sắp xếp theo thứ tự storytelling logic
3. Mỗi câu chuyện cần có: Bối cảnh → Vấn đề → Nguyên nhân → Đề xuất
4. Đánh giá mỗi câu chuyện theo tiêu chí rubric

**✅ Checklist kiểm thử:**
- [ ] Đã chọn đúng 5 câu chuyện
- [ ] Mỗi câu chuyện có đủ: Context → Problem → Root Cause → Recommendation
- [ ] Thứ tự sắp xếp logic và hấp dẫn
- [ ] Phù hợp để fit vào 4 trang report

---

## 🗓️ NGÀY 6 (25/04) — Narrative cho Visualization

### Task 6.1: Narrative Descriptive + Diagnostic
- **Mã Jira**: `[25/04-EDA-NAR.1]` | **Ưu tiên**: 🟢 Low
- **Output**: Update cấu trúc `.tex`

**Hướng dẫn từng bước:**
1. Với **mỗi biểu đồ** trong các notebook (tất cả module), viết:
   - **Mô tả**: Biểu đồ thể hiện gì?
   - **Key findings**: 2-3 điểm chính (kèm số liệu)
   - **Business implication**: Ý nghĩa kinh doanh
2. Đảm bảo narrative dùng ngôn ngữ business (không technical)

**✅ Checklist kiểm thử:**
- [ ] Mỗi biểu đồ Descriptive có narrative
- [ ] Mỗi biểu đồ Diagnostic có narrative
- [ ] Narrative có số liệu cụ thể
- [ ] Ngôn ngữ business, không quá kỹ thuật

---

### Task 6.2: Narrative Predictive + Prescriptive
- **Mã Jira**: `[25/04-EDA-NAR.2]` | **Ưu tiên**: 🟢 Low
- **Output**: Update cấu trúc `.tex`

**Hướng dẫn từng bước:**
1. Viết narrative cho phần Predictive: giải thích logic dự báo bằng ngôn ngữ business
2. Viết narrative cho phần Prescriptive: đề xuất hành động cụ thể
3. Mỗi đề xuất cần có: Expected impact + Timeline + Priority

**✅ Checklist kiểm thử:**
- [ ] Predictive narrative giải thích forecast bằng business language
- [ ] Prescriptive recommendations có expected impact
- [ ] Đề xuất có priority ranking

---

## 🗓️ NGÀY 7 (26/04) — Viết Report (Chủ lực)

### Task 7.1: Report — Introduction & Framework
- **Mã Jira**: `[26/04-REPO-02.1]` | **Ưu tiên**: 🔴 Highest
- **Output**: Source thư mục `report/`

**Hướng dẫn từng bước:**
1. Viết **Introduction**: Business context, dataset overview, objectives
2. Viết **Methodology/Framework**: Giải thích framework 4 cấp độ EDA
3. Giữ ngắn gọn (khoảng 0.5-0.75 trang)
4. Format theo NeurIPS LaTeX template

**Lưu ý:**
- Intro phải hook reader ngay từ câu đầu
- Nêu rõ business question chính mà team đang trả lời

**✅ Checklist kiểm thử:**
- [ ] Introduction có business context rõ ràng
- [ ] Framework 4 cấp độ được giải thích
- [ ] Không quá 0.75 trang
- [ ] LaTeX compile không lỗi

---

### Task 7.2: Report — EDA & Business Insights
- **Mã Jira**: `[26/04-REPO-02.2]` | **Ưu tiên**: 🔴 Highest
- **Output**: Source thư mục `report/`

**Hướng dẫn từng bước:**
1. Chuyển "Top 5 câu chuyện" vào report với storytelling mạch lạc
2. Chèn biểu đồ quan trọng nhất (5-7 charts max)
3. Mỗi chart cần caption + narrative ngắn gọn trong text
4. Kết nối các insights thành một câu chuyện tổng thể
5. Kết thúc bằng prescriptive recommendations

**Lưu ý:**
- Đây là phần **quan trọng nhất** — chiếm 60% điểm
- Chọn chart kỹ: chất lượng hơn số lượng
- Storytelling > liệt kê facts

**✅ Checklist kiểm thử:**
- [ ] 5 câu chuyện chính đã viết vào report
- [ ] Biểu đồ chèn đúng, có caption
- [ ] Flow từ Desc → Diag → Pred → Presc rõ ràng
- [ ] Chiếm khoảng 2-2.5 trang

---

## 🗓️ NGÀY 8 (27/04) — Polish Report

### Task 8.1: Polish Flow & Grammar
- **Mã Jira**: `[27/04-REPO-06.1]` | **Ưu tiên**: 🟠 High
- **Output**: `main.tex`

**Hướng dẫn từng bước:**
1. Đọc lại toàn bộ report từ đầu đến cuối
2. Chỉnh sửa theo review comments từ NQ Khánh
3. Làm mượt câu văn, sửa grammar
4. Đảm bảo flow logic xuyên suốt

### Task 8.2: Add References
- **Mã Jira**: `[27/04-REPO-06.2]` | **Ưu tiên**: 🟠 High
- **Output**: `report/references.bib`

**Hướng dẫn:** Thêm references cho các phương pháp phân tích, model, framework đã sử dụng.

**✅ Checklist kiểm thử (cả 2 task):**
- [ ] Report đọc mượt, không lỗi grammar
- [ ] Số liệu trong report khớp với code output
- [ ] References đầy đủ và đúng format BibTeX
- [ ] Report vẫn ≤ 4 trang sau khi polish

---

## 🗓️ NGÀY 9 (28/04) — Nộp bài

### Task 9.1: Export Final PDF
- **Mã Jira**: `[28/04-REPO-05.1]` | **Ưu tiên**: 🔴 Highest
- **Output**: `report_final.pdf`

**Hướng dẫn từng bước:**
1. Compile LaTeX lần cuối → kiểm tra PDF
2. Đảm bảo: ≤ 4 trang, hình ảnh rõ nét, text không bị cắt
3. Kiểm tra: page numbers, headers, captions, references

### Task 9.2: Nộp bài qua Submission Portal
- **Mã Jira**: `[28/04-REPO-05.2]` | **Ưu tiên**: 🔴 Highest
- **Output**: Screenshot submit hoàn tất

**Hướng dẫn từng bước:**
1. Điền form nộp bài đầy đủ thông tin
2. Upload: Report PDF, link GitHub, link Kaggle
3. Upload ảnh thẻ SV (nhận từ Nhân)
4. Tick xác nhận tham gia Chung kết 23/05
5. **Screenshot** xác nhận đã nộp thành công

**✅ Checklist nộp bài cuối cùng:**
- [ ] Report PDF ≤ 4 trang, NeurIPS template ✅
- [ ] Đáp án 10 câu MCQ đã điền
- [ ] `submission.csv` đã nộp Kaggle
- [ ] GitHub repo public, có README
- [ ] Link Kaggle submission
- [ ] Ảnh thẻ SV tất cả thành viên
- [ ] Tickbox xác nhận Chung kết 23/05
- [ ] Screenshot nộp bài thành công

---

## 🗓️ NGÀY 10 (29/04) — Buffer & Chuẩn bị Chung kết

### Task 10.1: Chuẩn bị Slide Pitch Deck
- **Mã Jira**: `[29/04-REPO-07.1]` | **Ưu tiên**: 🟢 Low
- **Output**: `presentation_outline.md`

**Hướng dẫn:** Soạn xương sống slide cho Chung kết 23/05. Review story flow.

**✅ Checklist:**
- [ ] Slide outline có đủ: Problem → Analysis → Insights → Recommendations
- [ ] Story flow logic và hấp dẫn

---

## ⚠️ Lưu ý tổng quan khi thực hiện

1. **EDA = 60% điểm** → Đầu tư nhiều nhất cho Ngày 2-5 (Module ❶ + Tổng hợp)
2. **Rubric yêu cầu 4 cấp độ EDA** — thiếu cấp nào mất điểm cấp đó
3. **Report chỉ 4 trang** → Chọn lọc kỹ, mỗi câu mỗi chart phải mang giá trị
4. **Storytelling > Liệt kê** → Kết nối insights thành câu chuyện, không chỉ show numbers
5. **Coding standards**: `random_state=42`, relative paths, comment đầy đủ
6. **Commit convention**: `[feat] Mô tả ngắn`, `[report] Mô tả ngắn`
7. **Sync với team**: Cần output từ HQ Khánh (forecast) và đọc notebook của NQ Khánh + Nhân
8. **Deadline**: Hoàn thành task trước 23:59 mỗi ngày. Trễ → báo trước 12:00 trưa

---

## 📊 Tóm tắt tiến độ

| Ngày | Task chính | Status |
|------|-----------|--------|
| 20/04 | Đọc đề + Lập outline report | ⏳ (1.1 Done) |
| 21/04 | M❶ Descriptive: Revenue, Margin, AOV | ✅ |
| 22/04 | M❶ Diagnostic: Margin squeeze, Segment | ⬜ |
| 23/04 | M❶ Predictive + Narrative end-to-end | ⬜ |
| 24/04 | Tổng hợp 5 module + Top 5 stories | ⬜ |
| 25/04 | Viết narrative cho tất cả biểu đồ | ⬜ |
| 26/04 | **Viết report** (Intro + EDA section) | ⬜ |
| 27/04 | Polish report + References | ⬜ |
| 28/04 | Export PDF + **NỘP BÀI** | ⬜ |
| 29/04 | Chuẩn bị slide Chung kết (optional) | ⬜ |

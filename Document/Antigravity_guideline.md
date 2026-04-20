# 🤖 Hướng dẫn sử dụng Antigravity — AI Coding Assistant

> Tài liệu này hướng dẫn chi tiết cách sử dụng **Antigravity** một cách hiệu quả trong suốt cuộc thi Datathon. Antigravity là một AI Agent mạnh mẽ có khả năng **viết code, chạy terminal, đọc/ghi file, và duyệt web** trực tiếp trên máy tính của bạn.

---

## 1. Tổng quan — Antigravity là gì?

Antigravity là một **AI Coding Assistant** hoạt động như một lập trình viên ảo ngồi cạnh bạn. Nó có thể:

| Khả năng | Ví dụ |
|---|---|
| ✍️ Viết & sửa code | Tạo notebook EDA, viết hàm xử lý data |
| 🖥️ Chạy lệnh Terminal | `git push`, `pip install`, `python script.py` |
| 📂 Đọc / Tạo file | Đọc CSV headers, tạo notebook mới, sửa markdown |
| 🔍 Tìm kiếm trong project | Grep tìm hàm, tìm file theo tên |
| 🌐 Tra cứu Internet | Tra cứu API docs, StackOverflow |
| 🐛 Debug lỗi | Phân tích traceback, đề xuất cách sửa |

> [!IMPORTANT]
> **Nguyên tắc vàng:** Antigravity là trợ lý, không phải thay thế. **Luôn kiểm tra lại** output của AI trước khi commit hoặc nộp bài.

---

## 2. Cách bắt đầu — Mở Antigravity

1. Mở **VS Code** (hoặc editor có tích hợp Antigravity).
2. Mở **Antigravity Panel** ở sidebar (biểu tượng chat).
3. Đảm bảo bạn đang mở đúng thư mục dự án: `Datathon_Outliers/`.
4. Bắt đầu gõ yêu cầu bằng tiếng Việt hoặc tiếng Anh.

> [!TIP]
> Antigravity sẽ tự động đọc file bạn đang mở trong editor. Hãy **mở sẵn file liên quan** trước khi hỏi để AI có ngữ cảnh tốt hơn.

---

## 3. Kỹ thuật Prompting — Cách ra lệnh hiệu quả

### 3.1 Nguyên tắc CLEAR

| Nguyên tắc | Mô tả | Ví dụ |
|---|---|---|
| **C**ontext | Cung cấp ngữ cảnh dự án / file | "Trong file `orders.csv` có cột `order_date`..." |
| **L**anguage | Nói rõ ngôn ngữ / thư viện muốn dùng | "Dùng Polars, không dùng Pandas" |
| **E**xpected output | Mô tả kết quả mong muốn | "Output là 1 biểu đồ bar chart có title và legend" |
| **A**ction | Hành động cụ thể cần làm | "Viết hàm", "Vẽ biểu đồ", "Fix lỗi này" |
| **R**estrictions | Ràng buộc / giới hạn | "Không dùng for loop, dùng vectorized operations" |

### 3.2 Prompt tệ vs Prompt tốt

❌ **Prompt tệ:**
```
Phân tích dữ liệu cho tôi
```

✅ **Prompt tốt:**
```
Đọc file Data/orders.csv bằng Polars, tính tổng doanh thu (cột total_amount) 
theo từng tháng trong năm 2022. Vẽ biểu đồ line chart với:
- Trục X: tháng (1-12)
- Trục Y: tổng doanh thu (format triệu VNĐ)
- Title: "Monthly Revenue Trend 2022"
Lưu kết quả vào file notebooks/02_revenue_trend.ipynb
```

### 3.3 Mẫu Prompt theo từng loại task

#### 📊 EDA — Phân tích dữ liệu
```
Đọc file Data/orders.csv và Data/customers.csv bằng Polars.
Join 2 bảng theo customer_id.
Phân tích phân bố đơn hàng theo vùng (region).
Vẽ biểu đồ horizontal bar chart, sắp xếp giảm dần.
Title: "Order Distribution by Region"
Lưu biểu đồ vào figures/order_by_region.png (dpi=300).
```

#### 🧮 MCQ — Giải trắc nghiệm
```
Đọc đề MCQ câu 3 trong file Document/Problem/mcq.md.
Dùng dữ liệu từ Data/payments.csv để tính toán đáp án.
Viết code rõ ràng, mỗi bước có comment giải thích.
In ra đáp án cuối cùng dạng: "Câu 3: Đáp án X — Giải thích: ..."
```

#### 📈 Forecasting — Dự báo
```
Đọc file Data/sales.csv bằng Polars.
Build model ARIMA(1,1,1) dự báo doanh thu 2023-2024.
Sử dụng random_state=42.
Tính metrics: MAE, RMSE, MAPE trên tập validation (2022).
Export kết quả theo format sample_submission.csv, lưu tại submissions/submission_v1.csv.
```

#### 📝 Report — Viết tài liệu
```
Dựa trên kết quả EDA ở notebook notebooks/02_revenue_trend.ipynb, 
viết một đoạn narrative 150 từ bằng tiếng Anh mô tả:
- Xu hướng chính
- 2-3 key findings (kèm con số cụ thể)
- Business implications
Format cho LaTeX NeurIPS template.
```

#### 🐛 Debug — Sửa lỗi
```
Code ở cell [5] trong notebook 02_eda.ipynb bị lỗi sau:
<paste traceback lỗi vào đây>
Hãy phân tích nguyên nhân và sửa cho tôi.
```

---

## 4. Nguyên tắc chia nhỏ Task — Chìa khoá cho output chất lượng

> [!IMPORTANT]
> AI hoạt động tốt nhất khi nhận **một yêu cầu rõ ràng, vừa đủ nhỏ**. Task càng lớn và mơ hồ → output càng kém chất lượng, dễ sai.

### 4.1 Tại sao phải chia nhỏ?

| Task lớn (❌ tránh) | Task nhỏ (✅ nên làm) |
|---|---|
| AI phải "đoán" nhiều → dễ sai hướng | AI tập trung vào 1 việc → chính xác hơn |
| Output dài → khó kiểm tra, dễ bỏ sót lỗi | Output ngắn → dễ review, phát hiện sai nhanh |
| Nếu sai phải làm lại toàn bộ | Nếu sai chỉ sửa 1 bước nhỏ |
| Tốn nhiều token (quota) cho 1 lần chạy | Tiết kiệm token, kiểm soát chi phí tốt hơn |

### 4.2 Cách chia nhỏ — Quy tắc "1 prompt = 1 việc"

**❌ Sai — Nhồi nhiều việc vào 1 prompt:**
```
Phân tích toàn bộ EDA cho dữ liệu orders: 
tính doanh thu theo tháng, theo vùng, theo sản phẩm, 
vẽ 5 biểu đồ, viết narrative, export figure.
```

**✅ Đúng — Chia thành chuỗi prompt nhỏ:**
```
Prompt 1: "Đọc file orders.csv bằng Polars, tính doanh thu theo tháng. Vẽ line chart."
Prompt 2: "Tiếp tục, tính doanh thu theo region. Vẽ bar chart ngang."
Prompt 3: "Dựa trên 2 biểu đồ trên, viết narrative 100 từ tiếng Anh mô tả key findings."
Prompt 4: "Export 2 biểu đồ trên vào figures/ với dpi=300."
```

### 4.3 Ví dụ thực tế — Chia nhỏ task EDA

| Bước | Prompt gợi ý | Output mong đợi |
|---|---|---|
| 1. Load & khám phá | "Đọc `orders.csv`, hiển thị 5 dòng đầu, kiểu dữ liệu, số null" | Hiểu cấu trúc data |
| 2. Tính toán chỉ số | "Tính doanh thu theo tháng, lưu vào DataFrame `monthly_rev`" | Bảng số liệu |
| 3. Vẽ biểu đồ | "Vẽ line chart từ `monthly_rev` với title, label đầy đủ" | Biểu đồ hoàn chỉnh |
| 4. Viết nhận xét | "Dựa trên chart, viết 3 key findings bằng tiếng Anh" | Đoạn văn narrative |
| 5. Export | "Lưu chart vào `figures/revenue_trend.png` dpi=300" | File ảnh sẵn sàng cho report |

> [!TIP]
> Mỗi bước xong → **Kiểm tra kết quả** → rồi mới sang bước tiếp theo. Đừng chạy liền 5 bước rồi mới kiểm tra.

---

## 5. Lên kế hoạch trước khi thực thi — "Plan trước, Code sau"

> [!IMPORTANT]
> Không bao giờ nhảy thẳng vào code mà không có kế hoạch. Hãy dành 5-10 phút đầu để nhờ AI **lên plan**, rồi mới bắt tay thực hiện.

### 5.1 Quy trình 3 bước: Plan → Execute → Verify

```
── Bước 1: PLAN (Lên kế hoạch) ──────────────────────────────
     Mô tả mục tiêu task cho AI
     → AI đề xuất các bước thực hiện
     → Bạn duyệt / điều chỉnh plan
                    ↓
── Bước 2: EXECUTE (Thực thi từng bước) ─────────────────────
     Thực hiện lần lượt từng bước trong plan
     → Kiểm tra output mỗi bước
     → Điều chỉnh nếu cần
                    ↓
── Bước 3: VERIFY (Kiểm tra tổng thể) ──────────────────────
     Chạy lại toàn bộ notebook / script
     → Kiểm tra kết quả cuối cùng
     → Commit & Push
```

### 5.2 Ví dụ thực tế — Lên plan trước khi làm EDA

**Bước 1 — Nhờ AI lên plan:**
```
Tôi cần phân tích EDA phần Descriptive cho doanh thu (revenue).
Dữ liệu: orders.csv, order_items.csv, geography.csv.
Hãy lên kế hoạch chi tiết các bước phân tích, 
liệt kê từng biểu đồ cần vẽ và insight mong đợi.
Chưa cần viết code, chỉ cần plan thôi.
```

**AI sẽ trả lời dạng:**
```
Plan phân tích Revenue Descriptive:
1. Tổng doanh thu theo tháng (line chart) → Tìm trend & seasonality
2. Doanh thu theo region (bar chart) → Tìm vùng mạnh/yếu  
3. Doanh thu theo category (treemap) → Tìm product mix
4. Phân bố giá trị đơn hàng (histogram) → Hiểu hành vi mua
5. Top 10 sản phẩm doanh thu cao nhất (horizontal bar)
```

**Bước 2 — Duyệt plan rồi bắt đầu thực hiện từng bước:**
```
Plan ổn rồi. Bắt đầu làm bước 1: Tổng doanh thu theo tháng.
Dùng Polars, vẽ line chart với Matplotlib.
```

### 5.3 Khi nào cần lên plan?

| Cần lên plan ✅ | Không cần plan ❌ |
|---|---|
| Task EDA mới (chưa biết phân tích gì) | Fix 1 lỗi nhỏ, sửa title biểu đồ |
| Xây dựng model Forecasting | Thêm 1 cột vào DataFrame |
| Viết 1 section trong report | Đổi màu biểu đồ |
| Thiết kế feature engineering pipeline | Commit & push code |
| Giải MCQ nhiều câu cùng lúc | Cài thêm 1 thư viện |

---

## 6. Chọn Model & Chế độ phù hợp — Tối ưu Quota

> [!WARNING]
> Antigravity có **giới hạn quota** (số lượng request/ngày). Chọn sai model hoặc sai chế độ sẽ **lãng phí quota** mà không đạt kết quả tốt. Hãy đọc kỹ phần này.

### 6.1 Hai chế độ hoạt động

Antigravity có **2 chế độ** chính, chuyển đổi bằng toggle trên giao diện:

| Chế độ | Biểu tượng | Đặc điểm | Khi nào dùng |
|---|---|---|---|
| **⚡ Fast Mode** | Tốc độ nhanh | Thực thi ngay, không lên plan. Phản hồi nhanh, tiết kiệm quota. | Task đơn giản, rõ ràng, không cần suy nghĩ nhiều |
| **📋 Planning Mode** | Suy nghĩ kỹ | AI sẽ lên plan → chờ bạn duyệt → mới thực thi. Tốn nhiều quota hơn nhưng chất lượng cao hơn. | Task phức tạp, cần chiến lược, nhiều bước |

### 6.2 Bảng chọn Model & Chế độ theo loại task

| Loại task | Model gợi ý | Chế độ | Lý do |
|---|---|---|---|
| Fix lỗi nhỏ, sửa typo | Gemini Flash | ⚡ Fast | Nhanh, rẻ, lỗi nhỏ không cần model mạnh |
| Viết utility function đơn giản | Gemini Flash | ⚡ Fast | Code ngắn, logic đơn giản |
| Giải 1-2 câu MCQ | Gemini Pro | ⚡ Fast | Cần tính toán chính xác nhưng logic không phức tạp |
| Vẽ 1 biểu đồ EDA | Gemini Pro | ⚡ Fast | Customization nhiều nhưng mỗi lần 1 biểu đồ |
| Viết notebook EDA hoàn chỉnh | Gemini Pro | 📋 Planning | Nhiều bước, cần plan trước |
| Feature engineering pipeline | Claude Sonnet | 📋 Planning | Logic phức tạp, cần hiểu domain |
| Build model Forecasting | Claude Sonnet | 📋 Planning | Nhiều bước, cần chiến lược rõ ràng |
| Debug lỗi phức tạp, lỗi logic | Claude Sonnet | ⚡ Fast | Cần suy luận sâu nhưng tập trung 1 vấn đề |
| Viết report section (narrative) | Claude Opus | 📋 Planning | Cần chất lượng văn bản cao, suy luận sâu |
| Thiết kế kiến trúc, strategy | Claude Opus | 📋 Planning | Quyết định chiến lược, cần phân tích nhiều chiều |

### 6.3 Chiến lược tiết kiệm Quota hàng ngày

```
🌅 Đầu ngày (quota đầy):
   → Dùng Planning Mode + Model mạnh (Sonnet/Opus) cho task khó
   → Lên plan cho cả ngày

🌤️ Giữa ngày (quota trung bình):
   → Dùng Fast Mode + Gemini Pro cho task EDA, code thông thường
   → Thực thi các bước theo plan đã duyệt buổi sáng

🌙 Cuối ngày (quota hạn chế):
   → Dùng Fast Mode + Gemini Flash cho fix lỗi nhỏ, format code
   → Commit & push code
```

### 6.4 Mẹo tối ưu quota

1. **Dùng Flash cho thử nghiệm** — Khi chưa chắc prompt đúng chưa, thử với Flash trước (rẻ nhất). Khi prompt đã ổn → chuyển qua model mạnh hơn.
2. **Dùng Planning Mode 1 lần, Fast Mode nhiều lần** — Lên plan bằng Planning Mode, rồi thực thi từng bước bằng Fast Mode.
3. **Mở file context trước** — AI không cần tốn token để đọc file nếu bạn đã mở sẵn.
4. **Tránh lặp lại prompt** — Nếu AI hiểu sai, hãy sửa prompt cho rõ hơn thay vì gửi lại cùng nội dung.
5. **Gộp các fix nhỏ** — Thay vì 5 prompt sửa 5 lỗi nhỏ riêng lẻ, hãy gom vào 1 prompt: "Sửa các lỗi sau: ..."

> [!TIP]
> **Quy tắc ngón tay cái:** Flash tiết kiệm gấp ~5 lần so với Opus. Chỉ dùng Opus khi thật sự cần thiết (report, chiến lược, debug khó).

---

## 7. Quy trình làm việc với Antigravity

### 7.1 Workflow chuẩn cho mỗi task

```
1. Mở file liên quan trong editor
        ↓
2. Chọn Model & Chế độ phù hợp (xem Mục 6)
        ↓
3. Nếu task phức tạp → Nhờ AI lên plan trước (xem Mục 5)
        ↓
4. Mô tả task rõ ràng cho AI (theo nguyên tắc CLEAR, Mục 3)
        ↓
5. Chia nhỏ thành từng bước, thực hiện lần lượt (xem Mục 4)
        ↓
6. Mỗi bước: Xem AI thực hiện → Approve/Reject lệnh terminal
        ↓
7. Kiểm tra output (chạy thử code, xem biểu đồ)
        ↓
8. Yêu cầu chỉnh sửa nếu cần ("sửa lại title thành...", "thêm legend...")
        ↓
9. Hài lòng → Commit & Push lên GitHub
```

### 7.2 Nhờ AI thao tác Git

Thay vì tự gõ lệnh Git, bạn có thể nhờ AI làm hoàn toàn:

```
Commit tất cả thay đổi với message "[feat] Add revenue EDA notebook" 
rồi push lên branch feature/le-bao-khanh
```

```
Tạo branch mới tên feature/mcq-answers từ develop, 
rồi checkout sang branch đó.
```

```
Pull code mới nhất từ develop về branch hiện tại.
```

> [!WARNING]
> **Quan trọng:** Antigravity sẽ hỏi xác nhận trước khi chạy các lệnh Git. **Đọc kỹ lệnh** trước khi bấm Approve — đặc biệt với `git push`, `git merge`, `git reset`.

---

## 8. Các lưu ý quan trọng

### ✅ Nên làm

- **Mở file context** trước khi hỏi AI — AI hiểu rõ hơn khi "thấy" code bạn đang làm.
- **Chia nhỏ yêu cầu** — Thay vì "làm toàn bộ EDA", hãy chia thành: "phân tích doanh thu" → "phân tích khách hàng" → "phân tích trả hàng".
- **Lên plan trước** — Dành 5 phút đầu để nhờ AI lên kế hoạch, rồi mới thực hiện.
- **Review code AI viết** — Đọc qua logic, kiểm tra con số, chạy thử trước khi commit.
- **Copy-paste lỗi đầy đủ** — Khi debug, đưa toàn bộ traceback cho AI, đừng chỉ mô tả chung chung.
- **Lưu context cho AI** — Khi mở session mới, hãy tóm tắt: "hôm qua tôi đang làm EDA revenue, cần tiếp tục phần phân tích theo vùng."
- **Chọn đúng chế độ** — Fast Mode cho việc nhỏ, Planning Mode cho việc lớn.

### ❌ Không nên làm

- **Không prompt mơ hồ** — "Phân tích cho tôi" → AI không biết phân tích gì, với data nào.
- **Không nhồi nhiều việc vào 1 prompt** — Chia nhỏ ra, mỗi prompt 1 việc.
- **Không approve lệnh không hiểu** — Nếu AI đề xuất lệnh terminal mà bạn không hiểu, hãy hỏi lại trước.
- **Không commit code chưa kiểm tra** — Đặc biệt code liên quan tính toán số liệu, MCQ answers.
- **Không để AI tự ý merge** — Việc merge vào `develop` do **Tech Lead** phụ trách.
- **Không gửi API keys hay mật khẩu** cho AI.
- **Không dùng Opus cho việc đơn giản** — Lãng phí quota, dùng Flash/Pro là đủ.

---

## 9. Xử lý khi AI trả lời sai hoặc không tốt

| Tình huống | Cách xử lý |
|---|---|
| Code chạy lỗi | Copy-paste lỗi, gửi lại cho AI: "Code bị lỗi này, sửa lại đi." |
| Kết quả không đúng ý | Mô tả lại cụ thể hơn: "Tôi muốn ... thay vì ..." |
| AI lặp đi lặp lại sai | Đổi sang model mạnh hơn (ví dụ: Flash → Pro → Opus) |
| AI không hiểu ngữ cảnh | Cung cấp thêm thông tin: mở file liên quan, paste thêm dữ liệu |
| Output quá dài, lan man | Yêu cầu rõ: "Chỉ trả lời phần X, không cần phần Y." |
| Lỗi quá phức tạp | Dừng lại, hỏi **Tech Lead** (Nguyễn Quốc Khánh) để hỗ trợ |

---

## 10. Ví dụ thực tế — Workflow End-to-End

### Ví dụ: Thực hiện task [21/04-MCQ-01.1] — Giải MCQ Q1-Q5

**Bước 1 — Chọn chế độ:**
> Chọn **Gemini Pro** + **Fast Mode** (MCQ cần chính xác nhưng logic mỗi câu không quá phức tạp).

**Bước 2 — Mở context:**
> Mở sẵn file đề MCQ và file `src/data_loader.py` trong editor.

**Bước 3 — Prompt cho AI (từng câu một):**
```
Đọc file đề MCQ câu 1 tại Document/Problem/.
Dùng data_loader từ src/data_loader.py để load data cần thiết.
Viết code Python + Polars để giải, có comment giải thích.
In ra đáp án cuối cùng dạng: "Câu 1: Đáp án X — Giải thích: ..."
```
> ✅ Kiểm tra đáp án câu 1 → Đúng → Tiếp tục câu 2.

```
Tiếp tục giải câu 2 với cách tiếp cận tương tự.
```
> ✅ Kiểm tra câu 2 → OK → Lặp lại đến câu 5.

**Bước 4 — Gom vào notebook:**
```
Gom code giải câu 1-5 vào notebooks/01_mcq_answers.ipynb.
Mỗi câu 1 section riêng, có heading rõ ràng.
```

**Bước 5 — Kiểm tra:**
> Mở notebook, chạy Run All, kiểm tra đáp án có logic không.

**Bước 6 — Commit:**
```
Commit file notebooks/01_mcq_answers.ipynb 
với message "[feat] Solve MCQ Q1-Q5" 
rồi push lên branch feature/luu-nguyen-thien-nhan
```

---

## 11. Hệ thống hỗ trợ

Khi gặp vấn đề, tuân thủ thứ tự xử lý:

```
Tự tìm hiểu (5 phút)
    ↓ Không được
Hỏi Antigravity (AI)
    ↓ AI không giải quyết được
Hỏi Tech Lead (Nguyễn Quốc Khánh) qua chat
    ↓ Cần thảo luận sâu
Lên lịch họp nhanh 15 phút với team
```

---

*📝 Tài liệu tạo bởi:* `Nguyễn Quốc Khánh (Tech Lead)` *— Cập nhật:* `20/04/2026`

# 📋 Kế hoạch Datathon 2026 — Team Outliers (10 ngày)

## Thông tin đội thi
| Thành viên | Vai trò | Nhiệm vụ chính |
|-----------|---------|-----------------|
| **Lê Bảo Khánh** | Business Analyst | EDA insights, business storytelling, viết report |
| **Nguyễn Quốc Khánh** | Tech Lead | Kiến trúc tổng thể, Forecasting model, code review |
| **Lưu Nguyễn Thiện Nhân** | Data Engineer | Data pipeline, MCQ, EDA visualization |
| **Hà Quốc Khánh** | ML Engineer | Feature engineering, Forecasting model, Kaggle submission |

---

## Phân bổ điểm & Chiến lược ưu tiên

| Phần | Điểm | Tỷ trọng | Độ ưu tiên | Lý do |
|------|------|----------|------------|-------|
| MCQ (10 câu) | 20 | 20% | 🟢 Cao — Làm sớm | Điểm chắc chắn, chỉ cần code đúng |
| EDA | 60 | 60% | 🔴 **Cao nhất** | Chiếm 60% tổng điểm, cần đầu tư nhiều nhất |
| Forecasting | 20 | 20% | 🟡 Trung bình | Cần thời gian train & tune model |

---

## Tổng quan dữ liệu

| File | Số dòng | Vai trò |
|------|---------|---------|
| `orders.csv` | 646,946 | Bảng giao dịch chính |
| `order_items.csv` | 714,670 | Chi tiết sản phẩm trong đơn |
| `payments.csv` | 646,946 | Thanh toán (1:1 với orders) |
| `shipments.csv` | 566,068 | Vận chuyển |
| `customers.csv` | 121,931 | Khách hàng |
| `reviews.csv` | 113,552 | Đánh giá |
| `inventory.csv` | 60,248 | Tồn kho hàng tháng |
| `returns.csv` | 39,940 | Trả hàng |
| `geography.csv` | 39,949 | Địa lý |
| `web_traffic.csv` | 3,653 | Lưu lượng web hàng ngày |
| `sales.csv` | 3,834 | Doanh thu train (2012-2022) |
| `sample_submission.csv` | 549 | Mẫu nộp bài (2023-2024) |
| `products.csv` | 2,413 | Danh mục sản phẩm |
| `promotions.csv` | 50 | Chiến dịch khuyến mãi |

---

## 📅 Kế hoạch chi tiết 10 ngày

---

### Ngày 1 — Setup & Khám phá dữ liệu
> **Mục tiêu**: Mọi người đều hiểu rõ dữ liệu, setup xong môi trường, chia nhánh GitHub.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** (Lead) | Setup GitHub repo, cấu trúc thư mục, tạo branch cho từng người. Viết script load data chung (`utils/data_loader.py`) bằng Polars. | Repo + data loader |
| **Lưu Nguyễn Thiện Nhân** | Chạy data profiling toàn bộ 15 file: kiểm tra null, kiểu dữ liệu, phân bố, outlier. | Notebook `00_data_profiling.ipynb` |
| **Hà Quốc Khánh** | Đọc hiểu `sales.csv` & `sample_submission.csv`. Phân tích time series: trend, seasonality, stationarity. | Notebook `00_sales_eda.ipynb` |
| **Lê Bảo Khánh** | Đọc đề kỹ, nghiên cứu rubric chấm điểm. Lập dàn ý report (NeurIPS template). Brainstorm các góc phân tích EDA tiềm năng. | File `report_outline.md` |

---

### 📦 Phân công EDA theo Module Kinh doanh

> **Nguyên tắc**: Mỗi người sở hữu (own) 1-2 module end-to-end, tự chịu trách nhiệm làm từ Descriptive → Diagnostic → Predictive → Prescriptive cho module đó.

| Module | Câu hỏi cốt lõi | Owner | Dữ liệu chính |
|--------|-----------------|-------|---------------|
| ❶ Tăng trưởng & Tài chính | Doanh nghiệp tăng trưởng hay suy giảm? | **Lê Bảo Khánh** | `sales`, `order_items`, `products` |
| ❷ Khách hàng & Retention | KH trung thành đến mức nào? | **Lưu Nguyễn Thiện Nhân** | `customers`, `orders`, `payments`, `reviews` |
| ❸ Sản phẩm & Pricing | Bán cái gì, giá bao nhiêu? | **Lưu Nguyễn Thiện Nhân** | `products`, `order_items`, `returns`, `inventory` |
| ❹ Vận hành & Supply Chain | Vận hành có hiệu quả không? | **Nguyễn Quốc Khánh** | `inventory`, `shipments`, `returns`, `orders` |
| ❺ Marketing & Digital | Kênh nào hiệu quả? | **Nguyễn Quốc Khánh** | `web_traffic`, `orders`, `promotions`, `customers` |

> **Hà Quốc Khánh** tập trung 100% cho Forecasting. **Lê Bảo Khánh** ngoài Module ❶ còn giữ vai trò Tổng hợp & Narrative cho report.

---

### Ngày 2 — Giải MCQ + Khởi động EDA
> **Mục tiêu**: Hoàn thành MCQ (20đ chắc chắn), bắt đầu EDA Module ❶.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Review code MCQ của Nhân. Bắt đầu thiết kế feature engineering pipeline cho Forecasting. | Code review + FE design doc |
| **Lưu Nguyễn Thiện Nhân** | Viết code giải 10 câu MCQ (Q1→Q10). Mỗi câu = 1 cell code rõ ràng, có comment. | Notebook `01_mcq_answers.ipynb` |
| **Hà Quốc Khánh** | Baseline forecasting model: ARIMA hoặc Prophet trên `sales.csv`. Submit lên Kaggle lần 1. | Notebook `01_baseline_forecast.ipynb` + Kaggle submission |
| **Lê Bảo Khánh** | **Module ❶ Descriptive**: Revenue YoY trend, Gross Margin trend, AOV trend, Revenue per Customer (RPU). | Notebook `02_M1_revenue_health.ipynb` |

---

### Ngày 3 — EDA Descriptive (đa module) & bắt đầu Diagnostic
> **Mục tiêu**: Mỗi người hoàn thành Descriptive cho module mình, bắt đầu Diagnostic.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | **Module ❹ Descriptive**: Delivery performance, Fulfillment rate, Return cost tổng quan. **Module ❺ Descriptive**: Traffic overview, Channel attribution, Conversion rate theo kênh. | `02_M4_operations_overview.ipynb` + `02_M5_marketing_overview.ipynb` |
| **Lưu Nguyễn Thiện Nhân** | **Module ❷ Descriptive**: Repeat Purchase Rate, Cohort Retention, RFM Segmentation (`customers` ↔ `orders` ↔ `payments`). | Notebook `02_M2_customer_retention.ipynb` |
| **Hà Quốc Khánh** | Feature engineering cho Forecasting: tạo features từ `inventory`, `web_traffic`, `promotions`. | Script `features/build_features.py` |
| **Lê Bảo Khánh** | **Module ❶ Diagnostic**: Tại sao margin giảm? COGS > Revenue cuối 2022. RPU trend. Revenue breakdown theo segment. Viết narrative đi kèm. | Notebook `03_M1_margin_diagnostic.ipynb` + narrative |

---

### Ngày 4 — EDA Diagnostic sâu
> **Mục tiêu**: Trả lời "Tại sao?" — nguyên nhân gốc rễ cho từng module.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | **Module ❹ Diagnostic**: Stockout impact (lost revenue), Overstock cost, Delivery gap theo vùng. **Module ❺ Diagnostic**: Promo ROI, Promotion Paradox (trước/trong/sau KM), Bounce rate analysis. | `03_M4_supply_chain_diagnostic.ipynb` + `03_M5_promo_effectiveness.ipynb` |
| **Lưu Nguyễn Thiện Nhân** | **Module ❷ Diagnostic**: CLV, Acquisition Channel Effectiveness. **Module ❸ Descriptive**: BCG Matrix, Price vs. Volume, Size Distribution vs. Return Rate. | `03_M2_clv_analysis.ipynb` + `02_M3_product_portfolio.ipynb` |
| **Hà Quốc Khánh** | Xây dựng model Forecasting v2: XGBoost/LightGBM với features mới. Submit Kaggle lần 2. | Notebook `02_advanced_forecast.ipynb` |
| **Lê Bảo Khánh** | **Module ❶ Predictive**: Revenue forecast interpretation (dùng output từ HQ Khánh). Viết narrative tổng hợp Module ❶ (Desc → Diag → Pred). | Notebook `04_M1_revenue_predictive.ipynb` + narrative |

---

### Ngày 5 — EDA Predictive & Prescriptive (Đạt 4 cấp độ)
> **Mục tiêu**: Hoàn thành 4 cấp độ phân tích cho tất cả 5 module để đạt điểm tối đa rubric.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | **Module ❹ Prescriptive**: Đề xuất reorder point, giảm delivery time, size guide ROI. **Module ❺ Prescriptive**: Tái phân bổ ngân sách marketing, chiến lược KM theo segment (fixed vs. percentage). | `04_M4_supply_prescriptive.ipynb` + `04_M5_marketing_prescriptive.ipynb` |
| **Lưu Nguyễn Thiện Nhân** | **Module ❸ Diagnostic + Prescriptive**: Size × Return Rate, Color preference, đề xuất loại bỏ Dogs / mở rộng Premium. **Module ❷ Prescriptive**: Loyalty program cho Champions, Win-back campaign cho At Risk. | `03_M3_product_diagnostic.ipynb` + `04_M2_customer_prescriptive.ipynb` |
| **Hà Quốc Khánh** | Forecasting v3: Ensemble model (XGBoost + Prophet + LSTM). Hyperparameter tuning. | Notebook `03_ensemble_forecast.ipynb` |
| **Lê Bảo Khánh** | **Tổng hợp 5 module**: Viết prescriptive recommendations xuyên suốt. Xây dựng "Top 5 câu chuyện" cho report (theo Business_Analytics.md §7). | File `eda_insights_summary.md` |

---

### Ngày 6 — Hoàn thiện Visualization
> **Mục tiêu**: Nâng cấp toàn bộ biểu đồ lên chất lượng trình bày (15đ rubric).

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Review toàn bộ notebook EDA (5 module). Đảm bảo code quality, reproducibility. | Code review comments |
| **Lưu Nguyễn Thiện Nhân** | Thiết kế & tạo các biểu đồ chất lượng cao cho tất cả modules: color palette thống nhất, tiêu đề, nhãn trục, chú thích đầy đủ. Export HQ figures. | Thư mục `figures/` |
| **Hà Quốc Khánh** | Forecasting: Cross-validation đúng chiều thời gian. SHAP values / Feature importance. Submit Kaggle lần 3. | Notebook `04_final_forecast.ipynb` |
| **Lê Bảo Khánh** | Viết narrative cho từng biểu đồ across all modules: mô tả, key findings (có số liệu), business implications. | Draft report sections |

---

### Ngày 7 — Viết Report (NeurIPS format)
> **Mục tiêu**: Hoàn thành draft báo cáo 4 trang.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Viết phần Forecasting trong report: pipeline, methodology, results. Thêm SHAP plot. | Report Section 3 |
| **Lưu Nguyễn Thiện Nhân** | Chèn biểu đồ vào report. Format LaTeX. Đảm bảo figure captions đầy đủ. | Report formatting |
| **Hà Quốc Khánh** | Final tuning model. Submit Kaggle lần cuối (best score). Viết phần kỹ thuật model. | Final Kaggle submission |
| **Lê Bảo Khánh** | **Chủ lực viết report**: Introduction, EDA analysis, Business insights, Conclusions. Đảm bảo storytelling mạch lạc. | Report draft v1 |

---

### Ngày 8 — Review & Polish Report
> **Mục tiêu**: Report hoàn chỉnh, sẵn sàng nộp.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Review toàn diện report. Kiểm tra logic, số liệu, công thức. Cross-check với code. | Review comments |
| **Lưu Nguyễn Thiện Nhân** | Kiểm tra reproducibility: chạy lại toàn bộ notebook từ đầu. Fix bugs nếu có. | Verified notebooks |
| **Hà Quốc Khánh** | Chuẩn bị `submission.csv` final. Double-check format khớp `sample_submission.csv`. | Final `submission.csv` |
| **Lê Bảo Khánh** | Chỉnh sửa report theo review. Polish language, grammar, flow. Thêm references. | Report v2 |

---

### Ngày 9 — Nộp bài & Double-check
> **Mục tiêu**: Nộp đầy đủ tất cả deliverables.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Clean up GitHub repo: README, folder structure, requirements.txt. Push final code. | GitHub repo ready |
| **Lưu Nguyễn Thiện Nhân** | MCQ: Double-check đáp án 10 câu. Chuẩn bị ảnh thẻ sinh viên của cả team. | MCQ answers verified |
| **Hà Quốc Khánh** | Kaggle: Kiểm tra submission cuối cùng. Screenshot leaderboard score. | Evidence submission |
| **Lê Bảo Khánh** | Export report PDF final. Điền form nộp bài. Upload tất cả tài liệu. | **Nộp bài hoàn tất** |

---

### Ngày 10 — Buffer & Backup
> **Mục tiêu**: Dự phòng cho rủi ro, cải thiện nếu còn thời gian.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Kiểm tra lại toàn bộ submission. Backup repo. Chuẩn bị cho Vòng Chung kết. | Final check |
| **Lưu Nguyễn Thiện Nhân** | Cải thiện visualization nếu cần. Thêm interactive dashboard (bonus). | Optional dashboard |
| **Hà Quốc Khánh** | Thử thêm model mới hoặc feature mới nếu Kaggle score chưa tối ưu. | Optional improvement |
| **Lê Bảo Khánh** | Chuẩn bị slide tóm tắt (nếu cần cho Chung kết 23/05). Review story flow. | Presentation draft |

---

## 📊 Timeline tổng quan

```
Ngày:  1    2    3    4    5    6    7    8    9    10
       │    │    │    │    │    │    │    │    │    │
MCQ:   ░░░░░████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████░░░
       Setup Giải                              Check
       │    │    │    │    │    │    │    │    │    │
EDA:   ░░░░░░░░░░████████████████████░░░░░░░░░░░░░░░░
                 Descriptive→Diagnostic→Predict→Presc
       │    │    │    │    │    │    │    │    │    │
Fore:  ░░░░░████░░░░░████░░░░░████░████░░░░░░░░░░░░░
       EDA  Base      v2       v3  Final
       │    │    │    │    │    │    │    │    │    │
Report:░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████░░░░░
                                    Draft→Review→Submit
```

---

## 🎯 Checklist nộp bài cuối cùng

- [ ] Đáp án 10 câu MCQ đã điền vào form
- [ ] Report PDF (≤ 4 trang, NeurIPS template)
- [ ] `submission.csv` đã nộp trên Kaggle
- [ ] GitHub repository (public, có README)
- [ ] Link Kaggle submission
- [ ] Ảnh thẻ sinh viên tất cả thành viên
- [ ] Tickbox xác nhận tham gia Chung kết 23/05

---

## ⚠️ Lưu ý quan trọng

1. **EDA chiếm 60% điểm** → Đầu tư thời gian nhiều nhất cho phần này (Ngày 2-6).
2. **Rubric EDA yêu cầu 4 cấp độ**: Descriptive → Diagnostic → Predictive → Prescriptive. Thiếu bất kỳ cấp nào sẽ mất điểm.
3. **Report chỉ 4 trang** → Mỗi biểu đồ phải thật sắc bén, mỗi câu phải mang giá trị.
4. **Forecasting**: Không dùng dữ liệu ngoài. Phải giải thích được model (SHAP/feature importance).
5. **Reproducibility**: Đặt random seed, ghi rõ thư viện + version trong `requirements.txt`.

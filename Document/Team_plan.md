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

### Ngày 2 — Giải MCQ + Khởi động EDA
> **Mục tiêu**: Hoàn thành MCQ (20đ chắc chắn), bắt đầu EDA.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Review code MCQ của C. Bắt đầu thiết kế feature engineering pipeline cho Forecasting. | Code review + FE design doc |
| **Lưu Nguyễn Thiện Nhân** | Viết code giải 10 câu MCQ (Q1→Q10). Mỗi câu = 1 cell code rõ ràng, có comment. | Notebook `01_mcq_answers.ipynb` |
| **Hà Quốc Khánh** | Baseline forecasting model: ARIMA hoặc Prophet trên `sales.csv`. Submit lên Kaggle lần 1. | Notebook `01_baseline_forecast.ipynb` + Kaggle submission |
| **Lê Bảo Khánh** | Bắt đầu phân tích EDA cấp Descriptive: tổng quan doanh thu theo thời gian, phân bố đơn hàng theo vùng/thành phố. | Draft EDA section 1 |

---

### Ngày 3 — EDA Descriptive & Diagnostic
> **Mục tiêu**: Hoàn thành tầng Descriptive, bắt đầu Diagnostic.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | EDA: Phân tích hiệu quả khuyến mãi (`promotions` ↔ `order_items` ↔ `orders`). So sánh doanh thu có/không KM. | Notebook `02_promo_analysis.ipynb` |
| **Lưu Nguyễn Thiện Nhân** | EDA: Phân tích hành vi khách hàng — RFM segmentation (`customers` ↔ `orders` ↔ `payments`). | Notebook `02_customer_rfm.ipynb` |
| **Hà Quốc Khánh** | Feature engineering cho Forecasting: tạo features từ `inventory`, `web_traffic`, `promotions`. | Script `features/build_features.py` |
| **Lê Bảo Khánh** | EDA: Phân tích sản phẩm — Top sellers, margin analysis, seasonal trends theo category/segment. Viết narrative đi kèm biểu đồ. | Notebook `02_product_analysis.ipynb` + narrative |

---

### Ngày 4 — EDA Diagnostic sâu
> **Mục tiêu**: Trả lời "Tại sao?" — nguyên nhân gốc rễ.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | EDA: Phân tích tồn kho vs. doanh thu — stockout impact, overstock cost. Kết nối `inventory` ↔ `sales`. | Notebook `03_inventory_impact.ipynb` |
| **Lưu Nguyễn Thiện Nhân** | EDA: Phân tích trả hàng — return rate theo category, size, region. Root cause analysis. | Notebook `03_return_analysis.ipynb` |
| **Hà Quốc Khánh** | Xây dựng model Forecasting v2: XGBoost/LightGBM với features mới. Submit Kaggle lần 2. | Notebook `02_advanced_forecast.ipynb` |
| **Lê Bảo Khánh** | EDA: Phân tích web traffic ↔ conversion ↔ doanh thu. Kênh nào hiệu quả nhất? | Notebook `03_traffic_analysis.ipynb` + narrative |

---

### Ngày 5 — EDA Predictive & Prescriptive (Đạt 4 cấp độ)
> **Mục tiêu**: Hoàn thành 4 cấp độ phân tích (Descriptive → Diagnostic → Predictive → Prescriptive) để đạt điểm tối đa rubric.

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | EDA Predictive: Customer churn prediction — xác suất khách hàng không quay lại. | Notebook `04_churn_prediction.ipynb` |
| **Lưu Nguyễn Thiện Nhân** | EDA Prescriptive: Đề xuất tối ưu pricing/discount dựa trên elasticity analysis. | Notebook `04_pricing_optimization.ipynb` |
| **Hà Quốc Khánh** | Forecasting v3: Ensemble model (XGBoost + Prophet + LSTM). Hyperparameter tuning. | Notebook `03_ensemble_forecast.ipynb` |
| **Lê Bảo Khánh** | Tổng hợp toàn bộ EDA insights. Viết phần Prescriptive: actionable recommendations cho doanh nghiệp. | File `eda_insights_summary.md` |

---

### Ngày 6 — Hoàn thiện Visualization
> **Mục tiêu**: Nâng cấp toàn bộ biểu đồ lên chất lượng trình bày (15đ rubric).

| Người | Công việc | Output |
|-------|-----------|--------|
| **Nguyễn Quốc Khánh** | Review toàn bộ notebook EDA. Đảm bảo code quality, reproducibility. | Code review comments |
| **Lưu Nguyễn Thiện Nhân** | Thiết kế & tạo các biểu đồ chất lượng cao: color palette thống nhất, tiêu đề, nhãn trục, chú thích đầy đủ. | Thư mục `figures/` |
| **Hà Quốc Khánh** | Forecasting: Cross-validation đúng chiều thời gian. SHAP values / Feature importance. Submit Kaggle lần 3. | Notebook `04_final_forecast.ipynb` |
| **Lê Bảo Khánh** | Viết narrative cho từng biểu đồ: mô tả, key findings (có số liệu), business implications. | Draft report sections |

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

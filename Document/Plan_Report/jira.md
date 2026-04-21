# 📋 Danh sách Task Jira theo từng thành viên (10 ngày Datathon)

Dưới đây là danh sách các task Jira được nhóm theo từng thành viên, **phân chia EDA theo 5 Module Kinh doanh Cốt lõi** (xem `Business_Analytics.md` §2). Mỗi người sở hữu (own) module end-to-end để tránh overlap.

### Bảng phân công Module EDA

| Module | Owner | Câu hỏi cốt lõi |
|--------|-------|-----------------|
| ❶ Tăng trưởng & Tài chính | Lê Bảo Khánh | Doanh nghiệp tăng trưởng hay suy giảm? |
| ❷ Khách hàng & Retention | Lưu Nguyễn Thiện Nhân | KH trung thành đến mức nào? |
| ❸ Sản phẩm & Pricing | Lưu Nguyễn Thiện Nhân | Bán cái gì, giá bao nhiêu? |
| ❹ Vận hành & Supply Chain | Nguyễn Quốc Khánh | Vận hành có hiệu quả không? |
| ❺ Marketing & Digital | Nguyễn Quốc Khánh | Kênh nào hiệu quả? |

---

## 👤 Lê Bảo Khánh (Business Analyst)
*Vai trò: Owner Module ❶ + Tổng hợp Narrative & Report*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-REPO-01.1]** | Đọc đề & Nghiên cứu Rubric | Đọc kỹ yêu cầu đề, rubric chấm điểm. | File `notes_rubric.md` | Highest | `report` | 20/04 |
| **[20/04-REPO-01.2]** | Lập dàn ý Report (NeurIPS) | Lên dàn ý các phần cho báo cáo LaTeX. | File `report_outline.md` | Highest | `report` | 20/04 |
| **[21/04-EDA-M1.1]** | M❶ Descriptive: Revenue YoY trend | Revenue growth rate, CAGR qua các năm. | `02_M1_revenue_health.ipynb` | High | `eda` | 21/04 |
| **[21/04-EDA-M1.2]** | M❶ Descriptive: Margin & AOV trend | Gross Margin trend, AOV, Revenue per Customer (RPU). | `02_M1_revenue_health.ipynb` | High | `eda` | 21/04 |
| **[22/04-EDA-M1.3]** | M❶ Diagnostic: Margin squeeze | Tại sao margin giảm? Phân tích COGS > Revenue cuối 2022. | `03_M1_margin_diagnostic.ipynb` | High | `eda` | 22/04 |
| **[22/04-EDA-M1.4]** | M❶ Diagnostic: Revenue by segment | Revenue breakdown theo category/segment. RPU trend theo nhóm KH. | `03_M1_margin_diagnostic.ipynb` | High | `eda` | 22/04 |
| **[23/04-EDA-M1.5]** | M❶ Predictive: Revenue forecast interpret | Diễn giải output forecast từ HQ Khánh cho góc nhìn kinh doanh. | `04_M1_revenue_predictive.ipynb` | Medium | `eda` | 23/04 |
| **[23/04-EDA-M1.6]** | M❶ Narrative: Module ❶ end-to-end | Viết narrative tổng hợp Module ❶ (Desc → Diag → Pred). | Narrative trong notebook | Medium | `eda` | 23/04 |
| **[24/04-EDA-SUM.1]** | Tổng hợp 5 module: Insights summary | Tổng hợp prescriptive recommendations từ cả 5 module. | `eda_insights_summary.md` | High | `eda` | 24/04 |
| **[24/04-EDA-SUM.2]** | Xây dựng Top 5 câu chuyện cho Report | Chọn & sắp xếp 5 câu chuyện có impact cao nhất (theo BA §7). | `eda_insights_summary.md` | High | `eda` | 24/04 |
| **[25/04-EDA-NAR.1]** | Narrative: Descriptive + Diagnostic | Viết narrative cho tất cả biểu đồ Descriptive & Diagnostic. | Update cấu trúc `.tex` | Low | `eda` | 25/04 |
| **[25/04-EDA-NAR.2]** | Narrative: Predictive + Prescriptive | Mô tả logic dự báo & đề xuất hành động trên góc nhìn kinh doanh. | Update cấu trúc `.tex` | Low | `eda` | 25/04 |
| **[26/04-REPO-02.1]** | Report: Intro & Framework | Khung Intro, methodology, business context. | Source thư mục `report/` | Highest | `report` | 26/04 |
| **[26/04-REPO-02.2]** | Report: EDA & Business Insights | Viết phần trọng tâm: 5 module insights + storytelling. | Source thư mục `report/` | Highest | `report` | 26/04 |
| **[27/04-REPO-06.1]** | Polish: Flow & Grammar | Làm mượt báo cáo, sửa diễn đạt. | File `main.tex` | High | `report` | 27/04 |
| **[27/04-REPO-06.2]** | Polish: References | Phân loại & Add References đúng format. | `report/references.bib` | High | `report` | 27/04 |
| **[28/04-REPO-05.1]** | Final Export: Render LaTeX PDF | Render final PDF ≤ 4 trang, không lỗi. | `report_final.pdf` | Highest | `report` | 28/04 |
| **[28/04-REPO-05.2]** | Nộp bài qua cổng Submission | Điền form & upload tất cả tài liệu. | Screenshot submit hoàn tất | Highest | `report` | 28/04 |
| **[29/04-REPO-07.1]** | Chuẩn bị Slide (Chung Kết) | Soạn xương sống slide pitch deck. | `presentation_outline.md` | Low | `report` | 29/04 |

---

## 👤 Nguyễn Quốc Khánh (Tech Lead)
*Vai trò: Owner Module ❹ + ❺, Code Review, Forecasting architecture*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-SET-01.1]** | Setup GitHub Repo & Folders | Tạo repo, nhánh, cấu trúc thư mục. | Repo Git | Highest | `setup` | 20/04 |
| **[20/04-SET-01.2]** | Setup: Data Loader Utility | Viết logic load & cleaning chung bằng Polars. | `src/data_loader.py` | Highest | `setup` | 20/04 |
| **[21/04-FORE-05.1]** | FE Pipeline Design | Thiết kế list features cho Forecasting. | `Document/feature_pipeline.md` | High | `forecasting` | 21/04 |
| **[21/04-FORE-05.2]** | Review Code: MCQ | Cross-check PR giải MCQ của Thiện Nhân. | PR Review comments | High | `forecasting` | 21/04 |
| **[22/04-EDA-M4.1]** | M❹ Descriptive: Delivery performance | Thời gian order → ship → delivery. Fulfillment rate. | `02_M4_operations_overview.ipynb` | High | `eda` | 22/04 |
| **[22/04-EDA-M5.1]** | M❺ Descriptive: Traffic & Channel | Traffic overview, Channel attribution, Conversion rate. | `02_M5_marketing_overview.ipynb` | High | `eda` | 22/04 |
| **[23/04-EDA-M4.2]** | M❹ Diagnostic: Stockout impact | Lost revenue estimate từ stockout, Overstock cost. | `03_M4_supply_chain_diagnostic.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-M4.3]** | M❹ Diagnostic: Delivery gap by region | So sánh delivery time theo vùng (East/Central/West). | `03_M4_supply_chain_diagnostic.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-M5.2]** | M❺ Diagnostic: Promo ROI & Paradox | Promo ROI, Promotion Paradox (trước/trong/sau KM). | `03_M5_promo_effectiveness.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-M5.3]** | M❺ Diagnostic: Bounce rate analysis | Bounce rate theo source & device. | `03_M5_promo_effectiveness.ipynb` | Medium | `eda` | 23/04 |
| **[24/04-EDA-M4.4]** | M❹ Prescriptive: Reorder & Logistics | Đề xuất reorder point, giảm delivery time, size guide ROI. | `04_M4_supply_prescriptive.ipynb` | High | `eda` | 24/04 |
| **[24/04-EDA-M5.4]** | M❺ Prescriptive: Marketing budget | Tái phân bổ ngân sách marketing, KM theo segment. | `04_M5_marketing_prescriptive.ipynb` | High | `eda` | 24/04 |
| **[25/04-EDA-REV.1]** | Review Code Quality (Team) | Rà soát coding standard, docstrings của EDA code. | PR Approved/Merged | High | `eda` | 25/04 |
| **[25/04-EDA-REV.2]** | Review Reproducibility | Run All toàn bộ notebook, fix bugs. | Fix commits | High | `eda` | 25/04 |
| **[26/04-REPO-03.1]** | Report: Model pipeline description | Mô tả luồng Forecasting cho report. | Source thư mục `report/` | High | `report` | 26/04 |
| **[26/04-REPO-03.2]** | Report: Explainability section | SHAP plots, Feature Importance + diễn giải. | Source thư mục `report/` | High | `report` | 26/04 |
| **[27/04-REPO-04.1]** | Review Logic vs Storytelling | Validate logic dữ kiện + mạch truyện report. | Feedback list | Highest | `report` | 27/04 |
| **[27/04-REPO-04.2]** | Review Số liệu Report vs Code | Cross-check con số trong report vs code output. | Cập nhật LaTeX | Highest | `report` | 27/04 |
| **[28/04-REPO-08.1]** | Source Clean Up | Gom code sạch về main, xóa file tmp. | Repo updated | High | `report` | 28/04 |
| **[28/04-REPO-08.2]** | Environment Check | Fix `requirements.txt` theo version chính xác. | `requirements.txt` | High | `report` | 28/04 |
| **[29/04-REPO-09.1]** | Final Archive repo | Nén source + docs backup. | `Datathon_repo_backup.zip` | Low | `report` | 29/04 |

---

## 👤 Lưu Nguyễn Thiện Nhân (Data Engineer)
*Vai trò: Owner Module ❷ + ❸, Data pipeline, MCQ, Visualization*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-EDA-13.1]** | Profiling: Null & Outliers Test | Validation toàn bộ 15 bảng: null, outlier, phân bố. | `00_data_profiling.ipynb` | High | `eda` | 20/04 |
| **[20/04-EDA-13.2]** | Profiling: Schema Cast Types | Chỉnh data types, datetime parsing cho data loader. | Cập nhật `src/data_loader.py` | High | `eda` | 20/04 |
| **[21/04-MCQ-01.1]** | Code giải (Q1 - Q5) | Trả lời MCQ, logging block rõ ràng. | `01_mcq_answers.ipynb` | Highest | `mcq` | 21/04 |
| **[21/04-MCQ-01.2]** | Code giải (Q6 - Q10) | Hoàn thành 10 câu MCQ. | `01_mcq_answers.ipynb` | Highest | `mcq` | 21/04 |
| **[22/04-EDA-M2.1]** | M❷ Descriptive: Repeat Purchase Rate | Tỷ lệ KH mua lần 2, 3. Cohort Retention. | `02_M2_customer_retention.ipynb` | High | `eda` | 22/04 |
| **[22/04-EDA-M2.2]** | M❷ Descriptive: RFM Segmentation | Phân nhóm KH: Champions, Loyal, At Risk, Lost. | `02_M2_customer_retention.ipynb` | High | `eda` | 22/04 |
| **[23/04-EDA-M2.3]** | M❷ Diagnostic: CLV & Acquisition | CLV calculation, Channel Effectiveness analysis. | `03_M2_clv_analysis.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-M3.1]** | M❸ Descriptive: BCG Matrix | Category × Growth × Share classification. | `02_M3_product_portfolio.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-M3.2]** | M❸ Descriptive: Price vs Volume | Phân tích price tier vs volume vs margin. | `02_M3_product_portfolio.ipynb` | High | `eda` | 23/04 |
| **[24/04-EDA-M3.3]** | M❸ Diagnostic: Size × Return Rate | Cross-tab size × return rate, Color preference. | `03_M3_product_diagnostic.ipynb` | Medium | `eda` | 24/04 |
| **[24/04-EDA-M3.4]** | M❸ Prescriptive: Portfolio optimization | Đề xuất loại bỏ Dogs, mở rộng Premium, pricing A/B test. | `03_M3_product_diagnostic.ipynb` | Medium | `eda` | 24/04 |
| **[24/04-EDA-M2.4]** | M❷ Prescriptive: Loyalty & Win-back | Chương trình loyalty cho Champions, win-back cho At Risk. | `04_M2_customer_prescriptive.ipynb` | Medium | `eda` | 24/04 |
| **[25/04-EDA-VIZ.1]** | Polish: Design Palette Setup | Fix styles chuẩn cho Matplotlib/Seaborn. | `src/utils.py` | High | `eda` | 25/04 |
| **[25/04-EDA-VIZ.2]** | Polish: Export HQ Figures | Export biểu đồ chất lượng cao cho tất cả modules. | `figures/*.png` | High | `eda` | 25/04 |
| **[26/04-REPO-10.1]** | LaTeX: Insert Images | Chèn hình vào report LaTeX. | `\includegraphics{}` commands | High | `report` | 26/04 |
| **[26/04-REPO-10.2]** | LaTeX: Graphic Layout | Thiết lập layout hình ảnh trong report. | LaTeX layout tags | High | `report` | 26/04 |
| **[27/04-REPO-11.1]** | Reproducibility Pipeline Check | Chạy lại toàn bộ pipeline từ raw → output. | Fix commits | High | `report` | 27/04 |
| **[27/04-REPO-11.2]** | Bugfix cho Report LaTeX | Sửa lỗi hình scale, font overlap. | Report PDF builds OK | High | `report` | 27/04 |
| **[28/04-MCQ-02.1]** | Final Checklist MCQ | Dò chéo & confirm đáp án 10 câu. | Điền form submission | Highest | `mcq` | 28/04 |
| **[28/04-MCQ-02.2]** | Info Packaging: Ảnh thẻ SV | Scan thẻ/ảnh theo yêu cầu tổ chức. | `ID_team_assets.zip` | Highest | `mcq` | 28/04 |
| **[29/04-EDA-DASH.1]** | Dashboard Mini (Optional) | Interactive charts bằng Streamlit. | `streamlit_app.py` | Low | `eda` | 29/04 |

---

## 👤 Hà Quốc Khánh (ML Engineer)
*Vai trò: Feature engineering, Forecasting model, Kaggle submission (không tham gia EDA trực tiếp)*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-EDA-16.1]** | Phân tích Sales: Trend & Season | Phân rã time-series: trend, seasonality. | `01_sales_trend.ipynb` | High | `eda` | 20/04 |
| **[20/04-EDA-16.2]** | Phân tích Sales: ADF Stationarity | ADF Test xác nhận stationarity. | `01_sales_adf.ipynb` | High | `eda` | 20/04 |
| **[21/04-FORE-01.1]** | Baseline ARIMA/Prophet | Build model baseline. | `02_baseline_forecast.ipynb` | Highest | `forecasting` | 21/04 |
| **[21/04-FORE-01.2]** | Kaggle Format Check (Lần 1) | Chạy batch submit qua Kaggle check lỗi structure output submission. | `submission_baseline.csv` | Highest | `forecasting` | 21/04 |
| **[22/04-FORE-06.1]** | FE: Lags & Rolling features | Lags, rolling mean/std, datetime features. | `src/features.py` | High | `forecasting` | 22/04 |
| **[22/04-FORE-06.2]** | FE: Exogenous components | Ghép traffic, inventory, promotions vào train data. | `data/processed_train.csv` | High | `forecasting` | 22/04 |
| **[23/04-FORE-02.1]** | Model v2: LightGBM/XGBoost | Gradient boost với FE mới. | `03_lgbm_forecast.ipynb` | Highest | `forecasting` | 23/04 |
| **[23/04-FORE-02.2]** | Kaggle Submit lần 2 | Submit advanced model. | `submission_adv.csv` | Highest | `forecasting` | 23/04 |
| **[24/04-FORE-03.1]** | Ensemble: Blending setup | Combine outputs từ nhiều models. | `04_ensemble_model.ipynb` | Medium | `forecasting` | 24/04 |
| **[24/04-FORE-03.2]** | Hyperparameter Tuning (Optuna) | Dò tìm best config qua Optuna. | `models/best_lgbm_params.json` | Medium | `forecasting` | 24/04 |
| **[25/04-FORE-04.1]** | Cross-Validation (Time-series) | K-fold theo thời gian, tránh data leakage. | CV report markdown | High | `forecasting` | 25/04 |
| **[25/04-FORE-04.2]** | SHAP Feature Importance | SHAP plot + paragraph giải thích. | `shap_plot.png` + text | High | `forecasting` | 25/04 |
| **[26/04-FORE-07.1]** | Final model checkpoint | Fit final model trên full data, export checkpoint. | `models/final_model.pkl` | Highest | `forecasting` | 26/04 |
| **[26/04-FORE-07.2]** | Methodology Draft | Note quá trình train model cho report. | Draft text docs | Highest | `forecasting` | 26/04 |
| **[27/04-FORE-08.1]** | Final batch output check | Dò bug: missing dates, duplicate IDs. | `utils/check_sub.py` | Highest | `forecasting` | 27/04 |
| **[27/04-FORE-08.2]** | Kaggle Submit Final | Merge blend, chốt score cuối cùng. | `submission_final.csv` | Highest | `forecasting` | 27/04 |
| **[28/04-REPO-12.1]** | Archive Kaggle Results | Screenshot rank, backup evidence. | Kaggle Leaderboard Screenshot | High | `report` | 28/04 |
| **[29/04-FORE-09.1]** | Extension Tests (Optional) | Post-processing, threshold clip. | Test submission logs | Low | `forecasting` | 29/04 |

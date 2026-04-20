# 📋 Danh sách Task Jira theo từng thành viên (10 ngày Datathon)

Dưới đây là danh sách các task Jira được nhóm theo từng thành viên dựa trên Kế hoạch 10 ngày (`team_plan.md`) và Quy tắc Jira (`Workflow.md`) của team Outliers. Các đầu việc lớn mỗi ngày đã được bóc tách thành các tiểu task nhỏ và có cột "File Output" cụ thể để upload khi hoàn thành. Deadline theo ngày cũng đã được gán tự động vào đầu mã task.

---

## 👤 Lê Bảo Khánh (Business Analyst)
*Vai trò: EDA insights, business storytelling, viết report*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-REPO-01.1]** | Đọc đề & Nghiên cứu Rubric | Đọc kỹ yêu cầu đề, rubric chấm điểm. | File `notes_rubric.md` | Highest | `report` | 20/04 |
| **[20/04-REPO-01.2]** | Lập dàn ý Report (NeurIPS) | Lên dàn ý các phần cho báo cáo LaTeX. | File `report_outline.md` | Highest | `report` | 20/04 |
| **[21/04-EDA-01.1]** | Descriptive: Revenue overview | Phân tích tổng quan xu hướng doanh thu. | File `02_revenue_overview.ipynb` | High | `eda` | 21/04 |
| **[21/04-EDA-01.2]** | Descriptive: Revenue by region | Phân tích phân bố doanh thu theo khu vực. | File `02_revenue_geography.ipynb` | High | `eda` | 21/04 |
| **[22/04-EDA-02.1]** | Descriptive: Topsellers Analysis | Phân tích về các sản phẩm bán chạy. | File `02_product_analysis.ipynb` | High | `eda` | 22/04 |
| **[22/04-EDA-02.2]** | Descriptive: Margins & Seasonality | Phân tích lợi nhuận biên và tính mùa vụ. | File `02_margin_analysis.ipynb` | High | `eda` | 22/04 |
| **[23/04-EDA-08.1]** | Diagnostic: Web traffic trend | Tìm điểm nghẽn và xu hướng traffic web. | File `03_web_traffic.ipynb` | Medium | `eda` | 23/04 |
| **[23/04-EDA-08.2]** | Diagnostic: Traffic conversion | Tỉ lệ chuyển đổi đơn hàng vs traffic web. | File `03_conversion_rate.ipynb` | Medium | `eda` | 23/04 |
| **[24/04-EDA-06.1]** | Prescriptive: Revenue actions | Action points để cải thiện doanh thu. | File `revenue_recommendations.md` | High | `eda` | 24/04 |
| **[24/04-EDA-06.2]** | Prescriptive: Profit optimizations | Đề xuất hành động giảm chi/tối ưu lợi nhuận. | File `profit_optimizations.md` | High | `eda` | 24/04 |
| **[25/04-EDA-09.1]** | Narrative: Descriptive + Diagnostic | Viết narrative cho các biểu đồ liên quan. | Update cấu trúc `.tex` | Low | `eda` | 25/04 |
| **[25/04-EDA-09.2]** | Narrative: Predictive + Prescriptive | Mô tả logic dự báo trên business angle. | Update cấu trúc `.tex` | Low | `eda` | 25/04 |
| **[26/04-REPO-02.1]** | Report: Intro & Framework | Khung Intro và cách tiếp cận, methodology. | File Source thư mục `report/` | Highest | `report` | 26/04 |
| **[26/04-REPO-02.2]** | Report: EDA & Business Insights | Viết phần trọng tâm phân tích dữ liệu. | File Source thư mục `report/` | Highest | `report` | 26/04 |
| **[27/04-REPO-06.1]** | Polish: Flow & Grammar | Làm mượt báo cáo, đọc sửa diễn đạt lỗi. | File nguồn `main.tex` | High | `report` | 27/04 |
| **[27/04-REPO-06.2]** | Polish: Tài liệu tham khảo | Phân loại & Add References đúng format. | File `report/references.bib` | High | `report` | 27/04 |
| **[28/04-REPO-05.1]** | Final Export: Render LaTeX PDF | Render final file văn bản định dạng chuẩn không lỗi. | File `report_final.pdf` (max 4 trang) | Highest | `report` | 28/04 |
| **[28/04-REPO-05.2]** | Nộp bài qua cổng Submission | Kiểm tra link file và điền form đầy đủ. | Screenshot màn hình submit hoàn tất | Highest | `report` | 28/04 |
| **[29/04-REPO-07.1]** | Chuẩn bị Slide (Chung Kết) | Soạn trước xương sống slide pitch deck trình bày. | File `presentation_outline.md` | Low | `report` | 29/04 |

---

## 👤 Nguyễn Quốc Khánh (Tech Lead)
*Vai trò: Kiến trúc tổng thể, Forecasting model, code review*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-SET-01.1]** | Setup GitHub Repo & Folders | Tạo repo chung, tạo nhánh logic `main`/`develop`. | Khởi tạo cấu trúc Repo Git | Highest | `setup` | 20/04 |
| **[20/04-SET-01.2]** | Setup: Xây dựng Utility Code | Viết logic load & cleaning tự động chung. | File `src/data_loader.py` | Highest | `setup` | 20/04 |
| **[21/04-FORE-05.1]** | FE Pipeline Design | Thiết kế list các features cần tạo để train models. | File `Document/feature_pipeline.md` | High | `forecasting` | 21/04 |
| **[21/04-FORE-05.2]** | Review Code: MCQ Giải thuật | Cross-check PR của Data Engineer xử lý mục câu hỏi. | Approvals PR / Review comments | High | `forecasting` | 21/04 |
| **[22/04-EDA-04.1]** | Diagnostic: Promo Analytics | Cân đo chênh lệch doanh số Launch vs No Launch. | File `03_promo_sales.ipynb` | High | `eda` | 22/04 |
| **[22/04-EDA-04.2]** | Diagnostic: Promotions ROI | Đánh giá phân tích lại hiệu quả của Return Rate. | File `03_promo_roi.ipynb` | High | `eda` | 22/04 |
| **[23/04-EDA-10.1]** | Diagnostic: Stockout Impact | Phân tích định tính thiệt hại hụt kho trong sales. | File `03_stockout_impact.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-10.2]** | Diagnostic: Overstock Costs | Phân tích áp lực lên kho và đọng vốn do lưu kho dài. | File `03_overstock_cost.ipynb` | High | `eda` | 23/04 |
| **[24/04-EDA-11.1]** | Predictive: Churn Probability | Đánh giá rủi ro rời bỏ hệ thống từ khách hàng hiện tại. | File `04_churn_prediction.ipynb` | Medium | `eda` | 24/04 |
| **[24/04-EDA-11.2]** | Predictive: Churn Factors | Phân hóa các nguyên nhân kéo theo việc KH cắt dịch vụ. | File `04_churn_factors.ipynb` | Medium | `eda` | 24/04 |
| **[25/04-EDA-12.1]** | Review Code Quality (Team) | Rà soát coding standard, docstrings của EDA source code. | Approved/Merged định dạng PR | High | `eda` | 25/04 |
| **[25/04-EDA-12.2]** | Review Reproducibility | Reset memory, Run All toàn luồng để kiểm định lỗi môi trường. | Fix bugs / Commits trên các branch | High | `eda` | 25/04 |
| **[26/04-REPO-03.1]** | Report: Phác thảo Model pipeline | Mô tả luồng chạy thông tin model để chèn bài report chuẩn. | File Text Update folder `report/` | High | `report` | 26/04 |
| **[26/04-REPO-03.2]** | Report: Mảng Explainability | Chèn kết quả SHAP plots/ Feature Imps kèm diễn giải model. | File Text Update folder `report/` | High | `report` | 26/04 |
| **[27/04-REPO-04.1]** | Review Logic vs Storytelling | Validate logic dữ kiện từ Đầu tới Cuối cho mạch truyện hợp lý. | Ghi chú & List Feedback cập nhật lại | Highest | `report` | 27/04 |
| **[27/04-REPO-04.2]** | Review Số liệu Report vs Code | Cross-check trực quan các con số chênh lệch hay không. | Cập nhật số liệu chuẩn cấu trúc LaTeX | Highest | `report` | 27/04 |
| **[28/04-REPO-08.1]** | Source Clean Up | Gom code sạch về nhánh main, xử lý file tmp / test lỗi cũ. | Repo source code master update cuối | High | `report` | 28/04 |
| **[28/04-REPO-08.2]** | Environment Check | Kiểm định lại list các thư viện môi trường fix cứng theo version. | File `requirements.txt` chuẩn | High | `report` | 28/04 |
| **[29/04-REPO-09.1]** | Final Archive repo | Nén source đính kèm các file dữ liệu sample data, docs report đi kèm. | File gốc nén `Datathon_repo_backup.zip` | Low | `report` | 29/04 |

---

## 👤 Lưu Nguyễn Thiện Nhân (Data Engineer)
*Vai trò: Data pipeline, MCQ, EDA visualization*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-EDA-13.1]** | Profiling: Null & Outliers Test | Validation kiểm tra dị thường trên cả bộ DB 15 bảng con. | File `00_data_profiling.ipynb` | High | `eda` | 20/04 |
| **[20/04-EDA-13.2]** | Profiling: Schema Cast Types | Chỉnh chuẩn Data types thời gian thực phục vụ load đồng bộ. | Xây dựng logic chung tại `src/data_loader.py` | High | `eda` | 20/04 |
| **[21/04-MCQ-01.1]** | Code giải hệ (Q1 - Q5) | Trả lời trắc nghiệm & Cấu trúc Logging block rõ ràng, clear flow. | File root `01_mcq_answers.ipynb` | Highest | `mcq` | 21/04 |
| **[21/04-MCQ-01.2]** | Code giải hệ (Q6 - Q10) | Trả lời trắc nghiệm & Coding phần còn lại xuất text log ra output. | File cập nhật `01_mcq_answers.ipynb` | Highest | `mcq` | 21/04 |
| **[22/04-EDA-05.1]** | Predictive: R-F Calculation | Tính cụm biến Recency, Frequency dựa vào transactions khách. | File `04_rfm_calculation.ipynb` | High | `eda` | 22/04 |
| **[22/04-EDA-05.2]** | Predictive: M & Segmentation | Dùng thuật toán KMeans kết cụm profile theo tiêu chí Monetary. | File `04_rfm_segmentation.ipynb` | High | `eda` | 22/04 |
| **[23/04-EDA-03.1]** | Diagnostic: Return overall | Xác nhận tỷ trọng % bị back đơn, hoàn sản phẩm trên tổng volume. | File `03_return_general.ipynb` | High | `eda` | 23/04 |
| **[23/04-EDA-03.2]** | Diagnostic: Return Rootcause | Tìm mối liên kết trả về theo các Vùng/Category hoặc Campain Promo. | File `03_return_root_cause.ipynb` | High | `eda` | 23/04 |
| **[24/04-EDA-14.1]** | Prescriptive: Price Elasticity | Đánh giá độ co dãn định phí với các mặt hàng cốt lõi top SKU. | File gốc `04_price_elasticity.ipynb` | Medium | `eda` | 24/04 |
| **[24/04-EDA-14.2]** | Prescriptive: Discount Optimize | Gợi ý vùng discount % hợp lí làm kịch bản tối ưu cao tỷ lệ CVR. | Bảng chốt gợi ý `discount_recommend.csv` | Medium | `eda` | 24/04 |
| **[25/04-EDA-07.1]** | Polish: Design Palette Setup | Rà soát fix cứng styles chuẩn báo cáo cho module Matplotlib/Seaborn. | Cập nhật functions tại `src/utils.py` | High | `eda` | 25/04 |
| **[25/04-EDA-07.2]** | Polish: Export HQ Vector Graph | Cắt/Crop các biểu đồ sang chuẩn đẹp, file hình chất lượng cao đồ họa. | Các files nén lưu tại path `figures/*.eps` (hoặc png) | High | `eda` | 25/04 |
| **[26/04-REPO-10.1]** | LaTeX Formatting: Insert Images | Thêm list liên kết đường dẫn hình ảnh file gốc vào report văn bản LaTeX. | Lệnh code `\includegraphics{}` | High | `report` | 26/04 |
| **[26/04-REPO-10.2]** | LaTeX Formatting: Graphic Layout | Thiết lập ảnh cân xứng vào grid khung định hướng báo cáo 2 panel dọc. | Tags layout placement trong file tex | High | `report` | 26/04 |
| **[27/04-REPO-11.1]** | Reproducibility Pipeline Check | Test chạy auto-run lại pipeline lấy kết quả raw to output tự động. | Build tests clean Fix commit | High | `report` | 27/04 |
| **[27/04-REPO-11.2]** | Bugfix cho khung Report LaTeX | Giải quyết issue hình bị scale méo, lỗi font chữ bị Overlapping. | File Log kết quả in ra Report Pdf build successfully | High | `report` | 27/04 |
| **[28/04-MCQ-02.1]** | Final Checklist Submit MCQ | Dò chéo & Confirm bộ answers cho 10 cầu hạn chế lỗi sơ suất nhầm key. | Điền Form submission kết quả chính thức cho bộ phận | Highest | `mcq` | 28/04 |
| **[28/04-MCQ-02.2]** | Info Packaging Groups Member | Scan thẻ/Ảnh định dạng theo yêu cầu hội đồng tổ chức làm minh chứng. | Tệp zip nén hồ sơ team hình ảnh `ID_team_assets.zip` | Highest | `mcq` | 28/04 |
| **[29/04-EDA-15.1]** | Dashboard Mini tương tác (Optional)| Dành riêng 2-3 interactive charts đưa vào frontend trang web báo cáo. | Mã layout giao diện Web nhỏ gọi là `streamlit_app.py` | Low | `eda` | 29/04 |

---

## 👤 Hà Quốc Khánh (ML Engineer)
*Vai trò: Feature engineering, Forecasting model, Kaggle submission*

| Mã Task | Tên Task | Mô tả ngắn | File Output | Ưu tiên | Label | Ngày |
|---|---|---|---|---|---|---|
| **[20/04-EDA-16.1]** | Phân tích Sales: Trend & Season | Phân tích isolate chuỗi dữ liệu gốc thành thành phần xu hướng. | File notebook phân rã time-series `01_sales_trend.ipynb` | High | `eda` | 20/04 |
| **[20/04-EDA-16.2]** | Phân tích Sales: ADF Stationarity | Perform ADF Test làm điều kiện xác nhận phân phối Time-Series data. | File validation output TS `01_sales_adf.ipynb` | High | `eda` | 20/04 |
| **[21/04-FORE-01.1]** | Code Simple Linear Baseline | Build thuật toán ARIMA tối giản chạy thử mẫu kết quả format date chuỗi. | Code model base `02_baseline_forecast.ipynb` | Highest | `forecasting` | 21/04 |
| **[21/04-FORE-01.2]** | Kaggle Format Check (Lần 1) | Chạy batch submit qua Kaggle check lỗi structure output submission. | Export nén kết quả nộp Kaggle public `submission_baseline.csv` | Highest | `forecasting` | 21/04 |
| **[22/04-FORE-06.1]** | FE: Shifts Lags Datetime | Xây mới set thông tin lags dời ngày & cửa sổ tổng trung bình theo khối. | Core cập nhật features logic `src/features.py` | High | `forecasting` | 22/04 |
| **[22/04-FORE-06.2]** | FE: Add Exogenous Components | Ghép thông tin chuỗi `traffic` ngoại lai chung luồng cho việc đào tạo. | File raw DB build ra data pretrain chuẩn `data/processed_train.csv` | High | `forecasting` | 22/04 |
| **[23/04-FORE-02.1]** | Model Boost Tree Build | Build bộ model gradient boost nâng cấp chứa lượng FE lớn complex hơn. | Model tuning notebook `03_lgbm_forecast.ipynb` | Highest | `forecasting` | 23/04 |
| **[23/04-FORE-02.2]** | Advanced Kaggle Attempt (Lần 2) | Export nộp kết quả file output điểm qua API đẩy lên Leaderboard lấy rank. | File nộp batch score Kaggle version `submission_adv.csv` | Highest | `forecasting` | 23/04 |
| **[24/04-FORE-03.1]** | Blending Weights Setup | Xây logic pipeline combine outputs cho nhiều mô hình vào 1 tệp output. | Pipeline kiến trúc meta model `04_ensemble_model.ipynb` | Medium | `forecasting` | 24/04 |
| **[24/04-FORE-03.2]** | Framework Hyperparameter Tuning | Thêm vòng lặp config parameters qua Optuna module dò config hiệu quả. | Danh sách config model `models/best_lgbm_params.json` | Medium | `forecasting` | 24/04 |
| **[25/04-FORE-04.1]** | Cross-Validation Harness Build | Build setup k-fold riêng kiểm soát rò rỉ target variable theo date steps. | Report markdown thống kê hiệu suất chéo local CV vs public CV | High | `forecasting` | 25/04 |
| **[25/04-FORE-04.2]** | Interpret Global Features SHAP | Tạo plot cây đánh giá tham số nội tại độ ưu tiên có đúng thực tế không. | Capture hình `shap_plot.png` & paragraph text đi kèm tính năng | High | `forecasting` | 25/04 |
| **[26/04-FORE-07.1]** | Output Model Checkpoint Run | Fit tham số chốt vào block dữ liệu lớn max size đẩy ra mô hình tịnh tiến. | Checkpoint dump object nặng lưu vào vị trí `models/final_model.pkl` | Highest | `forecasting` | 26/04 |
| **[26/04-FORE-07.2]** | Soạn tóm tắt Methodology Draft | Cung cấp tài liệu note quá trình train model ML gửi bộ phận review tex. | Draft notes text docs miêu tả setup metrics loss của pipeline ML | Highest | `forecasting` | 26/04 |
| **[27/04-FORE-08.1]** | Filter Final Batch Output Script | Tự động hóa dò bug ngày nghỉ, Index Id trùng lặp khỏi array CSV. | Update logic vào script control `utils/check_sub.py` | Highest | `forecasting` | 27/04 |
| **[27/04-FORE-08.2]** | Final Lock Kaggle Submit | Merge run lấy bản nén blend chốt sổ dự phòng. Đẩy score lần cuối. | Record submission khóa Public file chốt `submission_final.csv` | Highest | `forecasting` | 27/04 |
| **[28/04-REPO-12.1]** | Archiving Rank Results Kaggle | Làm bản check giữ backup rank phòng trừ hệ thống cập nhật thay đổi muộn. | Chụp save/export bằng chứng rank list Kaggle Leaderboard Screenshot | High | `report` | 28/04 |
| **[29/04-FORE-09.1]** | Extension Tests | Thử post processing logic filter clip threshold <0 ... kiếm score extra. | Multiple version logs test submissions limit Kaggle (nếu rảnh dư) | Low | `forecasting` | 29/04 |

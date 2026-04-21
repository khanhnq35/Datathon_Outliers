# 📅 Hướng dẫn nhiệm vụ Ngày 1 (20/04) — Hà Quốc Khánh (ML Engineer)

Chào Khánh, đây là bản hướng dẫn chi tiết các đầu việc bạn cần thực hiện trong ngày đầu tiên của Datathon 2026.

---

## 🎯 Mục tiêu tổng quát
Hiểu rõ đặc tính của chuỗi thời gian doanh thu (`Revenue`) để định hình chiến lược xây dựng mô hình Forecasting (ARIMA, Prophet, hay Gradient Boosting).

---

## 📋 Danh sách Task chi tiết

### 1. Task [20/04-EDA-16.1]: Phân tích Sales (Trend & Seasonality)
*   **Mục tiêu**: Tách biệt các thành phần của chuỗi thời gian.
*   **Các bước thực hiện**:
    1.  Load file `Data/sales.csv` bằng Polars.
    2.  Chuyển cột `Date` sang định dạng datetime và set làm index.
    3.  Sử dụng `seasonal_decompose` từ thư viện `statsmodels` (hoặc `Prophet`) để phân rã chuỗi theo mô hình **Additive** hoặc **Multiplicative**.
    4.  **Visualize**: Vẽ 4 đồ thị: Observed, Trend, Seasonal, và Residual.
*   **Insight cần rút ra**:
    *   Doanh thu có xu hướng tăng/giảm theo năm không?
    *   Tính mùa vụ (mùa lễ hội, Tết, Black Friday) thể hiện rõ nhất vào tháng nào?
*   **Output**: `notebooks/01_sales_trend.ipynb`

### 2. Task [20/04-EDA-16.2]: Phân tích Sales (ADF Stationarity Test)
*   **Mục tiêu**: Kiểm tra tính dừng của dữ liệu.
*   **Các bước thực hiện**:
    1.  Thực hiện kiểm định **Augmented Dickey-Fuller (ADF)** trên cột `Revenue`.
    2.  Kiểm tra P-value:
        *   Nếu $P < 0.05$: Chuỗi có tính dừng (Stationary).
        *   Nếu $P \ge 0.05$: Chuỗi không dừng (Non-stationary) -> Cần lấy sai phân (Differencing).
    3.  Vẽ đồ thị **ACF (Autocorrelation)** và **PACF (Partial Autocorrelation)** để xác định các tham số $p, d, q$ cho model ARIMA.
*   **Output**: `notebooks/01_sales_adf.ipynb`

### 3. Nghiên cứu Submission Format
*   **File**: `Data/sample_submission.csv`.
*   **Yêu cầu**: Đảm bảo hiểu rõ cấu trúc file nộp bài (cột `Date`, `Revenue`) để khi xuất kết quả dự báo không bị lỗi format trên Kaggle.

---

## 🛠️ Công cụ & Thư viện khuyến nghị
*   **Xử lý data**: `polars` (Ưu tiên theo guideline của team).
*   **Time-series**: `statsmodels`, `pmdarima` (để auto-arima nếu cần).
*   **Visual**: `plotly` (để zoom-in các điểm dị thường dễ hơn) hoặc `seaborn`.

---

## 💡 Mẹo sử dụng AI Assistant (Antigravity)
Bạn có thể copy các câu lệnh sau để nhờ tôi hỗ trợ code nhanh:
*   *"Đọc sales.csv bằng Polars, thực hiện seasonal_decompose và vẽ biểu đồ vào file notebooks/01_sales_trend.ipynb"*
*   *"Chạy kiểm định ADF và vẽ biểu đồ ACF/PACF cho cột Revenue trong sales.csv, lưu vào notebooks/01_sales_adf.ipynb"*

---
*Chúc bạn có một ngày làm việc hiệu quả!* 🚀

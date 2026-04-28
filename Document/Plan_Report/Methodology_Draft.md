# 📝 Methodology Draft — Hà Quốc Khánh

> **Mục tiêu**: Tài liệu hóa quy trình xây dựng mô hình dự báo để đưa vào báo cáo NeurIPS.

## 1. Dữ liệu & Tiền xử lý (Preprocessing)
- **Detrending Strategy**: Doanh thu có xu hướng tăng trưởng mạnh theo năm. Chúng tôi thực hiện chuẩn hóa (Normalization) bằng cách chia giá trị `Revenue` và `COGS` cho `Mean` tương ứng của từng năm. Điều này giúp mô hình tập trung học các biến động ngắn hạn và tính chu kỳ (Seasonality) mà không bị nhiễu bởi xu hướng tăng trưởng dài hạn.
- **Outlier Handling**: Các giá trị doanh thu âm hoặc lỗi dữ liệu được xử lý trong bước Data Loader, đảm bảo tính nhất quán trước khi đưa vào mô hình.

## 2. Đặc trưng (Feature Engineering)
- **Time Features**: Month, Day, Day of week, Is_weekend.
- **Calendar & Special Events**: Chúng tôi xây dựng bộ đặc trưng riêng cho dịp Tết Nguyên Đán (`is_tet`, `days_to_tet`, `is_pre_tet`, `is_post_tet`) để mô hình bắt được các đỉnh mua sắm đặc thù tại Việt Nam.
- **Lag & Rolling Features**: Sử dụng các biến trễ (Lags) và trung bình trượt (Rolling mean) để mô hình nắm bắt được quán tính của thị trường.

## 3. Mô hình (Model Architecture)
- **Algorithm**: XGBoost Regressor (Detrended).
- **Hyperparameters**: Sử dụng bộ tham số tối ưu (learning_rate=0.05, max_depth=6, n_estimators=1000) kết hợp với Early Stopping để tránh Overfitting.
- **Reasoning**: XGBoost cho phép bắt các mối quan hệ phi tuyến phức tạp và có khả năng xử lý tốt các đặc trưng phân loại (Categorical) từ lịch trình sự kiện.

## 4. Đánh giá (Validation & Results)
- **Strategy**: Time-Series Cross-Validation (Expanding Window) với 5 folds, mỗi fold đánh giá trên 1 năm dữ liệu.
- **Metrics**: 
  - **Mean MAE**: 845,845 VND
  - **Mean RMSE**: 1,152,104 VND
  - **Mean R2**: 0.6307
- **Explainability**: Sử dụng SHAP values để xác định các yếu tố ảnh hưởng. Các biến quan trọng nhất gồm: `month` (Tính thời vụ theo tháng), `day` (Chu kỳ trong tháng), và `dayofweek`.

## 5. Kết luận
- Mô hình đạt độ ổn định cao trên các folds khác nhau (R2 đạt 0.81 ở fold 4).
- Các yếu tố thời gian (tháng, ngày) đóng vai trò quyết định đến doanh thu.
- Checkpoint cuối cùng đã được lưu trữ và sẵn sàng cho việc tái lập kết quả.

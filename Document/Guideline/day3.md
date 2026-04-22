# 📅 Nhiệm vụ Ngày 3 — Hà Quốc Khánh (ML Engineer)
**Ngày: 22/04/2026**

## 🎯 Mục tiêu chính
Nâng cấp từ mô hình Baseline đơn giản lên hệ thống **Feature Engineering nâng cao**. Tích hợp các yếu tố ngoại lai (Exogenous) để chuẩn bị cho việc huấn luyện các mô hình Boosting Tree.

---

## 📝 Danh sách nhiệm vụ chi tiết (Jira Tasks)

### 1. [22/04-FORE-06.1] FE: Shifts Lags & Rolling Statistics
- **Mô tả**: Xây dựng bộ đặc trưng dời ngày (Lags: 1, 7, 14, 30 ngày) và các cửa sổ tổng hợp trung bình trượt (Rolling Mean: 7, 30 ngày) cho cả `Revenue` và `COGS`.
- **Đầu ra**: Cập nhật logic tạo đặc trưng vào file `src/features.py`.
- **Mức độ ưu tiên**: `High` 🔴

### 2. [22/04-FORE-06.2] FE: Tích hợp thành phần ngoại lai (Exogenous Components)
- **Mô tả**: Ghép chuỗi dữ liệu `web_traffic` (lượt truy cập), `promotions` (chiến dịch khuyến mãi) và `inventory` (tồn kho) vào cùng luồng dữ liệu `sales`.
- **Đầu ra**: Tập dữ liệu đã xử lý `Data/processed_train.csv` chuẩn bị cho Training.
- **Mức độ ưu tiên**: `High` 🔴

---

## ⏰ Lịch họp & Check-in (Theo Workflow)
- **20:00 — Check-in 1**: Báo cáo tiến độ Feature Engineering và kết quả Local Validation đầu tiên với bộ features mới.
- **Địa điểm**: Kênh Discord Team Outliers.

---

## 🛠 Công cụ & File liên quan
- **Script chính**: `src/features.py`
- **Dữ liệu nguồn**: `Data/sales.csv`, `Data/web_traffic.csv`, `Data/promotions.csv`
- **Output cần đạt**: `Data/processed_train.csv`

---

> [!TIP]
> Hãy chú ý xử lý các giá trị `NaN` phát sinh sau khi tạo Lags và Rolling Features (thường dùng `.fillna(0)` hoặc nội suy) để tránh lỗi khi đưa vào mô hình XGBoost.

# 🚀 Datathon 2026 - Team Outliers

![Datathon 2026](https://img.shields.io/badge/Competition-Datathon%202026-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange?style=for-the-badge)
![Team](https://img.shields.io/badge/Team-Outliers-green?style=for-the-badge)

Chào mừng bạn đến với repository của đội **Outliers** tham gia cuộc thi **Datathon 2026 - Vòng 1**. Đây là nơi lưu trữ toàn bộ mã nguồn, tài liệu phân tích và mô hình dự báo cho bài thi.

---

## 📋 Tổng quan dự án

Dự án tập trung vào phân tích dữ liệu kinh doanh của một doanh nghiệp thời trang E-commerce tại Việt Nam trong giai đoạn 2012-2022 và thực hiện dự báo doanh thu cho 18 tháng tiếp theo.

### Mục tiêu chính:
1.  **MCQ (20đ)**: Trả lời 10 câu hỏi trắc nghiệm dựa trên phân tích dữ liệu.
2.  **EDA (60đ)**: Phân tích dữ liệu khám phá theo 4 cấp độ (Descriptive, Diagnostic, Predictive, Prescriptive) nhằm đưa ra các quyết định kinh doanh chiến lược.
3.  **Forecasting (20đ)**: Xây dựng mô hình chuỗi thời gian để dự báo doanh thu (`Revenue`) hàng ngày.

---

## 🏗️ Cấu trúc thư mục

```bash
Datathon_Outliers/
├── Data/                   # Dữ liệu gốc (15 file CSV)
├── Document/               # Tài liệu hướng dẫn & Chiến lược
│   ├── Problem/            # Đề bài gốc từ BTC
│   ├── Guideline/          # Các guidline chuẩn (EDA, Forecasting, AI trợ lý)
│   └── Plan_Report/        # Kế hoạch phân chia Team và tiến độ Jira
├── notebooks/              # Jupyter notebooks dành cho phân tích
├── src/                    # Mã nguồn Python tái sử dụng (Loader, Features)
├── models/                 # Các file trọng số mô hình hoặc model dumps (.pkl, .h5)
├── figures/                # Các biểu đồ xuất ra cho báo cáo
├── submissions/            # Các bản submit Kaggle csv
├── report/                 # Báo cáo cuối cùng (NeurIPS template LaTeX)
├── requirements.txt        # Các thư viện cần thiết
└── README.md
```

---

## 👥 Đội ngũ thực hiện

| Thành viên | Vai trò | Trách nhiệm chính |
|-----------|---------|-------------------|
| **Lê Bảo Khánh** | Business Analyst | EDA insights, Storytelling, Viết report |
| **Nguyễn Quốc Khánh** | Tech Lead | Kiến trúc hệ thống, Review code, Dự báo |
| **Lưu Nguyễn Thiện Nhân** | Data Engineer | Data pipeline, MCQ, EDA Visualization |
| **Hà Quốc Khánh** | ML Engineer | Feature engineering, Mô hình Forecasting |

---

## 🛠️ Công nghệ sử dụng

- **Xử lý dữ liệu**: [Polars](https://pola.rs/) (Tối ưu cho dữ liệu lớn), Pandas.
- **Trực quan hóa**: Matplotlib, Seaborn, Plotly.
- **Dự báo**: LightGBM, XGBoost, Prophet, SARIMAX.
- **Công cụ hỗ trợ**: [Antigravity AI](https://github.com/google-deepmind/antigravity) (Pair programming), Jira (Quản lý task), Overleaf (Viết báo cáo).

---

## 🚀 Hướng dẫn cài đặt

Để chạy dự án này trên môi trường local, thực hiện các bước sau:

1.  **Clone repository**:
    ```bash
    git clone https://github.com/khanhnq35/Datathon_Outliers.git
    cd Datathon_Outliers
    ```

2.  **Tạo môi trường ảo & cài đặt thư viện**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate   # Windows
    pip install -r requirements.txt
    ```

3.  **Khám phá Notebook**:
    Truy cập folder `notebooks/` để bắt đầu phân tích.

---

## 🌿 Quy trình Làm việc nhóm (Git & Tools)

1.  **Sử dụng GitHub**:
    - **Không commit thẳng vào `main`.**
    - Mỗi cá nhân làm việc trên chi nhánh (branch) riêng có tên của bạn (ví dụ: `le-bao-khanh`).
    - Lấy cập nhật chung từ nhánh chuẩn `main`: `git pull origin main`.
    - Khi xong task báo Tech Lead (Nguyễn Quốc Khánh) review để merge code.
2.  **AI Assistant (Antigravity)**:
    - Team sử dụng AI để pair programming và tăng tốc xử lý dữ liệu. Tham khảo quy ước prompt chuẩn tại: `Document/Guideline/Antigravity_guideline.md`.
3.  **Quản lý Task**: Cập nhật file `Document/Plan_Report/jira.md` hằng ngày trước 10:00 sáng.


---

## 📈 Lộ trình bài thi (10 ngày)

- **Ngày 1-2**: Kick-off, Setup môi trường, Hoàn thành 10 câu MCQ.
- **Ngày 3-5**: Thực hiện EDA Descriptive & Diagnostic, xây dựng Baseline Forecast.
- **Ngày 6-7**: Hoàn thiện EDA Predictive & Prescriptive, tối ưu mô hình Forecasting.
- **Ngày 8-9**: Viết báo cáo NeurIPS (4 trang), kiểm tra tính tái lập của code.
- **Ngày 10**: Final review & Nộp bài.

---

## 📄 Giấy phép

Dự án này được thực hiện trong khuôn khổ cuộc thi Datathon 2026. Mọi quyền lợi về dữ liệu thuộc về Ban tổ chức cuộc thi.

---
*Created with ❤️ by Team Outliers*

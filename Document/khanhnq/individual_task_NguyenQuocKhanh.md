# 📋 Individual Tasks — Nguyễn Quốc Khánh (Tech Lead)

> **Mục tiêu**: Theo dõi tiến độ cá nhân của Tech Lead trong 10 ngày thi đấu Datathon 2026, bám sát [Team_plan.md](../Plan_Report/Team_plan.md).

---

## 🏗️ Nhiệm vụ chính
*   **Tech Lead**: Kiến trúc tổng thể hệ thống, quản lý repository.
*   **EDA Owner**: Module ❹ (Vận hành & Supply Chain) và Module ❺ (Marketing & Digital).
*   **Forecasting**: Hỗ trợ viết phần methodology và results trong report.
*   **Code Review**: Đảm bảo chất lượng code và tính tái lập (reproducibility) cho toàn đội.

---

## 📅 Lịch trình chi tiết (10 ngày)

### Ngày 1: Setup & Foundations
- [x] Setup GitHub repository & cấu trúc dự án.
- [x] Tạo branch cho tất cả thành viên.
- [x] Viết script load dữ liệu chung (`src/data_loader.py`) bằng **Polars**.

### Ngày 2: MCQ Review & FE Design
- [ ] Review code giải MCQ của Lưu Nguyễn Thiện Nhân.
- [x] Thiết kế pipeline Feature Engineering cho phần Forecasting.

### Ngày 3: EDA Descriptive — Module ❹ & ❺
- [x] **Module ❹**: Phân tích Delivery performance, Fulfillment rate, Return cost tổng quan.
- [ ] **Module ❺**: Traffic overview, Channel attribution, Conversion rate theo kênh.
- [x] Output: `02_M4_operations_overview.ipynb` + `02_M5_marketing_overview.ipynb`.

### Ngày 4: EDA Diagnostic — Module ❹ & ❺
- [x] **Module ❹**: Phân tích Stockout impact (lost revenue), Overstock cost, Delivery gap theo vùng.
- [ ] **Module ❺**: Promo ROI, Promotion Paradox (trước/trong/sau KM), Bounce rate analysis.
- [x] Output: `03_M4_supply_chain_diagnostic.ipynb` + `03_M5_promo_effectiveness.ipynb`.

### Ngày 5: EDA Prescriptive — Module ❹ & ❺
- [ ] **Module ❹**: Đề xuất reorder point, giảm delivery time, size guide ROI.
- [ ] **Module ❺**: Tái phân bổ ngân sách marketing, chiến lược KM theo segment.
- [ ] Output: `04_M4_supply_prescriptive.ipynb` + `04_M5_marketing_prescriptive.ipynb`.

### Ngày 6: Quality Assurance & Code Review
- [ ] Review toàn bộ notebook EDA của 5 module (team-wide).
- [ ] Đảm bảo Code Quality, Reproducibility và chuẩn hóa visualization.

### Ngày 7: Report Writing — Forecasting Section
- [ ] Viết nội dung phần Forecasting trong báo cáo (Methodology, Pipeline, Results).
- [ ] Trực quan hóa kết quả bằng SHAP plot hoặc Feature Importance.

### Ngày 8: Final Report Review
- [ ] Review toàn diện nội dung báo cáo: Logic, số liệu, công thức.
- [ ] Cross-check tính nhất quán giữa code và nội dung report.

### Ngày 9: Cleanup & Delivery
- [ ] Clean up GitHub repository (README, folder structure, requirements.txt).
- [ ] Thực hiện Push final code lên main branch.

### Ngày 10: Buffer & Final Check
- [ ] Kiểm tra lại toàn bộ submission (MCQ, Report, Kaggle).
- [ ] Sao lưu (Backup) repository và chuẩn bị cho Vòng Chung kết.

---

## ✅ Trạng thái hoàn thành: `17%`
- **Total tasks:** 24
- **Completed:** 4
- **In Progress:** 0

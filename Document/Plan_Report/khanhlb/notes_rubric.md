# 📝 Ghi chú Rubric & Yêu cầu Đề Bài
*(Dành cho Team Outliers - Datathon 2026)*

## 1. Phân bổ điểm (Tổng: 100 điểm)
- **MCQ (Trắc nghiệm): 20 điểm** (2đ/câu, không trừ điểm nếu sai).
- **EDA (Trực quan & Phân tích): 60 điểm** 🔴 *Quan trọng nhất*
- **Forecasting (Dự báo): 20 điểm**

---

## 2. Phân tích Rubric EDA (60 điểm)

Để đạt điểm tối đa phần EDA, bài làm phải bao phủ được **4 cấp độ phân tích**:
1. **Descriptive (Mô tả)**: Chuyện gì đã/đang xảy ra?
2. **Diagnostic (Chẩn đoán)**: Tại sao nó lại xảy ra?
3. **Predictive (Dự đoán)**: Điều gì sẽ xảy ra tiếp theo?
4. **Prescriptive (Đề xuất)**: Cần làm gì để giải quyết/cải thiện?

**Chi tiết thang điểm EDA:**
| Tiêu chí | Điểm | Diễn giải & Checklist |
|---|---|---|
| **Chất lượng trực quan** | 15đ | - Biểu đồ chuẩn xác, chọn đúng loại chart.<br>- **Bắt buộc**: Có tiêu đề, nhãn trục rõ ràng, chú thích (legend) phù hợp.<br>- Thẩm mỹ cao. |
| **Chiều sâu phân tích** | 25đ | - Đủ 4 cấp độ (Desc → Diag → Pred → Presc).<br>- Mỗi insight phải đi kèm với số liệu cụ thể để chứng minh. |
| **Insight kinh doanh** | 15đ | - Khám phá có ý nghĩa thực tiễn.<br>- Actionable recommendations (Đề xuất có thể thực hiện được). |
| **Tính sáng tạo** | 5đ | - Góc nhìn độc đáo, không rập khuôn.<br>- Kể chuyện (storytelling) thuyết phục. |

---

## 3. Rubric Forecasting (20 điểm)
- **Hiệu suất (12đ)**: Dựa trên điểm số (R², MAE, RMSE) trên Kaggle Leaderboard.
- **Báo cáo kỹ thuật (8đ)**: 
  - Chất lượng của data pipeline.
  - Khả năng giải thích mô hình (Explainability - ví dụ dùng SHAP).
  - Tính tái lập (Reproducibility).

---

## 4. Yêu cầu Báo cáo (Report) & Nộp bài
- **Template**: Bắt buộc dùng LaTeX NeurIPS.
- **Giới hạn**: Tối đa **4 TRANG** (không tính references & appendix). 
  - *Lưu ý: 4 trang rất ngắn, phải cực kỳ chắt lọc. Chỉ đưa những chart/insight "đắt" nhất vào.*
- **Nội dung Report**: Phải bao gồm cả phần phân tích EDA và phương pháp Forecasting.
- **Submit**: Report PDF, Link GitHub repo (public), Link Kaggle, Form (đáp án MCQ, Ảnh thẻ SV), xác nhận tham gia Chung kết 23/05.

---

## ⚠️ CẢNH BÁO: Những điểm dễ mất điểm (Cần nhắc team)
1. **Quên label/title biểu đồ**: Mất trắng điểm phần "Chất lượng trực quan" (15đ).
2. **Thiếu cấp độ phân tích**: Dừng lại ở mô tả (Descriptive) mà không giải thích "Tại sao" (Diagnostic) hoặc không đề xuất (Prescriptive) sẽ mất điểm nặng phần "Chiều sâu" (25đ).
3. **Kết luận chung chung**: Không có số liệu cụ thể chứng minh (VD: "Doanh thu tăng mạnh" thay vì "Doanh thu tăng mạnh 25% YoY").
4. **Report lố trang**: Vượt quá 4 trang sẽ vi phạm format.
5. **Thiếu giải thích mô hình**: Model xịn nhưng report không có phần giải thích pipeline/feature importance sẽ mất 8đ kỹ thuật.

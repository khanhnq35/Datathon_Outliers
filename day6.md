# 📑 Hướng dẫn công việc Ngày 6 — Hà Quốc Khánh (ML Engineer)

> **Ngày thực hiện**: 25/04 (Theo kế hoạch) | **Trạng thái**: Cần hoàn thiện
> **Mục tiêu**: Đảm bảo mô hình dự báo đạt chuẩn kỹ thuật (Robustness) và có khả năng giải thích (Explainability) để phục vụ viết Report NeurIPS.

---

## 1. Tổng quan nhiệm vụ

Dựa trên bảng Jira và kế hoạch chung, bạn cần hoàn thành 2 nội dung kỹ thuật then chốt trong notebook `04_final_forecast.ipynb`:

| Mã Task | Tên nhiệm vụ | Đầu ra mong đợi | Ưu tiên |
|:---|:---|:---|:---|
| **[25/04-FORE-04.1]** | Cross-Validation (Time-series) | Biểu đồ các Folds + Bảng kết quả MAE/RMSE/R2 | **Highest** |
| **[25/04-FORE-04.2]** | SHAP Feature Importance | Ảnh `shap_summary.png` + Diễn giải kinh doanh | **High** |

---

## 2. Hướng dẫn kỹ thuật chi tiết

### 2.1 Time-Series Cross-Validation
**Tại sao phải làm?** Dữ liệu chuỗi thời gian có tính phụ thuộc vào quá khứ. Việc dùng K-Fold ngẫu nhiên sẽ làm rò rỉ dữ liệu từ tương lai vào tập train.

**Cách triển khai (Sử dụng `TimeSeriesSplit`):**

```python
from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Khởi tạo dữ liệu
# Giả sử X là features, y là target (Revenue)
# Sắp xếp X theo Date trước khi split
X = X.sort_index() 
y = y.sort_index()

# 2. Thiết lập Splitter
tscv = TimeSeriesSplit(n_splits=5)

fold_results = []

for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
    
    # 3. Train Model (Ví dụ LightGBM)
    model = lgb.LGBMRegressor(n_estimators=1000, random_state=42)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(100), lgb.log_evaluation(0)]
    )
    
    # 4. Evaluate
    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    r2 = r2_score(y_val, preds)
    
    fold_results.append({'Fold': fold+1, 'MAE': mae, 'RMSE': rmse, 'R2': r2})
    print(f"Fold {fold+1} Completed. MAE: {mae:,.0f}")

# 5. Summary
df_results = pd.DataFrame(fold_results)
print("\n--- KẾT QUẢ CROSS VALIDATION ---")
print(df_results)
print(f"\nAverage MAE: {df_results['MAE'].mean():,.0f}")
```

---

### 2.2 Phân tích SHAP (Explainability)
**Tại sao phải làm?** Ban giám khảo cần biết mô hình của bạn hoạt động như thế nào, không phải là một "hộp đen". SHAP giúp định lượng đóng góp của từng feature vào giá trị dự báo.

**Cách triển khai:**

```python
import shap
import matplotlib.pyplot as plt

# 1. Tạo Explainer (dùng model đã được train trên toàn bộ tập dữ liệu)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_val)

# 2. Summary Plot - Biểu đồ quan trọng nhất
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_val, show=False)
plt.title("SHAP Feature Importance (Impact on Revenue)")
plt.savefig('../figures/shap_summary.png', bbox_inches='tight')
plt.show()

# 3. Beeswarm Plot - Hiểu về xu hướng tác động
shap.plots.beeswarm(explainer(X_val))
```

**💡 Gợi ý giải thích cho Report:**
- **COGS**: Nếu COGS đứng đầu, hãy giải thích: "Doanh thu biến động tỷ lệ thuận với giá vốn hàng bán, cho thấy mô hình capture tốt quy mô vận hành."
- **Month/Day of week**: Giải thích về tính chu kỳ (Seasonality).
- **Web traffic**: Giải thích về tác động của Marketing và lưu lượng truy cập.

---

## 3. Checklist hoàn thành "Ngày 6"

- [ ] Notebook `04_final_forecast.ipynb` chạy mượt từ đầu đến cuối không lỗi.
- [ ] Có bảng kết quả MAE/RMSE cho ít nhất 5 folds.
- [ ] Đã export file ảnh `shap_summary.png` vào thư mục `figures/`.
- [ ] Viết 1 đoạn văn (Markdown) trong notebook giải thích 3 features quan trọng nhất dựa trên SHAP.
- [ ] Chạy file nộp bài cuối cùng (với dữ liệu test đầy đủ 549 dòng).
- [ ] Push code lên branch cá nhân và báo Tech Lead review.

---
*Chúc bạn sớm hoàn thành task để team kịp chuyển sang giai đoạn viết Report vào ngày mai!*

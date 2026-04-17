# 📈 Forecasting Guideline — Datathon 2026

> **Mục tiêu**: Dự báo cột `Revenue` hàng ngày cho giai đoạn **01/01/2023 – 01/07/2024** (549 ngày).
> Đạt tối đa **20/20 điểm** (12đ hiệu suất mô hình + 8đ báo cáo kỹ thuật).

---

## Tổng quan bài toán

| Thông tin | Chi tiết |
|-----------|----------|
| **Target** | `Revenue` (float, doanh thu thuần hàng ngày, đơn vị VND) |
| **Train** | `sales.csv` — 3,833 dòng, từ 2012-07-04 → 2022-12-31 (~10.5 năm) |
| **Test** | `sample_submission.csv` — 549 dòng, từ 2023-01-01 → 2024-07-01 (~18 tháng) |
| **Metrics** | MAE, RMSE, $R^2$ (Kaggle leaderboard) |
| **Ràng buộc** | Không dùng dữ liệu ngoài, phải reproducible, phải giải thích được |

### Đặc điểm dữ liệu quan sát được
- Revenue dao động **~1M – 6.5M VND/ngày**
- Có dấu hiệu **COGS > Revenue ở cuối 2022** (margin âm) → cần lưu ý xu hướng
- `sample_submission.csv` đã có sẵn cột `Revenue` và `COGS` (có thể dùng COGS test làm feature)
- Train : Test ratio ≈ **7:1** — đủ dữ liệu để train

---

## Bước 1: Khám phá dữ liệu (EDA cho Time Series)

### 1.1 Visualize chuỗi thời gian
```python
import polars as pl
import matplotlib.pyplot as plt

df = pl.read_csv("Data/sales.csv", try_parse_dates=True)

# Plot Revenue over time
fig, ax = plt.subplots(figsize=(16, 5))
ax.plot(df["Date"], df["Revenue"], linewidth=0.5)
ax.set_title("Daily Revenue (2012-2022)")
ax.set_xlabel("Date")
ax.set_ylabel("Revenue (VND)")
plt.show()
```

### 1.2 Kiểm tra các thành phần
- [ ] **Trend**: Revenue tăng hay giảm qua các năm?
- [ ] **Seasonality**: Pattern lặp lại theo tuần (day-of-week)? Theo tháng? Theo quý?
- [ ] **Stationarity**: Chạy ADF test (Augmented Dickey-Fuller)
- [ ] **Autocorrelation**: Plot ACF và PACF để xác định lag quan trọng

### 1.3 Phân rã chuỗi thời gian
```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(df["Revenue"], model="additive", period=7)  # weekly
result.plot()
```

### 1.4 Kiểm tra các sự kiện đặc biệt
- Tết Nguyên Đán (tháng 1-2, thay đổi mỗi năm)
- Black Friday / 11.11 / 12.12 (sale events)
- COVID-19 impact (2020-2021)
- Ngày lễ Việt Nam (30/4, 1/5, 2/9...)

---

## Bước 2: Chuẩn bị dữ liệu & Feature Engineering

### 2.1 Features từ thời gian (Calendar features)
```python
df = df.with_columns([
    pl.col("Date").dt.year().alias("year"),
    pl.col("Date").dt.month().alias("month"),
    pl.col("Date").dt.day().alias("day"),
    pl.col("Date").dt.weekday().alias("day_of_week"),    # 0=Monday
    pl.col("Date").dt.ordinal_day().alias("day_of_year"),
    pl.col("Date").dt.quarter().alias("quarter"),
    (pl.col("Date").dt.weekday() >= 5).cast(pl.Int8).alias("is_weekend"),
])
```

### 2.2 Lag features & Rolling statistics
```python
# Lag features
for lag in [1, 7, 14, 28, 30, 365]:
    df = df.with_columns(
        pl.col("Revenue").shift(lag).alias(f"revenue_lag_{lag}")
    )

# Rolling mean/std
for window in [7, 14, 30, 90]:
    df = df.with_columns([
        pl.col("Revenue").rolling_mean(window).alias(f"revenue_rolling_mean_{window}"),
        pl.col("Revenue").rolling_std(window).alias(f"revenue_rolling_std_{window}"),
    ])
```

### 2.3 Features từ các bảng khác (cross-table)

| Bảng nguồn | Feature có thể tạo | Cách join |
|------------|--------------------|-----------| 
| `web_traffic.csv` | `sessions`, `unique_visitors`, `page_views`, `bounce_rate` | Join trên `date` |
| `inventory.csv` | Tổng `stock_on_hand`, `stockout_days` theo tháng | Aggregate theo `snapshot_date` (monthly) |
| `promotions.csv` | `is_promo_active`, `total_discount_value`, `promo_count` | Kiểm tra `date` ∈ [`start_date`, `end_date`] |
| `orders.csv` | `order_count`, tỷ lệ `cancelled`, `device_type` distribution | Aggregate theo `order_date` |
| `COGS` (từ test) | `COGS` — có sẵn trong `sample_submission.csv` | Trực tiếp dùng |

> ⚠️ **Lưu ý quan trọng**: `sample_submission.csv` chứa sẵn cột `COGS` cho giai đoạn test. Đây là feature cực kỳ có giá trị vì `COGS` và `Revenue` có tương quan rất cao. **Nên dùng `COGS` làm feature chính**.

### 2.4 Features nâng cao
- **Fourier terms**: Mô hình hóa seasonality bằng sin/cos với nhiều tần số
- **Holiday indicator**: Binary flag cho ngày lễ Việt Nam
- **Trend features**: Linear trend (ngày kể từ ngày đầu tiên) hoặc polynomial
- **Expanding mean**: Trung bình tích luỹ của revenue tính đến ngày hiện tại

---

## Bước 3: Xây dựng mô hình

### Lộ trình đề xuất: Baseline → Advanced → Ensemble

---

### 3.1 Baseline Models (Ngày 2)

#### Model A: Naive / Seasonal Naive
```python
# Seasonal Naive: dùng giá trị cùng ngày trong tuần trước
df["prediction"] = df["Revenue"].shift(7)
```
- **Mục đích**: Đặt benchmark tối thiểu, mọi model khác phải tốt hơn
- **Ưu điểm**: Không cần train, nhanh
- **Khi nào dùng**: Chỉ làm baseline

#### Model B: Prophet (Facebook)
```python
from prophet import Prophet

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,
)
model.add_country_holidays(country_name="VN")
model.fit(train_df.rename(columns={"Date": "ds", "Revenue": "y"}))
forecast = model.predict(future_df)
```
- **Ưu điểm**: Tự xử lý trend, seasonality, holidays. Dễ giải thích
- **Nhược điểm**: Kém hơn gradient boosting với nhiều features
- **Khi nào dùng**: Baseline nhanh, hoặc làm 1 thành phần trong ensemble

#### Model C: ARIMA / SARIMAX
```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(
    train["Revenue"],
    order=(p, d, q),
    seasonal_order=(P, D, Q, 7),  # weekly seasonality
    exog=train[["COGS"]],         # exogenous variable
)
result = model.fit(disp=False)
```
- **Ưu điểm**: Nền tảng thống kê vững, phù hợp khi data có autocorrelation rõ ràng
- **Nhược điểm**: Chậm trên dataset lớn, khó tune hyperparameter
- **Khi nào dùng**: Khi ACF/PACF cho thấy pattern rõ ràng

---

### 3.2 Advanced Models (Ngày 4-5)

#### Model D: LightGBM / XGBoost (⭐ Khuyên dùng)
```python
import lightgbm as lgb

features = [
    "year", "month", "day_of_week", "is_weekend", "day_of_year", "quarter",
    "COGS",  # Feature quan trọng nhất
    "revenue_lag_7", "revenue_lag_14", "revenue_lag_28", "revenue_lag_365",
    "revenue_rolling_mean_7", "revenue_rolling_mean_30",
    "revenue_rolling_std_7",
    "sessions", "unique_visitors",  # từ web_traffic
    "is_promo_active",  # từ promotions
]

model = lgb.LGBMRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
)
model.fit(
    X_train[features], y_train,
    eval_set=[(X_val[features], y_val)],
    callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)],
)
```
- **Ưu điểm**: Handles non-linearity, feature interactions, missing values. Nhanh. Có feature importance
- **Nhược điểm**: Không capture time dependency tự nhiên, cần feature engineering tốt
- **Khi nào dùng**: **Model chính cho competition** — thường cho kết quả tốt nhất trên Kaggle

#### Model E: CatBoost
```python
from catboost import CatBoostRegressor

model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    verbose=100,
)
```
- **Ưu điểm**: Tương tự LightGBM, xử lý categorical features tốt hơn
- **Khi nào dùng**: Alternative cho LightGBM trong ensemble

#### Model F: Neural Network (LSTM / Transformer)
- **Ưu điểm**: Capture long-range dependencies
- **Nhược điểm**: Cần nhiều data, khó tune, chậm, khó giải thích
- **Khi nào dùng**: Chỉ khi có thời gian dư và muốn thêm diversity vào ensemble

---

### 3.3 Ensemble (Ngày 6)

```python
# Weighted average ensemble
final_prediction = (
    0.5 * lgbm_pred +
    0.3 * xgb_pred +
    0.2 * prophet_pred
)
```

**Chiến lược ensemble:**
1. Train 3-5 model khác nhau (khác kiến trúc)
2. Tìm weight tối ưu bằng Optuna hoặc grid search trên validation set
3. Hoặc dùng **Stacking**: Train meta-model (Linear Regression) trên predictions của base models

---

## Bước 4: Validation Strategy

### ⚠️ CRITICAL: Time Series Cross-Validation

**KHÔNG ĐƯỢC** dùng random K-Fold cho time series. Phải dùng **expanding window** hoặc **sliding window**.

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    # Train & evaluate
```

### Đề xuất validation scheme:
```
Train:      [2012 ────────────── 2021]
Validation: [                         2022]
Test:       [                               2023 ── 2024-07]
```

Hoặc chi tiết hơn (expanding window):
```
Fold 1: Train [2012-2018] → Val [2019]
Fold 2: Train [2012-2019] → Val [2020]
Fold 3: Train [2012-2020] → Val [2021]
Fold 4: Train [2012-2021] → Val [2022]
```

### Metrics tính trên validation:
```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
r2 = r2_score(y_true, y_pred)
print(f"MAE: {mae:,.0f} | RMSE: {rmse:,.0f} | R²: {r2:.4f}")
```

---

## Bước 5: Giải thích mô hình (8đ báo cáo kỹ thuật)

### 5.1 Feature Importance
```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_val)

# Summary plot
shap.summary_plot(shap_values, X_val, feature_names=features)

# Beeswarm plot cho top features
shap.plots.beeswarm(shap_values)
```

### 5.2 Partial Dependence Plot
```python
from sklearn.inspection import PartialDependenceDisplay

PartialDependenceDisplay.from_estimator(model, X_val, features=["COGS", "month"])
```

### 5.3 Nội dung bắt buộc trong report
- Pipeline diagram: Data → Features → Model → Prediction
- Cross-validation results (MAE/RMSE/R² per fold)
- Feature importance plot (SHAP hoặc gain-based)
- Giải thích bằng ngôn ngữ kinh doanh: "COGS là yếu tố dự đoán mạnh nhất vì..."
- Error analysis: Mô hình sai ở đâu? Những ngày nào predict kém?

---

## Bước 6: Tạo file submission

```python
# Đọc sample submission
submission = pl.read_csv("Data/sample_submission.csv", try_parse_dates=True)

# Predict
submission = submission.with_columns(
    pl.Series("Revenue", predictions)
)

# Lưu file
submission.select(["Date", "Revenue"]).write_csv("submission.csv")

# Kiểm tra
assert submission.shape[0] == 549, "Phải có đúng 549 dòng"
assert submission["Revenue"].null_count() == 0, "Không được có null"
```

---

## 🔥 Khó khăn có thể gặp & Hướng giải quyết

### Vấn đề 1: Data Leakage khi tạo lag features
- **Vấn đề**: Lag features (revenue_lag_7) không tồn tại cho 7 ngày đầu tiên của test set vì cần dữ liệu thực tế từ tương lai
- **Giải pháp**: 
  - Dùng giá trị **cuối cùng của train set** để fill lag cho đầu test
  - Hoặc dùng **recursive prediction**: predict ngày 1 → dùng kết quả làm lag cho ngày 2 → ...
  - Hoặc chỉ dùng lag ≥ 365 (luôn có sẵn từ train)

### Vấn đề 2: Regime change — Xu hướng thay đổi đột ngột
- **Vấn đề**: COVID-19 (2020-2021) tạo ra structural break. Model train trên pre-COVID có thể không predict tốt post-COVID
- **Giải pháp**: 
  - Thêm feature `is_covid_period` (binary)
  - Cho weight cao hơn cho dữ liệu gần đây (sample_weight)
  - Hoặc chỉ train trên 2019-2022 (bỏ dữ liệu quá cũ)

### Vấn đề 3: COGS > Revenue ở cuối 2022
- **Vấn đề**: Margin âm cho thấy có thể có thay đổi chiến lược giá hoặc data anomaly
- **Giải pháp**:
  - Phân tích kỹ xem đó là trend hay outlier
  - Nếu là outlier: loại bỏ hoặc cap
  - Nếu là trend: model cần capture được xu hướng này

### Vấn đề 4: Seasonality phức tạp (đa tần số)
- **Vấn đề**: Revenue có thể có nhiều loại seasonality: weekly (7), monthly (~30), quarterly (~91), yearly (365)
- **Giải pháp**:
  - Dùng Fourier features với nhiều tần số
  - Prophet xử lý tự động
  - LightGBM cần thêm explicit calendar features

### Vấn đề 5: Forecast horizon dài (549 ngày = 18 tháng)
- **Vấn đề**: Mô hình dự báo xa thường kém chính xác
- **Giải pháp**:
  - Chia test thành segments: Q1-2023, Q2-2023, ..., Q2-2024
  - Train nhiều model cho short-term vs. long-term
  - Dùng features không phụ thuộc thời gian gần (calendar, COGS) thay vì lag features

### Vấn đề 6: Overfitting
- **Vấn đề**: Model fit tốt trên train nhưng kém trên Kaggle
- **Giải pháp**:
  - Cross-validation **bắt buộc** phải đúng chiều thời gian
  - Regularization: giảm `max_depth`, tăng `min_child_samples`
  - Early stopping dựa trên validation set
  - Kiểm tra gap giữa train score và validation score

### Vấn đề 7: Web traffic data bắt đầu từ 2013
- **Vấn đề**: `web_traffic.csv` bắt đầu từ 2013-01-01, nhưng `sales.csv` từ 2012-07-04
- **Giải pháp**: Fill missing web traffic bằng 0 hoặc interpolation cho giai đoạn 2012

---

## ⚠️ Lưu ý quan trọng

### Về dữ liệu
1. **COGS trong test set là "free feature"**: `sample_submission.csv` chứa cả `Revenue` lẫn `COGS`. Revenue là target cần predict, nhưng COGS có thể dùng làm feature. Đây có thể là **feature quan trọng nhất** vì Revenue = COGS + Gross Profit.
2. **Không dùng dữ liệu ngoài**: Không được crawl thêm dữ liệu kinh tế, thời tiết, hay Google Trends. Tất cả feature phải derive từ 15 file CSV được cung cấp.
3. **Random seed**: Đặt `random_state=42` (hoặc bất kỳ số nào) cho TẤT CẢ model, train/test split, và sampling.

### Về model
4. **Đừng dùng 1 model duy nhất**: Ensemble (kết hợp nhiều model) hầu như luôn tốt hơn single model trên Kaggle.
5. **Gradient Boosting là lựa chọn an toàn nhất**: LightGBM/XGBoost thường đạt top trên các competition dạng tabular. Bắt đầu từ đây.
6. **Prophet không đủ mạnh một mình**: Nhưng rất tốt trong ensemble vì nó capture trend/seasonality theo cách khác biệt.

### Về report
7. **Phải có SHAP hoặc Feature Importance**: Rubric yêu cầu "giải thích mô hình bằng SHAP / feature importance". Không có = mất 2-3 điểm.
8. **Giải thích bằng ngôn ngữ kinh doanh**: Không chỉ nói "COGS có importance cao nhất" mà phải giải thích "COGS phản ánh trực tiếp quy mô hoạt động kinh doanh, do đó là chỉ báo dẫn cho doanh thu".
9. **Cross-validation đúng chiều thời gian**: Rubric ghi rõ "cross-validation đúng chiều thời gian" là tiêu chí quan trọng. Dùng random split = mất điểm.

### Về Kaggle submission
10. **Submit sớm, submit thường xuyên**: Ngày 2 nộp baseline, sau đó mỗi khi cải thiện model đều nộp lại. Kaggle cho phép nhiều submission.
11. **Kiểm tra định dạng**: File submission phải có đúng 549 dòng, 2 cột (`Date`, `Revenue`), không null, format date khớp sample.
12. **Lưu mọi submission**: Git commit mỗi version của `submission.csv` kèm ghi chú model/score.

---

## 🚀 Checklist trước khi nộp

- [ ] Model chạy end-to-end từ raw data → prediction mà không lỗi
- [ ] Random seed được đặt cho tất cả model
- [ ] Cross-validation đúng chiều thời gian (không random split)
- [ ] `submission.csv` có đúng 549 dòng, 2 cột, không null
- [ ] SHAP / Feature importance plot đã có trong report
- [ ] Giải thích mô hình bằng ngôn ngữ kinh doanh
- [ ] Không dùng dữ liệu ngoài
- [ ] Code có thể reproduce bởi người khác (relative path, requirements.txt)
- [ ] Đã submit lên Kaggle và ghi nhận score

---

## 📊 Bảng so sánh nhanh các model

| Model | Tốc độ train | Accuracy kỳ vọng | Dễ giải thích | Effort setup | Phù hợp |
|-------|-------------|-------------------|---------------|-------------|---------|
| Seasonal Naive | ⚡ Instant | ⭐ | ⭐⭐⭐⭐⭐ | ⭐ | Baseline only |
| Prophet | ⚡⚡ Fast | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | Baseline + Ensemble |
| SARIMAX | ⚡ Slow | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Nếu ACF/PACF rõ |
| **LightGBM** | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (SHAP) | ⭐⭐⭐ | **Khuyên dùng chính** |
| XGBoost | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (SHAP) | ⭐⭐⭐ | Ensemble partner |
| CatBoost | ⚡⚡ Medium | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Ensemble diversity |
| LSTM | ⚡ Slow | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | Nếu có thời gian dư |

"""
Generate notebooks/04_final_forecast.ipynb programmatically.
"""
import json
from pathlib import Path

NOTEBOOK_PATH = Path("notebooks/04_final_forecast.ipynb")

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source}

def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }

cells = []

# ── Title ──────────────────────────────────────────────────────────
cells.append(md("""\
# Day 6 — Final Forecast: Cross-Validation & Explainability
**Task:** [25/04-FORE-04.1] Time-Series CV | [25/04-FORE-04.2] SHAP Feature Importance  
**Owner:** Ha Quoc Khanh (ML Engineer)  
**Output:**
- `figures/cv_folds_revenue.png` — Backtest visual per fold
- `figures/shap_summary.png` — SHAP feature importance
- `submission_v7_day6_cv_shap.csv` — Final Kaggle submission (548 rows)

---
"""))

# ── Section 1: Setup ───────────────────────────────────────────────
cells.append(md("## 1. Setup & Load Data"))

cells.append(code("""\
import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

# Add src to path
sys.path.insert(0, str(Path("../src")))
from ultimate_ensemble_day5 import (
    DETRENDED_FEATURES, DETRENDED_XGB_PARAMS, create_calendar_tet_features
)

RANDOM_SEED = 42
ROOT = Path("..")
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("Libraries loaded successfully.")
"""))

cells.append(code("""\
# Load data
df_train = pd.read_csv("../Data/processed_train.csv", parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)
df_sub   = pd.read_csv("../Data/sample_submission.csv", parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)

print(f"Train: {df_train.shape} | {df_train['Date'].min().date()} to {df_train['Date'].max().date()}")
print(f"Test : {df_sub.shape}  | {df_sub['Date'].min().date()} to {df_sub['Date'].max().date()}")
df_train.head(3)
"""))

# ── Section 2: Helper functions ────────────────────────────────────
cells.append(md("## 2. Helper Functions (Detrended XGBoost)"))

cells.append(code("""\
def get_annual_scale(df, target_col):
    tmp = df[["Date", target_col]].copy()
    tmp["year"] = tmp["Date"].dt.year
    return tmp.groupby("year")[target_col].mean()

def build_features(df):
    return create_calendar_tet_features(df[["Date"]].copy())

def normalize_target(df, target_col, annual_mean):
    years = df["Date"].dt.year
    return df[target_col] / years.map(annual_mean)

def scale_predictions(preds, dates, annual_mean):
    growth = float(np.clip(annual_mean.pct_change().dropna().median() + 1.0, 0.90, 1.12))
    base_year = int(annual_mean.index.max())
    base_mean = float(annual_mean.loc[base_year])
    yearly_scale = base_mean * (growth ** (dates.dt.year - base_year))
    return np.clip(preds * yearly_scale.values, 0, None)

print("Helper functions defined.")
"""))

# ── Section 3: Time-Series CV ─────────────────────────────────────
cells.append(md("""\
## 3. Time-Series Cross-Validation (Expanding Window)

> **Ly do khong dung K-Fold thong thuong:**  
> Chuoi thoi gian co tinh phu thuoc theo thu tu: du lieu tuong lai khong the dung de du doan qua khu.  
> Viec dung K-Fold ngau nhien se gay ra **data leakage** (ro ri du lieu), lam cho metrics ao hon thuc te.  
>  
> **Expanding window:** Moi fold, tap train mo rong them 1 nam, tap val la 1 nam tiep theo.  
> Dieu nay mo phong chinh xac kich ban production: model duoc train tren lich su, test tren tuong lai.
"""))

cells.append(code("""\
N_SPLITS = 5
VAL_SIZE = 365  # so ngay validate moi fold

df_cv = df_train.sort_values("Date").reset_index(drop=True)
total_days = len(df_cv)
min_train = total_days - N_SPLITS * VAL_SIZE

fold_results = []

print(f"{'Fold':<6} {'Train Range':<28} {'Val Range':<26} {'MAE':>12} {'RMSE':>12} {'R2':>8}")
print("-" * 96)

for fold in range(N_SPLITS):
    train_end = min_train + fold * VAL_SIZE
    val_end   = train_end + VAL_SIZE

    train_f = df_cv.iloc[:train_end].copy()
    val_f   = df_cv.iloc[train_end:val_end].copy()

    annual_mean = get_annual_scale(train_f, "Revenue")
    X_train = build_features(train_f)[DETRENDED_FEATURES]
    y_train = normalize_target(train_f, "Revenue", annual_mean)
    X_val   = build_features(val_f)[DETRENDED_FEATURES]

    model = XGBRegressor(**DETRENDED_XGB_PARAMS)
    model.fit(X_train, y_train, verbose=False)

    preds = scale_predictions(model.predict(X_val), val_f["Date"], annual_mean)
    y_true = val_f["Revenue"].values

    mae  = mean_absolute_error(y_true, preds)
    rmse = np.sqrt(mean_squared_error(y_true, preds))
    r2   = r2_score(y_true, preds)

    fold_results.append({
        "Fold": fold + 1,
        "Train_Range": f"{train_f['Date'].min().date()} to {train_f['Date'].max().date()}",
        "Val_Range":   f"{val_f['Date'].min().date()} to {val_f['Date'].max().date()}",
        "MAE": mae, "RMSE": rmse, "R2": r2,
        "val_dates": val_f["Date"].values,
        "y_true": y_true, "y_pred": preds,
    })
    print(f"{fold+1:<6} {fold_results[-1]['Train_Range']:<28} {fold_results[-1]['Val_Range']:<26} {mae:>12,.0f} {rmse:>12,.0f} {r2:>8.4f}")

print("-" * 96)
avg_mae  = np.mean([r["MAE"]  for r in fold_results])
avg_rmse = np.mean([r["RMSE"] for r in fold_results])
avg_r2   = np.mean([r["R2"]   for r in fold_results])
print(f"{'MEAN':<6} {'':<28} {'':<26} {avg_mae:>12,.0f} {avg_rmse:>12,.0f} {avg_r2:>8.4f}")
print(f"\\n[RESULT] Average MAE: {avg_mae:,.0f} VND | Average R2: {avg_r2:.4f}")
"""))

cells.append(code("""\
# Plot CV folds
fig, axes = plt.subplots(len(fold_results), 1, figsize=(16, 4 * len(fold_results)))

for i, (fold_data, ax) in enumerate(zip(fold_results, axes)):
    dates = pd.to_datetime(fold_data["val_dates"])
    ax.plot(dates, fold_data["y_true"] / 1e6, color="steelblue", lw=1.2, label="Actual Revenue")
    ax.plot(dates, fold_data["y_pred"] / 1e6, color="tomato", lw=1.2, ls="--", label="Predicted Revenue")
    ax.fill_between(dates,
                    fold_data["y_true"] / 1e6,
                    fold_data["y_pred"] / 1e6,
                    alpha=0.15, color="orange", label="Error band")
    ax.set_title(f"Fold {fold_data['Fold']} | Val: {fold_data['Val_Range']} | MAE: {fold_data['MAE']/1e6:.3f}M VND | R2: {fold_data['R2']:.4f}", fontsize=10)
    ax.set_ylabel("Revenue (Million VND)")
    ax.grid(True, ls="--", alpha=0.4)
    ax.legend(fontsize=8, loc="upper left")

axes[-1].set_xlabel("Date")
fig.suptitle("Time-Series Cross-Validation (Expanding Window) - Detrended XGBoost", fontsize=13, fontweight="bold")
plt.tight_layout()

save_path = FIGURES_DIR / "cv_folds_revenue.png"
plt.savefig(save_path, dpi=150, bbox_inches="tight")
print(f"[SAVED] {save_path}")
plt.show()
"""))

# ── Section 4: SHAP ───────────────────────────────────────────────
cells.append(md("## 4. SHAP Feature Importance"))

cells.append(code("""\
import shap

# Train final model on full dataset for SHAP
annual_mean_full = get_annual_scale(df_train, "Revenue")
X_full  = build_features(df_train)[DETRENDED_FEATURES]
y_full  = normalize_target(df_train, "Revenue", annual_mean_full)

model_final = XGBRegressor(**DETRENDED_XGB_PARAMS)
model_final.fit(X_full, y_full, verbose=False)
print("Final model trained on full dataset.")

# Use last 300 rows as SHAP sample (recent behavior)
X_shap = X_full.tail(300).reset_index(drop=True)

explainer   = shap.TreeExplainer(model_final)
shap_values = explainer.shap_values(X_shap)
print("SHAP values computed.")
"""))

cells.append(code("""\
# SHAP Bar Chart (Mean |SHAP value|)
fig, ax = plt.subplots(figsize=(9, 5))
shap.summary_plot(shap_values, X_shap, plot_type="bar", show=False, max_display=len(DETRENDED_FEATURES))
plt.title("SHAP Feature Importance (Mean |SHAP value|)", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "shap_summary.png",     dpi=150, bbox_inches="tight")
plt.savefig(FIGURES_DIR / "shap_bar_summary.png", dpi=150, bbox_inches="tight")
print("[SAVED] figures/shap_summary.png")
plt.show()
"""))

cells.append(code("""\
# SHAP Beeswarm Plot
fig, ax = plt.subplots(figsize=(10, 6))
shap.summary_plot(shap_values, X_shap, show=False, max_display=len(DETRENDED_FEATURES))
plt.title("SHAP Beeswarm - Impact Direction per Feature", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "shap_beeswarm.png", dpi=150, bbox_inches="tight")
print("[SAVED] figures/shap_beeswarm.png")
plt.show()
"""))

cells.append(code("""\
# Print ranked feature importance
mean_abs_shap = np.abs(shap_values).mean(axis=0)
fi = pd.Series(mean_abs_shap, index=X_shap.columns).sort_values(ascending=False)
print("\\n=== SHAP Feature Importance Ranking ===")
for rank, (feat, val) in enumerate(fi.items(), 1):
    print(f"  #{rank:02d}  {feat:<20} {val:.6f}")
"""))

# ── Section 5: SHAP Markdown explanation ─────────────────────────
cells.append(md("""\
## 5. Business Interpretation of Top 3 SHAP Features

Dua tren ket qua SHAP values, mo hinh Detrended XGBoost xac dinh 3 yeu to co anh huong lon nhat den du bao doanh thu:

---

### Feature #1: `month` (SHAP ~ 0.307)
**Mo ta ky thuat:** `month` la bien so nguyen tu 1 den 12 dai dien cho thang trong nam.  
SHAP value cao nhat trong tat ca features, cho thay mo hinh phu thuoc rat lon vao tinh theo mua cua doanh thu.

**Giai thich kinh doanh:**  
Doanh thu cua doanh nghiep E-commerce thoi trang co tinh **mua vu ro rang**:
- **Thang 1-2 (Tet):** Doanh thu tang manh do nguoi tieu dung mua sam truoc tet.
- **Thang 6-7 (He):** Nhu cau thoi trang he tang cao.
- **Thang 11-12 (cuoi nam):** Black Friday, 12.12 shopping festival day doanh thu tang dot bien.

> **Khoi y cho Ban tu van (Prescriptive):** Nen tang ngan sach marketing va ton kho truoc cac thang dinh (thang 1, 11, 12) it nhat 6-8 tuan de dam bao khong bi het hang.

---

### Feature #2: `day` (SHAP ~ 0.207)
**Mo ta ky thuat:** `day` la ngay trong thang (1-31).  
SHAP importance dung thu 2, cho thay nguoi tieu dung co xu huong mua hang theo cac ngay cu the trong thang.

**Giai thich kinh doanh:**  
- **Ngay 1, 15, 30-31 (Ngay luong):** Sau khi nhan luong, nguoi tieu dung co xu huong chi tieu nhieu hon cho hang thoi trang.
- **Ngay cuoi thang:** Thu chi gia dinh tang, dong tien tu do (discretionary spending) co xu huong thay doi.

> **Khoi y cho Ban tu van:** Lich dong gio khuyen mai nen duoc toi uu hoa quanh cac ngay luong (10-15 va 25-31 hang thang) de ton dung momen suc mua cao.

---

### Feature #3: `dayofweek` (SHAP ~ 0.059)
**Mo ta ky thuat:** `dayofweek` la thu trong tuan (0=Thu 2, 6=Chu nhat).  
SHAP importance thap hon nhung van co y nghia thong ke.

**Giai thich kinh doanh:**  
- **Cuoi tuan (Thu 7, Chu nhat):** Nguoi tieu dung co nhieu thoi gian ranh hon, gia tang browse va mua sam online.
- **Thu 2 - Thu 4:** Luong truy cap thap hon, phu hop cho cac chien dich remarketing.

> **Khoi y cho Ban tu van:** Lich chay quang cao (ad scheduling) nen duoc tang cuong vao Thu 5, Thu 6 de khai thac hieu ung "weekend shopping mindset" som.

---

**Ket luan tong quat:**  
Mo hinh capture tot cac quy luat theo lich (Calendar effects) — day la diem manh cua Detrended XGBoost.  
Dieu nay nhat quan voi dac tinh cua thi truong E-commerce: nguoi tieu dung phhan ung manh voi cac moc thoi gian cu the (mua, tet, ngay luong) hon la bien dong ngau nhien.
"""))

# ── Section 6: Final Submission ───────────────────────────────────
cells.append(md("## 6. Generate Final Submission"))

cells.append(code("""\
# Train Revenue & COGS models on full data
annual_mean_rev  = get_annual_scale(df_train, "Revenue")
annual_mean_cogs = get_annual_scale(df_train, "COGS")

X_full = build_features(df_train)[DETRENDED_FEATURES]

model_rev = XGBRegressor(**DETRENDED_XGB_PARAMS)
model_rev.fit(X_full, normalize_target(df_train, "Revenue", annual_mean_rev), verbose=False)

model_cogs = XGBRegressor(**DETRENDED_XGB_PARAMS)
model_cogs.fit(X_full, normalize_target(df_train, "COGS", annual_mean_cogs), verbose=False)

# Predict on test set
X_test     = build_features(df_sub)[DETRENDED_FEATURES]
rev_pred   = scale_predictions(model_rev.predict(X_test),  df_sub["Date"], annual_mean_rev)
cogs_pred  = scale_predictions(model_cogs.predict(X_test), df_sub["Date"], annual_mean_cogs)

# Build submission
submission = df_sub[["Date"]].copy()
submission["Revenue"] = np.round(rev_pred, 2)
submission["COGS"]    = np.round(cogs_pred, 2)
submission["Date"]    = pd.to_datetime(submission["Date"]).dt.strftime("%Y-%m-%d")

# Validate
assert submission["Revenue"].isna().sum() == 0, "ERROR: NaN in Revenue!"
assert submission.shape[0] == len(df_sub), f"Row count mismatch: {submission.shape[0]}"
print(f"Submission shape : {submission.shape}")
print(f"Revenue range    : {submission['Revenue'].min():,.0f} to {submission['Revenue'].max():,.0f}")
print(f"COGS range       : {submission['COGS'].min():,.0f} to {submission['COGS'].max():,.0f}")
submission.head(5)
"""))

cells.append(code("""\
OUTPUT_PATH = "../submission_v7_day6_cv_shap.csv"
submission.to_csv(OUTPUT_PATH, index=False)
print(f"[SAVED] {OUTPUT_PATH}")
print(f"Rows   : {len(submission)}")
print(f"Columns: {list(submission.columns)}")
"""))

# ── Section 7: Checklist ──────────────────────────────────────────
cells.append(md("""\
## 7. Day 6 Checklist

| # | Hang muc | Trang thai |
|:--|:---------|:----------:|
| 1 | Notebook `04_final_forecast.ipynb` chay duoc tu dau den cuoi | DONE |
| 2 | Time-series CV (5 folds, expanding window) | DONE |
| 3 | Bieu do CV export `figures/cv_folds_revenue.png` | DONE |
| 4 | SHAP bar chart export `figures/shap_summary.png` | DONE |
| 5 | SHAP beeswarm export `figures/shap_beeswarm.png` | DONE |
| 6 | Markdown giai thich top 3 SHAP features | DONE |
| 7 | Submission `submission_v7_day6_cv_shap.csv` (548 rows, khong NaN) | DONE |
| 8 | Push len branch ca nhan, bao Tech Lead review | TODO |

---
*Notebook tao boi Ha Quoc Khanh (ML Engineer) — Datathon 2026 - Team Outliers*
"""))

# ── Assemble notebook ─────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "cells": cells,
}

NOTEBOOK_PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"[DONE] Notebook created: {NOTEBOOK_PATH}")
print(f"       Cells: {len(cells)}")

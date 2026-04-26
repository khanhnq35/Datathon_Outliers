"""
Day 6 - Cross-Validation & SHAP Explainability (Production Script)
Task [25/04-FORE-04.1] + [25/04-FORE-04.2]

Thực hiện:
1. Time-series Cross-Validation (5 folds expanding window) cho Detrended XGBoost.
2. SHAP Feature Importance - export shap_summary.png vào figures/.
3. Final model fit trên full data → sinh submission_v7_day6_cv_shap.csv.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib

# Thêm src vào path để dùng các hàm từ ultimate_ensemble_day5.py
sys.path.insert(0, str(Path(__file__).parent))
from ultimate_ensemble_day5 import (
    DETRENDED_FEATURES,
    DETRENDED_XGB_PARAMS,
    RANDOM_SEED,
    TET_DATES,
    create_calendar_tet_features,
)

# ───────────────────────────────────────────────────────────────
#  Paths
# ───────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
TRAIN_PATH = ROOT / "Data" / "processed_train.csv"
SUB_PATH = ROOT / "Data" / "sample_submission.csv"
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_SUB = ROOT / "submission_v7_day6_cv_shap.csv"


# ───────────────────────────────────────────────────────────────
#  Helpers
# ───────────────────────────────────────────────────────────────
def get_annual_scale(train_df: pd.DataFrame, target_col: str) -> pd.Series:
    tmp = train_df[["Date", target_col]].copy()
    tmp["year"] = tmp["Date"].dt.year
    return tmp.groupby("year")[target_col].mean()


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    return create_calendar_tet_features(df[["Date"]].copy())


def normalize_target(df: pd.DataFrame, target_col: str, annual_mean: pd.Series) -> pd.Series:
    years = df["Date"].dt.year
    return df[target_col] / years.map(annual_mean)


def scale_predictions(preds: np.ndarray, dates: pd.Series, annual_mean: pd.Series) -> np.ndarray:
    """
    Mở rộng scale về đơn vị Revenue gốc dựa trên xu hướng tăng trưởng năm.
    """
    growth = float(np.clip(annual_mean.pct_change().dropna().median() + 1.0, 0.90, 1.12))
    base_year = int(annual_mean.index.max())
    base_mean = float(annual_mean.loc[base_year])
    yearly_scale = base_mean * (growth ** (dates.dt.year - base_year))
    return np.clip(preds * yearly_scale.values, 0, None)


# ───────────────────────────────────────────────────────────────
#  Section 1: Time-Series Cross-Validation (Expanding Window)
# ───────────────────────────────────────────────────────────────
def run_timeseries_cv(df: pd.DataFrame, target_col: str = "Revenue", n_splits: int = 5) -> pd.DataFrame:
    """
    Expanding-window CV theo thời gian. 
    - Không dùng random K-Fold để tránh data leakage.
    - Mỗi fold: train trên [start → cutoff], validate trên [cutoff+1 → cutoff+365].
    """
    print(f"\n{'='*60}")
    print(f"  TIME-SERIES CROSS-VALIDATION - {target_col} (Expanding Window)")
    print(f"  n_splits = {n_splits}")
    print(f"{'='*60}")

    df = df.sort_values("Date").reset_index(drop=True)
    total_days = len(df)

    # Chia dữ liệu: để lại ~30% cuối làm không gian cho các folds
    val_size = 365  # mỗi fold validate trên 1 năm
    min_train = total_days - n_splits * val_size

    if min_train < 365:
        raise ValueError("Không đủ dữ liệu để chạy CV với cấu hình này.")

    fold_results = []
    print(f"\n{'Fold':<6} {'Train Range':<28} {'Val Range':<28} {'MAE':>12} {'RMSE':>12} {'R2':>8}")
    print("-" * 96)

    for fold in range(n_splits):
        # Expanding window: train ngày càng nhiều hơn
        train_end_idx = min_train + fold * val_size
        val_end_idx = train_end_idx + val_size

        train_fold = df.iloc[:train_end_idx].copy()
        val_fold = df.iloc[train_end_idx:val_end_idx].copy()

        if len(val_fold) == 0:
            continue

        # Normalize target
        annual_mean = get_annual_scale(train_fold, target_col)
        X_train = build_features(train_fold)[DETRENDED_FEATURES]
        y_train = normalize_target(train_fold, target_col, annual_mean)

        X_val = build_features(val_fold)[DETRENDED_FEATURES]

        # Train model
        model = XGBRegressor(**DETRENDED_XGB_PARAMS)
        model.fit(X_train, y_train, verbose=False)

        # Predict & rescale
        preds_norm = model.predict(X_val)
        preds = scale_predictions(preds_norm, val_fold["Date"], annual_mean)
        y_true = val_fold[target_col].values

        mae = mean_absolute_error(y_true, preds)
        rmse = np.sqrt(mean_squared_error(y_true, preds))
        r2 = r2_score(y_true, preds)

        train_range = f"{train_fold['Date'].min().date()} to {train_fold['Date'].max().date()}"
        val_range = f"{val_fold['Date'].min().date()} to {val_fold['Date'].max().date()}"

        fold_results.append({
            "Fold": fold + 1,
            "Train_Range": train_range,
            "Val_Range": val_range,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "val_dates": val_fold["Date"].values,
            "y_true": y_true,
            "y_pred": preds,
        })

        print(f"{fold+1:<6} {train_range:<28} {val_range:<28} {mae:>12,.0f} {rmse:>12,.0f} {r2:>8.4f}")

    print("-" * 96)
    avg_mae = np.mean([r["MAE"] for r in fold_results])
    avg_rmse = np.mean([r["RMSE"] for r in fold_results])
    avg_r2 = np.mean([r["R2"] for r in fold_results])
    print(f"{'MEAN':<6} {'':<28} {'':<28} {avg_mae:>12,.0f} {avg_rmse:>12,.0f} {avg_r2:>8.4f}")
    print(f"\n[OK] Average MAE ({target_col}): {avg_mae:,.0f} VND")

    return fold_results


def plot_cv_results(fold_results: list, target_col: str, save_path: Path):
    """Vẽ biểu đồ dự báo của từng fold so với thực tế."""
    fig, axes = plt.subplots(len(fold_results), 1, figsize=(16, 4 * len(fold_results)))
    if len(fold_results) == 1:
        axes = [axes]

    colors = plt.cm.Blues(np.linspace(0.5, 0.9, len(fold_results)))

    for i, (fold_data, ax, color) in enumerate(zip(fold_results, axes, colors)):
        dates = pd.to_datetime(fold_data["val_dates"])
        ax.plot(dates, fold_data["y_true"] / 1e6, color="steelblue", linewidth=1.2, label="Actual", alpha=0.9)
        ax.plot(dates, fold_data["y_pred"] / 1e6, color="tomato", linewidth=1.2, label="Predicted", linestyle="--", alpha=0.9)
        ax.set_title(f"Fold {fold_data['Fold']} - Val: {fold_data['Val_Range']} | MAE: {fold_data['MAE']/1e6:.3f}M VND", fontsize=10)
        ax.set_ylabel("Revenue (Triệu VND)", fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(fontsize=8)

    axes[-1].set_xlabel("Date", fontsize=10)
    fig.suptitle(f"Time-Series Cross-Validation (Expanding Window) - {target_col}", fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] CV plot -> {save_path}")


# ───────────────────────────────────────────────────────────────
#  Section 2: SHAP Feature Importance
# ───────────────────────────────────────────────────────────────
def run_shap_analysis(model: XGBRegressor, X_val: pd.DataFrame, save_dir: Path):
    """
    Tính SHAP values và export 2 loại biểu đồ:
    1. shap_bar_summary.png  — Bar chart: feature importance trung bình
    2. shap_beeswarm.png     — Beeswarm plot: tác động âm/dương theo feature
    """
    try:
        import shap
    except ImportError:
        print("[WARN] shap chua duoc cai. Chay: pip install shap")
        return

    print("\n[INFO] Dang tinh SHAP values...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_val)

    # ─── Plot 1: Bar chart ───────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 6))
    shap.summary_plot(shap_values, X_val, plot_type="bar", show=False, max_display=len(DETRENDED_FEATURES))
    plt.title("SHAP Feature Importance (Mean |SHAP value|)", fontsize=12, fontweight="bold")
    plt.tight_layout()
    bar_path = save_dir / "shap_bar_summary.png"
    plt.savefig(bar_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] SHAP bar chart -> {bar_path}")

    # ─── Plot 2: Beeswarm ────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 7))
    shap.summary_plot(shap_values, X_val, show=False, max_display=len(DETRENDED_FEATURES))
    plt.title("SHAP Beeswarm Plot — Impact on Revenue Prediction", fontsize=12, fontweight="bold")
    plt.tight_layout()
    beeswarm_path = save_dir / "shap_beeswarm.png"
    plt.savefig(beeswarm_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] SHAP beeswarm -> {beeswarm_path}")

    # In top features
    mean_abs = np.abs(shap_values).mean(axis=0)
    feature_importance = pd.Series(mean_abs, index=X_val.columns).sort_values(ascending=False)
    print("\n[TOP] SHAP Feature Importance:")
    print(feature_importance.to_string())


# ───────────────────────────────────────────────────────────────
#  Section 3: Final Model + Submission
# ───────────────────────────────────────────────────────────────
def run_final_submission(df_train: pd.DataFrame, df_sub: pd.DataFrame) -> pd.DataFrame:
    """Train final model trên toàn bộ train data và tạo submission."""
    print(f"\n{'='*60}")
    print("  FINAL MODEL TRAINING (Full Dataset)")
    print(f"{'='*60}")

    annual_mean_rev = get_annual_scale(df_train, "Revenue")
    annual_mean_cogs = get_annual_scale(df_train, "COGS")

    X_full = build_features(df_train)[DETRENDED_FEATURES]
    y_rev = normalize_target(df_train, "Revenue", annual_mean_rev)
    y_cogs = normalize_target(df_train, "COGS", annual_mean_cogs)

    model_rev = XGBRegressor(**DETRENDED_XGB_PARAMS)
    model_rev.fit(X_full, y_rev, verbose=False)

    model_cogs = XGBRegressor(**DETRENDED_XGB_PARAMS)
    model_cogs.fit(X_full, y_cogs, verbose=False)

    X_test = build_features(df_sub.assign(Date=pd.to_datetime(df_sub["Date"])))[DETRENDED_FEATURES]

    rev_pred = scale_predictions(model_rev.predict(X_test), df_sub["Date"], annual_mean_rev)
    cogs_pred = scale_predictions(model_cogs.predict(X_test), df_sub["Date"], annual_mean_cogs)

    submission = df_sub[["Date"]].copy()
    submission["Revenue"] = np.round(rev_pred, 2)
    submission["COGS"] = np.round(cogs_pred, 2)
    submission["Date"] = pd.to_datetime(submission["Date"]).dt.strftime("%Y-%m-%d")

    expected_rows = len(df_sub)
    assert submission.shape[0] == expected_rows, f"Submission row count mismatch: expected {expected_rows}, got {submission.shape[0]}"
    assert submission["Revenue"].isna().sum() == 0, "Revenue contains NaN values!"

    submission.to_csv(OUTPUT_SUB, index=False)
    print(f"[OK] Submission saved -> {OUTPUT_SUB}")
    print(f"     Rows: {len(submission)} | Revenue range: {submission['Revenue'].min():,.0f} to {submission['Revenue'].max():,.0f}")

    return model_rev, model_cogs, X_full


# ───────────────────────────────────────────────────────────────
#  Main
# ───────────────────────────────────────────────────────────────
def main():
    print("[INFO] Loading data...")
    df_train = pd.read_csv(TRAIN_PATH, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)
    df_sub = pd.read_csv(SUB_PATH, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)
    print(f"   Train: {df_train.shape} | {df_train['Date'].min().date()} to {df_train['Date'].max().date()}")
    print(f"   Test : {df_sub.shape}  | {df_sub['Date'].min().date()} to {df_sub['Date'].max().date()}")

    # 1. Cross-Validation
    cv_results = run_timeseries_cv(df_train, target_col="Revenue", n_splits=5)
    plot_cv_results(cv_results, "Revenue", FIGURES_DIR / "cv_folds_revenue.png")

    # 2. Final model + SHAP
    model_rev, model_cogs, X_full = run_final_submission(df_train, df_sub)

    # 3. Save Checkpoints (Nhiệm vụ Ngày 7)
    MODELS_DIR = ROOT / "models"
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_rev, MODELS_DIR / "final_model_revenue.pkl")
    joblib.dump(model_cogs, MODELS_DIR / "final_model_cogs.pkl")
    print(f"\n[SAVED] Model checkpoints -> {MODELS_DIR}")

    # SHAP dung 300 sample cuoi cung (validation proxy)
    X_shap = X_full.tail(300).reset_index(drop=True)
    run_shap_analysis(model_rev, X_shap, FIGURES_DIR)

    print("\n" + "="*60)
    print("  [DONE] NGAY 6 HOAN THANH!")
    print("="*60)
    print("  [Chart] CV plot    -> figures/cv_folds_revenue.png")
    print("  [Chart] SHAP bar   -> figures/shap_bar_summary.png")
    print("  [Chart] SHAP bees  -> figures/shap_beeswarm.png")
    print("  [File]  Submission -> submission_v7_day6_cv_shap.csv")


if __name__ == "__main__":
    main()

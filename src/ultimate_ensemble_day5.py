"""
Day 5 - Ultimate Forecasting Optimization (Production Script)

Điểm nâng cấp chính so với bản cũ:
1) Có rolling-origin backtest chuẩn horizon 548 ngày trước khi chốt model.
2) Tránh phụ thuộc quá nhiều vào recursive feature giả lập (mean-fill exogenous).
3) Auto-chọn chiến lược tốt nhất theo MAE trung bình Revenue/COGS.

Strategies hỗ trợ:
- detrended: Detrended XGBoost (khuyến nghị mặc định).
- legacy_recursive: Mô phỏng hướng recursive Day 5 cũ (để đối chiếu).
- hybrid: Blend detrended + legacy (để thử nghiệm tính robust).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


RANDOM_SEED = 42
HORIZON = 548

LEGACY_FEATURES = [
    "month",
    "day",
    "dayofweek",
    "is_weekend",
    "is_payday",
    "is_double_day",
    "traffic",
    "is_promo",
    "total_units_sold_lag1",
    "revenue_lag_1",
    "revenue_lag_7",
    "revenue_lag_14",
    "revenue_lag_30",
    "revenue_roll_mean_7",
    "revenue_roll_mean_30",
    "sin_year",
    "cos_year",
    "is_pre_tet",
    "is_tet_week",
    "is_post_tet",
]

DETRENDED_FEATURES = [
    "month",
    "day",
    "dayofweek",
    "is_weekend",
    "is_holiday",
    "days_to_tet",
    "is_pre_tet",
    "is_tet_week",
    "is_post_tet",
]

TET_DATES = pd.to_datetime(
    [
        "2012-01-23",
        "2013-02-10",
        "2014-01-31",
        "2015-02-19",
        "2016-02-08",
        "2017-01-28",
        "2018-02-16",
        "2019-02-05",
        "2020-01-25",
        "2021-02-12",
        "2022-02-01",
        "2023-01-22",
        "2024-02-10",
    ]
)

DETRENDED_XGB_PARAMS = {
    "n_estimators": 1334,
    "learning_rate": 0.0201745325919737,
    "max_depth": 5,
    "subsample": 0.6555722188096532,
    "colsample_bytree": 0.7322563076249518,
    "min_child_weight": 10,
    "random_state": RANDOM_SEED,
    "objective": "reg:squarederror",
    "tree_method": "hist",
    "n_jobs": -1,
}

LEGACY_XGB_PARAMS = {
    "n_estimators": 800,
    "learning_rate": 0.03,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_SEED,
    "objective": "reg:squarederror",
    "tree_method": "hist",
    "n_jobs": -1,
}


def create_calendar_tet_features(date_df: pd.DataFrame) -> pd.DataFrame:
    out = date_df.copy()
    out["month"] = out["Date"].dt.month
    out["day"] = out["Date"].dt.day
    out["dayofweek"] = out["Date"].dt.dayofweek
    out["is_weekend"] = out["dayofweek"].isin([5, 6]).astype(int)

    out["is_holiday"] = 0
    for month, day in [(1, 1), (4, 30), (5, 1), (9, 2), (12, 25)]:
        out.loc[(out["month"] == month) & (out["day"] == day), "is_holiday"] = 1

    out["days_to_tet"] = 999
    for tet in TET_DATES:
        diff = (out["Date"] - tet).dt.days
        mask = (diff >= -21) & (diff <= 30)
        out.loc[mask, "days_to_tet"] = diff[mask]

    out["is_pre_tet"] = ((out["days_to_tet"] >= -21) & (out["days_to_tet"] < 0)).astype(int)
    out["is_tet_week"] = ((out["days_to_tet"] >= 0) & (out["days_to_tet"] <= 7)).astype(int)
    out["is_post_tet"] = ((out["days_to_tet"] > 7) & (out["days_to_tet"] <= 30)).astype(int)
    return out


def fit_predict_detrended(train_df: pd.DataFrame, future_dates: Iterable[pd.Timestamp], target_col: str) -> np.ndarray:
    tr = train_df[["Date", target_col]].copy()
    tr["year"] = tr["Date"].dt.year

    annual_mean = tr.groupby("year")[target_col].mean()
    tr["norm_target"] = tr[target_col] / tr["year"].map(annual_mean)

    x_train = create_calendar_tet_features(tr[["Date"]].copy())
    x_future = create_calendar_tet_features(pd.DataFrame({"Date": pd.to_datetime(list(future_dates))}))

    model = XGBRegressor(**DETRENDED_XGB_PARAMS)
    model.fit(x_train[DETRENDED_FEATURES], tr["norm_target"])

    if len(annual_mean) >= 2:
        growth = float(annual_mean.pct_change().dropna().median() + 1.0)
        growth = float(np.clip(growth, 0.90, 1.12))
    else:
        growth = 1.0

    base_year = int(annual_mean.index.max())
    base_mean = float(annual_mean.loc[base_year])
    yearly_scale = base_mean * (growth ** (x_future["Date"].dt.year - base_year))

    pred = model.predict(x_future[DETRENDED_FEATURES]) * yearly_scale
    return np.clip(pred, 0, None)


def predict_detrended_both(train_df: pd.DataFrame, future_dates: Iterable[pd.Timestamp]) -> Tuple[np.ndarray, np.ndarray]:
    rev_pred = fit_predict_detrended(train_df, future_dates, "Revenue")
    cogs_pred = fit_predict_detrended(train_df, future_dates, "COGS")
    return rev_pred, cogs_pred


def _make_legacy_feature_row(date_value: pd.Timestamp, history_df: pd.DataFrame, train_df: pd.DataFrame) -> dict:
    return {
        "month": date_value.month,
        "day": date_value.day,
        "dayofweek": date_value.dayofweek,
        "is_weekend": int(date_value.dayofweek >= 5),
        "is_payday": int(date_value.day in [15, 30, 31]),
        "is_double_day": int(date_value.month == date_value.day),
        "traffic": float(train_df["traffic"].mean()),
        "is_promo": 0,
        "total_units_sold_lag1": float(train_df["total_units_sold_lag1"].mean()),
        "revenue_lag_1": float(history_df["Revenue"].iloc[-1]),
        "revenue_lag_7": float(history_df["Revenue"].iloc[-7]),
        "revenue_lag_14": float(history_df["Revenue"].iloc[-14]),
        "revenue_lag_30": float(history_df["Revenue"].iloc[-30]),
        "revenue_roll_mean_7": float(history_df["Revenue"].tail(7).mean()),
        "revenue_roll_mean_30": float(history_df["Revenue"].tail(30).mean()),
        "sin_year": float(np.sin(2 * np.pi * date_value.dayofyear / 365.25)),
        "cos_year": float(np.cos(2 * np.pi * date_value.dayofyear / 365.25)),
        "is_pre_tet": 0,
        "is_tet_week": 0,
        "is_post_tet": 0,
    }


def predict_legacy_recursive_both(train_df: pd.DataFrame, future_dates: Iterable[pd.Timestamp]) -> Tuple[np.ndarray, np.ndarray]:
    x_train = train_df[LEGACY_FEATURES].fillna(0)

    model_rev = XGBRegressor(**LEGACY_XGB_PARAMS)
    model_cogs = XGBRegressor(**LEGACY_XGB_PARAMS)
    model_rev.fit(x_train, train_df["Revenue"])
    model_cogs.fit(x_train, train_df["COGS"])

    history = train_df[["Date", "Revenue", "COGS"]].copy()
    revenue_preds: List[float] = []
    cogs_preds: List[float] = []

    for date_value in pd.to_datetime(list(future_dates)):
        feat = _make_legacy_feature_row(date_value, history, train_df)
        xt = pd.DataFrame([feat])[LEGACY_FEATURES]

        pred_rev = float(model_rev.predict(xt)[0])
        pred_cogs = float(model_cogs.predict(xt)[0])

        pred_rev = max(0.0, pred_rev)
        pred_cogs = max(0.0, pred_cogs)

        revenue_preds.append(pred_rev)
        cogs_preds.append(pred_cogs)

        history = pd.concat(
            [
                history,
                pd.DataFrame([{"Date": date_value, "Revenue": pred_rev, "COGS": pred_cogs}]),
            ],
            ignore_index=True,
        )

    return np.array(revenue_preds), np.array(cogs_preds)


def predict_hybrid(train_df: pd.DataFrame, future_dates: Iterable[pd.Timestamp]) -> Tuple[np.ndarray, np.ndarray]:
    rev_d, cogs_d = predict_detrended_both(train_df, future_dates)
    rev_l, cogs_l = predict_legacy_recursive_both(train_df, future_dates)

    n = len(rev_d)
    # Trọng số ưu tiên detrended vì backtest thực tế mạnh hơn rõ rệt.
    w_rev = np.linspace(0.95, 0.85, n)
    w_cogs = np.linspace(0.95, 0.90, n)

    rev_h = (w_rev * rev_d) + ((1 - w_rev) * rev_l)
    cogs_h = (w_cogs * cogs_d) + ((1 - w_cogs) * cogs_l)
    return np.clip(rev_h, 0, None), np.clip(cogs_h, 0, None)


def predict_by_strategy(train_df: pd.DataFrame, future_dates: Iterable[pd.Timestamp], strategy: str) -> Tuple[np.ndarray, np.ndarray]:
    if strategy == "detrended":
        return predict_detrended_both(train_df, future_dates)
    if strategy == "legacy_recursive":
        return predict_legacy_recursive_both(train_df, future_dates)
    if strategy == "hybrid":
        return predict_hybrid(train_df, future_dates)
    raise ValueError(f"Unsupported strategy: {strategy}")


def get_backtest_cutoffs(df: pd.DataFrame, horizon: int = HORIZON) -> List[pd.Timestamp]:
    preferred = [pd.Timestamp("2020-12-31"), pd.Timestamp("2021-06-30")]
    valid_cutoffs: List[pd.Timestamp] = []

    min_date = df["Date"].min()
    max_date = df["Date"].max()

    for cutoff in preferred:
        forecast_end = cutoff + pd.Timedelta(days=horizon)
        if cutoff >= min_date and forecast_end <= max_date:
            valid_cutoffs.append(cutoff)

    if valid_cutoffs:
        return valid_cutoffs

    # Fallback nếu dữ liệu thay đổi.
    fallback = max_date - pd.Timedelta(days=(2 * horizon))
    return [fallback]


def backtest_strategy(df: pd.DataFrame, strategy: str, horizon: int = HORIZON) -> pd.DataFrame:
    rows = []
    for cutoff in get_backtest_cutoffs(df, horizon=horizon):
        train_split = df[df["Date"] <= cutoff].copy().reset_index(drop=True)
        valid_split = df[(df["Date"] > cutoff) & (df["Date"] <= cutoff + pd.Timedelta(days=horizon))].copy().reset_index(drop=True)

        if len(valid_split) == 0:
            continue

        rev_pred, cogs_pred = predict_by_strategy(train_split, valid_split["Date"], strategy)

        revenue_mae = float(mean_absolute_error(valid_split["Revenue"], rev_pred))
        cogs_mae = float(mean_absolute_error(valid_split["COGS"], cogs_pred))

        rows.append(
            {
                "strategy": strategy,
                "cutoff": cutoff.strftime("%Y-%m-%d"),
                "horizon_days": len(valid_split),
                "revenue_mae": revenue_mae,
                "cogs_mae": cogs_mae,
                "avg_mae": (revenue_mae + cogs_mae) / 2,
            }
        )

    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Day 5 production forecasting pipeline with backtest-driven strategy selection")
    parser.add_argument("--train", default="Data/processed_train.csv", help="Path to processed training data")
    parser.add_argument("--sample-sub", default="Data/sample_submission.csv", help="Path to sample submission file")
    parser.add_argument("--output", default="submission_v6_day5_max_optimized.csv", help="Output submission path")
    parser.add_argument(
        "--strategy",
        choices=["auto", "detrended", "legacy_recursive", "hybrid"],
        default="auto",
        help="Forecast strategy. 'auto' will pick best strategy by rolling backtest",
    )
    parser.add_argument("--backtest-report", default="scratch/day5_backtest_report.csv", help="Where to save backtest report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    train_path = Path(args.train)
    sub_path = Path(args.sample_sub)

    if not train_path.exists():
        raise FileNotFoundError(f"Training file not found: {train_path}")
    if not sub_path.exists():
        raise FileNotFoundError(f"Sample submission file not found: {sub_path}")

    df_train = pd.read_csv(train_path, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)
    df_sub = pd.read_csv(sub_path, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)

    required_cols = {"Date", "Revenue", "COGS"}
    if not required_cols.issubset(df_train.columns):
        missing = required_cols - set(df_train.columns)
        raise ValueError(f"Training file missing required columns: {missing}")

    strategies = [args.strategy] if args.strategy != "auto" else ["detrended", "hybrid", "legacy_recursive"]

    print("\n[1/3] Running rolling backtests...")
    all_bt = []
    for strategy in strategies:
        bt_df = backtest_strategy(df_train, strategy, horizon=HORIZON)
        if bt_df.empty:
            print(f"- {strategy}: no valid backtest splits")
            continue
        all_bt.append(bt_df)
        print(
            f"- {strategy}: avg MAE = {bt_df['avg_mae'].mean():,.0f} "
            f"(Revenue={bt_df['revenue_mae'].mean():,.0f}, COGS={bt_df['cogs_mae'].mean():,.0f})"
        )

    if not all_bt:
        raise RuntimeError("No valid backtest results were generated. Check date range/horizon.")

    backtest_report = pd.concat(all_bt, ignore_index=True)
    backtest_report_path = Path(args.backtest_report)
    backtest_report_path.parent.mkdir(parents=True, exist_ok=True)
    backtest_report.to_csv(backtest_report_path, index=False)

    summary = (
        backtest_report.groupby("strategy", as_index=False)
        .agg(revenue_mae=("revenue_mae", "mean"), cogs_mae=("cogs_mae", "mean"), avg_mae=("avg_mae", "mean"))
        .sort_values("avg_mae")
    )

    if args.strategy == "auto":
        chosen_strategy = str(summary.iloc[0]["strategy"])
    else:
        chosen_strategy = args.strategy

    print("\n[2/3] Strategy ranking (lower is better):")
    print(summary.to_string(index=False, formatters={"revenue_mae": "{:,.0f}".format, "cogs_mae": "{:,.0f}".format, "avg_mae": "{:,.0f}".format}))
    print(f"\nChosen strategy: {chosen_strategy}")

    print("\n[3/3] Training on full data and generating submission...")
    rev_pred, cogs_pred = predict_by_strategy(df_train, df_sub["Date"], chosen_strategy)

    submission = df_sub[["Date"]].copy()
    submission["Revenue"] = np.clip(rev_pred, 0, None)
    submission["COGS"] = np.clip(cogs_pred, 0, None)
    submission["Date"] = submission["Date"].dt.strftime("%Y-%m-%d")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(output_path, index=False)

    print(f"✅ Submission saved to: {output_path}")
    print(f"✅ Backtest report saved to: {backtest_report_path}")


if __name__ == "__main__":
    main()

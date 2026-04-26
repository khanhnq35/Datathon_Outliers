import polars as pl
import numpy as np

def add_time_series_features(df: pl.DataFrame) -> pl.DataFrame:
    """
    Adds lags and rolling statistics for Revenue and COGS using Polars.
    Also includes calendar and holiday features.
    """
    # 1. Calendar Features
    df = df.with_columns([
        pl.col("Date").dt.month().alias("month"),
        pl.col("Date").dt.day().alias("day"),
        pl.col("Date").dt.weekday().alias("dayofweek"),
    ])
    
    df = df.with_columns([
        (pl.col("dayofweek") >= 6).cast(pl.Int8).alias("is_weekend"),
        ((pl.col("day") >= 25) | (pl.col("day") <= 5)).cast(pl.Int8).alias("is_payday"),
        (pl.col("month") == pl.col("day")).cast(pl.Int8).alias("is_double_day"),
    ])

    # Ensure dataframe is sorted by Date before shifting
    df = df.sort("Date")

    # 2. Shifts / Lags (1, 7, 14, 30 days)
    lags = [1, 7, 14, 30]
    lag_cols = []
    for col in ["Revenue", "COGS"]:
        for lag in lags:
            lag_cols.append(
                pl.col(col).shift(lag).fill_null(0).alias(f"{col.lower()}_lag_{lag}")
            )
    
    # 3. Rolling Statistics (7, 30 days)
    windows = [7, 30]
    rolling_cols = []
    for col in ["Revenue", "COGS"]:
        for window in windows:
            rolling_cols.append(
                pl.col(col).shift(1).rolling_mean(window_size=window).fill_null(0).alias(f"{col.lower()}_roll_mean_{window}")
            )

    # 4. Sin/Cos for yearly seasonality
    df = df.with_columns([
        (2 * np.pi * pl.col("Date").dt.ordinal_day() / 365.25).alias("day_rad")
    ])
    df = df.with_columns([
        pl.col("day_rad").sin().alias("sin_year"),
        pl.col("day_rad").cos().alias("cos_year"),
    ]).drop("day_rad")

    # Combine everything
    df = df.with_columns(lag_cols + rolling_cols)
    
    return df

def add_tet_features(df: pl.DataFrame) -> pl.DataFrame:
    """Adds specific Tet holiday features."""
    tet_dates = [
        '2012-01-23', '2013-02-10', '2014-01-31', '2015-02-19', '2016-02-08',
        '2017-01-28', '2018-02-16', '2019-02-05', '2020-01-25', '2021-02-12',
        '2022-02-01', '2023-01-22', '2024-02-10'
    ]
    tet_dates = [pl.Series([d]).str.to_date()[0] for d in tet_dates]
    
    # Simple logic for Tet window
    df = df.with_columns(pl.lit(999).alias("days_to_tet"))
    
    for tet in tet_dates:
        df = df.with_columns(
            pl.when((pl.col("Date") - tet).dt.total_days().is_between(-21, 30))
            .then((pl.col("Date") - tet).dt.total_days())
            .otherwise(pl.col("days_to_tet"))
            .alias("days_to_tet")
        )
    
    df = df.with_columns([
        ((pl.col("days_to_tet") >= -21) & (pl.col("days_to_tet") < 0)).cast(pl.Int8).alias("is_pre_tet"),
        ((pl.col("days_to_tet") >= 0) & (pl.col("days_to_tet") <= 7)).cast(pl.Int8).alias("is_tet_week"),
        ((pl.col("days_to_tet") > 7) & (pl.col("days_to_tet") <= 30)).cast(pl.Int8).alias("is_post_tet"),
    ])
    
    return df

if __name__ == "__main__":
    # Small test
    from data_loader import DataLoader
    loader = DataLoader()
    sales = loader.load("sales")
    
    features_df = add_time_series_features(sales)
    features_df = add_tet_features(features_df)
    
    print("Features created successfully. Shape:", features_df.shape)
    print(features_df.head())

import polars as pl
from src.data_loader import DataLoader
from src.features import add_time_series_features, add_tet_features
from pathlib import Path

def build_processed_dataset():
    print("[*] Starting dataset construction...")
    loader = DataLoader()
    
    # 1. Load Core Data
    sales = loader.load("sales")
    traffic = loader.load("web_traffic")
    promos = loader.load("promotions")
    inventory = loader.load("inventory")
    
    # 2. Process Web Traffic
    traffic = traffic.rename({"date": "Date", "unique_visitors": "traffic"})
    traffic = traffic.select(["Date", "traffic"])
    
    # 3. Process Promotions (Optimized)
    print("[*] Processing promotions...")
    all_dates = sales.select("Date").unique().sort("Date")
    promo_master = all_dates.with_columns(pl.lit(0).alias("is_promo"))
    
    for row in promos.to_dicts():
        start, end = row['start_date'], row['end_date']
        promo_master = promo_master.with_columns(
            pl.when(pl.col("Date").is_between(pl.lit(start), pl.lit(end)))
            .then(1)
            .otherwise(pl.col("is_promo"))
            .alias("is_promo")
        )

    # 4. Process Inventory (Aggregate by date and shift to avoid leakage)
    print("[*] Processing inventory...")
    inv_daily = inventory.group_by("snapshot_date").agg([
        pl.col("stock_on_hand").sum().alias("total_stock"),
        pl.col("units_sold").sum().shift(1).alias("total_units_sold_lag1")
    ]).rename({"snapshot_date": "Date"})
    
    # 5. Merge Everything
    print("[*] Merging datasets...")
    df = sales.join(traffic, on="Date", how="left")
    df = df.join(promo_master, on="Date", how="left")
    df = df.join(inv_daily, on="Date", how="left")
    
    # Fill missing values
    df = df.with_columns([
        pl.col("traffic").fill_null(strategy="forward").fill_null(0),
        pl.col("is_promo").fill_null(0),
        pl.col("total_stock").fill_null(strategy="forward"),
        pl.col("total_units_sold_lag1").fill_null(0),
    ])
    
    # 6. Apply Feature Engineering
    print("[*] Applying Feature Engineering...")
    df = add_time_series_features(df)
    df = add_tet_features(df)
    
    # 7. Save to CSV
    output_path = Path("Data/processed_train.csv")
    df.write_csv(output_path)
    print(f"[+] Success! Processed dataset saved to: {output_path}")
    print(f"Final shape: {df.shape}")

if __name__ == "__main__":
    build_processed_dataset()

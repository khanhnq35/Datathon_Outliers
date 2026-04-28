import polars as pl
from datetime import timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join("..", "src")))
from data_loader import DataLoader

loader = DataLoader()
promotions = loader.load("promotions")
sales = loader.load("sales")

promotions = promotions.with_columns([
    pl.col("start_date").str.strptime(pl.Date, "%Y-%m-%d", strict=False).cast(pl.Datetime),
    pl.col("end_date").str.strptime(pl.Date, "%Y-%m-%d", strict=False).cast(pl.Datetime)
])
sales = sales.with_columns(pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d", strict=False).cast(pl.Datetime))

promo_effects = []
for row in promotions.iter_rows(named=True):
    start = row["start_date"]
    end = row["end_date"]
    if start is None or end is None: continue
    
    before_start = start - timedelta(days=14)
    before_end = start - timedelta(days=1)
    
    after_start = end + timedelta(days=1)
    after_end = end + timedelta(days=14)
    
    rev_before = sales.filter((pl.col("Date") >= before_start) & (pl.col("Date") <= before_end))["Revenue"].mean()
    rev_during = sales.filter((pl.col("Date") >= start) & (pl.col("Date") <= end))["Revenue"].mean()
    rev_after = sales.filter((pl.col("Date") >= after_start) & (pl.col("Date") <= after_end))["Revenue"].mean()
    
    promo_effects.append({
        "promo_name": row["promo_name"],
        "Before": rev_before,
        "During": rev_during,
        "After": rev_after
    })

effects_df = pl.DataFrame(promo_effects).drop_nulls()
avg_effects = effects_df.select([pl.col("Before").mean(), pl.col("During").mean(), pl.col("After").mean()])
print(avg_effects)

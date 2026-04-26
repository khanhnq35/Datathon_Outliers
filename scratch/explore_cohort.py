import sys
import polars as pl
import pandas as pd
import numpy as np

sys.path.append('d:/Datathon_Outliers')
from src.data_loader import DataLoader

loader = DataLoader()
dfs = loader.load_all()
orders = dfs['orders']

# Check date range and order status values
print("=== Date range ===")
print(f"Min: {orders['order_date'].min()}, Max: {orders['order_date'].max()}")
print(f"\n=== Order status ===")
print(orders['order_status'].value_counts())
print(f"\n=== Total orders: {len(orders):,}")

# Build cohort data
cohort_data = orders.group_by('customer_id').agg([
    pl.col('order_date').min().alias('first_order_date')
])
orders_cohort = orders.join(cohort_data, on='customer_id')
orders_cohort = orders_cohort.with_columns([
    pl.col('first_order_date').dt.truncate('1mo').alias('cohort_month'),
    pl.col('order_date').dt.truncate('1mo').alias('order_month')
])
def diff_months(col_end, col_start):
    return (col_end.dt.year() - col_start.dt.year()) * 12 + (col_end.dt.month() - col_start.dt.month())

orders_cohort = orders_cohort.with_columns([
    diff_months(pl.col('order_month'), pl.col('cohort_month')).alias('cohort_index')
])
cohort_counts = orders_cohort.group_by(['cohort_month', 'cohort_index']).agg([
    pl.col('customer_id').n_unique().alias('active_customers')
]).sort(['cohort_month', 'cohort_index'])

retention_matrix = cohort_counts.to_pandas().pivot(index='cohort_month', columns='cohort_index', values='active_customers')
cohort_sizes = retention_matrix.iloc[:, 0]
retention_pct = retention_matrix.divide(cohort_sizes, axis=0) * 100
retention_pct.index = pd.to_datetime(retention_pct.index).strftime('%Y-%m')

print("\n=== Cohort matrix shape ===", retention_pct.shape)
print("\n=== Cohort sizes (top 10) ===")
print(cohort_sizes.sort_values(ascending=False).head(10))

# Month-1 retention per cohort
if 1 in retention_pct.columns:
    m1 = retention_pct[1].dropna()
    print(f"\n=== Month-1 Retention ===")
    print(f"Average: {m1.mean():.2f}%")
    print(f"Max: {m1.max():.2f}% at {m1.idxmax()}")
    print(f"Min: {m1.min():.2f}% at {m1.idxmin()}")

# Average retention curve (first 12 months)
avg_curve = retention_pct.iloc[:, :13].mean(axis=0)
print("\n=== Average retention curve (Month 0-12) ===")
print(avg_curve.round(2))

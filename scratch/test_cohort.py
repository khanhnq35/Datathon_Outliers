import sys
from pathlib import Path
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path('.').resolve()))
from src.data_loader import DataLoader

loader = DataLoader()
all_dfs = loader.load_all()

orders = all_dfs['orders']
customers = all_dfs['customers']

print("Loaded data")

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
retention_percentage = retention_matrix.divide(cohort_sizes, axis=0) * 100

print("Finished successfully")

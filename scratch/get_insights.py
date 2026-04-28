import sys
from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np

sys.path.append('d:/Datathon_Outliers')
from src.data_loader import DataLoader

loader = DataLoader()
dfs = loader.load_all()
orders = dfs['orders']
payments = dfs['payments']

# 1. Repeat Rate
purchase_counts = orders.group_by('customer_id').agg([
    pl.count('order_id').alias('order_count')
])
total_customers = purchase_counts.height
repeat_customers = purchase_counts.filter(pl.col('order_count') > 1).height
repeat_rate = (repeat_customers / total_customers) * 100
print(f"Repeat Rate: {repeat_rate:.2f}% ({repeat_customers}/{total_customers})")

# 2. Cohort
cohort_data = orders.group_by('customer_id').agg([pl.col('order_date').min().alias('first_order_date')])
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
# Find max retention at index 1
if 1 in retention_percentage.columns:
    max_ret_m1 = retention_percentage[1].max()
    max_ret_m1_cohort = retention_percentage[1].idxmax()
    print(f"Best Cohort Month 1: {max_ret_m1_cohort.strftime('%Y-%m')} ({max_ret_m1:.1f}%)")

# 3. RFM
order_payments = orders.join(payments, on='order_id')
current_date = orders['order_date'].max() + pl.duration(days=1)
rfm = order_payments.group_by('customer_id').agg([
    ((current_date - pl.col('order_date').max()).dt.total_days()).alias('recency'),
    pl.col('order_id').n_unique().alias('frequency'),
    pl.col('payment_value').sum().alias('monetary')
])
rfm_pd = rfm.to_pandas()
rfm_pd['r_score'] = pd.qcut(rfm_pd['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm_pd['f_score'] = pd.cut(rfm_pd['frequency'], bins=[0, 1, 2, 3, 4, float('inf')], labels=[1, 2, 3, 4, 5])
rfm_pd['m_score'] = pd.qcut(rfm_pd['monetary'], 5, labels=[1, 2, 3, 4, 5])

def segment_customer(df):
    r = int(df['r_score'])
    f = int(df['f_score'])
    if r >= 4 and f >= 4: return 'Champions'
    if r >= 3 and f >= 3: return 'Loyal Customers'
    if r >= 4 and f <= 2: return 'New Customers'
    if r <= 2 and f >= 4: return 'At Risk'
    if r <= 2 and f <= 2: return 'Lost'
    return 'Potential Loyalist'

rfm_pd['segment'] = rfm_pd.apply(segment_customer, axis=1)
print("\nRFM Segments:")
print(rfm_pd['segment'].value_counts(normalize=True) * 100)

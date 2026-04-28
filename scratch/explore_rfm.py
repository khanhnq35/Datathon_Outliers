import sys
import polars as pl
import pandas as pd
import numpy as np

sys.path.append('d:/Datathon_Outliers')
from src.data_loader import DataLoader

loader = DataLoader()
dfs = loader.load_all()
orders = dfs['orders']
payments = dfs['payments']
customers = dfs['customers']

# Build RFM
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

print("=== Segment counts & % ===")
print(rfm_pd['segment'].value_counts(normalize=True).mul(100).round(2))

print("\n=== Avg Recency / Frequency / Monetary by Segment ===")
seg_summary = rfm_pd.groupby('segment').agg(
    count=('customer_id', 'count'),
    avg_recency=('recency', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_monetary=('monetary', 'mean'),
    total_monetary=('monetary', 'sum')
).round(2)
print(seg_summary.to_string())

print("\n=== Pareto: Revenue contribution ===")
total_rev = rfm_pd['monetary'].sum()
seg_rev_share = rfm_pd.groupby('segment')['monetary'].sum().sort_values(ascending=False)
print((seg_rev_share / total_rev * 100).round(2))

print("\n=== Recency quantile thresholds ===")
print(pd.qcut(rfm_pd['recency'], 5).value_counts().sort_index())

print("\n=== Monetary range ===")
print(rfm_pd['monetary'].describe())
print(f"\nTop segment by revenue: {seg_rev_share.idxmax()} ({seg_rev_share.max()/total_rev*100:.1f}%)")

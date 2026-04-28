import sys, polars as pl, pandas as pd
sys.path.append('d:/Datathon_Outliers')
from src.data_loader import DataLoader

dfs = DataLoader().load_all()
orders = dfs['orders']
customers = dfs['customers']

# Purchase counts per customer
purchase_counts = orders.group_by('customer_id').agg([
    pl.count('order_id').alias('order_count')
])

total = purchase_counts.height
repeat = purchase_counts.filter(pl.col('order_count') > 1).height
print(f"Total customers: {total:,}")
print(f"Repeat customers: {repeat:,}  ({repeat/total*100:.2f}%)")
print(f"One-time only: {total-repeat:,}  ({(total-repeat)/total*100:.2f}%)")

# Distribution breakdown
pc_pd = purchase_counts.to_pandas()
for i in [1,2,3,4,5]:
    cnt = (pc_pd['order_count'] == i).sum()
    print(f"  Exactly {i} order(s): {cnt:,} ({cnt/total*100:.1f}%)")
cnt_6plus = (pc_pd['order_count'] >= 6).sum()
print(f"  6+ orders: {cnt_6plus:,} ({cnt_6plus/total*100:.1f}%)")

# By acquisition channel
print("\n=== Repeat rate by acquisition_channel ===")
merged = purchase_counts.join(
    customers.select(['customer_id','acquisition_channel']),
    on='customer_id', how='left'
).to_pandas()
merged['is_repeat'] = merged['order_count'] > 1

channel_stats = merged.groupby('acquisition_channel').agg(
    total=('customer_id','count'),
    repeat=('is_repeat','sum'),
    avg_orders=('order_count','mean')
).reset_index()
channel_stats['repeat_rate'] = channel_stats['repeat'] / channel_stats['total'] * 100
print(channel_stats.sort_values('repeat_rate', ascending=False).to_string(index=False))

print("\n=== Avg orders per customer by channel ===")
print(merged.groupby('acquisition_channel')['order_count'].mean().sort_values(ascending=False).round(2))

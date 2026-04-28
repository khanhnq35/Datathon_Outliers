import sys
from pathlib import Path
import polars as pl
import pandas as pd

sys.path.append('d:/Datathon_Outliers')
from src.data_loader import DataLoader

loader = DataLoader()
dfs = loader.load_all()
orders = dfs['orders']
payments = dfs['payments']

order_payments = orders.join(payments, on='order_id')
current_date = orders['order_date'].max() + pl.duration(days=1)

rfm = order_payments.group_by('customer_id').agg([
    ((current_date - pl.col('order_date').max()).dt.total_days()).alias('recency'),
    pl.col('order_id').n_unique().alias('frequency'),
    pl.col('payment_value').sum().alias('monetary')
])

rfm_pd = rfm.to_pandas()
print("Starting pd.qcut")
rfm_pd['r_score'] = pd.qcut(rfm_pd['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm_pd['f_score'] = pd.qcut(rfm_pd['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm_pd['m_score'] = pd.qcut(rfm_pd['monetary'], 5, labels=[1, 2, 3, 4, 5])

print("Finished successfully")

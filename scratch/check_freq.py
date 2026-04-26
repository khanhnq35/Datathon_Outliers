import sys
from pathlib import Path
import polars as pl
import pandas as pd

sys.path.append('d:/Datathon_Outliers')
from src.data_loader import DataLoader

loader = DataLoader()
dfs = loader.load_all()
orders = dfs['orders']

freq = orders.group_by('customer_id').agg(pl.col('order_id').n_unique().alias('frequency')).to_pandas()
print(freq['frequency'].value_counts().sort_index().head(10))

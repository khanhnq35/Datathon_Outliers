import polars as pl
from pathlib import Path
from typing import Dict, Optional, List

class DataLoader:
    """
    A unified data loader for the Datathon project using Polars for high performance.
    Automatically handles path resolution and date parsing for consistent team usage.
    """

    def __init__(self, data_dir: str = "Data"):
        # Resolve path relative to this file (works from anywhere in the project)
        self.base_path = Path(__file__).parent.parent / data_dir
        
        # Mapping of tables to their specific date columns
        self.date_columns = {
            "customers": ["signup_date"],
            "orders": ["order_date"],
            "shipments": ["ship_date", "delivery_date"],
            "inventory": ["snapshot_date"],
            "web_traffic": ["date"],
            "sales": ["Date"],
            "promotions": ["start_date", "end_date"],
        }

    def _get_file_path(self, table_name: str) -> Path:
        """Returns the absolute path for a given table name."""
        return self.base_path / f"{table_name.lower()}.csv"

    def load(self, table_name: str) -> pl.DataFrame:
        """
        Loads a single CSV file as a Polars DataFrame with optimized types.
        
        Args:
            table_name (str): Name of the table (e.g., 'orders', 'customers')
            
        Returns:
            pl.DataFrame: The loaded and parsed data.
        """
        file_path = self._get_file_path(table_name)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found at: {file_path}")

        # Basic load
        df = pl.read_csv(file_path)

        # Automated Date Parsing
        date_cols = self.date_columns.get(table_name.lower(), [])
        for col in date_cols:
            if col in df.columns:
                # Try parsing with standard ISO format
                df = df.with_columns(pl.col(col).str.to_date(strict=False))

        return df

    def load_all(self) -> Dict[str, pl.DataFrame]:
        """
        Loads all 15 core CSV files into a dictionary for easy access.
        
        Returns:
            Dict[str, pl.DataFrame]: Dictionary mapping table names to DataFrames.
        """
        tables = [
            "customers", "geography", "inventory", "order_items", "orders",
            "payments", "products", "promotions", "returns", "reviews",
            "sales", "sample_submission", "shipments", "web_traffic"
        ]
        
        all_dfs = {}
        for table in tables:
            try:
                all_dfs[table] = self.load(table)
                print(f"✅ Loaded {table}: {len(all_dfs[table]):,} rows")
            except Exception as e:
                print(f"❌ Failed to load {table}: {e}")
                
        return all_dfs

if __name__ == "__main__":
    # Quick sanity check
    loader = DataLoader()
    dfs = loader.load_all()
    print("\nSample from 'orders':")
    print(dfs['orders'].head())

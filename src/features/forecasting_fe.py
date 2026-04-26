import polars as pl
from typing import List, Optional

class ForecastingFeaturePipeline:
    """
    Pipeline tạo Features cho Forecasting Model dự báo doanh thu hàng ngày.
    Sử dụng Polars để tối ưu hóa hiệu năng, đặc biệt xử lý Data Leakage
    nhờ vào kỹ thuật shift (lag/trễ).
    """
    def __init__(self, 
                 df_sales: pl.DataFrame, 
                 df_traffic: Optional[pl.DataFrame] = None, 
                 df_promotions: Optional[pl.DataFrame] = None):
        
        # Đảm bảo cột Date là dạng Date và sort tăng dần
        if df_sales.schema["Date"] == pl.Utf8:
            self.df = df_sales.with_columns(pl.col("Date").str.to_date(strict=False))
        else:
            self.df = df_sales
            
        self.df = self.df.sort("Date")
        
        self.df_traffic = df_traffic
        if self.df_traffic is not None and self.df_traffic.schema.get("date") == pl.Utf8:
            self.df_traffic = self.df_traffic.with_columns(pl.col("date").str.to_date(strict=False))
            
        self.df_promotions = df_promotions

    def add_temporal_features(self) -> "ForecastingFeaturePipeline":
        """Thêm các đặc trưng chu kỳ thời gian (Temporal features)"""
        self.df = self.df.with_columns([
            pl.col("Date").dt.weekday().alias("day_of_week"),
            pl.col("Date").dt.day().alias("day_of_month"),
            pl.col("Date").dt.month().alias("month"),
            pl.col("Date").dt.quarter().alias("quarter"),
            pl.col("Date").dt.year().alias("year"),
            pl.col("Date").dt.weekday().is_in([6, 7]).cast(pl.Int8).alias("is_weekend")
        ])
        return self

    def add_lag_features(self, lags: List[int] = [1, 7, 30]) -> "ForecastingFeaturePipeline":
        """Thêm các đặc trưng độ trễ (Lag features) cho Revenue và COGS"""
        lag_exprs = []
        for lag in lags:
            lag_exprs.extend([
                pl.col("Revenue").shift(lag).alias(f"Revenue_lag_{lag}"),
                pl.col("COGS").shift(lag).alias(f"COGS_lag_{lag}")
            ])
        
        self.df = self.df.with_columns(lag_exprs)
        return self

    def add_rolling_features(self, windows: List[int] = [7, 14, 30]) -> "ForecastingFeaturePipeline":
        """
        Thêm các đặc trưng trung bình chạy (Rolling features).
        Lưu ý: Phải shift 1 ngày TRƯỚC KHI tính rolling để tránh Data Leakage (dùng data ngày hiện tại).
        """
        # Tạo bản sao revenue bị trễ 1 ngày để tính rolling chuẩn 
        # (việc rolling lên ngày nào thì sẽ tính trên quá khứ không chứa chính ngày đó)
        rolling_base = self.df.select(["Date", pl.col("Revenue").shift(1).alias("Revenue_shifted")])
        
        for w in windows:
            rolling_base = rolling_base.with_columns([
                pl.col("Revenue_shifted").rolling_mean(window_size=w).alias(f"Revenue_rolling_mean_{w}"),
                pl.col("Revenue_shifted").rolling_std(window_size=w).alias(f"Revenue_rolling_std_{w}"),
                pl.col("Revenue_shifted").rolling_max(window_size=w).alias(f"Revenue_rolling_max_{w}"),
                pl.col("Revenue_shifted").rolling_min(window_size=w).alias(f"Revenue_rolling_min_{w}")
            ])
            
        rolling_base = rolling_base.drop("Revenue_shifted")
        self.df = self.df.join(rolling_base, on="Date", how="left")
        return self

    def _get_daily_promotions(self) -> pl.DataFrame:
        """Đếm số lượng campaign promotion hoạt động mỗi ngày tương thích cross dates"""
        if self.df_promotions is None or "start_date" not in self.df_promotions.columns:
            return pl.DataFrame(schema={"Date": pl.Date, "active_promotions_count": pl.UInt32})
            
        # Parse dates
        df_promo = self.df_promotions.with_columns([
            pl.col("start_date").str.to_date(strict=False),
            pl.col("end_date").str.to_date(strict=False)
        ])
        
        # Lấy tất cả Date hiện có
        dates_df = self.df.select("Date").unique()
        
        # Dùng Cross Join để ghép toàn bộ Date với toàn bộ Promotion.
        # Polars tối ưu Cross Join rất tốt nếu size data nhỏ.
        joined = dates_df.join(df_promo, how="cross")
        
        # Chỉ lấy các dòng nằm trong thời gian diễn ra khuyến mãi
        valid_promos = joined.filter(
            (pl.col("Date") >= pl.col("start_date")) & 
            (pl.col("Date") <= pl.col("end_date"))
        )
        
        daily_promo = valid_promos.group_by("Date").agg(
            pl.len().alias("active_promotions_count")
        )
        return daily_promo

    def add_external_features(self) -> "ForecastingFeaturePipeline":
        """Tích hợp features ngoại vi. Áp dụng lag=1 nếu là data biến động theo ngày, không lag cho config trước kế hoạch."""
        
        # 1. Web Traffic (Áp dụng Data Shift lag=1)
        if self.df_traffic is not None:
            traffic_agg = self.df_traffic.group_by("date").agg([
                pl.col("sessions").sum().alias("total_sessions"),
                pl.col("page_views").sum().alias("total_page_views"),
                pl.col("avg_session_duration_sec").mean().alias("mean_session_duration")
            ]).sort("date")
            
            # Shift traffic đi 1 ngày vì traffic ở cuối ngày mới có số full
            traffic_shifted = traffic_agg.with_columns([
                pl.col("total_sessions").shift(1),
                pl.col("total_page_views").shift(1),
                pl.col("mean_session_duration").shift(1)
            ])
            self.df = self.df.join(traffic_shifted, left_on="Date", right_on="date", how="left")

        # 2. Promotions (Không lag vì lịch được cung cấp trước theo campaign dates)
        if self.df_promotions is not None:
            daily_promo = self._get_daily_promotions()
            self.df = self.df.join(daily_promo, on="Date", how="left").with_columns(
                pl.col("active_promotions_count").fill_null(0)
            )
            
        return self

    def run(self) -> pl.DataFrame:
        """Thực thi tuần tự toàn bộ Data Pipeline cho Machine Learning Models"""
        return (self
                .add_temporal_features()
                .add_lag_features()
                .add_rolling_features()
                .add_external_features()
                .df)

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Import DataLoader from parent src
    sys.path.append(str(Path(__file__).parent.parent))
    try:
        from data_loader import DataLoader
        loader = DataLoader()
        print("Tải dữ liệu để test ForecastingFeaturePipeline...")
        df_sales = loader.load("sales")
        df_traffic = loader.load("web_traffic")
        df_promotions = loader.load("promotions")
        
        pipeline = ForecastingFeaturePipeline(df_sales, df_traffic, df_promotions)
        features_df = pipeline.run()
        
        print(f"✅ Hoàn thành trích xuất {len(features_df.columns)} tính năng cho {len(features_df)} ngày.")
        print(features_df.head(5))
        
    except Exception as e:
        print(f"⚠️ Không thể chạy test loader: {e}")

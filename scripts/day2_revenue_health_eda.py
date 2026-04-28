import sys, os
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Thư viện cho Time Series
from statsmodels.tsa.seasonal import seasonal_decompose

# Set random state and plot style
np.random.seed(42)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Add src to path
sys.path.append(os.path.abspath("src"))
from data_loader import DataLoader

# ============================================================
# CELL 1: Setup & Load Data
# ============================================================
print("=== CELL 1: Setup & Load Data ===")
loader = DataLoader()

# Load necessary tables
sales = loader.load("sales")

print("Sales data shape:", sales.shape)
print("Date range:", sales['Date'].min(), "to", sales['Date'].max())
print(sales.head(3))


# ============================================================
# CELL 2: DQA - Check Nulls & Logical Errors
# ============================================================
print("\n=== CELL 2: DQA - Null & Logical Checks ===")
# 1. Check Nulls
null_counts = sales.null_count()
print("Null Counts:")
print(null_counts)

# 2. Xử lý Logical Errors (Revenue hoặc COGS <= 0)
invalid_rows = sales.filter((pl.col("Revenue") <= 0) | (pl.col("COGS") <= 0))
if invalid_rows.height > 0:
    print(f"⚠️ Phát hiện {invalid_rows.height} dòng có Revenue hoặc COGS <= 0. Tiến hành lọc bỏ...")
    sales = sales.filter((pl.col("Revenue") > 0) & (pl.col("COGS") > 0))
else:
    print("✅ Không có dòng dữ liệu Revenue/COGS <= 0.")

# 3. Thêm các cột thời gian cần thiết
sales = sales.with_columns([
    pl.col("Date").dt.year().alias("Year"),
    pl.col("Date").dt.month().alias("Month"),
    pl.col("Date").dt.quarter().alias("Quarter"),
    pl.col("Date").dt.strftime("%Y-%m").alias("YearMonth")
])


# ============================================================
# CELL 3: DQA - Outlier Detection (IQR Method)
# ============================================================
print("\n=== CELL 3: DQA - Outlier Detection ===")
def remove_outliers_iqr(df, col_name, multiplier=1.5):
    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    
    # Gom các dòng Outliers
    outliers = df.filter((pl.col(col_name) < lower_bound) | (pl.col(col_name) > upper_bound))
    print(f"Cột {col_name}: Phát hiện {outliers.height} outliers (ngưỡng {multiplier} IQR).")
    
    # Data sạch
    df_clean = df.filter((pl.col(col_name) >= lower_bound) & (pl.col(col_name) <= upper_bound))
    return df_clean, outliers

# Lọc Outliers và lưu nhóm Outliers ra riêng để phân tích
original_height = sales.height
sales, rev_outliers = remove_outliers_iqr(sales, "Revenue", 3.0)
sales, cogs_outliers = remove_outliers_iqr(sales, "COGS", 3.0)

# Gộp chung toàn bộ Outliers của cả Revenue và COGS lại thành 1 bảng duy nhất
sales_outliers = pl.concat([rev_outliers, cogs_outliers])

print(f"Đã loại bỏ tổng cộng {original_height - sales.height} dòng cực đoan.")
print(f"Tổng số Outliers gom được để Deep Dive: {sales_outliers.height} dòng.")

# INSIGHT:
# >> "Đã làm sạch dữ liệu: Không có Null, loại bỏ các đơn hàng doanh thu âm, và lọc các Outliers cực đoan để biểu đồ phản ánh đúng xu hướng thực tế."


# ============================================================
# CELL 4: Financial Health - Gross Profit & Margin
# ============================================================
print("\n=== CELL 4: Gross Profit & Margin Calculation ===")
# Tạo cột Gross Profit và Gross Margin
sales = sales.with_columns([
    (pl.col("Revenue") - pl.col("COGS")).alias("Gross_Profit")
])

sales = sales.with_columns([
    (pl.col("Gross_Profit") / pl.col("Revenue") * 100).alias("Gross_Margin_%")
])

print(sales.select(["Date", "Revenue", "COGS", "Gross_Profit", "Gross_Margin_%"]).head())


# ============================================================
# CELL 5: Revenue YoY Trend & CAGR (Full Years Only)
# ============================================================
print("\n=== CELL 5: YoY Growth & CAGR ===")
# Loại bỏ năm 2012 (năm khuyết) để tính YoY và CAGR cho chuẩn xác
sales_full_years = sales.filter(pl.col("Year") >= 2013)

yearly_sales = sales_full_years.group_by("Year").agg(
    pl.col("Revenue").sum().alias("Total_Revenue"),
    pl.col("Gross_Profit").sum().alias("Total_Gross_Profit")
).sort("Year")

yearly_sales = yearly_sales.with_columns([
    (pl.col("Total_Revenue").diff() / pl.col("Total_Revenue").shift(1) * 100).alias("YoY_Growth_Rate_%"),
    (pl.col("Total_Gross_Profit") / pl.col("Total_Revenue") * 100).alias("Avg_Gross_Margin_%")
])

print(yearly_sales)

# Tính CAGR (2013-2022)
start_year = 2013
end_year = yearly_sales["Year"][-1]
num_years = end_year - start_year

start_revenue = yearly_sales.filter(pl.col("Year") == start_year)["Total_Revenue"][0]
end_revenue = yearly_sales.filter(pl.col("Year") == end_year)["Total_Revenue"][0]

cagr = ((end_revenue / start_revenue) ** (1 / num_years)) - 1
print(f"\nCAGR ({start_year}-{end_year}): {cagr * 100:.2f}%")

# Vẽ biểu đồ kép: Revenue vs Gross Margin
fig, ax1 = plt.subplots(figsize=(12, 6))
years = yearly_sales["Year"].to_list()
revenue = yearly_sales["Total_Revenue"].to_list()
margin = yearly_sales["Avg_Gross_Margin_%"].to_list()

color = 'tab:blue'
ax1.set_xlabel('Year', fontweight='bold')
ax1.set_ylabel('Total Revenue ($)', color=color, fontweight='bold')
line1 = ax1.plot(years, revenue, marker='o', linewidth=2.5, color=color, label='Revenue')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(years)

formatter = plt.FuncFormatter(lambda x, pos: f'${x*1e-6:.1f}M')
ax1.yaxis.set_major_formatter(formatter)

ax2 = ax1.twinx()  
color2 = 'tab:red'
ax2.set_ylabel('Gross Margin (%)', color=color2, fontweight='bold')
line2 = ax2.plot(years, margin, marker='s', linestyle='--', color=color2, label='Gross Margin (%)')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Revenue & Gross Margin YoY Trend (2013 - 2022)', fontsize=16, fontweight='bold')
fig.tight_layout()

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

plt.savefig(os.path.join(FIGURES_DIR, "day2_revenue_margin_yoy.png"), bbox_inches="tight")
plt.show()

# INSIGHT:
# >> "CAGR đạt ...%. Dù doanh thu (Revenue) có xu hướng tăng, nhưng Biên lợi nhuận gộp (Gross Margin) có đang được duy trì ổn định hay không? Nếu Biên giảm, có nghĩa chi phí giá vốn (COGS) đang ăn mòn lợi nhuận."


# ============================================================
# CELL 6: QoQ Trend (Quarter over Quarter)
# ============================================================
print("\n=== CELL 6: QoQ Growth Trend ===")
sales = sales.with_columns([
    (pl.col("Year").cast(pl.String) + "-Q" + pl.col("Quarter").cast(pl.String)).alias("YearQuarter")
])

quarterly_sales = sales_full_years.group_by(["Year", "Quarter"]).agg(
    pl.col("Revenue").sum().alias("Total_Revenue")
).sort(["Year", "Quarter"])

quarterly_sales = quarterly_sales.with_columns([
    (pl.col("Year").cast(pl.String) + "-Q" + pl.col("Quarter").cast(pl.String)).alias("YearQuarter"),
    (pl.col("Total_Revenue").diff() / pl.col("Total_Revenue").shift(1) * 100).alias("QoQ_Growth_Rate_%")
])

# Plot QoQ Growth
plt.figure(figsize=(14, 6))
q_labels = quarterly_sales["YearQuarter"].to_list()
q_growth = quarterly_sales["QoQ_Growth_Rate_%"].fill_null(0).to_list()

plt.bar(q_labels, q_growth, color=np.where(np.array(q_growth) > 0, '#2ecc71', '#e74c3c'))
plt.xticks(rotation=45, ha='right')
plt.axhline(0, color='black', linewidth=1)
plt.ylabel('QoQ Growth Rate (%)', fontweight='bold')
plt.title('Quarter-over-Quarter (QoQ) Revenue Growth (2013-2022)', fontweight='bold', fontsize=16)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day2_qoq_growth.png"), bbox_inches="tight")
plt.show()

# INSIGHT:
# >> "Nhìn vào QoQ, chúng ta thấy rõ những nhịp gãy (Quý nào thường bị sụt giảm mạnh) và nhịp phục hồi. Q4 thường có mức phục hồi rất tốt sau điểm trũng của Q3."


# ============================================================
# CELL 7: Monthly Seasonality & 12-Month Rolling Average
# ============================================================
print("\n=== CELL 7: Monthly Rolling Average ===")
monthly_sales = sales.group_by("YearMonth").agg(
    pl.col("Revenue").sum().alias("Total_Revenue")
).sort("YearMonth")

# Chuyển sang Pandas để dùng hàm rolling dễ dàng hơn
monthly_pd = monthly_sales.to_pandas()
monthly_pd['12M_Rolling_Avg'] = monthly_pd['Total_Revenue'].rolling(window=12, min_periods=1).mean()

plt.figure(figsize=(14, 6))
plt.plot(monthly_pd['YearMonth'], monthly_pd['Total_Revenue'], alpha=0.5, label='Monthly Revenue', color='tab:blue')
plt.plot(monthly_pd['YearMonth'], monthly_pd['12M_Rolling_Avg'], linewidth=3, label='12-Month Rolling Avg', color='tab:red')

# Rút gọn nhãn trục X cho đỡ rối
step = len(monthly_pd) // 15
plt.xticks(monthly_pd['YearMonth'][::step], rotation=45)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'${x*1e-6:.1f}M'))
plt.ylabel('Revenue ($)', fontweight='bold')
plt.title('Monthly Revenue with 12-Month Rolling Average', fontweight='bold', fontsize=16)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day2_monthly_rolling.png"), bbox_inches="tight")
plt.show()

# INSIGHT:
# >> "Đường Rolling Average làm mượt (smooth) biểu đồ, cho thấy rõ ràng chu kỳ vĩ mô: Giai đoạn đi ngang 2014-2015, suy thoái 2019-2021 và sự phục hồi vào cuối 2022."


# ============================================================
# CELL 8: Time-Series Decomposition (Advanced)
# ============================================================
print("\n=== CELL 8: Time-Series Decomposition ===")
# Chuẩn bị dữ liệu chuỗi thời gian cho statsmodels
import pandas as pd
ts_data = monthly_sales.to_pandas()
ts_data['Date'] = pd.to_datetime(ts_data['YearMonth'])
ts_data.set_index('Date', inplace=True)

# Thực hiện bóc tách (Decomposition)
# Chu kỳ 12 tháng (mùa vụ năm)
result = seasonal_decompose(ts_data['Total_Revenue'], model='multiplicative', period=12)

# Custom Plotting cho đẹp hơn
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

ax1.plot(result.observed, color='tab:blue')
ax1.set_ylabel('Observed', fontweight='bold')
ax1.set_title('Time-Series Decomposition of Monthly Revenue', fontweight='bold', fontsize=16)

ax2.plot(result.trend, color='tab:orange', linewidth=2.5)
ax2.set_ylabel('Trend', fontweight='bold')

ax3.plot(result.seasonal, color='tab:green')
ax3.set_ylabel('Seasonality', fontweight='bold')

ax4.scatter(result.resid.index, result.resid, color='tab:red', s=10)
ax4.axhline(1, color='black', linestyle='--')
ax4.set_ylabel('Residuals', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day2_ts_decomposition.png"), bbox_inches="tight")
plt.show()

# INSIGHT:
# >> "1. Trend: Biểu đồ Trend bóc tách hoàn toàn nhiễu, cho thấy xu hướng cốt lõi.\n>> 2. Seasonality: Chu kỳ rõ rệt lặp lại hàng năm (Ví dụ: Thấp ở đầu năm và lập đỉnh vào T11-T12).\n>> 3. Residuals: Các chấm đỏ lệch xa mốc 1.0 là những tháng có dị thường (Anomaly). Cần đào sâu xem có phải do khuyến mãi mạnh hay đứt gãy chuỗi cung ứng không."

# ============================================================
# CELL 9: Outliers Deep Dive (Phân tích ngoại lai chuyên sâu)
# ============================================================
print("\n=== CELL 9: Outliers Deep Dive ===")
if sales_outliers.height > 0:
    print(f"Tiến hành phân tích sâu {sales_outliers.height} ngày Outliers...")
    
    import pandas as pd
    sales_pd = sales.to_pandas()
    outliers_pd = sales_outliers.to_pandas()
    
    # ----------------------------------------------------
    # CHart 1: Timeline Scatter Plot (Vị trí các Outliers)
    # ----------------------------------------------------
    plt.figure(figsize=(14, 6))
    plt.scatter(sales_pd['Date'], sales_pd['Revenue'], color='tab:blue', alpha=0.5, label='Normal Days', s=10)
    plt.scatter(outliers_pd['Date'], outliers_pd['Revenue'], color='red', alpha=0.9, label='Outliers (Top 1%)', s=40, edgecolors='black')
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'${x*1e-6:.1f}M'))
    plt.title('Daily Revenue Timeline: Normal Days vs Outliers', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Daily Revenue ($)', fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "day2_outliers_timeline.png"), bbox_inches="tight")
    plt.show()

    # ----------------------------------------------------
    # Chart 2: Outliers Frequency by Month
    # ----------------------------------------------------
    outliers_pd['Month'] = outliers_pd['Date'].dt.month
    outliers_by_month = outliers_pd['Month'].value_counts().sort_index()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=outliers_by_month.index, y=outliers_by_month.values, palette='Reds_r')
    plt.title('Outliers Frequency Distribution by Month', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontweight='bold')
    plt.ylabel('Number of Outlier Days', fontweight='bold')
    plt.xticks(ticks=range(len(outliers_by_month)), labels=[f"Tháng {int(m)}" for m in outliers_by_month.index])
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "day2_outliers_by_month.png"), bbox_inches="tight")
    plt.show()

    # ----------------------------------------------------
    # Chart 3: Gross Margin Comparison
    # ----------------------------------------------------
    sales_pd['Type'] = 'Normal'
    outliers_pd['Type'] = 'Outlier'
    
    sales_pd['Gross_Margin_%'] = (sales_pd['Revenue'] - sales_pd['COGS']) / sales_pd['Revenue'] * 100
    outliers_pd['Gross_Margin_%'] = (outliers_pd['Revenue'] - outliers_pd['COGS']) / outliers_pd['Revenue'] * 100
    
    combined_df = pd.concat([sales_pd, outliers_pd])
    
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=combined_df, x='Type', y='Gross_Margin_%', palette=['#3498db', '#e74c3c'])
    plt.title('Gross Margin Comparison: Normal vs Outlier Days', fontsize=14, fontweight='bold')
    plt.ylabel('Gross Margin (%)', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "day2_outliers_margin_compare.png"), bbox_inches="tight")
    plt.show()

# INSIGHT:
# >> "1. Timeline Chart: Cú sốc lớn nhất diễn ra vào chuỗi ngày Hè 2018 và 2017 với mức doanh thu có lúc chạm mốc 20 triệu USD/ngày.\n>> 2. Tháng: 100% Outliers tập trung vào tháng 3, 4, 5, 6 (Đỉnh điểm mùa Xuân Hè).\n>> 3. Gross Margin: Nhóm Outliers có mức biên lợi nhuận cực kỳ chênh lệch (có những ngày biên lợi nhuận bị ép xuống mức rất thấp). Điều này càng củng cố giả thuyết đây là các đợt Mega Sale xả kho giữa năm với mức Discount sâu để đẩy doanh số."

"""
Day 3: EDA — Promotions Analysis
Owner: Nguyễn Quốc Khánh (Tech Lead)
Mục tiêu: Phân tích hiệu quả khuyến mãi, so sánh doanh thu có/không promo,
          chuẩn bị feature cho Forecasting model.
"""

# ============================================================
# CELL 1: Setup & Imports
# ============================================================
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os
import warnings

warnings.filterwarnings("ignore")
sys.path.append(os.path.abspath(os.path.join("..", "src")))
from data_loader import DataLoader

np.random.seed(42)
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")
plt.rcParams.update({"figure.dpi": 120, "font.size": 11, "axes.titlesize": 14})

FIGURES_DIR = os.path.abspath(os.path.join("..", "figures"))
os.makedirs(FIGURES_DIR, exist_ok=True)
print("✅ Setup complete.")

# ============================================================
# CELL 2: Load Data (Section 1 — Data Preparation)
# ============================================================
loader = DataLoader(data_dir="../Data")

promotions = loader.load("promotions")
order_items = loader.load("order_items")
orders = loader.load("orders")

print(f"promotions:  {promotions.shape}")
print(f"order_items: {order_items.shape}")
print(f"orders:      {orders.shape}")

# ============================================================
# CELL 3: Quick Schema Inspection
# ============================================================
print("=== promotions columns ===")
print(promotions.schema)
print(promotions.head(3))

print("\n=== order_items columns ===")
print(order_items.schema)
print(order_items.head(3))

print("\n=== orders columns ===")
print(orders.schema)
print(orders.head(3))

# ============================================================
# CELL 4: Merge into Master DataFrame
# ============================================================
# Step 1: order_items + orders on order_id
master = order_items.join(orders, on="order_id", how="left")

# Step 2: left join with promotions on promo_id
master = master.join(promotions, on="promo_id", how="left")

# Tạo cột line_revenue = quantity * unit_price - discount_amount
master = master.with_columns(
    (pl.col("quantity") * pl.col("unit_price") - pl.col("discount_amount")).alias(
        "line_revenue"
    )
)

print(f"Master DataFrame shape: {master.shape}")
print(master.head(5))

# ============================================================
# SECTION 2: DATA QUALITY ASSURANCE (DQA)
# ============================================================

# ============================================================
# CELL 5: 2.1 — Missing / Null Values Analysis
# ============================================================
null_counts = master.null_count()
total_rows = master.height

print("=== Null Count per Column ===")
for col_name in master.columns:
    n_null = null_counts[col_name][0]
    pct = n_null / total_rows * 100
    if n_null > 0:
        print(f"  {col_name:25s} -> {n_null:>10,} nulls  ({pct:.2f}%)")

# ============================================================
# CELL 6: 2.1b — Fill Null for promo columns
# ============================================================
# promo_id null => đơn hàng không sử dụng khuyến mãi
promo_str_cols = ["promo_id", "promo_name", "promo_type", "promo_channel"]
for c in promo_str_cols:
    if c in master.columns:
        master = master.with_columns(pl.col(c).fill_null("No_Promo"))

# Fill numeric promo cols with 0
promo_num_cols = ["discount_value", "min_order_value", "stackable_flag"]
for c in promo_num_cols:
    if c in master.columns:
        master = master.with_columns(pl.col(c).fill_null(0))

print("✅ Null values filled for promo columns.")
print(f"Remaining total nulls: {master.null_count().sum_horizontal()[0]}")

# ============================================================
# CELL 7: 2.2 — Validate Data Types
# ============================================================
# Cast ID columns to String
id_cols = ["order_id", "product_id", "customer_id", "promo_id"]
for c in id_cols:
    if c in master.columns:
        master = master.with_columns(pl.col(c).cast(pl.Utf8))

# Cast numeric columns to Float64
num_cols = ["unit_price", "discount_amount", "line_revenue", "discount_value"]
for c in num_cols:
    if c in master.columns:
        master = master.with_columns(pl.col(c).cast(pl.Float64))

print("✅ Data types validated.")
print(master.schema)

# ============================================================
# CELL 8: 2.3 — Outlier Detection (IQR method)
# ============================================================
def detect_outliers_iqr(df: pl.DataFrame, col: str) -> dict:
    """Detect outliers using IQR method. Returns stats dict."""
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    n_outliers = df.filter(
        (pl.col(col) < lower) | (pl.col(col) > upper)
    ).height
    return {
        "column": col,
        "Q1": q1, "Q3": q3, "IQR": iqr,
        "lower_bound": lower, "upper_bound": upper,
        "n_outliers": n_outliers,
        "pct_outliers": n_outliers / df.height * 100,
    }


outlier_cols = ["unit_price", "discount_amount", "line_revenue", "quantity"]
outlier_results = []
for c in outlier_cols:
    if c in master.columns:
        stats = detect_outliers_iqr(master, c)
        outlier_results.append(stats)
        print(f"[{c}] Outliers: {stats['n_outliers']:,} ({stats['pct_outliers']:.2f}%) "
              f"| Bounds: [{stats['lower_bound']:.2f}, {stats['upper_bound']:.2f}]")

# ============================================================
# CELL 9: 2.3b — Visualize Outliers (Boxplots)
# ============================================================
fig, axes = plt.subplots(1, len(outlier_cols), figsize=(5 * len(outlier_cols), 6))
if len(outlier_cols) == 1:
    axes = [axes]

for ax, col in zip(axes, outlier_cols):
    if col in master.columns:
        data = master[col].drop_nulls().to_list()
        ax.boxplot(data, vert=True)
        ax.set_title(f"Outlier Distribution: {col}", fontweight="bold")
        ax.set_ylabel(col)

plt.suptitle("Outlier Detection — IQR Method", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day3_outlier_boxplots.png"), bbox_inches="tight")
plt.show()

# ============================================================
# CELL 10: 2.3c — Sanity Checks (logic-based)
# ============================================================
# Check: discount_amount > line_revenue (vô lý)
neg_revenue = master.filter(pl.col("line_revenue") < 0)
print(f"⚠️  Đơn hàng có line_revenue < 0: {neg_revenue.height:,}")

# Check: discount_amount lớn hơn giá trị đơn
if "discount_amount" in master.columns:
    illogical = master.filter(
        pl.col("discount_amount") > (pl.col("quantity") * pl.col("unit_price"))
    )
    print(f"⚠️  discount_amount > order value: {illogical.height:,}")

# Decision: Giữ nguyên dữ liệu nhưng flag lại
master = master.with_columns(
    (pl.col("line_revenue") < 0).alias("flag_negative_revenue")
)
print("✅ Flagged anomalies. Keeping data for now (không drop, chỉ flag).")

# ============================================================
# SECTION 3: EXPLORATORY DATA ANALYSIS
# ============================================================

# ============================================================
# CELL 11: 3.1 — Promotion Penetration Rate
# ============================================================
master = master.with_columns(
    pl.when(pl.col("promo_type") == "No_Promo")
    .then(pl.lit("No Promotion"))
    .otherwise(pl.lit("Has Promotion"))
    .alias("has_promo_label")
)

promo_counts = master.group_by("has_promo_label").agg(
    pl.count().alias("n_orders"),
)
promo_counts = promo_counts.with_columns(
    (pl.col("n_orders") / pl.col("n_orders").sum() * 100).alias("pct")
)
print(promo_counts)

# Pie chart
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

labels = promo_counts["has_promo_label"].to_list()
sizes = promo_counts["n_orders"].to_list()
colors = ["#2ecc71", "#e74c3c"]
explode = (0.05, 0)

axes[0].pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct="%1.1f%%", shadow=True, startangle=90,
            textprops={"fontsize": 12})
axes[0].set_title("Promotion Penetration Rate\n(% of Order Lines)", fontweight="bold")

# Bar chart
axes[1].bar(labels, sizes, color=colors, edgecolor="black", linewidth=0.5)
for i, (lbl, val) in enumerate(zip(labels, sizes)):
    axes[1].text(i, val + val * 0.01, f"{val:,}", ha="center", fontweight="bold")
axes[1].set_ylabel("Number of Order Lines", fontweight="bold")
axes[1].set_title("Order Lines: Promo vs No Promo", fontweight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day3_promo_penetration.png"), bbox_inches="tight")
plt.show()

# INSIGHT:
# >> Viết insight tại đây sau khi chạy, ví dụ:
# >> "Chỉ X% đơn hàng sử dụng khuyến mãi, cho thấy tỷ lệ penetration còn thấp."

# ============================================================
# CELL 12: 3.2 — Revenue & AOV Comparison
# ============================================================
# Aggregate tổng revenue và AOV theo nhóm promo
revenue_comparison = master.group_by("has_promo_label").agg(
    pl.col("line_revenue").sum().alias("total_revenue"),
    pl.col("line_revenue").mean().alias("avg_order_value"),
    pl.col("line_revenue").median().alias("median_order_value"),
    pl.col("line_revenue").std().alias("std_order_value"),
    pl.count().alias("n_orders"),
)
print("=== Revenue & AOV by Promo Group ===")
print(revenue_comparison)

# ============================================================
# CELL 13: 3.2b — Violin Plot: Revenue Distribution
# ============================================================
# Sample để vẽ nhanh nếu data quá lớn
sample_size = min(50_000, master.height)
sample_df = master.sample(n=sample_size, seed=42).to_pandas()

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Violin plot
sns.violinplot(data=sample_df, x="has_promo_label", y="line_revenue",
               palette=["#2ecc71", "#e74c3c"], ax=axes[0], cut=0)
axes[0].set_title("Revenue Distribution: Promo vs No Promo", fontweight="bold")
axes[0].set_xlabel("Promotion Status", fontweight="bold")
axes[0].set_ylabel("Line Revenue ($)", fontweight="bold")

# Boxplot (zoomed — clip to Q99 for readability)
q99 = sample_df["line_revenue"].quantile(0.99)
clipped = sample_df[sample_df["line_revenue"] <= q99]
sns.boxplot(data=clipped, x="has_promo_label", y="line_revenue",
            palette=["#2ecc71", "#e74c3c"], ax=axes[1])
axes[1].set_title("Revenue Distribution (Clipped at Q99)", fontweight="bold")
axes[1].set_xlabel("Promotion Status", fontweight="bold")
axes[1].set_ylabel("Line Revenue ($)", fontweight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day3_revenue_violin_box.png"), bbox_inches="tight")
plt.show()

# ============================================================
# CELL 14: 3.2c — AOV Bar Chart with Error Bars
# ============================================================
rev_pd = revenue_comparison.to_pandas()

fig, ax = plt.subplots(figsize=(8, 6))
x_pos = range(len(rev_pd))
bars = ax.bar(x_pos, rev_pd["avg_order_value"],
              yerr=rev_pd["std_order_value"],
              color=["#2ecc71", "#e74c3c"], edgecolor="black",
              capsize=8, linewidth=0.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(rev_pd["has_promo_label"], fontweight="bold")
ax.set_ylabel("Average Order Value ($)", fontweight="bold")
ax.set_title("AOV Comparison: Promo vs No Promo\n(with Std Dev error bars)", fontweight="bold")

for bar, val in zip(bars, rev_pd["avg_order_value"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
            f"${val:,.0f}", ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day3_aov_comparison.png"), bbox_inches="tight")
plt.show()

# INSIGHT:
# >> "Nhóm có khuyến mãi có AOV thấp hơn / cao hơn X% so với nhóm không có."

# ============================================================
# CELL 15: 3.3 — Promo Type Performance
# ============================================================
# Chỉ lọc các đơn CÓ khuyến mãi
promo_only = master.filter(pl.col("promo_type") != "No_Promo")

promo_perf = promo_only.group_by("promo_type").agg(
    pl.count().alias("n_orders"),
    pl.col("line_revenue").sum().alias("total_revenue"),
    pl.col("line_revenue").mean().alias("avg_revenue"),
    pl.col("discount_amount").sum().alias("total_discount_given"),
    pl.col("discount_value").mean().alias("avg_discount_pct"),
).sort("total_revenue", descending=True)

# Tính ROI sơ bộ = total_revenue / total_discount_given
promo_perf = promo_perf.with_columns(
    (pl.col("total_revenue") / pl.col("total_discount_given")).alias("roi_ratio")
)
print("=== Promo Type Performance ===")
print(promo_perf)

# ============================================================
# CELL 16: 3.3b — Promo Type Charts
# ============================================================
perf_pd = promo_perf.to_pandas()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# (1) Total Revenue by Promo Type
axes[0, 0].barh(perf_pd["promo_type"], perf_pd["total_revenue"], color=sns.color_palette("viridis", len(perf_pd)))
axes[0, 0].set_xlabel("Total Revenue ($)", fontweight="bold")
axes[0, 0].set_title("Total Revenue by Promo Type", fontweight="bold")

# (2) Number of Orders by Promo Type
axes[0, 1].barh(perf_pd["promo_type"], perf_pd["n_orders"], color=sns.color_palette("magma", len(perf_pd)))
axes[0, 1].set_xlabel("Number of Orders", fontweight="bold")
axes[0, 1].set_title("Order Count by Promo Type", fontweight="bold")

# (3) AOV by Promo Type
axes[1, 0].barh(perf_pd["promo_type"], perf_pd["avg_revenue"], color=sns.color_palette("coolwarm", len(perf_pd)))
axes[1, 0].set_xlabel("Avg Revenue per Order ($)", fontweight="bold")
axes[1, 0].set_title("AOV by Promo Type", fontweight="bold")

# (4) ROI Ratio
axes[1, 1].barh(perf_pd["promo_type"], perf_pd["roi_ratio"], color=sns.color_palette("Set2", len(perf_pd)))
axes[1, 1].set_xlabel("ROI Ratio (Revenue / Discount)", fontweight="bold")
axes[1, 1].set_title("ROI Ratio by Promo Type", fontweight="bold")

plt.suptitle("Promotion Type Performance Dashboard", fontsize=18, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "day3_promo_type_performance.png"), bbox_inches="tight")
plt.show()

# ============================================================
# CELL 17: 3.4 — Promotion Effectiveness Over Time (Bonus)
# ============================================================
# Thêm Year/Month từ order_date
if "order_date" in master.columns:
    master = master.with_columns([
        pl.col("order_date").dt.year().alias("year"),
        pl.col("order_date").dt.month().alias("month"),
        pl.col("order_date").dt.quarter().alias("quarter"),
    ])

    # Revenue theo thời gian: Promo vs No Promo
    monthly_rev = master.group_by(["year", "month", "has_promo_label"]).agg(
        pl.col("line_revenue").sum().alias("total_revenue"),
        pl.count().alias("n_orders"),
    ).sort(["year", "month"])

    # Pivot cho dễ vẽ
    monthly_pd = monthly_rev.to_pandas()
    monthly_pd["year_month"] = monthly_pd["year"].astype(str) + "-" + monthly_pd["month"].astype(str).str.zfill(2)

    fig, ax = plt.subplots(figsize=(18, 7))
    for label, grp in monthly_pd.groupby("has_promo_label"):
        ax.plot(grp["year_month"], grp["total_revenue"], label=label, linewidth=1.5, alpha=0.8)

    ax.set_title("Monthly Revenue Trend: Promo vs No Promo", fontsize=16, fontweight="bold")
    ax.set_xlabel("Year-Month", fontweight="bold")
    ax.set_ylabel("Total Revenue ($)", fontweight="bold")
    ax.legend(title="Promotion Status", fontsize=11)
    # Chỉ hiện 1 tick mỗi 6 tháng để không bị rối
    tick_labels = monthly_pd["year_month"].unique()
    ax.set_xticks(range(0, len(tick_labels), 6))
    ax.set_xticklabels(tick_labels[::6], rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "day3_monthly_revenue_trend.png"), bbox_inches="tight")
    plt.show()

# ============================================================
# CELL 18: 3.5 — Promo Channel Analysis (Bonus)
# ============================================================
if "promo_channel" in master.columns:
    channel_perf = promo_only.group_by("promo_channel").agg(
        pl.count().alias("n_orders"),
        pl.col("line_revenue").sum().alias("total_revenue"),
        pl.col("line_revenue").mean().alias("avg_revenue"),
    ).sort("total_revenue", descending=True)
    print("=== Promo Channel Performance ===")
    print(channel_perf)

    ch_pd = channel_perf.to_pandas()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].bar(ch_pd["promo_channel"], ch_pd["total_revenue"],
                color=sns.color_palette("Set2", len(ch_pd)), edgecolor="black")
    axes[0].set_title("Total Revenue by Promo Channel", fontweight="bold")
    axes[0].set_ylabel("Total Revenue ($)", fontweight="bold")
    axes[0].set_xlabel("Channel", fontweight="bold")

    axes[1].bar(ch_pd["promo_channel"], ch_pd["avg_revenue"],
                color=sns.color_palette("Pastel1", len(ch_pd)), edgecolor="black")
    axes[1].set_title("AOV by Promo Channel", fontweight="bold")
    axes[1].set_ylabel("Avg Revenue ($)", fontweight="bold")
    axes[1].set_xlabel("Channel", fontweight="bold")

    plt.suptitle("Promo Channel Effectiveness", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "day3_promo_channel.png"), bbox_inches="tight")
    plt.show()

# ============================================================
# CELL 19: 3.6 — Stackable Promotion Impact (Bonus)
# ============================================================
if "stackable_flag" in master.columns and "promo_id_2" in master.columns:
    master = master.with_columns(
        pl.when(pl.col("promo_id_2").is_not_null() & (pl.col("promo_id_2") != ""))
        .then(pl.lit("Stacked (2 Promos)"))
        .otherwise(
            pl.when(pl.col("promo_type") != "No_Promo")
            .then(pl.lit("Single Promo"))
            .otherwise(pl.lit("No Promo"))
        )
        .alias("promo_stack_label")
    )

    stack_perf = master.group_by("promo_stack_label").agg(
        pl.count().alias("n_orders"),
        pl.col("line_revenue").sum().alias("total_revenue"),
        pl.col("line_revenue").mean().alias("avg_revenue"),
        pl.col("discount_amount").mean().alias("avg_discount"),
    )
    print("=== Stacked Promo Impact ===")
    print(stack_perf)

    st_pd = stack_perf.to_pandas()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(st_pd["promo_stack_label"], st_pd["avg_revenue"],
                  color=["#95a5a6", "#3498db", "#e67e22"], edgecolor="black")
    for bar, val in zip(bars, st_pd["avg_revenue"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                f"${val:,.0f}", ha="center", fontweight="bold")
    ax.set_title("AOV: No Promo vs Single vs Stacked Promotions", fontweight="bold")
    ax.set_ylabel("Average Order Value ($)", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "day3_stacked_promo.png"), bbox_inches="tight")
    plt.show()

# ============================================================
# SECTION 4: FEATURE ENGINEERING FOR FORECASTING
# ============================================================

# ============================================================
# CELL 20: 4.1 — Create Promotion Features
# ============================================================
master = master.with_columns([
    # Binary: có khuyến mãi hay không
    pl.when(pl.col("promo_type") != "No_Promo")
    .then(pl.lit(1))
    .otherwise(pl.lit(0))
    .alias("has_promotion"),

    # Discount percentage = discount_amount / (quantity * unit_price) * 100
    pl.when(pl.col("quantity") * pl.col("unit_price") > 0)
    .then(pl.col("discount_amount") / (pl.col("quantity") * pl.col("unit_price")) * 100)
    .otherwise(pl.lit(0.0))
    .alias("discount_pct"),
])

print("=== Feature Preview ===")
feat_cols = ["order_id", "promo_type", "has_promotion", "discount_pct",
             "discount_amount", "line_revenue"]
print(master.select([c for c in feat_cols if c in master.columns]).head(10))
print(f"\nhas_promotion distribution:\n{master['has_promotion'].value_counts()}")

# ============================================================
# CELL 21: 4.2 — Export Processed Data
# ============================================================
DATA_DIR = os.path.abspath(os.path.join("..", "Data"))

export_cols = [
    "order_id", "product_id", "customer_id", "order_date",
    "quantity", "unit_price", "discount_amount", "line_revenue",
    "promo_id", "promo_type", "promo_channel",
    "has_promotion", "discount_pct",
    "order_status", "payment_method", "device_type", "order_source",
    "flag_negative_revenue",
]
# Chỉ giữ các cột tồn tại
export_cols = [c for c in export_cols if c in master.columns]

master_export = master.select(export_cols)
export_path = os.path.join(DATA_DIR, "processed_promo_features.parquet")
master_export.write_parquet(export_path)
print(f"✅ Exported {master_export.shape} to {export_path}")
print(f"   File size: {os.path.getsize(export_path) / 1e6:.2f} MB")

# ============================================================
# CELL 22: Summary Statistics & Final Narrative
# ============================================================
print("=" * 60)
print("📝 SUMMARY — Day 3 Promotions EDA")
print("=" * 60)
print(f"Total order lines analyzed: {master.height:,}")

has_promo = master.filter(pl.col("has_promotion") == 1).height
no_promo = master.filter(pl.col("has_promotion") == 0).height
print(f"With Promotion:    {has_promo:,} ({has_promo/master.height*100:.1f}%)")
print(f"Without Promotion: {no_promo:,} ({no_promo/master.height*100:.1f}%)")

rev_promo = master.filter(pl.col("has_promotion") == 1)["line_revenue"].sum()
rev_no = master.filter(pl.col("has_promotion") == 0)["line_revenue"].sum()
print(f"\nRevenue (Promo):    ${rev_promo:,.0f}")
print(f"Revenue (No Promo): ${rev_no:,.0f}")

aov_promo = master.filter(pl.col("has_promotion") == 1)["line_revenue"].mean()
aov_no = master.filter(pl.col("has_promotion") == 0)["line_revenue"].mean()
print(f"\nAOV (Promo):    ${aov_promo:,.2f}")
print(f"AOV (No Promo): ${aov_no:,.2f}")

if "promo_type" in master.columns:
    best = promo_perf.row(0)
    print(f"\nBest performing promo type: {best[0]} (Revenue: ${best[2]:,.0f})")

print("\n" + "=" * 60)
print("📊 Figures saved to:", FIGURES_DIR)
print("📦 Features exported to:", export_path)
print("=" * 60)

# BUSINESS INSIGHTS (Điền sau khi chạy):
# 1. [Insight về Promotion Penetration Rate]
# 2. [Insight về AOV gap giữa hai nhóm]
# 3. [Insight về Promo Type hiệu quả nhất]
# 4. [Insight về xu hướng thời gian]
# 5. [Insight về Promo Channel]
